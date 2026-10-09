# Source notes

Checked on 2026-10-07. No paper PDF is redistributed here.

| Source | Material inspected | Observation used |
|---|---|---|
| Hu et al., [LoRA: Low-Rank Adaptation of Large Language Models](https://arxiv.org/abs/2106.09685v2), 2021 | Version 2 abstract and metadata | The base weights are frozen while trainable low-rank updates adapt the model. |
| Dettmers et al., [QLoRA: Efficient Finetuning of Quantized LLMs](https://arxiv.org/pdf/2305.14314v1), 2023 | Version 1 abstract, introduction, Section 2 text, and reference [28] | Adaptation combines a frozen 4-bit base with low-rank adapters. Activation-related memory also matters. |

## Verified forward citation

**QLoRA → LoRA** means QLoRA cites LoRA.

QLoRA's introduction cites low-rank adapters as reference [28]. That bibliography entry identifies Hu et al. and arXiv:2106.09685. The edge is supported by the paper text, not inferred from the names.

Locations in QLoRA v1: introduction on printed page 1; Section 2 on printed pages 3–4; bibliography entry [28] on printed page 18. These are one-based printed/PDF pages, not zero-based page indices.

## Limits

These are selected passages, not exhaustive paper readings or a current literature search. Figures were not independently analyzed. No benchmark results were reproduced.

The example's sequence-length study, controls, and decision rules are proposed here. Neither paper is cited as proving this proposal's outcome. Before making a publication novelty claim, search subsequent work and adjacent terminology.
