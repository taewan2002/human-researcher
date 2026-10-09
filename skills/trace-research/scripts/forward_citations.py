#!/usr/bin/env python3
"""Find citing papers using indexes and arXiv bibliographies (Python 3.9+).

Basic queries need no key. OPENALEX_API_KEY optionally raises the service budget.
Index evidence is work-level, not proof of agreement, quality, or full coverage.
Use run_lookup for canonical metadata and source-specific relationship evidence.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import json
import os
import re
import socket
from urllib.error import HTTPError, URLError
from urllib.parse import quote, unquote, urlencode, urlsplit
from urllib.request import Request, urlopen

API = 'https://api.openalex.org'


def normalize_id(value):
    value=unquote(value.strip())
    if value.startswith(('https://','http://')):
        parts=urlsplit(value)
        if parts.hostname in ('doi.org','dx.doi.org'):value=parts.path.lstrip('/')
        elif parts.hostname in ('arxiv.org','www.arxiv.org','export.arxiv.org'):
            value=re.sub(r'^/(abs|pdf)/','',parts.path).removesuffix('.pdf')
        else:raise ValueError('Expected a DOI or arXiv identifier, not this URL.')
    value=re.sub(r'^doi:\s*','',value,flags=re.I)
    value=re.sub(r'^arxiv:\s*','',value,flags=re.I)
    if re.fullmatch(r'10\.\d{4,9}/\S+',value) and len(value)<=512:
        return 'doi',value.lower()
    if re.fullmatch(r'(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?',value,re.I):
        return 'arxiv',re.sub(r'v\d+$','',value,flags=re.I).lower()
    raise ValueError('Expected a DOI or arXiv identifier.')


class OpenAlex:
    def __init__(self, timeout=15, api_key=None):
        self.timeout=timeout; self.api_key=api_key

    def get(self,path,params=None):
        url=API+path+('?' + urlencode(params) if params else '')
        headers={'User-Agent':'HumanResearcher/0.1.0 (forward-citation lookup)', 'Accept':'application/json'}
        if self.api_key:headers['Authorization']='Bearer '+self.api_key
        with urlopen(Request(url,headers=headers),timeout=self.timeout) as response:
            return json.load(response)


def matches(work,kind,identifier):
    doi=str(work.get('doi') or '').lower().removeprefix('https://doi.org/').removeprefix('http://doi.org/')
    if kind=='doi':return doi==identifier
    if doi=='10.48550/arxiv.'+identifier:return True
    for location in work.get('locations') or []:
        for key in ('landing_page_url','pdf_url'):
            url=location.get(key)
            if not url:continue
            try:
                if normalize_id(url)==('arxiv',identifier):return True
            except ValueError:pass
    return False


def work_id(value):
    match=re.fullmatch(r'(?:https?://openalex.org/)?(W\d+)',str(value),re.I)
    if not match:raise ValueError('OpenAlex returned an invalid work identifier.')
    return match[1].upper()


def resolve(client,kind,identifier):
    doi=identifier if kind=='doi' else '10.48550/arxiv.'+identifier
    try:
        work=client.get('/works/'+quote('https://doi.org/'+doi,safe='/:'))
        if matches(work,kind,identifier):work_id(work.get('id'));return work
    except HTTPError as exc:
        if exc.code!=404:raise
    if kind=='arxiv':
        # Search is candidate discovery only. Accept an exact DOI/location match.
        candidates=client.get('/works',{'search':identifier,'per_page':100}).get('results',[])
        exact={work_id(w.get('id')):w for w in candidates if matches(w,kind,identifier)}
        if len(exact)==1:return next(iter(exact.values()))
    raise ValueError('No unique exact identifier match in OpenAlex; verification unavailable.')


def lookup_index(identifier,limit=20,client=None,sort="newest",search=None,from_year=None,to_year=None):
    if not 1<=limit<=1000:raise ValueError('limit must be between 1 and 1000')
    kind,normalized=normalize_id(identifier)
    client=client or OpenAlex(api_key=os.environ.get('OPENALEX_API_KEY'))
    result={'status':'unverified','message':'검증 안 됨','requested_id':identifier,
            'checked_at':datetime.now(timezone.utc).isoformat(),'works':[]}
    try:
        seed=resolve(client,kind,normalized);seed_id=work_id(seed['id'])
        rows=[];seen=set();cursor='*';cursors=set();total=None
        while len(rows)<limit:
            if cursor in cursors:raise ValueError('Repeated pagination cursor.')
            cursors.add(cursor)
            params={'filter':'cites:'+seed_id,'per_page':min(100,limit-len(rows)),
                    'cursor':cursor,'select':'id,doi,title,publication_year,referenced_works,locations,cited_by_count'}
            params['sort']={'newest':'publication_date:desc','oldest':'publication_date:asc','citations':'cited_by_count:desc','relevance':'relevance_score:desc'}[sort]
            if search:params['search']=search
            if sort=='relevance' and not search:params['sort']='cited_by_count:desc'
            if from_year:params['filter']+=',from_publication_date:'+str(from_year)+'-01-01'
            if to_year:params['filter']+=',to_publication_date:'+str(to_year)+'-12-31'
            page=client.get('/works',params)
            if not isinstance(page.get('results'),list):raise ValueError('Invalid works response.')
            meta=page.get('meta',{});total=meta.get('count',total)
            for work in page['results']:
                wid=work_id(work.get('id'))
                if seed_id not in {work_id(x) for x in work.get('referenced_works',[])}:
                    raise ValueError('Returned work lacks the requested reference in index metadata.')
                if wid not in seen:
                    rows.append({'id':'https://openalex.org/'+wid,'doi':work.get('doi'),
                        'title':work.get('title'),'year':work.get('publication_year'),
                        'cites':'https://openalex.org/'+seed_id,'locations':work.get('locations',[]),'cited_by_count':work.get('cited_by_count',0),
                        'relationship_source':'OpenAlex cites filter and referenced_works'})
                    seen.add(wid)
            cursor=meta.get('next_cursor')
            if not cursor or not page['results']:break
        result.update(status='indexed',message='OpenAlex 인덱스 내부 연결 조회',
            seed={'id':seed['id'],'doi':seed.get('doi'),'title':seed.get('title')},
            works=rows[:limit],total_in_index=total,
            truncated=(total>len(rows)) if isinstance(total,int) else bool(cursor),
            limits='B → A means B cites A in OpenAlex. Index metadata can be incomplete or incorrect; '
                   'results do not establish agreement, full-text support, or version-specific citations.')
    except (HTTPError,URLError,TimeoutError,socket.timeout,ValueError,KeyError,TypeError) as exc:
        # Never turn an API/network failure into an empty, verified citation set.
        result['reason']='HTTP '+str(exc.code) if isinstance(exc,HTTPError) else str(exc)
    return result


# Keep the command directly runnable and importable without installing a package.
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from citation_sources import (HTTP, FetchError, canonical_arxiv, search_arxiv,
                              normalized_title, verify_arxiv_bibliography)


class CachedOpenAlex(OpenAlex):
    def __init__(self, http):
        self.http = http

    def get(self, path, params=None):
        headers = {}
        key = os.environ.get('OPENALEX_API_KEY')
        if key: headers['Authorization'] = 'Bearer '+key
        try:
            return self.http.json(API+path+('?' + urlencode(params) if params else ''), headers)
        except FetchError as exc:
            if exc.http_status == 404:
                raise HTTPError(API+path,404,str(exc),{},None) from exc
            raise URLError(str(exc)) from exc


def arxiv_id(work):
    candidates = [work.get('doi', '')]
    candidates += [l.get(k, '') for l in work.get('locations', []) for k in ('landing_page_url', 'pdf_url')]
    for value in candidates:
        if not value: continue
        try:
            kind, identifier = normalize_id(value)
            if kind == 'arxiv': return identifier
            if identifier.startswith('10.48550/arxiv.'):
                return identifier.split('arxiv.', 1)[1]
        except ValueError:
            pass
    return None


def semantic_citations(http, identifier, limit, search, from_year, to_year, sort):
    kind, value = normalize_id(identifier)
    seed = ('ARXIV:' if kind == 'arxiv' else 'DOI:')+value
    fields = 'title,externalIds,year,citationCount'
    headers = {'x-api-key':os.environ['SEMANTIC_SCHOLAR_API_KEY']} if os.environ.get('SEMANTIC_SCHOLAR_API_KEY') else {}
    root = 'https://api.semanticscholar.org/graph/v1/paper/'+quote(seed, safe=':')
    record = http.json(root+'?'+urlencode({'fields':fields}), headers)
    external = record.get('externalIds') or {}
    if (kind == 'arxiv' and external.get('ArXiv') != value) or (kind == 'doi' and str(external.get('DOI','')).lower() != value):
        raise FetchError('unavailable', 'Semantic Scholar identifier mismatch')
    # One bounded pool; do not claim globally filtered/sorted Semantic Scholar coverage.
    data = http.json(root+'/citations?'+urlencode({'fields':fields, 'limit':min(100,max(limit,20))}), headers)
    works = []
    for row in data.get('data', []):
        work = row.get('citingPaper') or {}
        year = work.get('year')
        if from_year and (not year or year < from_year): continue
        if to_year and (not year or year > to_year): continue
        if search and search.casefold() not in (work.get('title') or '').casefold(): continue
        ids = work.get('externalIds') or {}
        works.append({'id':'https://www.semanticscholar.org/paper/'+work['paperId'],
            'title':work.get('title'), 'year':year, 'arxiv':ids.get('ArXiv'),
            'doi':'https://doi.org/'+ids['DOI'] if ids.get('DOI') else None,
            'cited_by_count':work.get('citationCount',0)})
    if sort != 'relevance':
        works.sort(key=lambda w:(w.get('cited_by_count') or 0) if sort=='citations' else (w.get('year') or 0), reverse=sort!='oldest')
    return record, works[:limit], {'pool_size':len(data.get('data',[])), 'has_more':data.get('next') is not None,
        'ordering_scope':'bounded fetched pool; search is title-only, not global ranking'}


def run_lookup(identifier, limit=20, provider='auto', sort='newest', search=None,
               from_year=None, to_year=None, discover_limit=5, citing=None, http=None):
    if not 1 <= limit <= 1000 or not 0 <= discover_limit <= 20:
        raise ValueError('limit must be 1–1000 and discover-limit 0–20')
    if any(year is not None and not 1000<=year<=2999 for year in (from_year,to_year)):
        raise ValueError('years must be between 1000 and 2999')
    if from_year and to_year and from_year > to_year:
        raise ValueError('from-year must not exceed to-year')
    if sort == 'relevance' and not search:
        raise ValueError('relevance sort requires --search')
    kind, value = normalize_id(identifier)
    seed_arxiv = value if kind=='arxiv' else (value.split('arxiv.',1)[1] if value.startswith('10.48550/arxiv.') else None)
    if seed_arxiv:
        seed_arxiv = re.sub(r'v\d+$', '', seed_arxiv, flags=re.I)
        identifier = seed_arxiv
    http = http or HTTP()
    result = {'schema_version':2, 'status':'unverified', 'message':'검증 안 됨',
        'checked_at':datetime.now(timezone.utc).isoformat(), 'requested_id':identifier,
        'seed':{'identity_status':'unverified'}, 'sources':[], 'works':[], 'related_candidates':[], 'candidate_checks':[],
        'query':{'provider':provider,'sort':sort,'search':search,'from_year':from_year,'to_year':to_year,
                 'index_limit_per_provider':limit,'arxiv_discovery_limit':discover_limit},
        'coverage':'Partial, source-specific coverage. Counts are never summed across providers. Missing index entries are not evidence of no citation.'}
    canonical = None
    if seed_arxiv:
        try:
            canonical = canonical_arxiv(http, seed_arxiv)
            result['seed'] = {**canonical, 'identity_status':'confirmed_arxiv_metadata'}
        except FetchError as exc:
            result['sources'].append({'provider':'arxiv_metadata','status':exc.status,'reason':str(exc)})
    pending = []
    for name in (['openalex','semantic-scholar'] if provider=='auto' else [provider]):
        try:
            if name == 'openalex':
                indexed = lookup_index(identifier,limit,CachedOpenAlex(http),sort,search,from_year,to_year)
                if indexed['status'] != 'indexed':
                    result['sources'].append({'provider':name,'status':'unavailable','reason':indexed.get('reason')})
                    continue
                record = indexed['seed']; works = indexed['works']
                details = {'matched_total_in_index':indexed['total_in_index'],'truncated':indexed['truncated'],
                           'ordering_scope':'server-side filtered index query'}
            else:
                record, works, details = semantic_citations(http,identifier,limit,search,from_year,to_year,sort)
            consistency = ('consistent' if normalized_title(record.get('title') or '') == normalized_title(canonical['title'])
                           else 'metadata_conflict') if canonical else 'not_independently_checked'
            result['sources'].append({'provider':name, 'status':'indexed','metadata_status':consistency,
                                      'record':record, **details})
            if not canonical and not result['seed'].get('title'):
                result['seed'].update(title=record.get('title'), source=name)
            for work in works:
                work = {k:v for k,v in work.items() if k not in ('locations','referenced_works','relationship_source','cites')}
                if not work.get('arxiv'):
                    original = next((w for w in works if w['id']==work['id']), work)
                    work['arxiv'] = arxiv_id(original)
                work['evidence'] = [{'source':name,'status':'indexed','seed_metadata_status':consistency}]
                work['discovered_via'] = [name+'_citations']
                work['edge_status'] = 'metadata_conflict' if consistency=='metadata_conflict' else 'indexed'
                pending.append(work)
        except (FetchError, ValueError, KeyError, TypeError) as exc:
            result['sources'].append({'provider':name,'status':getattr(exc,'status','unavailable'),'reason':str(exc)})
    discovered = []
    if canonical and discover_limit:
        # Search finds candidates; only their actual bibliography can establish an edge.
        term = canonical['title'].split(':',1)[0] if ':' in canonical['title'] else canonical['title']
        quote_term = lambda t: t.replace('"',' ').replace('\\',' ')
        query = 'all:"'+quote_term(term)+'"'
        if search: query += ' AND all:"'+quote_term(search)+'"'
        if from_year or to_year:
            query += ' AND submittedDate:['+str(from_year or 1991)+'01010000 TO '+str(to_year or 2999)+'12312359]'
        try:
            discovered = search_arxiv(http,query,discover_limit,sort)
            result['sources'].append({'provider':'arxiv_search','status':'candidates_only','query':query,
                'returned':len(discovered),'sort':sort if sort in ('newest','oldest') else 'relevance'})
        except FetchError as exc:
            result['sources'].append({'provider':'arxiv_search','status':exc.status,'reason':str(exc),'query':query})
    for candidate in discovered:
        if candidate['arxiv'] != seed_arxiv:
            pending.append({**candidate,'id':candidate['url'],'edge_status':'unverified',
                            'evidence':[],'discovered_via':['arxiv_search']})
    for supplied in citing or []:
        try:
            c_kind, c_id = normalize_id(supplied)
            if c_kind != 'arxiv':raise ValueError('--citing currently takes arXiv IDs')
            candidate = canonical_arxiv(http,c_id)
            pending.append({**candidate,'id':candidate['url'],'edge_status':'unverified',
                            'evidence':[],'discovered_via':['user_supplied_candidate']})
        except (FetchError, ValueError) as exc:
            result['candidate_checks'].append({'requested_id':supplied,'status':'unavailable','reason':str(exc)})
    # Exact identifiers only: title similarity never merges two papers.
    merged = {}
    for work in pending:
        key = ('arxiv:'+work['arxiv']) if work.get('arxiv') else ((work.get('doi') or work['id']).lower())
        if key in merged:
            existing = merged[key]
            existing['evidence'] += work['evidence']
            existing['discovered_via'] = list(dict.fromkeys(existing['discovered_via']+work['discovered_via']))
            if work.get('versioned_id'):existing.update({k:work[k] for k in ('versioned_id','title','url','authors')})
            if work['edge_status']=='indexed':existing['edge_status']='indexed'
        else:merged[key]=work
    for work in merged.values():
        if canonical and work.get('arxiv') and ('arxiv_search' in work['discovered_via'] or 'user_supplied_candidate' in work['discovered_via']):
            evidence = verify_arxiv_bibliography(http, work, seed_arxiv, canonical['title'])
            work['evidence'].append(evidence)
            result['candidate_checks'].append({'arxiv':work['arxiv'],**evidence})
            if evidence['status']=='bibliography_verified':work['edge_status']='bibliography_verified'
        target = 'works' if work['edge_status'] in ('indexed','bibliography_verified') else 'related_candidates'
        result[target].append(work)
    if result['works'] or any(s['status'] in ('indexed','candidates_only') for s in result['sources']):
        result['status']='partial'
        result['message']='부분 조회 — 논문 정보와 인용 근거 상태를 항목별로 확인하세요'
    return result


def main():
    p=argparse.ArgumentParser(description='Find citing candidates and distinguish index edges from bibliography evidence.')
    p.add_argument('identifier');p.add_argument('--limit',type=int,default=20)
    p.add_argument('--provider',choices=['auto','openalex','semantic-scholar'],default='auto')
    p.add_argument('--sort',choices=['newest','oldest','citations','relevance'],default='newest')
    p.add_argument('--search');p.add_argument('--from-year',type=int);p.add_argument('--to-year',type=int)
    p.add_argument('--discover-limit',type=int,default=5)
    p.add_argument('--citing',action='append',help='Check a supplied arXiv candidate; does not count as discovery')
    p.add_argument('--cache-dir',type=Path,default=Path.home()/'.cache/human-researcher/citations')
    p.add_argument('--no-cache',action='store_true')
    args=p.parse_args()
    try:
        result=run_lookup(args.identifier,args.limit,args.provider,args.sort,args.search,args.from_year,args.to_year,
                          args.discover_limit,args.citing,HTTP(None if args.no_cache else args.cache_dir))
    except ValueError as exc:p.error(str(exc))
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__':main()
