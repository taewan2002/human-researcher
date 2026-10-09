#!/usr/bin/env python3
"""Validate packaging and evaluation inputs, not scientific or model behavior."""
from __future__ import annotations

import json
from html.parser import HTMLParser
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote, urlsplit

import yaml
from markdown_it import MarkdownIt


class UniqueLoader(yaml.SafeLoader):
    pass


def unique_mapping(loader, node, deep=False):
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if not isinstance(key, str):
            raise ValueError('YAML mapping keys must be strings')
        if key in result:
            raise ValueError(f'duplicate YAML key: {key}')
        result[key] = loader.construct_object(value_node, deep=deep)
    return result


UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, unique_mapping)


def read_yaml(text):
    return yaml.load(text, Loader=UniqueLoader)


class HTMLLinks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links, self.anchors = [], set()

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if value and key in ('href', 'src'):
                self.links.append(value)
            if value and (key == 'id' or (tag == 'a' and key == 'name')):
                self.anchors.add(value)


def document_targets(path):
    text = path.read_text(encoding='utf-8')
    html = HTMLLinks()
    if path.suffix.lower() != '.md':
        html.feed(text)
        return html.links, html.anchors
    links, anchors, slugs = [], set(), set()
    tokens = MarkdownIt().parse(text)
    for i, token in enumerate(tokens):
        if token.type == 'heading_open':
            content = tokens[i + 1].children or []
            label = ''.join(t.content for t in content if t.type in ('text', 'code_inline'))
            base = ''.join(c for c in label.lower() if c in ('-', '_', ' ') or
                           unicodedata.category(c)[0] not in ('P', 'S', 'C')).replace(' ', '-')
            slug, n = base, 0
            while slug in slugs:
                n += 1
                slug = f'{base}-{n}'
            slugs.add(slug)
            anchors.add(slug)
        for item in [token] + (token.children or []):
            if item.type in ('html_block', 'html_inline'):
                html.feed(item.content)
            for key in ('href', 'src'):
                if item.attrGet(key):
                    links.append(item.attrGet(key))
    return links + html.links, anchors | html.anchors


def local_links(path: Path, boundary: Path):
    errors = []
    for target in document_targets(path)[0]:
        parts = urlsplit(target)
        if parts.scheme == 'file':
            errors.append(f'{path}: file URI cannot travel with the package: {target}')
            continue
        if parts.scheme or parts.netloc:
            continue
        local = unquote(parts.path)
        if Path(local).is_absolute():
            errors.append(f'{path}: absolute file link cannot travel with the package: {target}')
            continue
        dest = (path.parent / local).resolve() if local else path.resolve()
        if not dest.is_relative_to(boundary.resolve()):
            errors.append(f'{path}: link escapes package: {target}')
        elif not dest.exists():
            errors.append(f'{path}: missing local link: {target}')
        elif parts.fragment and dest.suffix.lower() in ('.md', '.html', '.svg'):
            if unquote(parts.fragment) not in document_targets(dest)[1]:
                errors.append(f'{path}: missing local anchor: {target}')
    return errors


def validate_skill(folder: Path):
    errors = []
    if folder.is_symlink():
        return [f'{folder}: skill package root must not be a symlink']
    path = folder / 'SKILL.md'
    if not path.is_file():
        return [f'{folder}: missing SKILL.md']
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---\n(.*)$', text, re.S)
    if not match:
        return [f'{path}: missing YAML frontmatter']
    try:
        meta = read_yaml(match[1])
    except (yaml.YAMLError, ValueError) as exc:
        return [f'{path}: invalid YAML: {exc}']
    if not isinstance(meta, dict):
        return [f'{path}: frontmatter must be a mapping']
    if not isinstance(meta.get('metadata', {}), dict):
        errors.append(f'{path}: metadata must be a mapping')
    name = meta.get('name')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name) or len(name) > 64:
        errors.append(f'{path}: invalid skill name')
    elif name != folder.name:
        errors.append(f'{path}: name does not match folder')
    description = meta.get('description')
    if not isinstance(description, str) or not 1 <= len(description.strip()) <= 1024:
        errors.append(f'{path}: description must be 1–1024 characters')
    if not match[2].strip() or re.search(r'\[TODO:|\[TBD:', text):
        errors.append(f'{path}: empty instructions or unfinished scaffold')
    ui_path = folder / 'agents' / 'openai.yaml'
    if ui_path.exists():
        try:
            ui = read_yaml(ui_path.read_text(encoding='utf-8'))
            if not isinstance(ui, dict) or not isinstance(ui.get('interface'), dict):
                raise ValueError('interface mapping is required')
            interface = ui['interface']
            for key in ('display_name', 'short_description', 'default_prompt'):
                if not isinstance(interface.get(key), str) or not interface[key].strip():
                    raise ValueError(f'{key} must be a nonempty string')
            if not 25 <= len(interface['short_description']) <= 64:
                raise ValueError('short_description must be 25–64 characters')
            if f'${name}' not in interface['default_prompt']:
                raise ValueError('default_prompt must refer to this skill')
            policy = ui.get('policy', {})
            if not isinstance(policy, dict):
                raise ValueError('policy must be a mapping')
            if 'allow_implicit_invocation' in policy and not isinstance(policy['allow_implicit_invocation'], bool):
                raise ValueError('allow_implicit_invocation must be boolean')
        except (yaml.YAMLError, ValueError) as exc:
            errors.append(f'{ui_path}: {exc}')
    for file in folder.rglob('*'):
        if file.is_symlink() and not file.resolve().is_relative_to(folder.resolve()):
            errors.append(f'{file}: symlink escapes skill package')
        elif file.is_file() and file.suffix == '.md':
            errors.extend(local_links(file, folder))
    return errors


def validate_repo(root: Path):
    root = root.resolve()
    errors = []
    skills_dir = root / 'skills'
    if not skills_dir.is_dir():
        return ['Missing skills directory'], 0, 0
    if skills_dir.is_symlink():
        return ['Skills directory must not be a symlink'], 0, 0
    folders = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    names = {p.name for p in folders}
    if not folders:
        errors.append('No skills found')
    for folder in folders:
        errors.extend(validate_skill(folder))
    version_path = root / 'VERSION'
    if version_path.exists():
        version = version_path.read_text().strip()
        if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-z0-9.-]+)?', version):
            errors.append('VERSION must contain a release version')
        for folder in folders:
            if folder.is_symlink():
                continue
            try:
                front = re.match(r'^---\n(.*?)\n---', (folder / 'SKILL.md').read_text(), re.S)
                meta = read_yaml(front[1]) if front else {}
                if meta.get('metadata', {}).get('version') != version:
                    errors.append(f'{folder}: metadata.version does not match VERSION')
            except (OSError, ValueError, yaml.YAMLError, AttributeError):
                pass  # The skill validator reports malformed frontmatter.
    document_paths = list(root.glob('*.md'))
    for directory in ('docs', 'examples', '.github'):
        for suffix in ('*.md', '*.html', '*.svg'):
            document_paths.extend((root / directory).rglob(suffix))
    for path in document_paths:
        errors.extend(local_links(path, root))
    cases = []
    try:
        cases = json.loads((root / 'tests' / 'cases.json').read_text(encoding='utf-8'))
        if not isinstance(cases, list) or not cases:
            raise ValueError('cases must be a nonempty list')
        seen, covered = set(), set()
        for case in cases:
            if not isinstance(case, dict) or not isinstance(case.get('id'), str) or not case['id']:
                raise ValueError('each case needs a nonempty id')
            if case['id'] in seen:
                raise ValueError(f'duplicate case id: {case["id"]}')
            seen.add(case['id'])
            expected = case.get('skills')
            if not isinstance(expected, list) or not expected or any(not isinstance(s, str) or s not in names for s in expected):
                raise ValueError(f'{case["id"]}: unknown or missing skills')
            covered.update(expected)
            if not isinstance(case.get('prompt'), str) or not case['prompt'].strip():
                raise ValueError(f'{case["id"]}: missing prompt')
            criteria = case.get('criteria')
            if not isinstance(criteria, list) or not criteria or any(not isinstance(c, str) or not c.strip() for c in criteria):
                raise ValueError(f'{case["id"]}: missing behavior criteria')
            fixtures = case.get('fixtures', [])
            if not isinstance(fixtures, list) or any(not isinstance(f, str) for f in fixtures):
                raise ValueError(f'{case["id"]}: fixtures must be paths')
            for fixture in fixtures:
                dest = (root / fixture).resolve()
                if not dest.is_relative_to(root / 'tests' / 'fixtures') or not dest.is_file():
                    raise ValueError(f'{case["id"]}: invalid fixture {fixture}')
        if names - covered:
            errors.append(f'Skills without behavior cases: {", ".join(sorted(names - covered))}')
    except (OSError, ValueError) as exc:
        errors.append(f'Evaluation cases: {exc}')
    routing_path = root / 'tests' / 'routing.json'
    if routing_path.exists():
        errors.extend(validate_routing(routing_path, names))
    return errors, len(folders), len(cases) if isinstance(cases, list) else 0


def validate_routing(path, names):
    try:
        rows = json.loads(path.read_text())
        if not isinstance(rows, list) or not rows:
            raise ValueError('routing cases must be a nonempty list')
        seen, covered = set(), set()
        for row in rows:
            if not isinstance(row, dict) or not isinstance(row.get('id'), str) or not row['id']:
                raise ValueError('routing cases need an id')
            if row['id'] in seen:
                raise ValueError('duplicate routing id')
            seen.add(row['id'])
            if not isinstance(row.get('request'), str) or not row['request'].strip():
                raise ValueError('routing cases need a request')
            if row.get('expected') not in names | {'none'}:
                raise ValueError('unknown routing target')
            covered.add(row['expected'])
        if (names | {'none'}) - covered:
            raise ValueError('routing cases must cover all skills and none')
    except (OSError, ValueError, TypeError) as exc:
        return [f'Routing cases: {exc}']
    return []


if __name__ == '__main__':
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1]
    issues, skills_count, cases_count = validate_repo(root)
    if issues:
        for issue in issues:
            print(issue, file=sys.stderr)
        raise SystemExit(1)
    print(f'Validated {skills_count} skill packages and {cases_count} behavior-case definitions.')
    print('Structural validation only; model behavior and research outcomes are not evaluated.')
