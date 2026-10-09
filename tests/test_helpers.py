import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError, URLError

ROOT=Path(__file__).resolve().parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module
citations=load('citations','skills/trace-research/scripts/forward_citations.py')
pages=load('pages','skills/write-proposal/scripts/check_pdf_pages.py')
evaluation=load('evaluation','scripts/evaluate.py')

class FakeClient:
    def __init__(self,replies):self.replies=iter(replies);self.calls=[]
    def get(self,path,params=None):
        self.calls.append((path,params));reply=next(self.replies)
        if isinstance(reply,Exception):raise reply
        return reply

def seed():return {'id':'https://openalex.org/W1','doi':'https://doi.org/10.1234/example','title':'Seed'}
def work(n):return {'id':f'https://openalex.org/W{n}','title':f'Paper {n}', 'referenced_works':['https://openalex.org/W1']}

class CitationTests(unittest.TestCase):
    def test_normalizes_doi_modern_and_legacy_arxiv(self):
        self.assertEqual(('doi','10.1234/example'),citations.normalize_id('https://doi.org/10.1234/Example'))
        self.assertEqual(('arxiv','2106.09685'),citations.normalize_id('https://arxiv.org/pdf/2106.09685v2.pdf'))
        self.assertEqual(('arxiv','hep-th/9901001'),citations.normalize_id('arXiv:hep-th/9901001v3'))
        with self.assertRaises(ValueError):citations.normalize_id('https://unrelated.test/paper')
    def test_uses_forward_filter_and_paginates(self):
        client=FakeClient([seed(),{'results':[work(2)],'meta':{'count':2,'next_cursor':'next'}},
                           {'results':[work(3)],'meta':{'count':2,'next_cursor':None}}])
        result=citations.lookup_index('10.1234/example',2,client)
        self.assertEqual('indexed',result['status']);self.assertEqual(2,len(result['works']))
        self.assertEqual('cites:W1',client.calls[1][1]['filter'])
        self.assertEqual('next',client.calls[2][1]['cursor']);self.assertFalse(result['truncated'])
    def test_network_failure_is_not_verified_empty(self):
        for error in (URLError('offline'),TimeoutError('timed out'),HTTPError('url',429,'rate limited',{},None)):
            result=citations.lookup_index('10.1234/example',client=FakeClient([error]))
            self.assertEqual('unverified',result['status']);self.assertEqual('검증 안 됨',result['message'])
    def test_cursor_alone_does_not_imply_truncation_when_total_is_known(self):
        result=citations.lookup_index('10.1234/example',1,FakeClient([seed(),{'results':[work(2)],'meta':{'count':1,'next_cursor':'unused'}}]))
        self.assertFalse(result['truncated'])
    def test_wrong_edge_is_not_reported(self):
        wrong=work(2);wrong['referenced_works']=[]
        result=citations.lookup_index('10.1234/example',client=FakeClient([seed(),{'results':[wrong],'meta':{}}]))
        self.assertEqual('unverified',result['status']);self.assertEqual([],result['works'])
    def test_empty_success_is_distinct_from_network_failure(self):
        result=citations.lookup_index('10.1234/example',client=FakeClient([seed(),{'results':[],'meta':{'count':0}}]))
        self.assertEqual('indexed',result['status']);self.assertEqual(0,result['total_in_index'])
    def test_truncation_and_identifier_mismatch(self):
        result=citations.lookup_index('10.1234/example',1,FakeClient([seed(),{'results':[work(2)],'meta':{'count':500,'next_cursor':'x'}}]))
        self.assertTrue(result['truncated'])
        other=seed();other['doi']='https://doi.org/10.1234/other'
        self.assertEqual('unverified',citations.lookup_index('10.1234/example',client=FakeClient([other]))['status'])
    def test_arxiv_search_requires_exact_location_not_title_similarity(self):
        missing=HTTPError('url',404,'missing',{},None)
        near={'id':'https://openalex.org/W8','title':'2106.09685','locations':[]}
        exact={'id':'https://openalex.org/W1','title':'Resolved','locations':[{'landing_page_url':'http://arxiv.org/abs/2106.09685v2'}]}
        client=FakeClient([missing,{'results':[near,exact]},{'results':[],'meta':{'count':0}}])
        self.assertEqual('indexed',citations.lookup_index('2106.09685',client=client)['status'])

class PDFTests(unittest.TestCase):
    def test_actual_one_and_two_page_files(self):
        from pypdf import PdfWriter
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'a PDF.pdf'
            for count in (1,2):
                writer=PdfWriter()
                for _ in range(count):writer.add_blank_page(width=420,height=297)
                with p.open('wb') as f:writer.write(f)
                result,code=pages.check(p)
                self.assertEqual(count,result['pages']);self.assertEqual(0 if count==1 else 1,code)
    def test_corrupt_missing_and_encrypted_are_unverified(self):
        from pypdf import PdfWriter
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'input.pdf'
            self.assertEqual(2,pages.check(p)[1])
            p.write_bytes(b'not a PDF');self.assertEqual(2,pages.check(p)[1])
            w=PdfWriter();w.add_blank_page(width=10,height=10);w.encrypt('secret')
            with p.open('wb') as f:w.write(f)
            self.assertEqual(2,pages.check(p)[1])
    def test_pdfinfo_fallback_checks_process_result(self):
        import subprocess
        with tempfile.TemporaryDirectory() as temp:
            p=Path(temp)/'a.pdf';p.write_bytes(b'%PDF')
            with patch.dict('sys.modules',{'pypdf':None}),patch('shutil.which',return_value='/bin/pdfinfo'),patch('subprocess.run',return_value=subprocess.CompletedProcess([],0,'Pages: 2\n','')):
                self.assertEqual((2,'pdfinfo'),pages.count_pages(p))

class EvaluationTests(unittest.TestCase):
    def test_execution_does_not_receive_grading_criteria(self):
        case={'id':'neutral','skills':['read-paper'],'fixtures':['tests/fixtures/papers.md'],
              'prompt':'Summarize the abstract.','criteria':['SECRET EXPECTED ANSWER']}
        for condition in (False,True):
            text=evaluation.execution_prompt(case,ROOT,condition)
            self.assertNotIn('SECRET EXPECTED ANSWER',text)
            self.assertEqual(condition,'<skill name=' in text)
    def test_missing_grade_is_an_incomplete_run(self):
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp)
            jobs=[({'id':'a'},'with_skill'),({'id':'a'},'without_skill')]
            evaluation.write_json(run/'cases/a/with_skill/grade.json',{'criteria':[]})
            self.assertEqual(['a/without_skill'],evaluation.missing_grades(run,jobs))
    def test_summary_keeps_unassessed_separate(self):
        with tempfile.TemporaryDirectory() as temp:
            run=Path(temp);evaluation.write_json(run/'cases/a/without_skill/grade.json',{'criteria':[{'verdict':'pass'},{'verdict':'unassessed'}]})
            result=evaluation.summarize(run)['without_skill']
            self.assertEqual(0,result['all_pass_cases']);self.assertEqual(1,result['unassessed'])
    def test_claude_engine_is_isolated_without_web_tools(self):
        cmd=evaluation.claude_command('sonnet','low')
        self.assertIn('--safe-mode',cmd);self.assertIn('--no-session-persistence',cmd)
        tools=cmd[cmd.index('--tools')+1].split(',')
        self.assertNotIn('WebSearch',tools);self.assertNotIn('WebFetch',tools)
        self.assertTrue(json.loads(cmd[cmd.index('--settings')+1])['sandbox']['enabled'])
    def test_claude_engine_records_result_and_errors(self):
        import subprocess
        reply=json.dumps({'result':'answer','is_error':False,'usage':{'output_tokens':3},'modelUsage':{'claude-test':{}}})
        with tempfile.TemporaryDirectory() as temp:
            log=Path(temp)/'log'
            with patch('subprocess.run',return_value=subprocess.CompletedProcess([],0,reply,'')):
                meta=evaluation.invoke('prompt',Path(temp),log,'sonnet','low',60,engine='claude')
            self.assertEqual('completed',meta['status']);self.assertEqual(['claude-test'],meta['reported_models'])
            self.assertEqual('answer',(log/'output.txt').read_text())
            failed=json.dumps({'result':'Not logged in','is_error':True})
            with patch('subprocess.run',return_value=subprocess.CompletedProcess([],0,failed,'')):
                meta=evaluation.invoke('prompt',Path(temp),Path(temp)/'failed','sonnet','low',60,engine='claude')
            self.assertEqual('error',meta['status']);self.assertFalse((Path(temp)/'failed/output.txt').exists())


class RoutingTests(unittest.TestCase):
    def test_routing_hides_expected_labels_and_compares_exactly(self):
        import sys
        sys.path.insert(0,str(ROOT/'scripts'))
        import evaluate_routing
        cases=[{'id':'a','request':'Read this paper','expected':'read-paper'}]
        text=evaluate_routing.routing_prompt(cases,{'read-paper':'Read a paper'})
        self.assertNotIn('expected',text)
        rows=evaluate_routing.compare(cases,[{'id':'a','skill':'none','reason':'wrong'}])
        self.assertFalse(rows[0]['pass'])
        with self.assertRaises(ValueError):evaluate_routing.compare(cases,[])

if __name__ == '__main__':
    unittest.main()
