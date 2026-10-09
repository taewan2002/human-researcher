# Supplied literature packet

All publications and observations below are fictional evaluation inputs, not real papers or independently reproduced findings. Only the provided excerpts are available. The packet was assembled on 2026-09-30; it contains no external search log.

## fixture:S1 — Exact Deletion in Small Search Indexes (2016)

Authors: Morgan Example and Riley Sample, Sample Systems Lab.

Access: method and results excerpts, plus complete references.

Method §2: A full index rebuild after each committed deletion removes every deleted identifier from the next query's candidate set. The guarantee assumes readers wait for the rebuild to commit.

Results §4: Rebuild cost grows with collection size. A single update per hour on the supplied small collection did not exceed the authors' application budget. No burst-deletion workload was tested.

References: none in this fictional packet.

## fixture:S2v1 — Dependency-Tracked Index Refresh (2025 preprint)

Authors: Morgan Example and Taylor Sample, Sample Systems Lab.

Access: abstract only.

Abstract: Dependency tracking is proposed for incremental index refresh. Experiments on insertions report lower refresh cost than full rebuilds. Deletion behavior is left for future work.

Version note: The supplied title page of S2v2 identifies this as the earlier version of the same work.

## fixture:S2v2 — Dependency-Tracked Index Refresh (2026-04 revision)

Authors: Morgan Example and Taylor Sample, Sample Systems Lab.

Access: method, results, limitations, and complete references excerpts.

Method §3: Maintain a reverse map from each document identifier to cached query entries. On deletion, invalidate the entries listed in that map. The map is built from entries observed during warm-up.

Results §5: Refresh work decreased against rebuilds for warm-up-covered entries.

Limitations §6: Queries not represented during warm-up were excluded.

References: fixture:S1.

## fixture:S3 — Refresh Under Bursty Deletions (2026-08)

Authors: Jamie Example, Other Systems Lab.

Access: setup, results, and complete references excerpts.

Setup §2: Compare full rebuilds and dependency-tracked refresh on a serial-reader workload with burst deletions; include queries absent from warm-up.

Results §4: Dependency tracking used less refresh work in the reported setting, but some cold queries returned deleted identifiers. The full-rebuild comparison did not show these violations.

References: fixture:S1; fixture:S2v2.

## fixture:S4 — Query-Time Deletion Checks (2026-09)

Authors: Casey Sample, affiliation not provided.

Access: abstract only; full text and bibliography unavailable.

Abstract: A deletion ledger filters candidate identifiers at query time. The authors report eliminating stale identifiers in their workload with additional query-time work.
