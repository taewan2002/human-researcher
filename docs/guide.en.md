# Using Human Researcher

[README](../README.en.md) · [한국어 가이드](guide.md) · [Installation and updates](installation.md)

**Provide what you have and say what you want to receive.** You do not need to manage internal stages or run all seven skills in sequence.

## Your first session

### 1. Install

Paste this into Codex or Claude Code:

```text
Install all eight Human Researcher packages (seven research skills and one guide) by following:
https://raw.githubusercontent.com/taewan2002/human-researcher/v0.1.0/docs/installation.md
```

The default is personal scope for the agent you are using. Add “for this project only” or name a subset when needed. If the verified installation does not appear yet, start a new session or reload your agent. Follow the [installation guide](installation.md) for locations, conflicts, and updates.

### 2. Provide context

Fill in what you know; unknowns can stay unknown. Attach paper PDFs, links, notes, or an existing draft. Supply text or excerpts if the agent cannot read a file.

```text
Research interest / question:
Direction I have already chosen:
Sources: [links, attached PDFs, notes, or file paths]
Resources: [hardware, data, people, available time]
Target conference/year/track or journal/article type: [optional]
Desired result: [explanation, survey, proposal, poster, etc.]
Scope: [review only / revise, whether external search is allowed]
Output language:
```

For example, “one researcher, ten hours a week for four weeks; GPU access is unconfirmed” is more useful than a vague request for a feasible plan. Separate confirmed resources from assumptions.

### 3. Pick an entry point

| What you have | Start with | First useful outcome |
|---|---|---|
| One paper | `read-paper` | Understand its question, claims, and evidence |
| A research interest | `trace-research` or `develop-idea` | Find seed papers or frame a question |
| Several papers and notes | `map-field` | Understand approach families and your idea's position |
| A chosen idea | `design-research` or `write-proposal` | Connect it to a feasible method and evaluation |
| A proposal draft | `review-proposal` | Identify core gaps and useful next improvements |

## Copyable requests

### Read a paper top-down

```text
Use read-paper to explain this paper top-down:
problem, central idea, key evidence, then limitations.
Identify the sections, figures, and tables worth reading for my question.
Separate the paper's findings from your interpretation.
```

Expect claims linked to inspectable evidence locations. Abstract-only access should not turn into claims about unseen methods or appendices.

### Follow citing papers and synthesize the literature

```text
Use trace-research to start with papers that actually cite this seed.
Trace relevant author and lab research threads.
Synthesize foundations, recent work, closest alternatives, and contrary evidence.
Explain what should change in my question, baselines, or evaluation.
Record search dates, coverage, and inaccessible sources.
```

“B cites A” is different from “B discusses a similar topic.” A survey should explain agreements, differences, and decisions rather than stop at separate summaries.

### Build a branching taxonomy

```text
Use map-field to build a hierarchical taxonomy:
field → approach families → subfamilies → representative papers.
State each split criterion and its evidence. Preserve overlapping membership
and unknown properties, and locate my idea.
Save an editable SVG and the classification evidence.
```

Use the [hierarchical example](../examples/visual-taxonomy/README.md) to specify the intended form. A new branch or empty category does not establish novelty.

### Develop an idea

```text
Use develop-idea to frame a concrete research question and hypothesis.
Compare the actual difference from the closest work. State the strongest
counterargument and the first test that could distinguish it.
Explain what we could learn even if the favored method fails.
Keep my chosen direction: [direction].
```

If no direction is chosen, replace the last line with a request to compare a few alternatives and recommend one under the stated constraints.

### Design the study and timeline

```text
Use design-research to specify the method and evaluation for this question.
Connect inputs, outputs, implementation, baselines, controls, measurements,
fair conditions, and decisions under positive, negative, or ambiguous results.
Within [resources and time], identify the smallest useful test and expansion gates.
Plan only; do not run experiments.
```

A timeline without measured throughput is conditional. Separate person time, device occupancy, and external waiting, and identify what to re-estimate first.

### Write for a publication target

```text
Use write-proposal to turn this material into a research proposal.
My target is [conference/year/track or journal/article type].
Check current official scope, review criteria, and relevant deadlines.
Connect them to the contribution, literature, evaluation, resources, and timeline.
Separate official requirements from your strategic recommendations.
Draft, review, and fix core gaps that available evidence can resolve.
```

Omit the target line if it is undecided. Ask for the internal proposal length you need; the eventual paper's page allowance does not determine the proposal's format.

### Review or revise a draft

For review only:

```text
Use review-proposal to assess this draft without changing the original.
Score Timely, Practical, Analytical, Implementable, and Measurable.
Show evidence locations, core defects, and the highest-priority improvements.
Assess [target venue/year/track] fit separately from the score.
```

For actual revision, follow with:

```text
Apply the core fixes supported by the available material.
Preserve my direction and meaning; update the prose and figures together.
Explain material changes, identify unresolved inputs, and recheck the result.
```

### Read the full proposal in a browser

```text
Use write-proposal to complete a proposal from these materials.
Deliver a standalone browser-readable HTML file and editable Markdown.
Make the need, the change from the existing approach, and the informative test
clear at a glance. Identify citations by paper title and original link,
explain why each is used, and show the inspected location and access scope.
Keep hypotheses and proposed work distinct from observed results.
```

Download the [full proposal reader example](../examples/quantized-adaptation/proposal-reader.html) and open it locally; no server is needed. GitHub displays HTML source rather than this reading view. The contents links and cited titles lead to sections and source cards with original links, inspected passages, relevance, and limits. Opening the original papers requires network access.

The document adapts to screen width, lets readers expand supporting detail, and prints that detail even when collapsed. Unlike a one-page poster, a full reader may print across several pages. Request HTML only if that is all you need; a Markdown-only task should not produce extra HTML.

### Explain the proposal on one page

```text
Use write-proposal to create a one-page proposal poster in [language].
Connect the problem, source evidence, question, method, evaluation, and decisions.
Visually separate proposed work from established findings.
Save editable HTML/SVG. If the tools support PDF export, also check the actual
page count, readable text, connectors, and source links.
```

[Poster example](../examples/quantized-adaptation/poster.pdf) · [Editable HTML](../examples/quantized-adaptation/poster.html). For a smaller task, explicitly request a table or text-only explanation.

### Prepare for an advisor or collaborator meeting

```text
Use write-proposal to turn these notes into a one-page meeting draft.
Include my question and chosen direction, current evidence, the most important
unresolved choice, and focused questions for feedback. Explain which decisions
the answers would change. Label missing inputs and deliver a draft we can discuss.
```

For an existing draft, ask `review-proposal` to identify the key issues and discussion questions without rewriting it. Readiness to discuss a gap does not mean the proposal's core defects are resolved.

After the meeting, provide the actual feedback and your decisions. Ask for the requested revisions with reasons, keeping advice distinct from verified evidence. Preparing a brief does not itself authorize sending it or scheduling a meeting.

## Walk through a real-source example

The [LoRA and QLoRA walkthrough](../examples/quantized-adaptation/README.md) narrows a broad memory-efficiency idea into a question about the effect of sequence length on the memory benefit of quantizing frozen weights, with model and data conditions held fixed.

1. Inspect the verified relationship and access scope in the [source notes](../examples/quantized-adaptation/sources.md).
2. Review the controls, measurements, and resource gate in the [proposal](../examples/quantized-adaptation/proposal.md).
3. Compare the corrected claims and design choices in the [review](../examples/quantized-adaptation/review.md).
4. Check that the [poster](../examples/quantized-adaptation/poster.pdf) preserves the same question and assumptions.

To try it yourself, start from the request, original papers, and your constraints; inspect the finished example afterward. It is a curated proposed study, not an experiment report or novelty demonstration. The example artifacts are in Korean; requests can use your preferred language.

## Reading the scorecard

| Score | Meaning |
|---|---|
| 0 | An essential connection is absent in the supplied scope, or a demonstrated contradiction defeats it |
| 1 | The connection is asserted, with important reasoning or design choices largely unspecified |
| 2 | A concrete route exists, but a consequential gap remains |
| 3 | Evidence and design connect, with credible checks for remaining assumptions |
| 4 | The plan also addresses the strongest relevant counterargument or constraint and states its boundaries |
| Unassessed | Available material or access is insufficient to judge |

When all five criteria can be assessed, sum out of 20; multiply by five for an optional score out of 100. Withhold a full total if any criterion is unassessed. **A missing evaluation plan is different from a planned experiment that has not been run.** The score is an improvement aid, not an acceptance probability or a prediction of results.

A clear document does not demonstrate its author's understanding or implementation ability. To inspect your own understanding, explain why the closest alternative is insufficient and which result would overturn your hypothesis, then ask the agent to critique your explanation.

## Improve an unhelpful answer

| Problem | Useful follow-up |
|---|---|
| The summary is long and unfocused | “Keep only the three claims that affect my question, with evidence locations.” |
| Many papers, no direction | “Focus on the closest alternatives and contrary findings; narrow the decision I need to make.” |
| A matrix appeared instead of a taxonomy | “Use a branching hierarchy with split criteria; follow this example's structure.” |
| The method has no discriminating test | “Connect the hypothesis and strongest alternative to controls, measurements, and decisions.” |
| A claim has no support | “Show the inspected source location; mark unsupported content as unverified.” |
| The figure contradicts the revised text | “Update the prose, taxonomy, and poster so their terms and claims agree.” |

To keep records, request source-preserving notes, proposal, review, and visual files in your existing project structure. Conversational work does not require extra files.

Capabilities depend on your agent's model and available search, file, and rendering tools. If source access or export is unavailable, ask for the verified portion and the remaining work separately. See [Contributing](../CONTRIBUTING.md) for reporting a reproducible failure.

## Retrieve arXiv papers

```text
Use trace-research to retrieve https://arxiv.org/abs/2106.09685v1.
Confirm the version and title, and save the available HTML or PDF.
Find related 2023 quantization papers that cite it.
Distinguish search candidates from citations checked in their bibliographies.
```

The helper records canonical arXiv metadata and tries PDF when usable HTML is unavailable. Abstract access, full-text download, text extraction, and visual inspection remain distinct. Specify a version such as `v1` when it matters. Conflicting local files are preserved. See [commands, options, and limits](../skills/trace-research/references/retrieval.md).

## Choosing a next task

```text
Use using-human-researcher to recommend my next task.
I have already [read papers / chosen a question]. My current bottleneck is [decision].
Explain the next step, why it matters, and what would count as completing it.
Guidance only for now.
```

The guide is optional. Clear summaries, drafts, or critiques can go directly to the corresponding research skill; all seven tasks need not be run.

## Estimating the research and building its story

```text
Use write-proposal to develop these notes into a proposal.
Connect the reader's evidenced need, current limitations, proposed insight, and required evidence.
Identify the hardest assumption and the smallest informative check under [resources].
Specify conditions for continuing, narrowing, or stopping, and distinguish person time from device time and waiting.
Before results, define meaningful effects, needed precision, and outcome-dependent interpretations.
Keep hoped-for findings separate from observations.
```
