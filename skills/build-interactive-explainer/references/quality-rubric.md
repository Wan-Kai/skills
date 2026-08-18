# Quality rubric

Score each dimension `0`, `1`, or `2` and cite a concrete passage, state, or interaction. Review from the perspective of an intelligent reader who reads slowly, has weak working memory for unfamiliar terms, and will not infer missing causal steps.

## Critical gates

Any failure below blocks delivery regardless of total score:

- A central claim lacks a direct source or overstates the source.
- The thesis, input, mechanism, or output cannot be identified in plain language.
- An interaction changes more than one unexplained variable at once.
- The animation's visible result contradicts its written explanation.
- The HTML requires an external script, stylesheet, font, image, or network call to function.
- A keyboard or reduced-motion user loses explanatory information.

## Scored dimensions

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Orientation | Reader cannot tell the question or payoff | Question exists but payoff is delayed | Tension and one-sentence thesis establish both immediately |
| Vocabulary | Undefined terms accumulate | Most terms defined, some arrive early | Ordinary idea precedes stable formal term; evidence terms are also glossed |
| Causal continuity | Important steps or arithmetic are implied | Chain is mostly complete | Every step names cause, mechanism, observable effect, and complete supporting arithmetic |
| Example continuity | Examples reset or introduce noise | Some reuse | One example evolves through the causal spine and signature experiment |
| Interaction value | Decorative, replaceable, or reveals its answer in advance | Useful but loosely connected | An unspoiled prediction and manipulation reveal a relationship a static view hides |
| Counterfactuals | Only the successful path appears | A contrast is mentioned | Correct/wrong or before/after states are directly comparable |
| Evidence literacy | Numbers lack setup or source type | Sources exist but scope is uneven | Evidence type, setup, uncertainty, and limits are visible |
| Failure boundaries | Article sounds universal | Some caveats appear at the end | Boundaries are taught where the mechanism breaks |
| Explanatory completeness | Essential reasoning is missing or hidden | Main path is mostly complete but one link requires inference | One default path connects intuition, mechanism, evidence, derivation, and limits without irrelevant detours |
| Visual coherence | Generic template ornament or conflicting visual systems | Styling is consistent but weakly related to the subject | One subject-derived metaphor controls typography, layout, accent, shape, and experiment treatment |
| Accessibility | Controls or motion exclude users | Basic labels exist | Keyboard, focus, redundant encoding, live results, reduced motion work |
| Shareability | Requires a development environment | Opens locally with minor dependencies | One offline HTML file works without adjacent resources |

## Decision rule

Require no critical failure, a total score of at least `21/24`, and no zero in any dimension. Prefer an independent reviewer who cold-reads the built HTML before seeing the Skill, intended answers, research notes, rubric, or source. Record the review in `novice-review.md` with:

- the three learning-contract questions answered in the reviewer's own words;
- the first point where the reviewer hesitated;
- every term the reviewer had to reread;
- one prediction made before using the signature interaction;
- the rubric table and evidence;
- the smallest revisions that would improve understanding.

Do not award points for visual polish when the reader cannot explain the mechanism afterward.

If no independent reviewer is available, label the result “author self-review.” It can find defects but cannot prove independent comprehension quality.
