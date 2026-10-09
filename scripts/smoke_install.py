#!/usr/bin/env python3
"""Check project-scoped package installation, not model behavior or host discovery."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import subprocess
import sys
import tempfile


CLI_VERSION = '1.7.1'


def package_files(folder: Path):
    return {
        path.relative_to(folder).as_posix(): path.read_bytes()
        for path in folder.rglob('*')
        if path.is_file() and '__pycache__' not in path.parts
        and path.suffix not in ('.pyc', '.pyo') and path.name != '.DS_Store'
    }


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', default=str(root), help='Local path or published owner/repository')
    args = parser.parse_args()
    expected = {
        folder.name: package_files(folder)
        for folder in (root / 'skills').iterdir()
        if folder.is_dir()
    }
    if not expected:
        raise ValueError('No source packages found')
    env = dict(os.environ, DISABLE_TELEMETRY='1')
    for agent, relative in [('codex', '.agents/skills'), ('claude-code', '.claude/skills')]:
        with tempfile.TemporaryDirectory(prefix=f'human-researcher-{agent}-') as temp:
            result = subprocess.run(
                ['npx', '--yes', f'skills@{CLI_VERSION}', 'add', args.source,
                 '--agent', agent, '--skill', '*', '--copy', '--yes'],
                cwd=temp, env=env, text=True, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, timeout=120,
            )
            if result.returncode:
                raise RuntimeError(f'{agent} installation failed:\n{result.stdout}')
            destination = Path(temp) / relative
            installed = {p.name for p in destination.iterdir() if p.is_dir()} if destination.exists() else set()
            if installed != set(expected):
                raise ValueError(f'{agent}: installed packages differ: {sorted(installed)}')
            for name, files in expected.items():
                if package_files(destination / name) != files:
                    raise ValueError(f'{agent}: content mismatch for {name}')
            print(f'{agent}: {len(expected)} packages installed; all files match source.', flush=True)
    print('Installation only; no agent runtime or research model was invoked.')


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
