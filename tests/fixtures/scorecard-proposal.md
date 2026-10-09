# Deletion-safe retrieval for a local research library

Revision: 1. This is the entire current proposal draft. It is fictional test input; no experiments have been run. The following prose was prepared with an AI assistant. No explanation given by the researcher is included.

## Problem and value

A local search application must stop returning a document once its deletion has committed. Frequent deletions make rebuild latency a relevant constraint. Establishing when cheap incremental refresh is unsafe would be useful even if the new method offers no improvement.

## Related work and question

The supplied-source survey covers S1 through S4, assembled on 2026-09-30. S1 supplies a serial full-rebuild reference. S2v2 is the later version of S2v1 and adds deletion handling, but excludes cold queries. S3 reports stale identifiers for cold queries under burst deletions. S4 offers query-time ledger checks, although only its abstract is available.

Question: Can dependency invalidation plus a query-time deletion ledger preserve post-commit deletion safety while reducing the cost of repeated rebuilds for a single-user local library?

This combines existing mechanisms; whether the combination has been investigated elsewhere is unverified. A ledger-only method is the strongest simpler alternative. Concurrent readers are outside this initial question.

## Proposed method and reasoning

Inputs are a local collection, a fixed document identifier per item, and an ordered stream of insert, delete, and query operations. Deleting an item first commits its identifier to a deletion ledger, then invalidates known cached entries. Every query filters candidate identifiers through that ledger before returning them. Identifiers are not reused. The first version serializes operations, avoiding reader races. A stopped process must recover the ledger before serving another query.

The ledger is intended to cover entries missed by a warm-up-derived reverse map. Its memory and query-time cost could remove the refresh savings. If a ledger-only method performs equally well, the extra dependency machinery may be unnecessary.

## Resources and work plan

The project has a reserved 8-core CPU workstation with 32 GB RAM for four weeks, at 10 researcher hours per week. A local index wrapper and generated document inputs already exist. Week 1 implements ordered operations and ledger recovery; week 2 adds dependency invalidation; week 3 integrates the methods; week 4 prepares the report. No external data approval or paid API is needed. At the end of week 1, an in-memory version is the fallback if persistence exceeds the budget; that version cannot support crash-recovery claims.

## Expected contribution

The proposed outcome is a deletion-safe method with less update work for local libraries and a clearer account of when incremental updates are useful. Success has not been established.
