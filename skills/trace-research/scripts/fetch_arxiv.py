#!/usr/bin/env python3
"""Retrieve canonical arXiv metadata and versioned HTML/PDF without claiming to read it."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sys

# Isolated Python omits the script directory from its import path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from forward_citations import normalize_id
from citation_sources import HTTP, FetchError, canonical_arxiv, pdf_pages, normalized_title


def input_id(value):
    kind, identifier = normalize_id(value)
    if kind == 'doi' and identifier.startswith('10.48550/arxiv.'):
        identifier = re.sub(r'v\d+$', '', identifier.split('arxiv.',1)[1], flags=re.I)
    elif kind != 'arxiv':
        raise ValueError('Expected an arXiv ID, arXiv URL, or arXiv DOI')
    # Citation matching is work-level; retrieval preserves an explicitly requested version.
    version = re.search(r'(v\d+)(?:\.pdf)?(?:[?#].*)?$',value,re.I)
    return identifier+(version[1].lower() if version else '')


def fetch(value, destination, format='auto', extract_text=False, http=None):
    http = http or HTTP()
    record = {'status':'unavailable','requested_id':value,'retrieved_at':datetime.now(timezone.utc).isoformat(),
              'access':'none','render_inspected':False,'files':[]}
    identifier = input_id(value)
    try:
        metadata = canonical_arxiv(http,identifier)
        record.update(metadata=metadata,access='abstract',status='metadata_only')
        version = metadata['versioned_id']
        filename = version.replace('/','_')
        destination = Path(destination)
        destination.mkdir(parents=True,exist_ok=True)
        def save(name,content,source):
            target=destination/name
            if target.exists() and target.read_bytes()!=content:
                raise FetchError('local_conflict','Existing local file differs: '+name)
            if not target.exists():
                with target.open('xb') as f:f.write(content)
            entry={'name':name,'source':source,'bytes':len(content),'sha256':hashlib.sha256(content).hexdigest()}
            record['files'].append(entry)
        save(filename+'.metadata.json',(json.dumps(metadata,ensure_ascii=False,indent=2)+'\n').encode(),metadata['url'])
        if format in ('auto','html'):
            url='https://arxiv.org/html/'+version
            try:
                html=http.text(url)
                if 'ltx_document' not in html or normalized_title(metadata['title']) not in normalized_title(html):
                    raise FetchError('unavailable','Response is not the expected paper HTML')
                save(filename+'.html',html.encode(),url)
                record.update(access='full_text_html',status='downloaded')
            except FetchError as exc:
                if exc.status=='local_conflict':raise
                record['html_status']=str(exc)
        if format=='pdf' or (format=='auto' and record['access']!='full_text_html'):
            url='https://arxiv.org/pdf/'+version
            raw=http.raw(url)
            if not raw.startswith(b'%PDF-'):raise FetchError('unavailable','Response is not a PDF')
            save(filename+'.pdf',raw,url)
            record.update(access='full_text_pdf',status='downloaded')
            if extract_text:
                try:
                    pages=pdf_pages(raw)
                    text='\n\n'.join('--- PDF page '+str(i+1)+' ---\n'+s for i,s in enumerate(pages))
                    save(filename+'.txt',text.encode(),url)
                    record['text_extraction']={'status':'extracted' if any(p.strip() for p in pages) else 'no_text','pages':len(pages),'visual_inspection':False}
                except FetchError as exc:
                    record['text_extraction']={'status':exc.status,'reason':str(exc)}
    except OSError as exc:
        record['reason']='Local file operation failed: '+type(exc).__name__
        record['error_status']='local_io_error'
    except FetchError as exc:
        record['reason']=str(exc)
        record['error_status']=exc.status
    return record


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('identifier');p.add_argument('--output',type=Path,required=True)
    p.add_argument('--format',choices=['auto','html','pdf'],default='auto')
    p.add_argument('--text',action='store_true',help='Extract PDF text with optional pypdf; not visual review')
    p.add_argument('--cache-dir',type=Path,default=Path.home()/'.cache/human-researcher/citations')
    p.add_argument('--no-cache',action='store_true');args=p.parse_args()
    try:record=fetch(args.identifier,args.output,args.format,args.text,HTTP(None if args.no_cache else args.cache_dir))
    except ValueError as exc:p.error(str(exc))
    print(json.dumps(record,ensure_ascii=False,indent=2))
    return 0 if record['status']=='downloaded' and 'error_status' not in record else 2

if __name__=='__main__':raise SystemExit(main())
