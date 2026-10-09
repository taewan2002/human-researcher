# A browser-readable proposal

Use for a requested HTML proposal or browser reading view. Adapt [proposal-reader.html](../assets/proposal-reader.html), a standalone responsive document with inline styles, local navigation, native details, and print styles. Its sections are a starting composition, not mandatory chapters.

## Show the idea, then make it inspectable

Open with the plain-language question, evidenced need, and proposed change. Show inputs → mechanism → output, highlighting the change and fixed comparison conditions. Connect the test to possible outcomes and decisions, keeping unrun work explicit.

Retain the related work, reasoning, controls, measures, feasibility, risks, and unresolved decisions needed beneath the overview. Fold secondary implementation detail, not essential qualifications. Use [source evidence](source-evidence.md) for citation identity, provenance, locations, and missing links.

## Use the template components

The HTML contains three commented examples; adapt only the relevant markup and remove example comments from the final file.

| Component | Use |
|---|---|
| `.source` with `dl` | Title, evidence and access details; a unique source ID connects inline citations to the card |
| `a.external`, `.back` | A verified-as-present URL is printed with its address; a back link returns to an existing citation anchor |
| `.two`, `.comparison`, `.comparison.proposed` | Existing/proposed approaches side by side; stack on phones |
| `.flow`, `.node`, `.node.change`, `.arrow` | Labeled input-to-output flow; emphasize the actual changed component |
| `.badge`, `.badge.reported`, `.badge.unknown` | Explicit proposed, reported, or unknown text; color alone is insufficient |

Examples use placeholders, not fictional source URLs. When a link is unavailable, replace the anchor with the missing-link text. Match each internal `href` to a unique real target.

## Files and inspection

Create only the requested formats. A Markdown companion is generated only when requested; do not append a routine offer. If several formats are requested, reconcile claims, evidence, conditions, thresholds, and unknowns.

Keep assets inline or package required relative assets together. No CDN, remote fonts, runtime build, account, or server is needed; source links require network only when opened.

Open the output at desktop and phone widths. Check wrapping, diagram labels, table scrolling, keyboard navigation, internal source/return targets, and absence of page-wide overflow. Check external targets when access is allowed; distinguish that check from claim verification.

Inspect print layout with details closed; printed content must expose their contents, sources, and essential qualifications. A reader can span several pages. Inspect an exported PDF only if one is part of the deliverable. Remove placeholders and report only actual checks and consequential limits.
