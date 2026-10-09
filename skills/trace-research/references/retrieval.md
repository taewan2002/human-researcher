# arXiv retrieval and citation evidence

Run these commands from this skill directory with Python 3.9+. They write only to the requested output or cache directory. No server or API key is required for arXiv; optional index keys can raise provider limits.

## Retrieve the exact paper

```sh
python3 scripts/fetch_arxiv.py https://arxiv.org/abs/2106.09685v1 --output papers/lora --format auto
python3 scripts/fetch_arxiv.py 2106.09685v1 --output papers/lora --format pdf --text
```

Accepts an arXiv ID, abs/PDF URL, arXiv DOI, and legacy IDs such as `hep-th/9901001`. Explicit `v1` is preserved; an unversioned input resolves to the version returned by arXiv's metadata API. Metadata records title, authors, abstract, year, source URL, and resolved version. Files are named by version, with byte counts and SHA-256 hashes in the output record. Differing local files are preserved and reported as conflicts.

`auto` tries official HTML and falls back to the versioned PDF when usable HTML is unavailable. `html` and `pdf` request only that representation. PDF download needs no extraction library; `--text` needs optional `pypdf` and produces page-marked text. Install it in the agent's permitted Python environment only when needed. Scanned PDFs may yield no text, and equations/tables can lose structure. Inspect the rendered relevant pages with available PDF tools before relying on their layout or contents. Downloading, extracting text, and visual inspection are different actions.

Read the JSON `access` field: `none`, `abstract`, `full_text_html`, or `full_text_pdf`. Failed full-text retrieval leaves `metadata_only`, not a claim to have read the paper. Exit code 2 means no full-text download or a file operation failed; inspect the record for partial progress. A separate `text_extraction` status reports optional extraction failures even when the PDF download succeeded.

## Find papers that cite a seed

```sh
python3 scripts/forward_citations.py 2106.09685 --search quantized --from-year 2023 --to-year 2023 --sort oldest --limit 5 --discover-limit 10
python3 scripts/forward_citations.py 2106.09685 --citing 2305.14314 --discover-limit 0
```

The first command discovers candidates without specifying a follow-up paper. The second checks a user-supplied candidate; it is not a discovery result. Preserve the distinction in your report.

- `--provider auto` queries OpenAlex and Semantic Scholar independently. Select either with `openalex` or `semantic-scholar`. Optional environment variables are `OPENALEX_API_KEY` and `SEMANTIC_SCHOLAR_API_KEY`; never place keys in prompts or output files.
- `--sort newest|oldest|citations|relevance`, `--search TEXT`, and year bounds control scope. OpenAlex applies filters and ordering before the limit. Semantic Scholar applies them to one bounded fetched pool (20–100 records), with title-only keyword matching; it is not a globally ranked result. arXiv uses submitted-date ordering for newest/oldest, relevance otherwise; it has no citation-count ranking.
- `--discover-limit` is 0–20, default 5. arXiv search uses the seed title/acronym plus requested terms and year bounds. Search relevance only finds candidates; each discovered candidate's bibliography is checked separately. Searches are bounded and incomplete. A missing result or a failed request does not establish absence.
- arXiv metadata supplies the canonical seed identity. Conflicting index titles are marked `metadata_conflict`; that source's edges stay in `related_candidates` unless another source supports them. Matching titles alone do not merge different identifiers.

## Interpret evidence precisely

| Status | What it establishes |
|---|---|
| `indexed` | A provider reports B citing A; index metadata may be incomplete or wrong. |
| `bibliography_verified` | B's inspected HTML bibliography contains A's exact identifier, or a bounded numbered PDF reference contains A's identifier and title. The output links to the entry or actual PDF page. |
| `title_match_only` | A similar title occurs in a bibliography; identity still needs confirmation. |
| `metadata_conflict` | Canonical arXiv metadata disagrees with an index record. |
| `unavailable`, `rate_limited`, `dependency_missing` | The check could not complete. |
| `not_found_in_checked_bibliography`, `not_found_in_extracted_references` | No match in the checked representation; not proof that the paper never cites A. |

HTML bibliography checking falls back to PDF extraction only when a readable HTML bibliography is unavailable. PDF verification currently supports numbered references with the title and identifier on the same page. Unnumbered references, split entries, OCR failures, or references expressed only through a publication DOI require manual checking. Citation evidence establishes neither agreement nor reproduction. Index totals remain source-specific and are never added together.

## Network and cache behavior

Public responses are cached for one day under `~/.cache/human-researcher/citations`; use `--cache-dir DIR` or `--no-cache`. Cache files contain public response bodies, not request headers or API keys. Failures are not cached. Requests time out after 15 seconds and responses are limited to 32 MB; PDF extraction is capped at 300 pages. arXiv API requests are spaced by at least three seconds within a process; avoid parallel batches across processes. On HTTP 429, one retry is allowed only when a short `Retry-After` is supplied; otherwise the provider is stopped for that run. Record the limitation and continue with sources that remain accessible.

Provider references: [arXiv API manual](https://info.arxiv.org/help/api/user-manual.html), [OpenAlex filtering](https://help.openalex.org/api/filtering/), [OpenAlex sorting](https://help.openalex.org/api/sorting/), [Semantic Scholar API](https://api.semanticscholar.org/api-docs/graph).
