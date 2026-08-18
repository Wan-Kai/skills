# Evidence rules

## Build a claim ledger

Record each material claim before writing the article:

| Claim | Evidence type | Direct source | Scope and setup | Confidence | Article wording |
|---|---|---|---|---|---|

Use these evidence types consistently:

- **Paper result**: report the model, dataset, sample size, metric, baseline, and experimental condition needed to interpret the number.
- **Official fact**: state only what the organization, specification, or product documentation actually discloses.
- **Code fact**: cite the authoritative implementation and distinguish defaults from required behavior.
- **Author self-test**: identify missing code, data, controls, or reproducibility details.
- **Teaching parameter**: mark a value chosen to make a mechanism visible; never imply production performance.
- **Inference**: explain which sources support the synthesis and what would falsify it.

## Paper mode

Read the abstract, method, experimental setup, main results, ablations, limitations, and appendix sections required to interpret headline claims. Follow citations backward when a mechanism or baseline originated elsewhere. Inspect first-party code when the explanation depends on implementation details.

Separate four questions:

1. What problem does the paper define?
2. What mechanism is genuinely new?
3. What evidence supports the claimed improvement?
4. Which conclusions extend beyond the tested setup?

## Concept mode

Find the concept's competing definitions and choose one operational definition for the article. When multiple method families share only a high-level intuition, teach the shared intuition first and add a compact comparison showing where the algorithms diverge.

## Required boundary pass

Before publishing, search the draft for numbers, absolutes, causal verbs, superlatives, and product claims. For each one, confirm that the source supports the exact scope. Convert missing evidence into an explicit unknown rather than a confident sentence.
