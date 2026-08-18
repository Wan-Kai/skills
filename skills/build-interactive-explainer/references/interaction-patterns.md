# Interaction patterns

Choose interaction by the relationship the reader must discover. Every experiment needs a learning question, one controllable variable, visible before/after evidence, a reset path, and a stable textual conclusion. Preserve the prediction loop: controls may reveal inputs, but truth labels, outcome classifications, and explanatory hints stay hidden until the reader runs or commits to a prediction.

## Reusable patterns

| Learning relationship | Interaction | Required evidence |
|---|---|---|
| A probability creates a distribution | One trial / many trials | Current outcome, running counts, expected distribution |
| An intervention changes a system | Before/after toggle | Ghosted baseline and changed state in the same frame |
| Context changes classification | Small multiples | Same candidates, changed context, consistent encoding |
| Weak evidence accumulates | Sample-size control | Count, rate, threshold, and written verdict |
| Robustness degrades with perturbation | Semantic slider presets | Changed artifact, surviving signal, and consequence |
| A process has dependent stages | Stepper with prediction | Current state, changed variable, next-state explanation |
| Two methods differ structurally | Synchronized comparison | Same input and metric for both paths |

## Experiment brief

Write this before coding:

```text
Learning question:
Reader prediction:
Controlled variable:
Fixed variables:
Visible transition:
Final evidence:
Wrong interpretation prevented:
Why a static figure is insufficient:
What remains hidden before prediction:
```

If the last answer is weak, use static SVG or HTML instead.

## Motion grammar

- Use 150–300 ms transitions for direct manipulation.
- Use a slower single run to reveal sequence and a batch control to reveal distribution.
- Keep layout stable; animate the measured property rather than moving the whole card.
- Preserve the previous value with a baseline, trail, or paired state when comparison matters.
- Stop at a meaningful state. Display the result as text in an `aria-live` region.
- Provide restart or reset when randomness, sequence, or exploration can obscure the baseline.
- Distinguish system state from an external oracle. If the experiment compares an approximate answer with ground truth, label the truth as external and explain that the system itself does not store it.
- Under `prefers-reduced-motion`, jump to the same final state and retain every number and explanation.

## Visual encoding

Define one semantic visual language for the whole article. Reinforce color with shape, fill, underline, border, or labels. Use utility typography for numbers and evidence labels. Avoid hover-only explanations.

## Failure patterns

- A scroll reveal that exposes no causal state.
- Several sliders changing the result simultaneously.
- Motion whose final state disappears before it can be read.
- A decorative simulation whose numbers do not correspond to the explanation.
- A chart with unlabeled axes, missing baseline, or no statement of what changed.
- A reset that changes hidden random seeds and makes comparisons impossible.
- A button label, metric, or hint that reveals the result before the reader predicts.
- A “ground truth” field that appears to belong to a system which does not actually contain that information.
