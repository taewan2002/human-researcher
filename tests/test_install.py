import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

spec=importlib.util.spec_from_file_location('installer',Path(__file__).resolve().parents[1]/'scripts/install.py')
installer=importlib.util.module_from_spec(spec);spec.loader.exec_module(installer)

class InstallTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name)
        self.source=self.root/'source';self.target=self.root/'target'
        self.package=self.source/'skills'/'read-paper';self.package.mkdir(parents=True)
        (self.package/'SKILL.md').write_text('original')
    def tearDown(self):self.temp.cleanup()
    def run_install(self,rev='a',dry=False):
        return installer.install(self.source,self.target,['read-paper'],rev,'v0.1.0',dry)['packages'][0]['status']
    def test_install_records_source_and_unchanged_update_is_safe(self):
        self.assertEqual('installed',self.run_install())
        lock=json.loads((self.target/installer.LOCK_NAME).read_text())
        self.assertEqual('a',lock['packages']['read-paper']['commit'])
        self.assertEqual('already_present',self.run_install())
        (self.package/'SKILL.md').write_text('upstream update')
        self.assertEqual('updated',self.run_install('b'))
        self.assertEqual('upstream update',(self.target/'read-paper/SKILL.md').read_text())
    def test_local_edits_and_unknown_package_are_preserved(self):
        self.run_install();dest=self.target/'read-paper/SKILL.md';dest.write_text('local edit')
        (self.package/'SKILL.md').write_text('new upstream')
        self.assertEqual('conflict',self.run_install('b'));self.assertEqual('local edit',dest.read_text())
        (self.target/installer.LOCK_NAME).unlink()
        self.assertEqual('conflict',self.run_install('b'))
    def test_rollback_to_original_is_possible(self):
        self.run_install();(self.package/'SKILL.md').write_text('new')
        self.run_install('b');(self.package/'SKILL.md').write_text('original')
        self.assertEqual('updated',self.run_install('a'))
    def test_dry_run_and_symlink_do_not_replace_content(self):
        self.assertEqual('installed',self.run_install(dry=True));self.assertFalse(self.target.exists())
        self.target.mkdir();(self.target/'read-paper').symlink_to(self.package,target_is_directory=True)
        self.assertEqual('conflict',self.run_install());self.assertTrue((self.target/'read-paper').is_symlink())
    def test_runtime_cache_is_not_installed_or_treated_as_user_edit(self):
        cache=self.package/'__pycache__';cache.mkdir();(cache/'script.pyc').write_bytes(b'cache')
        self.run_install()
        self.assertFalse((self.target/'read-paper/__pycache__').exists())
        cache=self.target/'read-paper/__pycache__';cache.mkdir();(cache/'runtime.pyc').write_bytes(b'cache')
        self.assertEqual('already_present',self.run_install())
    def test_only_tracked_source_files_are_distributed(self):
        (self.package/'.env').write_text('private')
        installer.install(self.source,self.target,['read-paper'],'a','v0.1.0',tracked={'skills/read-paper/SKILL.md'})
        self.assertFalse((self.target/'read-paper/.env').exists())
    def test_extra_local_file_counts_as_a_local_edit(self):
        self.run_install();(self.target/'read-paper/notes.txt').write_text('user notes')
        self.assertEqual('conflict',self.run_install())

if __name__=='__main__':unittest.main()
