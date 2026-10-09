import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

import yaml

spec = importlib.util.spec_from_file_location('validate_repo', Path(__file__).resolve().parents[1] / 'scripts' / 'validate_repo.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.folder = Path(self.temp.name) / 'read-paper'
        self.folder.mkdir()
        self.path = self.folder / 'SKILL.md'
        self.base = '---\nname: read-paper\ndescription: Read a supplied paper.\n---\n\nRead claims against supplied evidence.\n'
        self.path.write_text(self.base)

    def tearDown(self):
        self.temp.cleanup()

    def test_standalone_package_with_own_reference(self):
        (self.folder / 'references').mkdir()
        (self.folder / 'references' / 'example.md').write_text('A local example.')
        self.path.write_text(self.base + '[Example](references/example.md)\n')
        self.assertEqual([], validator.validate_skill(self.folder))

    def test_folder_and_discovery_name_must_agree(self):
        self.path.write_text(self.base.replace('name: read-paper', 'name: another-skill'))
        self.assertTrue(any('match folder' in x for x in validator.validate_skill(self.folder)))

    def test_outside_reference_breaks_independent_install(self):
        (self.folder.parent / 'secret.md').write_text('Not packaged.')
        self.path.write_text(self.base + '[Reference](../secret.md)\n')
        self.assertTrue(any('escapes package' in x for x in validator.validate_skill(self.folder)))

    def test_missing_reference_is_reported(self):
        self.path.write_text(self.base + '[Reference](missing.md)\n')
        self.assertTrue(any('missing local link' in x for x in validator.validate_skill(self.folder)))

    def test_symlink_cannot_hide_external_dependency(self):
        target = self.folder.parent / 'private.md'
        target.write_text('Outside.')
        (self.folder / 'reference.md').symlink_to(target)
        self.assertTrue(any('symlink escapes' in x for x in validator.validate_skill(self.folder)))

    def test_ambiguous_yaml_keys_are_rejected(self):
        self.path.write_text(self.base.replace('name: read-paper', 'name: hidden\nname: read-paper'))
        self.assertTrue(any('duplicate YAML key' in x for x in validator.validate_skill(self.folder)))

    def test_unsafe_yaml_tags_are_not_executed(self):
        self.path.write_text(self.base.replace('name: read-paper', 'name: !!python/object/apply:builtins.str [read-paper]'))
        self.assertTrue(any('invalid YAML' in x for x in validator.validate_skill(self.folder)))

    def test_package_root_symlink_is_rejected(self):
        link = self.folder.parent / 'linked'
        link.symlink_to(self.folder, target_is_directory=True)
        self.assertTrue(any('root must not be a symlink' in x for x in validator.validate_skill(link)))

    def test_html_reference_links_and_fragments(self):
        self.path.write_text(self.base + '<a href="missing.md">Missing</a>\n[Ref][guide]\n\n[guide]: absent.md\n[Bad](#missing-heading)\n')
        errors = validator.validate_skill(self.folder)
        self.assertTrue(any('missing.md' in x for x in errors))
        self.assertTrue(any('absent.md' in x for x in errors))
        self.assertTrue(any('missing local anchor' in x for x in errors))

    def test_korean_duplicate_heading_anchors_and_fences(self):
        self.path.write_text(self.base + '\n## 연구 계획\n## 연구 계획\n[First](#연구-계획) [Second](#연구-계획-1)\n```md\n[Ignored](missing.md)\n```\n')
        self.assertEqual([], validator.validate_skill(self.folder))

    def test_ui_prompt_invokes_the_packaged_skill(self):
        (self.folder / 'agents').mkdir()
        ui = {'interface': {'display_name': 'Read Paper', 'short_description': 'Read a paper and inspect its evidence', 'default_prompt': '$wrong Read this paper.'}}
        (self.folder / 'agents' / 'openai.yaml').write_text(yaml.safe_dump(ui))
        self.assertTrue(any('default_prompt' in x for x in validator.validate_skill(self.folder)))


class RepositoryDocumentTests(unittest.TestCase):
    def test_nested_example_link_is_checked(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            skill = root / 'skills' / 'read-paper'
            skill.mkdir(parents=True)
            (skill / 'SKILL.md').write_text('---\nname: read-paper\ndescription: Read a supplied paper.\n---\nRead the paper.\n')
            (root / 'tests').mkdir()
            (root / 'tests' / 'cases.json').write_text(json.dumps([{
                'id': 'read', 'skills': ['read-paper'], 'prompt': 'Read the supplied abstract.',
                'criteria': ['Stay within supplied evidence.'],
            }]))
            example = root / 'examples' / 'case'
            example.mkdir(parents=True)
            (example / 'README.md').write_text('[Proposal](proposal.md)\n')
            issues, _, _ = validator.validate_repo(root)
            self.assertTrue(any('missing local link: proposal.md' in issue for issue in issues))
            (example / 'proposal.md').write_text('A proposed study, not an observed result.\n')
            self.assertEqual([], validator.validate_repo(root)[0])



class ReleaseAndRoutingTests(unittest.TestCase):
    def test_routing_rejects_unknown_target_and_requires_none(self):
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'routing.json'
            p.write_text(json.dumps([{'id':'x','request':'Read a paper','expected':'other'}]))
            self.assertTrue(validator.validate_routing(p,{'read-paper'}))
            p.write_text(json.dumps([{'id':'x','request':'Read a paper','expected':'read-paper'},
                                    {'id':'y','request':'Send mail','expected':'none'}]))
            self.assertEqual([],validator.validate_routing(p,{'read-paper'}))

if __name__ == '__main__':
    unittest.main()
