# README visual assets

These assets explain the project and show its outputs. Planned work and source-reported findings are labeled separately. They are not measurements of skill performance.

| Asset | Production and purpose |
|---|---|
| [human-researcher-hero.png](human-researcher-hero.png) | Original brand illustration generated with the built-in `image_gen` tool on 2026-10-07. The prompt below records the intended composition. Reviewed for title/tagline legibility and project fit. |
| [research-workflow.svg](research-workflow.svg) | Repository-authored, editable vector diagram grouping the seven existing skills. It is not a compulsory execution sequence. Includes a text description. |
| [peft-taxonomy-preview.png](peft-taxonomy-preview.png) | Newly authored hierarchy of seven public PEFT papers. [SVG](../../examples/peft-taxonomy/taxonomy.svg) and [evidence notes](../../examples/peft-taxonomy/evidence.md) retain classification criteria, versions, and limits. |
| [adaptation-proposal-preview.png](adaptation-proposal-preview.png) | Redesigned A3 research proposal, rendered from the same geometry as the [SVG](../../examples/quantized-adaptation/poster.svg), [HTML](../../examples/quantized-adaptation/poster.html), and [PDF](../../examples/quantized-adaptation/poster.pdf). |
| [evaluation-map-preview.png](evaluation-map-preview.png) | An outcome-to-decision figure based on the existing [proposal](../../examples/quantized-adaptation/proposal.md), with [editable SVG](../../examples/quantized-adaptation/evaluation.svg). All conditions are planned. |
| [meeting-brief-preview.png](meeting-brief-preview.png) | A [fictional library-signage study brief](../../examples/research-meeting/README.md) based on the public synthetic fixture, with [editable SVG](../../examples/research-meeting/brief.svg). |

The original [synthetic classification example](../../examples/visual-taxonomy/README.md) remains available alongside the new public-paper taxonomy. README alt text and adjacent captions provide the meaning of each visual without relying on image text alone. All project-bound assets are stored in this repository.

## Hero generation prompt

Mode: built-in `image_gen`; no CLI/API fallback. No input images were supplied. The output was copied unchanged into the repository; generation-source originals are not runtime dependencies.

```text
Use case: ads-marketing
Asset type: wide GitHub README hero banner for the open-source project Human Researcher.
Primary request: Create a polished editorial identity image for seven research-agent skills that help a human researcher move from papers to an evidence-backed proposal. This is a project banner, not a software screenshot.
Style: sophisticated scientific editorial illustration, tactile ivory paper, delicate charcoal ink, restrained muted green and warm ochre accents, generous whitespace, flat print-like finish, no 3D tech clichés.
Composition: very wide landscape, approximately 3:1. Clear readable typography on the left half, an elegant research-paper-to-research-proposal illustration on the right. Several small paper sheets connect through a branching taxonomy and an outlined research question to one carefully composed proposal sheet with a simple method diagram. The visual expresses human judgment organizing evidence. Keep all meaningful content comfortably inside generous safe margins.
Text, verbatim and only these two lines of copy:
"Human Researcher"
"From papers to a proposal you can defend."
Set the project name in large beautiful editorial serif type and the tagline in smaller clear sans serif type. Text must be exactly correct and highly legible at normal GitHub README width. Any paper-sheet marks should be abstract short lines, not invented scientific text.
Constraints: no robot, no brain icon, no trophy, no fake performance charts, no author byline, no corporate logos, no watermark, no badges, no UI controls. The proposal remains a research plan, not a completed result. Produce one finished cohesive banner.
```

## Updating the gallery

The four gallery figures were authored as vector diagrams on 2026-10-08. [build_gallery.py](../../scripts/build_gallery.py) uses shared geometry for editable SVG and PDF, then renders PNG previews through Poppler. The poster HTML embeds that SVG. The gallery figures are not generated raster illustrations; the hero above is the separate ImageGen asset.

The palette uses warm paper, charcoal, green, blue, and rust. Method labels, classification edges, status labels, and source references are written explicitly. No performance curves or measured values were invented for visual effect.

To rebuild, install ReportLab and Poppler (`pdftoppm`), then supply regular and bold Korean TrueType fonts:

```sh
python3 scripts/build_gallery.py --font-regular /path/to/NanumSquareR.ttf --font-bold /path/to/NanumSquareB.ttf
```

NanumSquare was used for the checked PDF and PNG renders; the SVG/HTML also name Korean system-font fallbacks. Font files are not redistributed. If substituting a font, recheck text widths and the rendered SVG as well as the PDF. The English display titles use Times. Reading the committed artifacts does not require Python, a server, or build dependencies.

Intermediate PDFs are written under ignored `eval-runs/gallery-2026-10-08/`. The committed poster is an A3 landscape PDF. After a change, inspect all four preview images and the poster's page count, page size, text, and source links. Keep the proposal and its visual summaries consistent. Edit the workflow overview directly as SVG.

## Browser reader preview

[proposal-reader-preview.png](proposal-reader-preview.png) is a 1440 × 1000 browser screenshot of the [standalone proposal reader](../../examples/quantized-adaptation/proposal-reader.html), captured on 2026-10-09. It is a UI preview, not a generated illustration or research result. The page uses the [reader template](../../skills/write-proposal/assets/proposal-reader.html), system fonts, and existing source notes. Screen, source-link, and print checks are recorded in [reader validation](../evaluation-reader.md).

## RetoVLA case preview

[retovla-reader-preview.png](retovla-reader-preview.png) is a 1440 × 960 browser screenshot of the [RetoVLA reader](../../examples/retovla/proposal-reader.html), captured on 2026-10-09. The HTML/CSS diagrams were authored for this example. No paper figure or external portrait is redistributed. The reader presents a research proposal for the RetoVLA idea: motivation, hypotheses, method, comparisons, decisions, and conditional estimates. It contains no completed RetoVLA performance results. Its [source notes](../../examples/retovla/sources.md) separate prior-work evidence from the example’s authorship context; this is not the original historical proposal.
