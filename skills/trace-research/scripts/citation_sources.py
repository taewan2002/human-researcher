"""HTTP, canonical arXiv metadata and bibliography evidence (stdlib, Python 3.9+)."""
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import hashlib
import base64
from io import BytesIO
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
import unicodedata
from urllib.error import HTTPError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


class FetchError(Exception):
    def __init__(self, status, reason, http_status=None):
        super().__init__(reason)
        self.status = status
        self.http_status = http_status


class HTTP:
    """Small public-response cache; keys and error responses are never persisted."""
    def __init__(self, cache=None, timeout=15, ttl=86400):
        self.cache = Path(cache).expanduser() if cache else None
        self.timeout, self.ttl = timeout, ttl
        self.last = {}
        self.blocked = set()

    def raw(self, url, headers=None):
        host = urlsplit(url).hostname
        if host in self.blocked:
            raise FetchError('rate_limited', 'Provider rate limit reached in this run')
        target = self.cache / (hashlib.sha256(url.encode()).hexdigest()+'.json') if self.cache else None
        if target and target.exists():
            try:
                saved = json.loads(target.read_text())
                if time.time()-saved['time'] < self.ttl:
                    return base64.b64decode(saved['data']) if 'data' in saved else saved['text'].encode('utf-8')
            except (ValueError, KeyError, OSError):
                pass
        # arXiv's API asks clients to space requests by three seconds.
        interval = 3 if host == 'export.arxiv.org' else (1 if host == 'api.semanticscholar.org' else 0)
        for attempt in range(2):
            time.sleep(max(0, interval-(time.monotonic()-self.last.get(host, 0))))
            self.last[host] = time.monotonic()
            try:
                request = Request(url, headers={'User-Agent':'HumanResearcher/0.1.0', **(headers or {})})
                with urlopen(request, timeout=self.timeout) as response:
                    raw = response.read(32_000_001)
                if len(raw) > 32_000_000:
                    raise FetchError('unavailable', 'Response exceeds 32 MB limit')
                if target:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_text(json.dumps({'time':time.time(), 'data':base64.b64encode(raw).decode('ascii')}))
                return raw
            except HTTPError as exc:
                if exc.code == 429:
                    value = exc.headers.get('Retry-After', '')
                    try:
                        delay = float(value)
                    except ValueError:
                        try:
                            delay = (parsedate_to_datetime(value)-datetime.now(timezone.utc)).total_seconds()
                        except (TypeError, ValueError):
                            delay = None
                    # Never retry earlier than Retry-After or spin on anonymous 429s.
                    if attempt == 0 and delay is not None and 0 <= delay <= 3:
                        time.sleep(delay)
                        continue
                    self.blocked.add(host)
                    raise FetchError('rate_limited', 'HTTP 429; no further requests to this provider this run') from exc
                raise FetchError('unavailable', 'HTTP '+str(exc.code), exc.code) from exc
            except (OSError, ValueError) as exc:
                raise FetchError('unavailable', type(exc).__name__) from exc
        raise FetchError('unavailable', 'Request did not complete')

    def text(self, url, headers=None):
        try:return self.raw(url, headers).decode('utf-8')
        except UnicodeError as exc:raise FetchError('unavailable', 'Non-text response') from exc

    def json(self, url, headers=None):
        try:
            return json.loads(self.text(url, headers))
        except (ValueError, TypeError) as exc:
            raise FetchError('unavailable', 'Invalid JSON response') from exc


ATOM = {'a':'http://www.w3.org/2005/Atom'}


def arxiv_entries(text):
    try:
        root = ET.fromstring(text)
        entries = []
        for item in root.findall('a:entry', ATOM):
            identifier = item.findtext('a:id', '', ATOM).split('/abs/')[-1]
            if not re.fullmatch(r'(?:\d{4}\.\d{4,5}|[a-z.-]+/\d{7})(?:v\d+)?', identifier, re.I):
                continue
            entries.append({'arxiv':re.sub(r'v\d+$', '', identifier), 'versioned_id':identifier,
                'title':' '.join(item.findtext('a:title', '', ATOM).split()),
                'authors':[a.findtext('a:name', '', ATOM) for a in item.findall('a:author', ATOM)],
                'abstract':' '.join(item.findtext('a:summary', '', ATOM).split()),
                'year':int(item.findtext('a:published', '0000', ATOM)[:4]),
                'url':'https://arxiv.org/abs/'+identifier})
        return entries
    except (ET.ParseError, ValueError) as exc:
        raise FetchError('unavailable', 'Invalid arXiv metadata response') from exc


def canonical_arxiv(http, identifier):
    entries = arxiv_entries(http.text('https://export.arxiv.org/api/query?'+urlencode({'id_list':identifier})))
    matches = [e for e in entries if e['arxiv'].lower() == re.sub(r'v\d+$', '', identifier.lower())]
    if len(matches) != 1:
        raise FetchError('unavailable', 'No unique arXiv metadata record')
    if not matches[0]['title']:
        raise FetchError('unavailable', 'arXiv metadata is missing the paper title')
    if re.search(r'v\d+$',identifier,re.I) and matches[0]['versioned_id'].lower()!=identifier.lower():
        raise FetchError('unavailable','arXiv returned a different version than requested')
    return matches[0]


def search_arxiv(http, query, limit, sort):
    order = {'oldest':('submittedDate','ascending'), 'newest':('submittedDate','descending')}.get(sort, ('relevance','descending'))
    return arxiv_entries(http.text('https://export.arxiv.org/api/query?'+urlencode({
        'search_query':query, 'start':0, 'max_results':limit, 'sortBy':order[0], 'sortOrder':order[1]})))


def normalized_title(title):
    return ''.join(c for c in unicodedata.normalize('NFKC', title).casefold() if c.isalnum())


class Bibliography(HTMLParser):
    """Extract actual LaTeXML bibliography entries, not arbitrary body mentions."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.entries = []
        self.current = None
        self.depth = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if self.current is None and 'ltx_bibitem' in attrs.get('class', '').split():
            self.current = {'anchor':attrs.get('id'), 'text':'', 'links':[]}
            self.depth = 1
        elif self.current is not None and tag == 'li':
            self.depth += 1
        if self.current is not None and tag == 'a' and attrs.get('href'):
            self.current['links'].append(attrs['href'])

    def handle_endtag(self, tag):
        if self.current is not None and tag == 'li':
            self.depth -= 1
            if self.depth == 0:
                self.current['text'] = ' '.join(self.current['text'].split())
                self.entries.append(self.current)
                self.current = None

    def handle_data(self, value):
        if self.current is not None:
            self.current['text'] += value+' '


def bibliography_match(html, seed_id, title):
    parser = Bibliography()
    parser.feed(html)
    possible = None
    for item in parser.entries:
        text = ' '.join([item['text'], *item['links']])
        # Identifier boundaries prevent 2106.09685 from matching 2106.096850.
        id_match = re.search(r'(?<![\w.])'+re.escape(seed_id)+r'(?:v\d+)?(?![\w.])', text, re.I)
        title_match = len(normalized_title(title)) >= 20 and normalized_title(title) in normalized_title(item['text'])
        linked_id = any(re.search(r'(?:arxiv\.org/(?:abs|pdf)/|doi\.org/10\.48550/arxiv\.)'+re.escape(seed_id)+r'(?:v\d+)?(?:\.pdf)?(?:[?#].*)?$', link, re.I) for link in item['links'])
        if id_match or linked_id:
            return {'status':'bibliography_verified','anchor':item['anchor'],'match':'exact_identifier'}
        if title_match:
            possible = {'status':'title_match_only','anchor':item['anchor'],'match':'title_only'}
    if possible:return possible
    return {'status':'not_found_in_checked_bibliography' if parser.entries else 'unavailable',
            'entries_checked':len(parser.entries)}


def pdf_pages(raw):
    if not raw.startswith(b'%PDF-'):
        raise FetchError('unavailable', 'Response is not a PDF')
    try:
        from pypdf import PdfReader
    except ImportError as exc:
        raise FetchError('dependency_missing', 'PDF text extraction needs optional pypdf') from exc
    try:
        reader = PdfReader(BytesIO(raw))
        if reader.is_encrypted:
            raise FetchError('unavailable', 'Encrypted PDF')
        if len(reader.pages)>300:
            raise FetchError('unavailable','PDF exceeds 300-page extraction limit')
        return [page.extract_text() or '' for page in reader.pages]
    except FetchError:
        raise
    except Exception as exc:
        raise FetchError('unavailable', 'PDF extraction failed: '+type(exc).__name__) from exc


def pdf_bibliography_match(pages, seed_id, title):
    # Search only an explicitly detected reference section, never arbitrary mentions.
    active = False
    seen_pages = []
    for number, text in enumerate(pages,1):
        if not active:
            heading = re.search(r'(?im)^\s*(?:\d+[. ]+)?(?:references|bibliography)\s*$',text)
            if heading:
                active = True
                text = text[heading.end():]
        if active:
            end = re.search(r'(?im)^\s*(?:appendix|appendices|supplementary material)\b',text)
            if end:text=text[:end.start()]
            seen_pages.append(number)
            # A whole page can contain the title and ID in different entries.
            # Only classify an edge when both occur in one bounded numbered entry.
            markers = list(re.finditer(r'(?m)^\s*(?:\[\d+\]|\d+\.)\s+', text))
            for i, marker in enumerate(markers):
                entry = text[marker.end():markers[i+1].start() if i+1<len(markers) else len(text)]
                exact = re.search(r'(?<![\w.])'+re.escape(seed_id)+r'(?:v\d+)?(?![\w.])',entry,re.I)
                if exact and len(normalized_title(title))>=20 and normalized_title(title) in normalized_title(entry):
                    return {'status':'bibliography_verified','page':number,'entry':marker[0].strip(),
                            'match':'identifier_and_title_in_numbered_reference'}
            if end:break
    return {'status':'not_found_in_extracted_references' if active else 'unavailable',
            'pages_checked':seen_pages,'limits':'PDF text extraction is not visual inspection; an absent match is not proof of no citation.'}


def verify_arxiv_bibliography(http, candidate, seed_id, title):
    url = 'https://arxiv.org/html/'+candidate['versioned_id']
    try:
        match = bibliography_match(http.text(url), seed_id, title)
        match['source'] = url+('#'+match['anchor'] if match.get('anchor') else '')
        if match['status']!='unavailable':return match
        html_status = 'No readable HTML bibliography'
    except FetchError as exc:
        html_status = str(exc)
    pdf_url = 'https://arxiv.org/pdf/'+candidate['versioned_id']
    try:
        match = pdf_bibliography_match(pdf_pages(http.raw(pdf_url)),seed_id,title)
        match['source'] = pdf_url+('#page='+str(match['page']) if match.get('page') else '')
        match['html_status'] = html_status
        return match
    except FetchError as exc:
        return {'status':exc.status,'reason':str(exc),'source':pdf_url,'html_status':html_status}
