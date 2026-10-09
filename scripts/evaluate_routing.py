#!/usr/bin/env python3
"""Evaluate skill selection from names/descriptions only; expected labels stay hidden."""
import argparse
import json
from pathlib import Path
import re
import tempfile
import yaml
from evaluate import ROOT, DEFAULT_MODEL, invoke, sha, write_json


def routing_prompt(cases, descriptions):
    return ('Select exactly one task skill for each request, or none when no skill fits. '
            'Use only the catalog descriptions, not skill bodies or external information. '
            'Choose by the requested deliverable. Do not execute the requests or use tools.\n'
            'CATALOG:\n'+json.dumps(descriptions,ensure_ascii=False)+'\nREQUESTS:\n'+
            json.dumps([{'id':c['id'],'request':c['request']} for c in cases],ensure_ascii=False))


def compare(cases, predictions):
    if len(predictions)!=len(cases) or {p['id'] for p in predictions}!={c['id'] for c in cases}:
        raise ValueError('Predictions must cover each request exactly once')
    by_id={p['id']:p for p in predictions}
    return [{'id':c['id'],'expected':c['expected'],'actual':by_id[c['id']]['skill'],
             'pass':c['expected']==by_id[c['id']]['skill'],'reason':by_id[c['id']]['reason']} for c in cases]


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-dir',type=Path,required=True)
    p.add_argument('--model');p.add_argument('--engine',choices=['codex','claude'],default='codex')
    args=p.parse_args();run=args.run_dir.resolve()
    args.model=args.model or (DEFAULT_MODEL if args.engine=='codex' else 'sonnet')
    if run.exists():p.error('Use a new run directory to preserve earlier results')
    cases=json.loads((ROOT/'tests/routing.json').read_text());descriptions={}
    for path in sorted((ROOT/'skills').glob('*/SKILL.md')):
        meta=yaml.safe_load(re.match(r'---\n(.*?)\n---',path.read_text(),re.S)[1])
        descriptions[meta['name']]=meta['description']
    schema={'type':'object','properties':{'predictions':{'type':'array','items':{'type':'object',
        'properties':{'id':{'type':'string'},'skill':{'type':'string','enum':list(descriptions)+['none']},'reason':{'type':'string'}},
        'required':['id','skill','reason'],'additionalProperties':False}}},'required':['predictions'],'additionalProperties':False}
    write_json(run/'inputs.json',{'cases':cases,'descriptions':descriptions,'catalog_sha256':sha(json.dumps(descriptions,sort_keys=True).encode())})
    with tempfile.TemporaryDirectory(prefix='hr-routing-') as temp:
        workspace=Path(temp);spec=workspace/'schema.json';write_json(spec,schema)
        if args.engine=='codex':
            meta=invoke(routing_prompt(cases,descriptions),workspace,run/'model',args.model,'low',600,spec)
        else:
            from evaluate_formats import claude_invoke
            log=run/'model';log.mkdir(parents=True,exist_ok=True)
            prompt=routing_prompt(cases,descriptions);(log/'prompt.txt').write_text(prompt)
            meta,_=claude_invoke(prompt,workspace,log,args.model,schema)
            write_json(log/'run.json',meta)
    if meta['status']!='completed':raise SystemExit('Routing model execution did not complete')
    predictions=json.loads((run/'model/output.txt').read_text())['predictions']
    rows=compare(cases,predictions);passed=sum(r['pass'] for r in rows)
    write_json(run/'summary.json',{'passed':passed,'total':len(rows),'rows':rows,'model':args.model,'engine':args.engine,
        'limitation':'One batched classification run; no runtime auto-discovery or research workflow was executed.'})
    print(f'Routing: {passed}/{len(rows)} matched expected labels')
    raise SystemExit(0 if passed==len(rows) else 1)

if __name__=='__main__':main()
