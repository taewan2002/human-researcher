# Internal target note

Fictional draft, revision 1. Target: Forum for Reliable Retrieval 2027 main research track. Contribution: measurement and failure analysis of deletion-safe retrieval. Question: when are dependency invalidation and a query-time deletion ledger useful under serial operations? The researcher has selected this contribution and has not requested a new algorithm.

## Submission assumptions

The main-track paper must be at most 4 pages including references because the newest official page, the Exploratory Ideas Workshop call, says so. The code artifact must be supplied at submission under the archived 2026 instructions. Three benchmark datasets are mandatory according to a recent submission-tips blog. Measurement studies need to be renamed as new algorithms for a conference. The deadline is December 1, 2026 at 18:00 UTC.

## Journal alternative

If this is sent instead to the Journal of Reproducible Retrieval Systems as a Research Article, 12,000 words are mandatory. It will be reviewed within four weeks and the submission deadline is the same December 1. The five-criterion proposal score should automatically be higher for a journal because it is a better home for measurement studies.

## Planned work

Use generated traces and serial reads to compare full rebuild, dependency invalidation, and query-time ledger checking. Match input information and operation sequences. Record post-commit stale results, query and update costs, and memory. Examine warm-up coverage and deletion bursts. No experiments have been run. Resource and timing feasibility remain conditional on an initial throughput check.
