# From two papers to a research plan

This is a curated walkthrough built from public sources and an original proposed study. It is **not** an experiment report, a claim of novelty, or a recorded independent evaluation of the skills.

## Starting request

```text
I want to study memory-efficient adaptation of language models.
Start with LoRA and follow it to QLoRA. Help me ask a narrower question,
design a fair comparison, and write a short proposal I can defend.
Keep the study modest and identify missing execution details.
```

## Read and trace

LoRA provides the seed. QLoRA is a verified citing paper, not merely a similarly named method. The [source notes](sources.md) record the inspected versions, the relationship, and the limits of the reading.

The useful distinction is between adapting with trainable low-rank components and also quantizing the frozen base. A comparison must keep other choices aligned.

## Develop the question

Initial idea:

> Make fine-tuning more memory efficient.

Refined question:

> For one fixed model and data pipeline, how does sequence length affect the peak-memory benefit of quantizing frozen base weights, under a predefined quality constraint?

This is a study question, not an established gap in current literature. Two papers are insufficient for a novelty claim.

## Design, write, and review

The [proposal](proposal.md) specifies matched precision comparisons at several sequence lengths, measurements, outcome interpretation, and a resource gate.

The [review](review.md) shows which weak claims and design ambiguities were corrected and which inputs still need a researcher decision. Future results remain unknown; missing model or dataset choices remain visible.

## Read the whole argument in a browser

The Korean [standalone HTML reader](proposal-reader.html) presents the same planned study as the [editable Markdown proposal](proposal.md): the need, matched precision comparison, conditional decisions, and unresolved resources. It includes source cards with full titles, original links, inspected locations, and why each source is used. Download the HTML and open it locally; GitHub itself displays its source.

The reader works at phone and desktop widths, has native expandable detail, and prints the full text with source URLs. It is a manually edited companion, not automatically synchronized with Markdown; changes must be reconciled across formats. It uses the package's [reader template](../../skills/write-proposal/assets/proposal-reader.html). No server, external font, or JavaScript dependency is required.

## Explain it on one page

The Korean [proposal poster (PDF)](poster.pdf) compresses the same study into an A3 landscape page: a two-paper comparison, the planned precision contrast, measurements, possible decisions, and unresolved resources. The [editable HTML with inline SVG](poster.html) and [standalone SVG](poster.svg) work locally without a server or external fonts; open it in a browser and print to A3 landscape with browser headers and footers disabled.

The companion [evaluation map](evaluation.svg) expands the outcome-to-decision logic in a separate figure. The [PEFT taxonomy](../peft-taxonomy/README.md) places the motivating methods alongside other approaches, and the [gallery](../README.md) shows other output formats.

The diagram describes a proposed experiment. It contains no invented performance results. The two-paper comparison is deliberately not presented as a taxonomy of the whole field. For a broader classification example with hybrid and unknown cases, see the [synthetic taxonomy](../visual-taxonomy/README.md).

This is a curated visual example, not an unedited model benchmark output. The poster remains a concise companion to the detailed proposal; its unresolved choices must not disappear when it is shared.

To try the workflow, give your agent the starting request, source links, and your own constraints. Read the proposal and review afterward as illustrations, not a hidden “correct answer.”
