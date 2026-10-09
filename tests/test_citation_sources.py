import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import HTTPError
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skills/trace-research/scripts'))
import citation_sources as sources
import forward_citations as citations

CANON={'arxiv':'2106.09685','versioned_id':'2106.09685v2','title':'A Reliable Canonical Seed Paper','authors':['A Author'],'year':2021,'url':'https://arxiv.org/abs/2106.09685v2'}
CAND={'arxiv':'2305.14314','versioned_id':'2305.14314v1','title':'A Follow-up Paper','authors':['B Author'],'year':2023,'url':'https://arxiv.org/abs/2305.14314v1'}
HTML='<li class="ltx_bibitem" id="bib28"><span>A Reliable Canonical Seed Paper.</span><a href="https://arxiv.org/abs/2106.09685">arXiv</a></li>'

class SourceTests(unittest.TestCase):
    def test_bibliography_requires_exact_identifier_in_entry(self):
        self.assertEqual('bibliography_verified',sources.bibliography_match(HTML,'2106.09685',CANON['title'])['status'])
        self.assertEqual('unavailable',sources.bibliography_match('<p>2106.09685</p>','2106.09685',CANON['title'])['status'])
        changed=HTML.replace('2106.09685','2106.096850').replace(CANON['title'],'Other title')
        self.assertEqual('not_found_in_checked_bibliography',sources.bibliography_match(changed,'2106.09685',CANON['title'])['status'])
        self.assertEqual('title_match_only',sources.bibliography_match(HTML.replace('2106.09685','9999.00000'),'2106.09685',CANON['title'])['status'])
    def test_empty_bibliography_is_not_no_citation(self):
        self.assertEqual('unavailable',sources.bibliography_match('<html>unavailable</html>','2106.09685','A title')['status'])
    def test_conflicting_index_title_is_not_verified_and_arxiv_can_recover(self):
        indexed={'status':'indexed','seed':{'id':'W1','title':'Wrong unrelated title'},'works':[
            {'id':'W2','title':'Indexed candidate','doi':'https://doi.org/10.48550/arxiv.2305.14314'}],
            'total_in_index':123,'truncated':True}
        with patch.object(citations,'canonical_arxiv',return_value=CANON),patch.object(citations,'lookup_index',return_value=indexed),patch.object(citations,'search_arxiv',return_value=[CAND]),patch.object(citations,'verify_arxiv_bibliography',return_value={'status':'bibliography_verified','source':'https://arxiv.org/html/2305.14314v1#bib28'}):
            d=citations.run_lookup('2106.09685',provider='openalex')
        self.assertEqual(CANON['title'],d['seed']['title'])
        self.assertEqual('metadata_conflict',d['sources'][0]['metadata_status'])
        self.assertEqual(1,len(d['works']))
        self.assertEqual('bibliography_verified',d['works'][0]['edge_status'])
        self.assertIn('arxiv_search',d['works'][0]['discovered_via'])
        with patch.object(citations,'canonical_arxiv',return_value=CANON),patch.object(citations,'lookup_index',return_value=indexed):
            d=citations.run_lookup('2106.09685',provider='openalex',discover_limit=0)
        self.assertEqual([],d['works']);self.assertEqual(1,len(d['related_candidates']))
    def test_provider_failure_does_not_hide_other_source_or_invent_discovery(self):
        with patch.object(citations,'canonical_arxiv',side_effect=[CANON,CAND]),patch.object(citations,'lookup_index',return_value={'status':'unverified','reason':'offline'}),patch.object(citations,'semantic_citations',side_effect=sources.FetchError('rate_limited','HTTP 429')),patch.object(citations,'verify_arxiv_bibliography',return_value={'status':'bibliography_verified','source':'primary'}):
            d=citations.run_lookup('2106.09685',discover_limit=0,citing=['2305.14314'])
        self.assertEqual('rate_limited',d['sources'][1]['status'])
        self.assertEqual(['user_supplied_candidate'],d['works'][0]['discovered_via'])
        self.assertEqual('partial',d['status'])
    def test_filters_are_sent_to_index_before_limit(self):
        class Client:
            def __init__(self):self.calls=[]
            def get(self,path,params=None):
                self.calls.append(params)
                if params is None:return {'id':'https://openalex.org/W1','doi':'https://doi.org/10.1234/test','title':'Seed'}
                return {'results':[],'meta':{'count':0}}
        client=Client()
        citations.lookup_index('10.1234/test',client=client,search='quantized',sort='oldest',from_year=2023,to_year=2024)
        self.assertEqual('publication_date:asc',client.calls[1]['sort'])
        self.assertEqual('quantized',client.calls[1]['search'])
        self.assertIn('from_publication_date:2023-01-01',client.calls[1]['filter'])
        self.assertIn('to_publication_date:2024-12-31',client.calls[1]['filter'])
    def test_long_retry_after_stops_and_does_not_cache_error(self):
        error=HTTPError('https://example.test',429,'rate limit',{'Retry-After':'3600'},None)
        with tempfile.TemporaryDirectory() as temp,patch.object(sources,'urlopen',side_effect=error) as request,patch.object(sources.time,'sleep') as sleep:
            http=sources.HTTP(temp)
            for _ in range(2):
                with self.assertRaises(sources.FetchError) as raised:http.text('https://example.test/a')
                self.assertEqual('rate_limited',raised.exception.status)
            self.assertEqual(1,request.call_count)
            self.assertEqual([],list(Path(temp).iterdir()))
            self.assertFalse(any(c.args[0]>3 for c in sleep.call_args_list))
    def test_success_cache_avoids_duplicate_requests(self):
        from io import BytesIO
        with tempfile.TemporaryDirectory() as temp,patch.object(sources,'urlopen',return_value=BytesIO(b'{"ok":true}')) as request:
            http=sources.HTTP(temp)
            self.assertEqual({'ok':True},http.json('https://example.test/a'))
            self.assertEqual({'ok':True},http.json('https://example.test/a'))
            self.assertEqual(1,request.call_count)
    def test_invalid_ranges_and_relevance_require_query(self):
        for kwargs in ({'from_year':2024,'to_year':2023},{'sort':'relevance'},{'discover_limit':21}):
            with self.assertRaises(ValueError):citations.run_lookup('2106.09685',**kwargs)
    def test_semantic_success_filters_only_its_bounded_pool(self):
        class Client:
            def json(self,url,headers):
                if '/citations?' not in url:
                    return {'title':CANON['title'],'externalIds':{'ArXiv':'2106.09685'}}
                return {'next':20,'data':[
                    {'citingPaper':{'paperId':'a','title':'Quantized method','year':2023,'citationCount':9,'externalIds':{'ArXiv':'2305.14314'}}},
                    {'citingPaper':{'paperId':'b','title':'Quantized later','year':2025,'citationCount':20}},
                    {'citingPaper':{'paperId':'c','title':'Other topic','year':2023}},
                ]}
        _,works,scope=citations.semantic_citations(Client(),'2106.09685',5,'quantized',2023,2023,'citations')
        self.assertEqual(['2305.14314'],[w['arxiv'] for w in works])
        self.assertTrue(scope['has_more']);self.assertEqual(3,scope['pool_size'])
    def test_arxiv_doi_version_does_not_change_work_level_lookup(self):
        with patch.object(citations,'canonical_arxiv',return_value=CANON) as canonical,patch.object(citations,'lookup_index',return_value={'status':'unverified','reason':'offline'}):
            citations.run_lookup('https://doi.org/10.48550/arxiv.2106.09685v1',provider='openalex',discover_limit=0)
        self.assertEqual('2106.09685',canonical.call_args.args[1])

if __name__=='__main__':unittest.main()
