# Literature packet

These five entries are fictional sources for a local evaluation. Identifiers refer to this packet only.

## R1 — Compact Text Ranker, version 1

The method scores documents from text using a supervised ranking loss. No document metadata enters at inference. The study evaluates short documents under a fixed compute budget.

## R2 — Field-Aware Ranker, version 2

The method combines document text, publication date, and source type in a learned scoring layer. A supervised ranking loss trains the layer. Its reference list contains R1.

## R3 — Metadata Rules, version 1

The method ranks documents using publication date and source type with fixed rules. It does not use document text or learned parameters. The evaluation includes both short and long documents.

## R4 — Mixed Signals, version 1

The method combines a supervised text-ranking score with a fixed metadata-based score. Its two branches are combined at inference. The available extract reports evaluation on short and long documents.

## R5 — Ranker in Practice, version 3

Only the abstract is available: the paper reports a ranking system used in a production setting.
