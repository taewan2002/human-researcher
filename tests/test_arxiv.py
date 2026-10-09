from io import BytesIO
from pathlib import Path
import sys
import os
import subprocess
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'skills/trace-research/scripts'))
import citation_sources as sources
import fetch_arxiv as fetcher
import forward_citations as citations

META = {'arxiv': '2106.09685', 'versioned_id': '2106.09685v1',
        'title': 'A Reliable Canonical Seed Paper', 'url': 'https://arxiv.org/abs/2106.09685v1'}


class ArxivTests(unittest.TestCase):
    def test_input_forms_preserve_version(self):
        for value in ('2106.09685v1', 'https://arxiv.org/abs/2106.09685v1',
                      'https://arxiv.org/pdf/2106.09685v1.pdf?download=1',
                      'https://doi.org/10.48550/arXiv.2106.09685v1'):
            self.assertEqual('2106.09685v1', fetcher.input_id(value))
        self.assertEqual('hep-th/9901001v3', fetcher.input_id('hep-th/9901001v3'))
        with self.assertRaises(ValueError):
            fetcher.input_id('https://example.com/paper.pdf')

    def test_wrong_metadata_version_is_rejected(self):
        with patch.object(sources, 'arxiv_entries', return_value=[META]), patch.object(sources.HTTP, 'text', return_value='unused'):
            with self.assertRaises(sources.FetchError):
                sources.canonical_arxiv(sources.HTTP(), '2106.09685v2')

    def test_binary_cache_preserves_pdf_bytes(self):
        raw = b'%PDF-1.7\n\xff\x00\xfe'
        with tempfile.TemporaryDirectory() as temp, patch.object(sources, 'urlopen', return_value=BytesIO(raw)) as request:
            http = sources.HTTP(temp)
            self.assertEqual(raw, http.raw('https://example.test/paper.pdf'))
            self.assertEqual(raw, http.raw('https://example.test/paper.pdf'))
            self.assertEqual(1, request.call_count)

    def test_html_failure_falls_back_to_versioned_pdf(self):
        class Client:
            def text(self, url):
                raise sources.FetchError('unavailable', 'HTTP 404')
            def raw(self, url):
                self.url = url
                return b'%PDF-test'
        http = Client()
        with tempfile.TemporaryDirectory() as temp, patch.object(fetcher, 'canonical_arxiv', return_value=META), patch.object(fetcher, 'pdf_pages', return_value=['First page', 'Second page']):
            record = fetcher.fetch('2106.09685v1', temp, extract_text=True, http=http)
            self.assertEqual('full_text_pdf', record['access'])
            self.assertEqual('https://arxiv.org/pdf/2106.09685v1', http.url)
            self.assertEqual(2, record['text_extraction']['pages'])
            self.assertFalse(record['render_inspected'])
            self.assertIn('--- PDF page 2 ---', (Path(temp) / '2106.09685v1.txt').read_text())

    def test_failed_body_keeps_abstract_only_and_no_false_pdf(self):
        class Client:
            def text(self, url):
                return '<html>Access denied</html>'
            def raw(self, url):
                return b'<html>Access denied</html>'
        with tempfile.TemporaryDirectory() as temp, patch.object(fetcher, 'canonical_arxiv', return_value=META):
            record = fetcher.fetch('2106.09685', temp, http=Client())
            self.assertEqual('metadata_only', record['status'])
            self.assertEqual('abstract', record['access'])
            self.assertEqual([], list(Path(temp).glob('*.pdf')))

    def test_existing_different_file_is_preserved(self):
        with tempfile.TemporaryDirectory() as temp, patch.object(fetcher, 'canonical_arxiv', return_value=META):
            path = Path(temp) / '2106.09685v1.metadata.json'
            path.write_text('local edits')
            record = fetcher.fetch('2106.09685', temp)
            self.assertEqual('local_conflict', record['error_status'])
            self.assertEqual('local edits', path.read_text())

    def test_pdf_reference_requires_same_entry_and_not_body(self):
        title = META['title']
        entry = '[28] A. Author. ' + title + '. arXiv:2106.09685, 2021.'
        match = sources.pdf_bibliography_match(['Body mentions 2106.09685.', 'References\n' + entry], '2106.09685', title)
        self.assertEqual('bibliography_verified', match['status'])
        self.assertEqual(2, match['page'])
        self.assertEqual('[28]', match['entry'])
        for text in (entry, 'References\n[1] ' + title + '\n[2] Other. 2106.09685',
                     'References\n[1] ' + title + '. 2106.096850',
                     'References\n[1] Other.\nAppendix A\n' + entry):
            self.assertNotEqual('bibliography_verified', sources.pdf_bibliography_match([text], '2106.09685', title)['status'])

    def test_bibliography_pdf_fallback_reports_page(self):
        class Client:
            def text(self, url):
                raise sources.FetchError('unavailable', 'HTTP 404')
            def raw(self, url):
                return b'%PDF-test'
        with patch.object(sources, 'pdf_pages', return_value=['References\n[1] ' + META['title'] + '. arXiv:2106.09685']):
            match = sources.verify_arxiv_bibliography(Client(), {'versioned_id': '2305.14314v1'}, '2106.09685', META['title'])
        self.assertEqual('bibliography_verified', match['status'])
        self.assertTrue(match['source'].endswith('2305.14314v1#page=1'))

    def test_pdf_extraction_uses_actual_pages(self):
        from pypdf import PdfWriter
        writer = PdfWriter()
        writer.add_blank_page(width=72, height=72)
        writer.add_blank_page(width=72, height=72)
        buffer = BytesIO()
        writer.write(buffer)
        self.assertEqual(['', ''], sources.pdf_pages(buffer.getvalue()))
        with self.assertRaises(sources.FetchError):
            sources.pdf_pages(b'<html>Not a PDF</html>')

    def test_cached_openalex_404_allows_identifier_fallback(self):
        class Client:
            def json(self, url, headers):
                if '/works/https:' in url:
                    raise sources.FetchError('unavailable', 'HTTP 404', 404)
                return {'results': [{'id': 'https://openalex.org/W1',
                                     'doi': 'https://doi.org/10.48550/arxiv.2106.09685'}]}
        result = citations.resolve(citations.CachedOpenAlex(Client()), 'arxiv', '2106.09685')
        self.assertEqual('https://openalex.org/W1', result['id'])


class IsolatedCLITests(unittest.TestCase):
    def test_isolated_entrypoints_find_siblings_without_cwd_or_pythonpath(self):
        scripts = Path(__file__).resolve().parents[1] / 'skills/trace-research/scripts'
        with tempfile.TemporaryDirectory() as temp:
            for name in ('forward_citations.py', 'citation_sources.py'):
                (Path(temp) / name).write_text('raise RuntimeError("Unexpected working-directory import")\n')
            for name in ('fetch_arxiv.py', 'forward_citations.py'):
                with self.subTest(script=name):
                    result = subprocess.run(
                        [sys.executable, '-I', str(scripts / name), '--help'],
                        cwd=temp, env=dict(os.environ, PYTHONPATH=temp),
                        text=True, capture_output=True, timeout=15)
                    self.assertEqual(0, result.returncode, result.stderr)
                    self.assertIn('usage:', result.stdout)

    def test_isolated_fetch_rejects_bad_input_before_network_or_writes(self):
        script = Path(__file__).resolve().parents[1] / 'skills/trace-research/scripts/fetch_arxiv.py'
        with tempfile.TemporaryDirectory() as temp:
            output = Path(temp) / 'paper'
            result = subprocess.run(
                [sys.executable, '-I', str(script), 'https://example.org/not-arxiv',
                 '--output', str(output), '--no-cache'],
                cwd=temp, text=True, capture_output=True, timeout=15)
            self.assertEqual(2, result.returncode)
            self.assertIn('Expected a DOI or arXiv', result.stderr)
            self.assertNotIn('Traceback', result.stderr)
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
