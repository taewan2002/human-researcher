# Taxonomies that support a research decision

Use a taxonomy to show how a field branches into approach families, subfamilies, and representative methods or papers. Match the user's language, requested medium, and supplied visual references. A taxonomy diagram and a comparison matrix serve different reading tasks; the matrix can support the diagram but should not silently replace it.

## Establish the classification

1. State the question the map should help answer and the source set actually inspected. A supplied set of five papers is not a census of the field.
2. Choose a root matching that scope, then define the criterion for each split: problem, assumptions, information, learning mechanism, or supervision. Siblings should answer the same question. Internal nodes name categories; leaves name methods or papers. Do not mix a dataset, an evaluation score, and an algorithm as equivalent children.
3. Assign each paper from an inspected passage. Keep a compact evidence table: paper ID and version, category path or parent memberships, supporting locator, and missing information. Do not invent a missing year, mechanism, metric, or affiliation.
4. Check awkward cases. A hybrid can have multiple parents in a directed acyclic graph, or its own meaningful subfamily. An unreported property stays unknown rather than becoming “no.” Revise the splits if they obscure the important distinctions. Do not add an invented category merely to balance the picture.

Separate an existing survey's taxonomy from your provisional synthesis. Record coverage and the reading date. If two papers support only a comparison, say so rather than presenting a field-wide taxonomy.

## Pick a visual grammar

| Relationship in the evidence | Useful form | Important constraint |
|---|---|---|
| Field → families → subfamilies → methods | Hierarchical tree, usually the taxonomy default | Parent-child means category membership, not citation or historical succession. |
| A method legitimately belongs to several families | Hierarchical network / DAG | One method node may have multiple parents; label the membership criterion and avoid accidental duplicate methods. |
| Two cross-cutting distinctions | Labeled matrix | Define both axes; retain unknown or multiple memberships outside or across cells. |
| Many independent overlapping properties | Faceted table alongside the map | Do not force an exclusive tree; explain why a single hierarchy would distort the evidence. |
| Verified citations | Directed graph | State “B → A means B cites A”; topical similarity is a different edge type. |
| Changes over time | Timeline or lanes | Use verified dates. Chronology alone does not establish influence. |

Do not use edge width, node size, position, or saturated color as an unstated score of quality. If several edge types are necessary, name them in a legend. Every arrow should answer “what relationship does this encode?”

## Lay out a readable hierarchy

- Pick top-to-bottom for a broad branching overview, or left-to-right when category names and method labels need more width. Follow the orientation of a user's reference when practical.
- Keep the root, families, subfamilies, and method leaves at recognizable levels. Prefer a small number of meaningful levels; do not create one-child chains merely to reach a fixed depth.
- Give families a consistent visual style and leaves a lighter one. Use restrained branch colors, short category labels, aligned siblings, and generous space between groups. Do not turn every node into a paragraph card.
- Route connectors between node boundaries through empty space. Avoid crossing labels and unrelated boxes; reduce crossings before shrinking text. Use orthogonal branches or clean curves. Arrowheads are optional for unambiguous category trees.
- Show cross-membership with multiple incoming edges only when justified. If an extra edge means “uses a component,” “cites,” or “influenced,” give it a distinct line style and a named legend; never mix those meanings with category membership.
- Put an unclassified paper in a clearly marked unresolved group outside the established branches. A missing property is not a new scientific approach.
- Show the proposed method as a distinctly outlined leaf under its supported family, or label a proposed branch as provisional. Make its closest existing neighbor easy to identify. A visually new branch does not establish novelty.

## Locate the proposed contribution

Put the user's idea into the hierarchy alongside prior work with an explicit “proposed” label and a distinct outline. Identify the closest comparable methods, what would change, and the test needed to determine whether that change matters. For a requested matrix, use the same axes as prior work.

An unoccupied cell means only “not represented in the inspected set.” It is not proof of novelty, importance, or a successful method. Do not fill it with fabricated papers. Distinguish an unresolved classification from an actual absence.

## Build and inspect the result

- Deliver the requested map, not merely instructions for drawing one. Use an editable table, SVG, HTML, or an available diagram tool appropriate to the task. A diagram source alone is acceptable when that is what the user asked for; otherwise provide a viewable artifact when tools permit.
- Create the smallest usable diagram first, then inspect it. A plain companion evidence table is enough; do not spend the rendering budget building an interactive documentation site unless requested.
- For larger trees or networks, use an available graph-layout tool and preserve a node/edge source such as Mermaid or DOT alongside SVG. This makes adding papers and rerouting branches practical. Tool availability should determine the renderer, not the scientific classification.
- Keep labels short and place detailed evidence in a companion table or accessible source section. Use stable paper IDs in both. Source locators must remain reachable after export; local Markdown line references are not portable PDF links.
- Use text or line style as well as color for “reported,” “proposed,” and “unknown.” Give the figure a title, split or axis definitions, coverage note, and edge legend.
- Render at the intended viewing size and inspect labels, connectors, clipping, contrast, and source references. If rendering is unavailable, deliver editable source and explicitly identify the unverified rendering.
- Recheck classifications against the evidence table after layout changes. Do not silently turn an ambiguous source term into a more specific claim to shorten a label.

Finish when the map supports the next reading or research decision, its memberships are justified, and its limits are visible. Preserve a text alternative so the map remains useful without color or graphics.

For each representative paper, provide a recognizable title and original-source link in the node or its reachable source entry, with author/year when known. The entry explains the classification evidence and inspected locator. Short node labels may use IDs only when the title and source can be reached from them. Do not invent unavailable URLs or locators.
