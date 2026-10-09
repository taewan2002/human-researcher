# Using Human Researcher

`using-human-researcher` is an optional guide alongside seven independent research task skills. Use it when the next task is unclear or several tasks need coordinating. It identifies the current bottleneck from supplied context, recommends the shortest useful path, and checks which skills are actually available. It does not install dependencies, require a fixed sequence, or intercept an already clear summary, draft, or review request.

Example: “I have read the papers and chosen a question, but do not know how to distinguish my explanation from the baseline. What should I do next?” The useful next step is measurement and comparison design, not repeating the entire literature workflow.

Choose the smallest task that resolves the current bottleneck. A whole-proposal request includes review and revision; a narrow request keeps its scope.

## Choose an entry point

| What you need | Entry point |
|---|---|
| Understand one paper | `read-paper`: big picture, central evidence, then relevant detail. |
| Find starting papers or later work | `trace-research`: discovery and verified citation, author, or lab threads. |
| Synthesize a literature survey | `trace-research`: scoped search, closest and contrary work, synthesis that informs the proposal. |
| Compare papers or organize a field | `map-field`: comparable conditions, provisional categories, open questions. |
| Clarify or challenge an idea | `develop-idea`: question, hypothesis, closest work, novelty limits, alternatives. |
| Specify a method, study, or timeline | `design-research`: implementation decisions, discriminating evaluation, dependencies. |
| Turn material into a full proposal | `write-proposal`: fill relevant gaps, draft, self-review, and revise. |
| Plan for a conference or journal | `write-proposal`: verify the target and connect audience, contribution, evidence, and resources. |
| Create a visual taxonomy | `map-field`: families, subfamilies, representative methods, justified overlaps, proposed position. |
| Explain a proposal on one page | `write-proposal`: visual argument, editable poster, rendered readability checks. |
| Inspect or improve an existing proposal | `review-proposal`: concrete findings, requested corrections, affected-section review. |
| Score an existing proposal | `review-proposal`: five evidence-linked criteria, missingness, core defects, and next improvements. |
| Assess target-venue fit | `review-proposal`: separate scientific readiness, target fit, and submission-format requirements. |

## Keep the boundaries clear

- Reading understands a source; tracing discovers sources and verifies their relationships.
- Mapping organizes a literature set; developing turns it into the researcher's own bounded question and hypothesis.
- Developing establishes what is worth asking; designing establishes how to answer it under constraints.
- Writing creates a proposal from evidence and plans; reviewing focuses on findings and changes to an existing proposal.

A review-only request does not authorize changing the document. A request to improve it should produce actual revised text, not just an offer to do so.

## Example paths

From a paper:

`read-paper → trace-research → map-field → develop-idea → design-research → write-proposal → review-proposal`

From an existing idea:

`develop-idea → design-research → write-proposal`

From a draft:

`review-proposal`

These are examples, not required pipelines. Skip work already supported by evidence. Check a missing consequential source without restarting the whole survey.

`write-proposal` includes self-review and revision, so a separate review skill is optional. Each skill can perform its scoped work without assuming other packages are installed. Do not claim independent review merely because a review step or a second skill was used.

## Literature survey and proposal scoring

Use `trace-research` to connect the evidence rather than collect isolated summaries. Carry the survey's search dates and scope, inspected source locations, version distinctions, closest alternatives, and contrary findings into the proposal. Each important gap should affect a question or design choice. Supplied-source synthesis remains useful when search is unavailable, but it does not establish field-wide novelty or current coverage.

For requested scoring, `review-proposal` provides a self-contained [five-criterion scorecard](../skills/review-proposal/references/proposal-scorecard.md): Timely, Practical, Analytical, Implementable, and Measurable. Use 0–4 per criterion, evidence and next actions alongside each judgment, and a total only when all five are assessable. Keep core defects separate from the sum and researcher understanding separate from document quality. Ordinary reviews and small edits do not require scoring.

The literature survey is the evidence base for these judgments, not an extra score rewarding the number of papers. Reassess after actual evidence or design changes using the same scope and rubric; do not claim a better score from cosmetic rewriting alone.

## Publication targets

Start from the researcher's intended contribution and exact target: venue, conference year and track, or journal article type and special issue. `write-proposal` includes a self-contained [planning guide](../skills/write-proposal/references/publication-target.md); `review-proposal` includes its own [fit review guide](../skills/review-proposal/references/venue-fit.md). Neither package requires the other.

Check official, applicable scope and criteria. Distinguish them from examples, third-party advice, strategic recommendations, and researcher constraints. Carry sources and dates forward. Do not substitute an older edition, a related workshop, or a supposed reviewer preference for verified rules. Without current information, continue the scientific plan and leave the target-specific judgment provisional.

Use the target to shape the scientific argument and necessary evidence, not just formatting. A measurement study need not be relabeled as a new algorithm. A negative result can be informative. If the target genuinely needs evidence that the resources cannot support, explain the mismatch and the cost of changing scope or target; preserve the researcher's choice unless the decision is delegated.

Scientific readiness, venue fit, and submission-format readiness are separate judgments. A venue switch does not automatically improve the five-criterion score. Format rules for the eventual paper do not silently override a short internal proposal request. An absent target does not trigger a compulsory selection stage.

## Carry forward only useful context

- The current question and the researcher's chosen direction.
- Intended audience, contribution type, publication target when chosen, and applicable criteria with source dates.
- Sources, versions, actual access scope, and important evidence locations.
- Findings, interpretations, hypotheses, and unknowns as separate states.
- Constraints, completed work, and prospective work.
- Why a decision changed and what still blocks the next decision.

Record keeping is part of each task. Preserve the existing structure, original sources, and raw observations. Do not turn a conversational request into mandatory new files.

## Completion

Check the chain from problem to evidence, question, method, evaluation, and feasibility. Apply concrete corrections, then recheck what they affect.

When outside input is needed, deliver the current revision, unresolved issue, and required input. Unknown future results do not justify endless revisions. Use the [proposal completion criteria](../skills/write-proposal/references/proposal-contract.md).

## Visual explanations and posters

For a taxonomy request, usually draw a hierarchy from field to approach families, subfamilies, and representative methods or papers. Follow supplied tree or network references. Use multiple parents for justified overlapping membership, with clearly defined edges. A requested matrix or short comparison can remain a table; do not silently substitute one for a taxonomy tree. Citation edges require verified citations and must look distinct from classification edges.

A poster request should produce an actual viewable artifact, not only an outline or code block. `write-proposal` includes a portable [visual guide](../skills/write-proposal/references/visual-proposal.md) and optional HTML/SVG template. Respect the requested language and format; keep an editable source. Export PDF when the environment supports it, then inspect its actual page count and rendered layout.

The poster and longer proposal must agree about claims, controls, and unresolved inputs. Label proposed studies as plans, connect classifications to sources, and preserve uncertainty. Show dependencies instead of inventing calendar dates when resources are unknown. Review both scientific meaning and legibility.

Text-only requests stay text-only. A visual request does not authorize external uploads, extra paid services, or installing design plugins. If rendering is unavailable, deliver the usable source and state what was not inspected.

## Limited environments

Read supplied excerpts when the PDF is inaccessible. Without search, do not claim a current or exhaustive novelty review. Without data, do not generate observed results.

Use available evidence, label limitations, and proceed with work that does not depend on missing inputs. Skill instructions do not add permission to install other skills, spawn agents, spend compute, transmit private data, or schedule recurring tasks.
