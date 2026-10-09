# Research notes

Selected direction: retain candidate B, which combines text with external document metadata.

Question: Under what input-length and metadata-availability conditions does external metadata improve ranking quality?

The literature packet is in visual-papers.md. Available documents: the five supplied extracts.

Proposed comparison: same text encoder and scoring head, trained with metadata versus without metadata. Use the same query/document splits, tuning budget, and relevance labels. A shuffled-metadata condition can probe whether document-metadata correspondence matters. Metadata must be available at the time the ranking is produced.

Measurements planned: nDCG@10 by input-length group, metadata retrieval latency, and missing-metadata rate. The length boundaries and acceptable latency still need to be fixed. No experiments have been run and there are no measured gains.

Available equipment, throughput, and data access dates have not been confirmed. The next work is to check metadata availability, define a matched pilot, and then choose a confirmation scope.

Audience: a research-group meeting. Desired language: Korean. The artifact should help the group decide whether the proposed comparison can answer the question.
