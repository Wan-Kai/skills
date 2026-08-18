# Explanation method

## Design for constrained working memory

Assume the reader can reason but cannot retain several undefined terms at once. A section fails when understanding it requires remembering more than one newly introduced abstraction from the previous section.

Create a learning contract with:

- three questions the reader should answer unaided;
- one prerequisite the article may assume;
- one likely misconception to overturn;
- one concrete example that can survive the whole explanation.

## Shape the causal spine

Use 3–6 steps. Each step contains:

1. **One idea** in a single sentence.
2. **One observable** the reader can see change.
3. **One mechanism** connecting cause to effect.
4. **One check** asking the reader to predict or compare.
5. **One takeaway** that can stand without the animation.

Prefer this article order:

```text
familiar tension
→ one-sentence thesis
→ causal spine
→ counterexample or failure boundary
→ method-family comparison
→ practical meaning
→ sources and deeper details
```

## Translate without distorting

Introduce the ordinary-language idea before its formal name. Reuse the same term afterward. If an analogy is used, immediately map every important part:

```text
analogy object → technical object
analogy action → algorithmic operation
analogy outcome → measured quantity
where analogy breaks → excluded behavior
```

Place formulas after the reader has already manipulated the quantities they relate, but keep any formula required for the central conclusion in the default reading path. Explain every symbol at the point of use and show one numerical example.

When a number supports the central thesis, show the complete derivation in the main causal path. For example, do not display two matrix shapes and expect the reader to infer the parameter saving; write both counts, substitute the current values, and state the comparison. A reader should never have to supply the missing arithmetic that makes the method worthwhile.

Attach teaching toys to the continuous example with an explicit label such as “the legal-email patch in a toy 8×8 layer.” A new toy that loses the original subject forces the reader to build a second mental model.

Gloss a specialist term in three to eight ordinary words at first use. If the term is not needed for the learning contract, remove it from the main path. Evidence vocabulary such as *optimizer*, *ablation*, or internal component abbreviations needs the same treatment as algorithm vocabulary.

## One complete reading path

- Start with the tension and one-sentence thesis.
- Continue through the full causal spine without asking the reader to choose a depth.
- Put the signature experiment where its variables first become meaningful.
- Include the evidence, necessary derivations, counterexamples, and failure boundaries in the main article.
- Reserve collapsible sections only for genuinely supplementary variants, source notes, or implementation details.

Each fact has one canonical home. Do not duplicate or hide essential explanations behind a reading-mode switch. “讲透” means completing the causal chain, not maximizing length: remove material that does not help answer the learning contract.

## Novice self-check

After drafting, answer these without specialized vocabulary:

- What goes in?
- What changes inside?
- What comes out?
- Why should the reader believe it?
- When does it stop working?
- What must the result not be interpreted as?

If any answer requires a term not yet defined, repair the causal spine before polishing prose.
