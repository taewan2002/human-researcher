# Review and applied corrections

This is an editorial self-review of the [example proposal](proposal.md), not an external peer review or model evaluation.

| Issue in the initial idea | Correction in the proposal |
|---|---|
| “More efficient” has no defined decision. | Bound the question to peak training memory under a quality constraint. |
| “LoRA versus QLoRA” could change many factors at once. | Compare base precision with matched adapter and training settings; record unavoidable stack differences. |
| Changing sequence length also changes context. | Compare precision within each length and limit the interpretation of cross-length changes. |
| A memory decrease alone sounds like overall superiority. | Measure quality, throughput, and feasibility as distinct outcomes. |
| A fixed schedule would invent hardware availability. | Use an explicit pilot and a conditional resource estimate. |
| A two-paper reading could be mistaken for a novelty search. | Label novelty unverified and require a broader search before claiming originality. |

## Still required before execution

- Choose and version the actual checkpoint, tokenizer, dataset, and split.
- Verify access, licenses, and hardware availability.
- Define the quality tolerance and justification.
- Use pilot measurements to choose repeats, measurement checks, and a resource cap.

These are visible execution gates. They are not disguised as completed results or precise duration estimates.

The scientific hypothesis itself is a manageable uncertainty because the proposal includes observations that could support, weaken, or complicate it. No result is needed to pretend that question is already answered.
