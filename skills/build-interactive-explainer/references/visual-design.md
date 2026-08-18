# Visual design for interactive explainers

## Start with a design read

Before changing markup or CSS, write one sentence:

```text
Reading this as: <page kind> for <reader>, with a <vibe> language, leaning toward <visual family>.
```

Then set `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY` from 1–10. An editorial technical explainer usually starts near `6 / 4 / 5`: asymmetric enough to create hierarchy, animated only when state changes, and dense enough to support a serious read.

For a redesign, first record the current palette, type stack, radii, layout rhythm, interaction states, recognizable elements, and generic patterns to retire. Preserve content, learning order, anchor IDs, accessibility behavior, and working interactions unless the user asks to change them.

## Derive a visual metaphor from the subject

Choose one visual world suggested by the material itself: laboratory notebook, annotated source file, field guide, score, map, instrument panel, archival dossier, or another defensible metaphor. Map the metaphor to real page decisions:

```text
subject property → visual token
causal sequence → page rhythm
evidence type → annotation treatment
interactive mechanism → primary visual surface
```

If the same palette, hero ornament, and card system could be pasted onto an unrelated topic unchanged, the direction is too generic.

## Compose the page

- Use one complete reading path. Do not add reading-depth modes.
- Keep the hero to an eyebrow or document mark, a headline, a short tension, a thesis, and at most one explanatory visual.
- Make the hero visual carry meaning. Prefer a mechanism map, transformed example, or real experimental state over decorative bars, blobs, grids, or fake product screenshots.
- Use content verbs as section labels. Avoid generic “第一步”, numbered eyebrows, and repeated micro-labels above every heading.
- Give long-form sections varied but calm rhythm. Use asymmetry, whitespace, sparse dividers, and occasional color fields instead of wrapping every idea in a card.
- Make the signature experiment the richest surface on the page. Its selected, loading, result, reset, focus, hover, and reduced-motion states must all be designed.
- Present more than five sources or checklist items as grouped chunks, a two-column index, or another scannable component instead of an undifferentiated list.
- Collapse every asymmetric layout to a strict single column below 768 px.

## Lock the system

- Choose one page theme. A print-emulating editorial explainer may deliberately use light-only; otherwise support the required theme behavior consistently.
- Use one accent color across the whole page. Do not introduce a new accent for each evidence type.
- Choose one shape rule: sharp, soft, or a documented mixed system. The default template uses sharp document edges.
- Use system-safe or self-hosted fonts only. Do not add a remote font dependency to the offline HTML.
- Keep body copy near 60–70 characters per line and at WCAG AA contrast or better.
- Avoid pure black and pure white, generic AI-purple gradients, ornamental glows, excessive pills, equal feature-card rows, and shadows that do not communicate hierarchy.
- Use no em dash or en dash in visible copy. Rewrite the sentence or use a regular hyphen for ranges.

## Motion

Every motion must explain hierarchy, feedback, or a state transition. Use transform and opacity only. A brief hero reveal is acceptable when it establishes reading order; experiment animation must show the causal change. Respect `prefers-reduced-motion` and preserve the same final information without animation.

## Visual preflight

Before delivery, verify mechanically:

- the design read and three dials exist in `research-notes.md`;
- the page has one theme, one accent, and one shape system;
- hero copy fits the initial viewport and its visual is explanatory;
- section labels describe content rather than numbering it;
- required derivations and evidence are visible in the default path;
- every button has readable text, visible focus, hover, active, disabled when applicable, result, and reset states;
- mobile width has no horizontal overflow and each multi-column section becomes one column;
- visible copy contains no em dash, decorative version stamp, scroll cue, fake precision, or unexplained placeholder;
- console logs are clean and the self-contained validator passes.
