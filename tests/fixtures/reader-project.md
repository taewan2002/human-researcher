# Project notes

Question: When publication dates are missing, does using them still improve document ranking compared with text alone?
Chosen direction: retain a text encoder plus publication-date feature.
Planned comparison: same encoder and head capacity, input documents, labels, splits, and tuning budget; compare real dates, a constant date input, and shuffled dates at matched missing-date rates.
Planned measurements: nDCG@10, missing-date rate, and retrieval latency. Acceptable latency and meaningful quality difference have not been chosen. Dates must be available before ranking.
No experiments have been run. Dataset permission, equipment, throughput, and repeat counts have not been confirmed. Available background is reader-papers.md.
Audience: a mixed research group; language: Korean.
