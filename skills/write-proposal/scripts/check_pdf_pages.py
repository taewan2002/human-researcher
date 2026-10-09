#!/usr/bin/env python3
"""Count actual PDF pages; exit 0 for expected count, 1 for mismatch, 2 if unverified.

Uses pypdf if installed, otherwise the Poppler pdfinfo executable. Python 3.9+.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def count_pages(path):
    path=Path(path).resolve(strict=True)
    if not path.is_file():raise ValueError('Input is not a regular file.')
    try:
        from pypdf import PdfReader
    except ImportError:
        if not shutil.which('pdfinfo'):
            raise RuntimeError('Install pypdf (python3 -m pip install pypdf) or Poppler pdfinfo.')
        proc=subprocess.run(['pdfinfo',str(path)],text=True,capture_output=True,timeout=20,
                            env=dict(os.environ,LC_ALL='C'))
        if proc.returncode:raise ValueError('pdfinfo could not read this PDF.')
        match=re.search(r'^Pages:\s+(\d+)\s*$',proc.stdout,re.M)
        if not match:raise ValueError('pdfinfo did not report a page count.')
        return int(match[1]),'pdfinfo'
    reader=PdfReader(str(path),strict=True)
    if reader.is_encrypted and not reader.decrypt(''):
        raise ValueError('PDF requires a password; page count is unverified.')
    return len(reader.pages),'pypdf'


def check(path,expected=1):
    if expected<1:raise ValueError('Expected pages must be positive.')
    try:
        pages,backend=count_pages(path)
        return {'status':'pass' if pages==expected else 'fail','pages':pages,
                'expected':expected,'backend':backend},0 if pages==expected else 1
    except Exception as exc:
        return {'status':'unverified','message':'검증 안 됨','reason':str(exc),'expected':expected},2


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('pdf',type=Path);p.add_argument('--expected',type=int,default=1)
    args=p.parse_args()
    if args.expected<1:p.error('--expected must be positive')
    result,status=check(args.pdf,args.expected)
    print(json.dumps(result,ensure_ascii=False,indent=2));return status

if __name__=='__main__':raise SystemExit(main())
