#!/usr/bin/env python3
"""Install verified local-checkout packages and record a baseline for safe updates.

The caller chooses the current agent's skill directory. This script never discovers
or edits other agents. A requested --ref must match the clean checkout's HEAD.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[1]
REPOSITORY='https://github.com/taewan2002/human-researcher'
LOCK_NAME='.human-researcher-lock.json'


def hashes(folder, included=None):
    if folder.is_symlink():raise ValueError(f'Symlink package is not supported: {folder.name}')
    result={}
    for p in sorted(folder.rglob('*')):
        relative=p.relative_to(folder).as_posix()
        if '__pycache__' in p.parts or p.suffix in ('.pyc','.pyo') or p.name=='.DS_Store':continue
        if included is not None and relative not in included:continue
        if p.is_symlink():raise ValueError(f'Symlink member is not supported: {p.name}')
        if p.is_file():result[relative]=hashlib.sha256(p.read_bytes()).hexdigest()
    return result


def save_lock(path, data):
    with tempfile.NamedTemporaryFile('w',dir=path.parent,prefix='.hr-lock-',delete=False) as f:
        json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n');temp=Path(f.name)
    os.replace(temp,path)


def install(source, target, names, revision, ref, dry_run=False, tracked=None):
    target=target.expanduser().resolve()
    if not dry_run:target.mkdir(parents=True,exist_ok=True)
    lock_path=target/LOCK_NAME
    lock=json.loads(lock_path.read_text()) if lock_path.exists() else {'schema_version':1,'repository':REPOSITORY,'packages':{}}
    if lock.get('schema_version')!=1 or lock.get('repository')!=REPOSITORY or not isinstance(lock.get('packages'),dict):
        raise ValueError('Unrecognized install provenance; no packages were changed.')
    report=[]
    for name in names:
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',name):raise ValueError('Invalid skill name')
        origin=source/'skills'/name;dest=target/name
        if not (origin/'SKILL.md').is_file():raise ValueError(f'Unknown skill: {name}')
        included={f[len('skills/'+name+'/'):] for f in tracked if f.startswith('skills/'+name+'/')} if tracked is not None else None
        expected=hashes(origin,included)
        if 'SKILL.md' not in expected:raise ValueError(f'Untracked package: {name}')
        if dest.is_symlink():report.append({'skill':name,'status':'conflict','reason':'Existing package is a symlink'});continue
        current=hashes(dest) if dest.is_dir() else None
        baseline=lock['packages'].get(name,{}).get('files')
        if dest.exists() and current!=expected and (current is None or baseline is None or current!=baseline):
            report.append({'skill':name,'status':'conflict','reason':'Untracked content or local edits; preserved'});continue
        status='already_present' if current==expected else ('updated' if current is not None else 'installed')
        if not dry_run:
            with tempfile.TemporaryDirectory(prefix='.hr-stage-',dir=target) as stage:
                staging=Path(stage)/name;backup=Path(stage)/'previous'
                staging.mkdir()
                for relative in expected:
                    out=staging/relative;out.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copy2(origin/relative,out)
                if hashes(staging)!=expected:raise ValueError('Staged files do not match source')
                if dest.exists():os.replace(dest,backup)
                try:
                    os.replace(staging,dest)
                    lock['packages'][name]={'repository':REPOSITORY,'ref':ref,'commit':revision,
                        'installed_at':datetime.now(timezone.utc).isoformat(),'files':expected}
                    save_lock(lock_path,lock)
                except BaseException:
                    if dest.exists():shutil.rmtree(dest)
                    if backup.exists():os.replace(backup,dest)
                    raise
        report.append({'skill':name,'status':status})
    return {'destination':str(target),'ref':ref,'commit':revision,'dry_run':dry_run,'packages':report}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--target',type=Path,required=True);p.add_argument('--ref',required=True)
    p.add_argument('--skills',nargs='+');p.add_argument('--dry-run',action='store_true');args=p.parse_args()
    def git(*parts):return subprocess.check_output(['git',*parts],cwd=ROOT,text=True).strip()
    revision=git('rev-parse','HEAD')
    if git('rev-parse',args.ref+'^{commit}')!=revision:p.error('--ref must resolve to this checkout\'s HEAD')
    if git('status','--porcelain','--','skills'):p.error('Commit or discard skill changes before installing a revision')
    names=args.skills or sorted(p.name for p in (ROOT/'skills').iterdir() if p.is_dir())
    tracked=set(git('ls-files','-z','--','skills').split('\0'))
    target=args.target.expanduser().resolve()
    if args.dry_run:
        report=install(ROOT,target,names,revision,args.ref,True,tracked)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 1 if any(x['status']=='conflict' for x in report['packages']) else 0
    target.mkdir(parents=True,exist_ok=True)
    guard=target/'.human-researcher-install.lock'
    try:
        with guard.open('x') as f:f.write(str(os.getpid()))
    except FileExistsError:p.error('Another install is active, or its lock needs inspection before retrying')
    try:
        report=install(ROOT,target,names,revision,args.ref,args.dry_run,tracked)
        print(json.dumps(report,ensure_ascii=False,indent=2))
        return 1 if any(x['status']=='conflict' for x in report['packages']) else 0
    finally:guard.unlink(missing_ok=True)

if __name__=='__main__':raise SystemExit(main())
