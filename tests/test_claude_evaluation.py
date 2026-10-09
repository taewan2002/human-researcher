import json
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from evaluate_formats import claude_invoke
from evaluate import snapshot


class ClaudeEvaluationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.log = self.root / 'logs'

    def tearDown(self):
        self.temp.cleanup()

    def response(self, **extra):
        return SimpleNamespace(returncode=0, stderr='', stdout=json.dumps({
            'result': 'A response.', 'modelUsage': {'reported-model': {}}, **extra}))

    def test_no_tools_isolated_auth_and_actual_model_record(self):
        with patch('evaluate_formats.subprocess.run', return_value=self.response()) as run:
            meta, answer = claude_invoke('input', self.root, self.log, 'sonnet')
        args = run.call_args.args[0]
        self.assertIn('--safe-mode', args)
        self.assertIn('--no-session-persistence', args)
        self.assertEqual('', args[args.index('--tools') + 1])
        self.assertEqual(['reported-model'], meta['reported_models'])
        self.assertEqual('A response.', answer)
        self.assertEqual('input', (self.log / 'prompt.txt').read_text())

    def test_file_tools_exclude_shell_and_network(self):
        with patch('evaluate_formats.subprocess.run', return_value=self.response()) as run:
            claude_invoke('input', self.root, self.log, 'opus', file_tools=True)
        args = run.call_args.args[0]
        self.assertEqual('Read,Glob,Grep,Write,Edit', args[args.index('--tools') + 1])
        self.assertEqual('dontAsk', args[args.index('--permission-mode') + 1])

    def test_structured_output_not_prose_is_used(self):
        with patch('evaluate_formats.subprocess.run', return_value=self.response(structured_output={'x': 1})):
            _, answer = claude_invoke('input', self.root, self.log, 'sonnet', {'type': 'object'})
        self.assertEqual({'x': 1}, json.loads(answer))

    def test_missing_structured_output_is_failure(self):
        with patch('evaluate_formats.subprocess.run', return_value=self.response()):
            with self.assertRaises(RuntimeError):
                claude_invoke('input', self.root, self.log, 'sonnet', {'type': 'object'})
        self.assertEqual('error', json.loads((self.log / 'run.json').read_text())['status'])

    def test_cli_error_is_not_a_passing_execution(self):
        with patch('evaluate_formats.subprocess.run', return_value=self.response(is_error=True)):
            with self.assertRaises(RuntimeError):
                claude_invoke('input', self.root, self.log, 'sonnet')
        self.assertFalse((self.log / 'output.txt').exists())

    def test_timeout_preserves_partial_logs_and_status(self):
        error = subprocess.TimeoutExpired('claude', 1, output=b'partial', stderr=b'waiting')
        with patch('evaluate_formats.subprocess.run', side_effect=error):
            with self.assertRaises(RuntimeError):
                claude_invoke('input', self.root, self.log, 'sonnet', timeout=1)
        self.assertEqual('partial', (self.log / 'events.json').read_text())
        self.assertEqual('timeout', json.loads((self.log / 'run.json').read_text())['status'])

    def test_snapshot_excludes_machine_cache(self):
        for name in ['skills', 'tests']:
            path = self.root / name
            (path / '__pycache__').mkdir(parents=True)
            (path / '__pycache__/cached.pyc').write_bytes(b'cache')
            (path / 'example.md').write_text('source')
        target = self.root / 'snapshot'
        snapshot(self.root, target)
        self.assertFalse(list(target.rglob('*.pyc')))
        self.assertEqual('source', (target / 'skills/example.md').read_text())


if __name__ == '__main__':
    unittest.main()
