---
name: build-interactive-explainer
description: Turn a research paper, technical article, or difficult concept into a novice-friendly interactive explainer and a self-contained shareable HTML file. Use when Codex needs to read and verify sources, teach a mechanism step by step, design small causal animations or experiments, or produce an offline HTML article from complex material.
---

# Build Interactive Explainer

Produce an explanation a patient beginner can follow and a single HTML file they can share. Treat research accuracy, teaching quality, interaction design, and offline delivery as four separate gates.

## Workflow

1. **Set the learning contract.** Name the intended reader, the three questions they should answer afterward, the minimum prior knowledge, and the most likely misconception. Default to an intelligent reader who lacks the topic's vocabulary and struggles to hold several new abstractions in working memory.
2. **Build the evidence ledger.** For a paper, read the paper and first-party code before secondary explanations. For a concept, triangulate primary papers, specifications, official documentation, or source code. Read [evidence-rules.md](references/evidence-rules.md) and keep `research-notes.md` beside the output.
3. **Find the causal spine.** Reduce the topic to 3–6 ordered ideas. Reuse one concrete example across the spine. Give every step one observable change and one plain-language takeaway. Read [explanation-method.md](references/explanation-method.md).
4. **Design experiments.** Turn only the relationships that benefit from manipulation into micro-experiments. Read [interaction-patterns.md](references/interaction-patterns.md). Use Vue for interactive state and build static diagrams as SVG/HTML. Do not create a separate vanilla-JavaScript branch.
5. **Implement the article.** Audit the current page when redesigning, state a one-line design read and explicit variance/motion/density dials, then copy or revise `assets/vue-template/`. Replace the demonstration content and experiment with topic-specific material while preserving accessibility and the complete single-path narrative. Follow [visual-design.md](references/visual-design.md) and [implementation.md](references/implementation.md).
6. **Build the deliverable.** Run `scripts/build_explainer.sh <project-dir>`. The required deliverables are the editable source project, `explainer.html`, and `research-notes.md`. The HTML may contain an inlined Vue runtime, but it must not require Vue, a CDN, a server, or adjacent files at viewing time.
7. **Verify understanding and delivery.** Apply every gate in [quality-rubric.md](references/quality-rubric.md), run `scripts/validate_html.mjs`, then serve the built file locally and inspect it in a real browser at desktop and mobile widths. Exercise every control, keyboard focus, reset path, reduced-motion behavior, source link, and final state. When subagents are available, require an independent reviewer to cold-read the HTML before seeing the Skill, source, research notes, or intended answers.

## Teaching contract

- Lead with a tension the reader already understands, then give one sentence that resolves it.
- Introduce one new idea per step and keep terminology stable.
- Pair each analogy with the exact technical mapping and its breaking point.
- Derive every central quantitative advantage step by step; never make the reader infer the arithmetic that supports the thesis.
- Keep the continuous example attached to the signature experiment; label toy dimensions as a view of that same example, not a new problem.
- Show before/after or correct/wrong counterfactuals instead of asserting causality.
- Preserve a genuine prediction loop: hide truth labels and outcome hints until the reader commits or runs the experiment.
- End every experiment with a stable number, state, or sentence that explains what changed and why.
- Design one complete default reading path that teaches the topic from intuition through mechanism, evidence, and limits. Do not add reading-depth modes. Keep prerequisite explanations next to the claims that need them; only genuinely supplementary material may be collapsible.
- Label claims as source fact, experiment result, author self-test, teaching parameter, or inference.
- State what the method cannot prove, where it fails, and what remains unknown.
- Write in the user's requested language; otherwise use the conversation language. Replace specialist terms with ordinary language or define them inline at first use.

## Runtime and output rules

- Use Vue 3, TypeScript, and Vite for interactive explainers.
- Prefer build-time SVG/HTML for diagrams that do not require user-controlled state.
- Inline all runtime code and CSS into `explainer.html`.
- Keep article content usable on narrow screens and without hover.
- Respect `prefers-reduced-motion`; preserve the same information in the reduced-motion state.
- Use motion to expose a state transition, not to decorate a section entrance.
- Make the subject's mechanism, notation, material, or instrument determine the visual metaphor. Do not ship the template palette and ornament unchanged when they do not belong to the subject.
- Publish only when the user explicitly asks. Local HTML generation is always in scope.

## Completion evidence

Do not report completion until all of these are present and inspected:

- A claim ledger with direct source links and explicit unknowns.
- A causal spine whose steps each add one idea.
- At least one interaction that materially improves understanding, plus a written reason it is interactive.
- A successful production build yielding one self-contained `explainer.html`.
- A validator pass proving no external runtime or stylesheet dependency.
- A real-browser pass against a locally served production HTML covering comprehension text, controls, responsive layout, and reduced motion; separately validate that the file has no runtime dependency.
- A visual preflight covering theme, accent, shape, typography, section rhythm, mobile collapse, visible copy, and the absence of generic template ornament.
- An independent novice-lens cold review scoring every rubric dimension with concrete evidence and no critical gate failure when subagents are available. Label an author self-review explicitly and do not present it as independent evidence.
