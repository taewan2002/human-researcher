# Contributing

Human Researcher helps researchers develop proposals they can explain and defend. Useful contributions improve an observable decision or output in one of the seven research skills or the optional usage guide.

English and Korean issues are welcome.

## Start with a concrete failure

Describe the request, the supplied material, what happened, and what should have happened. Use public or clearly synthetic inputs; do not include private research, credentials, or unpublished results.

Examples of useful changes:

- A citation edge was reversed or inferred from similarity.
- A narrow paper comparison unnecessarily triggered a full survey.
- A proposed experiment was described as completed.
- A proposal critique identified a weakness but missed the requested revision.
- A taxonomy forced unknown properties into a category, or a poster made planned results look measured.

Prefer a small correction supported by an example to a growing list of speculative rules.

## Keep seven research tasks and a thin usage guide

Version 0.1 keeps seven research tasks plus `using-human-researcher`, an optional guide for selecting a next task. The guide must not intercept clear requests, require every package, or impose a full pipeline. Add a procedure or conditional reference within the relevant skill before proposing another entry point.

A new skill needs a distinct user request and deliverable that the current seven cannot reasonably handle. Splitting an internal research step is not sufficient. Experiment execution, manuscript submission, and reviewer correspondence remain outside the current scope.

## Package skills independently

Each `skills/<name>/` folder must work without files from the repository root or another skill.

- Put the trigger in frontmatter and meaningful workflow, output, and completion conditions in the body.
- Load supporting references only when relevant.
- Preserve the user's chosen direction, existing authorization, and requested scope.
- Update English instructions and UI metadata consistently. Follow the user's requested output language.
- Keep the primary [Korean README](README.md) and [English README](README.en.md) aligned when changing public behavior or setup.

## Validate

Python 3.9+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate_repo.py
.venv/bin/python -m unittest discover -s tests -p 'test_*.py'
```

For distribution changes, also run the installation smoke check with Node.js 22.20+, Git, and network access:

```sh
python3 scripts/smoke_install.py
```

Update [behavior cases](tests/cases.json) for changed decisions. Follow the [evaluation guide](docs/evaluation.md) and report exactly which checks ran. Packaging tests and defined cases are not evidence of successful model behavior.

For visual changes, include editable source and inspect the actual render. Check labels, classification evidence, uncertainty, source links, clipping, and export page count. Keep synthetic fixtures neutral: expected classifications and review findings belong in evaluation criteria, not in the input packet. A polished example and an independent behavior run are different evidence.

## Open a pull request

Explain the concrete failure and resulting behavior first. Include the reproduction input, relevant changes, checks run, and remaining limitations.

Preserve useful counterevidence and distinguish completed work from proposed work. Do not add mandatory approvals, automatic subagents, or full-workflow execution to unrelated requests.

Contributions are covered by the repository's [MIT license](LICENSE). Only submit material you have the right to share.

## Run behavior and routing evaluations

With an authenticated Codex CLI that supports the flags in `scripts/evaluate.py`:

```sh
python3 scripts/evaluate.py --run-dir eval-runs/my-comparison --model gpt-6-astra --workers 3
python3 scripts/evaluate_routing.py --run-dir eval-runs/my-routing --model gpt-6-astra
```

These commands invoke models and consume the account's usage. They are separate from ordinary CI, which checks packaging, deterministic helpers, and case schemas. `--cases small-request` runs a narrow pilot. Full paired evaluation runs 45 cases in both conditions and a separate grading turn for each completed output.

Keep user-format constraints in the request visible to both conditions. Fixtures contain raw excerpts, draft prose, resources, and access metadata; evaluator conclusions belong in `criteria`. A format convention known only to the skill is not proof of improved research quality. Inspect model judgments rather than treating them as ground truth.

Before publishing, follow the [release process](docs/releases.md). Keep one collection version in `VERSION` and each skill's metadata. After the explicitly documented initial v0.1.0 consolidation, preserve published release tags and their history.

### Format checks and a second engine

```sh
python3 scripts/evaluate.py --engine claude --model sonnet --run-dir eval-runs/behavior-claude --cases imprecise-null supported-equivalence
python3 scripts/evaluate_formats.py --engine codex --run-dir eval-runs/formats-codex
python3 scripts/evaluate_formats.py --engine claude --model sonnet --run-dir eval-runs/formats-claude
python3 scripts/evaluate_routing.py --engine claude --model sonnet --run-dir eval-runs/routing-claude
```

Claude commands require the user's native Claude Code authentication. Do not request keys in chat or count an unavailable engine as passing. These are independent runs; a Codex result does not establish Claude behavior. Preserve raw local runs and publish sanitized shareable records as release assets, keeping concise summaries in `docs/`. Regression cases are not held-out evidence of research effectiveness; follow the [study protocol](docs/evaluation-study.md) for such claims.
