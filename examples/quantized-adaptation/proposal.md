# When does quantizing the frozen base help adaptation?

**Status:** Reviewed concept proposal with explicit execution gates. No experiments have been run for this example.

## Motivation and evidence

Low-rank adaptation freezes base weights while learning smaller updates. QLoRA combines such adaptation with a quantized frozen base. These mechanisms are supported by the selected passages in the [source notes](sources.md).

A researcher choosing a training configuration also needs to understand memory use under their own sequence lengths and quality requirements. This proposal investigates that conditional decision rather than claiming a new adaptation method.

## Question and hypothesis

For one fixed checkpoint, tokenizer, and data pipeline, how does sequence length affect the peak-memory benefit of 4-bit frozen-base quantization relative to a 16-bit frozen base, with otherwise matched low-rank adaptation?

**Hypothesis to test:** As sequence length grows, other memory components may reduce the fractional benefit from quantizing the base. The result may depend on kernels and configuration; it is not assumed.

Candidate contribution: a bounded measurement and decision guide for the chosen setup. Novelty remains unverified pending a broader search.

## Method and controls

Use two precision conditions: a 16-bit frozen base and a 4-bit frozen base. Train the same adapter configuration in both. This isolates a configured precision comparison; it is not a full reproduction or ranking of the original papers.

Use illustrative sequence lengths of 256, 512, and 1,024 tokens, subject to the chosen checkpoint's support and a feasibility pilot. Within each length, match:

- Base checkpoint revision, tokenizer, adapter targets, rank, scaling, and dropout.
- Dataset snapshot, split, token order, batches, training-token budget, and checkpoint-selection rule.
- Optimizer policy, effective tokens per update, compute precision where supported, and gradient-checkpointing policy.
- Hardware, software versions, measurement procedure, and warmup exclusion.

Document unavoidable precision-specific differences, including quantization metadata and kernel behavior. Treat the finding as conditional on this stack.

Across lengths, pack the same training-token stream into different segment sizes. This changes available context, so do not interpret cross-length quality differences as quantization effects. Compare precision conditions **within each length** and report how that difference varies with length.

## Measurements and confirmation

Measure peak allocated and reserved GPU memory with synchronized, reset measurement windows; retain whole-run maxima and step-level traces. Report tokens per second and out-of-memory failures alongside memory. Do not mix allocator statistics with device-level memory as if they were the same metric.

Evaluate held-out negative log-likelihood using identical examples and evaluation formatting within each pair. Freeze a quality tolerance and its decision rationale before confirmation; the example does not invent a universal acceptable loss.

Pilot one pair to check implementation and estimate runtime. Use it for feasibility and variability planning, not as held-out confirmation. Choose repeat counts and a resource cap before confirmation based on the pilot and available equipment. Use matched seed identifiers where meaningful; do not assume that identifiers alone make individual outcomes statistically paired.

Keep raw runs, failed runs, configuration revisions, and exclusions. An inconclusive result should remain inconclusive.

## Interpreting outcomes

| Observation | Decision |
|---|---|
| Memory falls and quality meets the predefined tolerance | Consider the quantized configuration for this setup; report the measured tradeoff. |
| Memory falls but quality fails the tolerance | Investigate the quality tradeoff; memory alone does not establish usefulness. |
| Fractional memory benefit changes with length | Inspect measured components and configuration differences before assigning a cause. |
| Uncertainty is large | Report insufficient precision and decide whether additional repeats fit the cap. |
| A paired condition cannot run | Report the feasibility boundary; do not fabricate a matched quality comparison. |

No outcome supports a universal claim about all models, datasets, or input lengths.

## Execution gates, resources, and timeline

Before confirmation, the researcher must choose an accessible checkpoint and dataset, verify their terms, fix the quality tolerance, reserve hardware, and set a compute cap. These are unresolved inputs, not completed setup.

Sequence the work as follows:

1. Verify data access, checkpoint compatibility, and the broader prior-work landscape.
2. Run the paired pilot; inspect memory measurements and estimate throughput.
3. Freeze the confirmation protocol, repeat count, and quality rule.
4. Execute only within the authorized cap; analyze the paired conditions and revise the proposal's claims.

A calendar estimate is deferred until throughput and availability are known. After the pilot, estimate device time from measured time per configuration, the number of configurations and repeats, plus stated overhead. Track researcher effort and booking waits separately.

If resources are insufficient, reduce model scale or the number of lengths **before** confirmation, revise the question, and retain matched conditions. If existing work already answers the question, narrow to a justified replication or choose a different question.

## Readiness

The concept is specific enough to discuss and refine. It is not execution-ready until the inputs above are fixed. [Review notes](review.md) explain the corrections and remaining gates.
