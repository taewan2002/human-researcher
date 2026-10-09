# Installation

## Ask your agent

Paste this into **Codex or Claude Code**:

```text
Install all eight Human Researcher packages (seven research skills and one guide) for me by reading and following:
https://raw.githubusercontent.com/taewan2002/human-researcher/v0.1.0/docs/installation.md
```

Or in Korean:

```text
아래 설치 안내를 읽고 Human Researcher의 연구 스킬 7개와 사용 안내 스킬 1개를 설치해 주세요.
https://raw.githubusercontent.com/taewan2002/human-researcher/v0.1.0/docs/installation.md
```

Your agent downloads the skill folders, installs them for the agent you are using, and checks that their supporting files are present. This works in a local coding-agent environment with network and filesystem access.

Personal installation is the default, so you can use the skills across projects. Add “for this project only” to choose project scope, or name individual skills if you want only a subset. You do not need to prepare Node.js or run terminal commands for this route.

## Instructions for the installing agent

Follow this section when the user has asked you to install Human Researcher. Perform the installation with your available tools rather than returning shell commands for the user to run.

### 1. Select scope and destination

Install for the **current agent only**. Honor a requested project scope or subset; otherwise use personal scope and all eight packages (seven research skills and one guide).

- **Codex:** prefer the available built-in `skill-installer` and its supported destination. It accepts GitHub repositories and multiple skill paths. Follow its actual instructions and configuration rather than assuming a local script path.
- **Codex without that installer:** copy packages to the local skill directory supported by the host. Current standalone discovery supports `~/.agents/skills/` for personal scope and `<project>/.agents/skills/` for project scope.
- **Claude Code:** use `~/.claude/skills/` for personal scope or `<project>/.claude/skills/` for project scope.
- Respect configured locations. Some Codex installations use `$CODEX_HOME/skills` or `~/.codex/skills`; do not create duplicate registrations just to match another layout.

Before writing, inspect any existing same-name package in the target scope. Reuse identical packages. Preserve differing existing content and report a specific conflict; an installation request does not imply replacing someone else's skill or discarding local edits. Continue with packages that have no conflict.

### 2. Obtain and install the packages

Source repository: `https://github.com/taewan2002/human-researcher`. Install the version-pinned release tag **`v0.1.0`**, not the moving `main` branch, unless the user explicitly requests a development revision. Pass `--ref v0.1.0` to an installer that supports it. GitHub source URL: `https://github.com/taewan2002/human-researcher/tree/v0.1.0`.

Use these paths with Codex's installer, or obtain the repository with the available Git/download tools and copy each whole folder:

```text
skills/read-paper
skills/trace-research
skills/map-field
skills/develop-idea
skills/design-research
skills/write-proposal
skills/review-proposal
skills/using-human-researcher
```

Keep each folder's name and contents, including `agents/` and any `references/`. In particular, `write-proposal/references/proposal-contract.md` is required by its entrypoint.

Use a temporary checkout or download of that exact tag. Keep whole packages, including `scripts/`, `assets/`, and references. A directory containing only `SKILL.md` is insufficient.

With Git and Python 3.9+ available, the repository includes a conflict-aware installer. Clone or check out `v0.1.0`, then run the following with the already selected agent directory (not the literal placeholder):

```sh
python3 scripts/install.py --target /chosen/agent/skills --ref v0.1.0
```

Use `--skills read-paper write-proposal` for a subset or `--dry-run` to inspect changes. The installer checks that the clean skill sources match the requested commit. It records repository, tag, commit, and per-file SHA-256 hashes in `<target>/.human-researcher-lock.json`. An update replaces only unchanged packages from a recorded baseline; local edits, unrelated packages, and package symlinks remain conflicts. Other nonconflicting packages continue.

If using the host's native installer instead, record the same source and file hashes beside the installed packages, or retain the installer's equivalent provenance record. Keep the record outside each package so source comparisons remain exact. Do not fabricate a commit when installing an archive; retain the release tag and actual file hashes and state that limitation.

Normal skill use needs no Node.js dependency installation, service account, running server, or repository test environment. Optional helpers use Python 3.9+: arXiv HTML/PDF retrieval and citation discovery use the standard library; PDF text extraction uses `pypdf`, and page counting uses `pypdf` or Poppler `pdfinfo`. Install dependencies only when needed and authorized. arXiv retrieval is keyless. OpenAlex and Semantic Scholar accept optional keys (`OPENALEX_API_KEY`, `SEMANTIC_SCHOLAR_API_KEY`); anonymous access can be rate-limited. See the [retrieval guide](../skills/trace-research/references/retrieval.md). Failures remain explicit, not verified empty results. Use normal host permissions.

### 3. Verify and report

- Confirm each requested package has a readable `SKILL.md` and matching frontmatter name.
- Check the installed files against the downloaded source and verify local references remain inside the package and resolve.
- Report installed or already-present skills, destination, and any unresolved conflicts. Record the release tag, resolved source revision, and file-hash baseline in the persistent installation record.
- If the host exposes skill discovery, verify it. Otherwise distinguish successful file installation from confirmed runtime discovery.
- Explain how to select the skill or ask for it. If it is not visible yet, start a new session or reload the agent.

Do not install into other agents, rewrite unrelated settings, or run the research workflow as part of installation.

Sources: [OpenAI's repository skill installer guidance](https://learn.chatgpt.com/docs/build-skills#install-curated-skills-for-local-use), [Codex local discovery](https://developers.openai.com/codex/skills), and [Claude Code skill locations](https://code.claude.com/docs/en/skills).

## First use

After installation, ask:

```text
Use write-proposal with these sources and my notes.
Draft the proposal, review its evidence and design, and apply concrete fixes.
Keep my chosen direction and label assumptions.
```

Codex CLI and the IDE extension also support `$write-proposal`; Claude Code supports `/write-proposal`. Desktop interfaces provide their own skill selectors. The skills follow your requested language, including Korean.

## Update later

Ask the same agent:

```text
Update my Human Researcher skills from taewan2002/human-researcher to the latest published release.
Show which release is installed and which one will be installed.
Keep the current installation scope and preserve any local edits.
```

Compare three states: the recorded installed baseline, current local files, and the selected release. Without a baseline, preserve differing content as a conflict rather than guessing which differences are local edits. Verify the new content and update the provenance only after successful installation. To roll back, request a specific earlier tag and use the same checks. For future releases, keep published tags fixed. The initial v0.1.0 was consolidated again on 2026-10-09 at the maintainer’s request; compare the resolved commit and file hashes when updating an earlier v0.1.0 installation. Keep a branch installation explicitly labeled as development.

The first official release is `v0.1.0`. For installations made before the initial release was consolidated, compare the resolved commit and file hashes as well as the tag name when updating. The installation behavior is covered by tests for clean updates, local edits, unrelated packages, and restoring a prior revision.

## Optional: install from a terminal

<details>
<summary>Skills CLI commands for users who prefer a terminal</summary>

This alternative uses Git and Node.js **22.20+**, with the tested [Skills CLI](https://github.com/vercel-labs/skills) version **1.7.1**. Run inside your research project.

```sh
# List packages without installing.
npx skills@1.7.1 add https://github.com/taewan2002/human-researcher/tree/v0.1.0 --list

# Install all eight packages into the current project for Codex.
npx skills@1.7.1 add https://github.com/taewan2002/human-researcher/tree/v0.1.0 --agent codex --skill '*' --copy --yes

# Or install them for Claude Code.
npx skills@1.7.1 add https://github.com/taewan2002/human-researcher/tree/v0.1.0 --agent claude-code --skill '*' --copy --yes
```

These commands use **project scope**, unlike the default personal scope in the agent-guided instructions. Replace `--skill '*'` with `--skill write-proposal` for one package.

The CLI is a separate tool with its own options and telemetry policy. `DISABLE_TELEMETRY=1` disables its telemetry.

</details>

## Maintainer checks

`python3 scripts/smoke_install.py` verifies the optional CLI route by installing into temporary Codex and Claude Code projects and comparing file contents. It needs Git, Node.js, and network access.

For the published tag, run `python3 scripts/smoke_install.py --source https://github.com/taewan2002/human-researcher/tree/v0.1.0`.

That automated check is separate from testing a natural-language installation request in a running agent. Package validation does not prove runtime discovery or model behavior.
