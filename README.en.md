![Human Researcher — From papers to a proposal you can defend.](docs/assets/human-researcher-hero.png)

<p align="center"><strong>Good papers begin with good questions and a rigorous research plan.</strong><br/>Seven research skills and one optional guide that keep the researcher's question and judgment at the center.</p>

<p align="center">
  <a href="README.md">한국어</a> ·
  <a href="docs/guide.en.md">User guide</a> ·
  <a href="examples/README.md">Visual gallery</a> ·
  <a href="docs/philosophy.en.md">Philosophy</a>
</p>

[![Validate skills](https://github.com/taewan2002/human-researcher/actions/workflows/validate.yml/badge.svg)](https://github.com/taewan2002/human-researcher/actions/workflows/validate.yml)
[![Release](https://img.shields.io/github/v/release/taewan2002/human-researcher)](https://github.com/taewan2002/human-researcher/releases/tag/v0.1.0)
[![License: MIT](https://img.shields.io/badge/license-MIT-55745a.svg)](LICENSE)

Human Researcher is a collection of skills that helps researchers turn the questions they care about into **testable proposals**. Work with AI to read papers top-down, follow citing work, and develop hypotheses and evaluation plans. Use the skills you need in your existing Codex or Claude Code environment.

**Understand papers → map the literature → frame your question → design the test → review and revise.**

## Why Human Researcher?

This project starts with **deciding what to study, why it matters, and how to investigate it**. A proposal should explain why the problem deserves attention, what prior work leaves unresolved, and what evidence would justify the claim.

**Human** means that ownership and responsibility stay with the researcher. AI can propose questions and hypotheses, find evidence and counterarguments, and help design tests. Researchers understand the reasons for their choices, revise their judgments as evidence changes, and determine the direction of their work.

**We aim for a research plan you can explain and defend yourself.** Build a strong proposal by drafting, exposing gaps, and refining it through feedback.

## Start here

**1. Ask your agent to install the skills.**

```text
Install all eight Human Researcher packages (seven research skills and one guide) by following this guide:
https://raw.githubusercontent.com/taewan2002/human-researcher/v0.1.0/docs/installation.md
```

**2. Attach your papers or notes and describe the result you want.**

```text
Use write-proposal to develop these papers and my idea into a research proposal.
My question is [what I want to learn]. My resources are [hardware, time, data].
Keep my chosen direction. Check the prior work and evaluation plan,
fix the gaps that the available evidence can resolve, and label remaining assumptions.
```

An idea is enough to begin. Start with `read-paper` for one paper or `review-proposal` for an existing draft. **You do not need to invoke all seven skills in order.**

[Follow the first-use guide →](docs/guide.en.md) · [Installation and updates](docs/installation.md)

If you are unsure where to begin, ask [using-human-researcher](skills/using-human-researcher/SKILL.md) to identify the next useful task from your notes and current bottleneck. Clear requests can go directly to a research skill.

## Start at your current question

![Understand papers and evidence, shape questions and tests, then write and review proposals. Human judgment connects every group; this is not a required sequence.](docs/assets/research-workflow.svg)

| What you want to do | Skill | What you receive |
|---|---|---|
| Understand a paper | [read-paper](skills/read-paper/SKILL.md) | Big picture, central claims, evidence locations, and details worth reading |
| Find what to read next | [trace-research](skills/trace-research/SKILL.md) | Verified citing papers, author/lab trajectories, and a literature survey |
| Locate your idea in the field | [map-field](skills/map-field/SKILL.md) | An evidence-linked hierarchical taxonomy and comparison |
| Turn a thought into a question | [develop-idea](skills/develop-idea/SKILL.md) | Question, hypothesis, closest work, and strongest counterargument |
| Decide how to investigate it | [design-research](skills/design-research/SKILL.md) | Method, controls, measurements, resources, milestones, and decisions |
| Develop a complete research plan | [write-proposal](skills/write-proposal/SKILL.md) | A proposal shaped for its audience, with a visual explanation |
| Inspect and improve a draft | [review-proposal](skills/review-proposal/SKILL.md) | Core gaps, evidence-linked scores, venue fit, and requested revisions |

## See the research argument

**Starting a study from an idea · RetoVLA proposal.** Propose register-based scene summaries for a lightweight VLA, connecting 13 prior works, a VLA taxonomy, hypotheses, controlled comparisons, and conditional estimates for one RTX 5090 GPU.

[![RetoVLA's research question and scene-summary-to-action information path in the HTML reader](docs/assets/retovla-reader-preview.png)](examples/retovla/proposal-reader.html)

[![A hierarchical taxonomy of eight representative VLA policies by action representation and generation, with the proposed RetoVLA positioned beside SmolVLA](examples/retovla/taxonomy.svg)](examples/retovla/taxonomy.md)

[HTML reader (Korean)](examples/retovla/proposal-reader.html) · [Example and request prompt (Korean)](examples/retovla/README.md) · [Editable Markdown (Korean)](examples/retovla/proposal.md) · [Sources and scope (Korean)](examples/retovla/sources.md)

Written as a **proposal before experiments**: improvements are hypotheses, and comparison criteria, budgets, and durations are proposed planning assumptions. Completed RetoVLA findings are not used to establish the proposed method’s effect. Download the [project ZIP](https://github.com/taewan2002/human-researcher/archive/refs/tags/v0.1.0.zip), extract it, and open `examples/retovla/proposal-reader.html` in a browser. The preview and taxonomy above are visible directly on GitHub.

**01 · Map the field.** Organize seven public PEFT papers by their main adaptation mechanisms, with explicit classification criteria and a separate axis for frozen-base quantization.

[![Hierarchical PEFT map covering BitFit, Prefix-Tuning, Adapters, IA3, LoRA, DoRA, and a separate QLoRA precision axis](docs/assets/peft-taxonomy-preview.png)](examples/peft-taxonomy/README.md)

[Classification evidence and sources](examples/peft-taxonomy/evidence.md) · [Editable SVG](examples/peft-taxonomy/taxonomy.svg)

**02 · Explain the plan on one page.** An A3 proposal poster connects a LoRA/QLoRA research question to evidence, a controlled comparison, measurements, and conditional decisions.

[![Planned comparison of 16-bit and 4-bit frozen bases with matched adapters, evidence, controls, measurements, and unresolved choices](docs/assets/adaptation-proposal-preview.png)](examples/quantized-adaptation/poster.pdf)

[PDF](examples/quantized-adaptation/poster.pdf) · [Editable HTML](examples/quantized-adaptation/poster.html) · [Full proposal](examples/quantized-adaptation/proposal.md)

| 03 · From experiments to decisions | 04 · From a draft to a useful meeting |
|---|---|
| [![Evaluation map linking measurements to quality, uncertainty, and OOM decisions](docs/assets/evaluation-map-preview.png)](examples/quantized-adaptation/evaluation.svg) | [![Fictional library-signage study with evidence limits and focused advisor questions](docs/assets/meeting-brief-preview.png)](examples/research-meeting/README.md) |
| Show what evidence would change the plan. | Connect unresolved choices to useful feedback. |

These curated examples use public papers or synthetic inputs. They distinguish plans from results and are not measured skill-performance outcomes. The figures and gallery are in Korean; click an image to inspect its full artifact and supporting material.

[Explore the full visual gallery →](examples/README.md) · [Synthetic taxonomy with hybrid and unknown cases](examples/visual-taxonomy/README.md)

**Read a full proposal in your browser.** Follow the need → proposed change → test and decision, then open cited paper titles to inspect source links and evidence. Request responsive HTML, editable Markdown, or a one-page poster as needed.

[![A browser-readable proposal with recognizable citations and source cards](docs/assets/proposal-reader-preview.png)](examples/quantized-adaptation/proposal-reader.html)

[HTML reader example](examples/quantized-adaptation/proposal-reader.html) · [Request it and open the file](docs/guide.en.md#read-the-full-proposal-in-a-browser)

## Three connections behind a strong proposal

**From literature to a question.** A literature survey combines foundations, recent work, closest alternatives, and contrary findings. Distinguish verified forward citations from topical similarity, and retain a route back to the source.

**From question to evidence.** Specify what comparison would distinguish the hypothesis and what result would change the plan. Keep expected effects separate from findings already established.

**From research to its audience.** Check the official criteria for the exact conference edition and track or journal article type. Connect them to the contribution, evidence, and timeline. Assess scientific readiness separately from venue fit. An unknown target does not block developing the question.

[Publication-target guidance](skills/write-proposal/references/publication-target.md) · [Proposal completion criteria](skills/write-proposal/references/proposal-contract.md)

## Estimate the research and its argument

Connect the supported need, tractability, hardest assumption, and smallest informative check. Separate person time, device time, and external waiting, with conditions for continuing, narrowing, or stopping.

Build the reader-facing story from **need → limits of current approaches → question → proposed insight → required evidence → conditional contribution**. Define outcome interpretations before seeing results, and check that the measure captures the claimed concept.

[Argument and feasibility table](skills/write-proposal/references/research-argument.md) · [Sources and adaptations](docs/research-foundations.md)

## Put research advice into practice

Public excerpts from 『대학원생 때 알았더라면 좋았을 것들』 [volume 1](https://www.yes24.com/product/goods/72231788) and [volume 2](https://www.yes24.com/product/goods/109305004) helped us refine guidance on researcher ownership, investigating new questions, and seeking feedback.

- **Keep ownership of the question.** Distinguish agent recommendations from researcher decisions.
- **Plan what to learn.** Explain which uncertainty each stage addresses and how the evidence could change the next decision.
- **Prepare a draft worth discussing.** For a requested meeting brief, make current evidence, unresolved choices, and focused feedback questions easy to inspect.

A defensible proposal explains its evidence, limits, and next test. Exposing an unknown can make a draft ready for useful discussion without making it scientifically complete.

[Source excerpts, page references, and our adaptations (Korean)](docs/research-foundations.md) · [Meeting preparation example](docs/guide.en.md#prepare-for-an-advisor-or-collaborator-meeting)

## A score that shows what to improve

On request, assess the proposal using five criteria. Every score comes with **evidence locations, reasoning, and the next useful action**.

| Criterion | What it asks |
|---|---|
| **Timely** | Why investigate this question now? |
| **Practical** | What practical or scientific value could it create? |
| **Analytical** | Can the question, hypothesis, mechanism, and counterarguments be explained? |
| **Implementable** | Is there a concrete route within the available resources? |
| **Measurable** | Does the measure capture the claimed concept and distinguish meaningful outcomes from insufficient precision? |

Use **0–4 per criterion**, totaling **20** when all five can be assessed; conversion to 100 is optional. Missing evidence means **unassessed**, and the full total is withheld. Core defects remain visible regardless of the sum. Document quality is distinct from the researcher's demonstrated understanding.

[How to request and read an assessment](docs/guide.en.md#reading-the-scorecard) · [Detailed rubric](skills/review-proposal/references/proposal-scorecard.md)

## Common questions

<details>
<summary><strong>Can I start without papers or a target venue?</strong></summary>

Yes. Describe your interests and constraints. Use `trace-research` to find sources or `develop-idea` to frame a question. Unknown decisions can remain unknown.

</details>

<details>
<summary><strong>Must I install and run every skill?</strong></summary>

No. Each package is independently usable, and `write-proposal` includes self-review and revision. A short summary or focused edit stays scoped to that request.

</details>

<details>
<summary><strong>Do I need a separate server or API key?</strong></summary>

Human Researcher needs no account, server, database, or API key of its own. It uses your agent's model and available search and file tools. Your agent and external services have their own costs and data-handling settings.

</details>

<details>
<summary><strong>Can I use Korean or work only from supplied documents?</strong></summary>

Yes. Specify the output language and say “use only the attached material, without external search” when appropriate. The agent should state the resulting coverage and access limits rather than claim a current or exhaustive literature check.

</details>

## Go further

[User guide](docs/guide.en.md) · [한국어 가이드](docs/guide.md) · [Installation](docs/installation.md) · [Workflows](docs/workflows.md) · [Philosophy](docs/philosophy.en.md) · [Contributing](CONTRIBUTING.md) · [Release notes](CHANGELOG.md)

Packaging and installation checks are separate from model behavior. The repository defines **58 synthetic behavior cases**; that count is not a pass rate or proof of research usefulness. See [evaluation and known limits](docs/evaluation.md).

Code and instructions are under the [MIT License](LICENSE). Referenced papers, datasets, and models retain their own terms. [Image production notes](docs/assets/README.md).
