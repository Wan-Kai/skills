# Implementation guide

## Create the project

Run:

```bash
scripts/create_explainer.sh <output-directory>
```

The copied Vue project is editable source, not the final deliverable. Replace the sample thesis, steps, experiment, evidence labels, and sources with topic-specific content. Keep the shell, complete single-path narrative, focus styles, responsive rules, and reduced-motion path unless the subject requires a deliberate redesign.

## Design before coding

Write a compact design plan in `research-notes.md`:

- subject, reader, and page's single job;
- one-line design read plus `DESIGN_VARIANCE`, `MOTION_INTENSITY`, and `VISUAL_DENSITY` values;
- 4–6 named colors with hex values and semantic roles;
- display, body, and utility typography roles using system-safe font stacks;
- one-column layout concept;
- one signature experiment tied to the subject;
- the one aesthetic risk and why the subject justifies it.

Derive the palette, typography, and signature visual from the topic's own materials, instruments, or notation. For every unusual visual token, record the subject fact that motivated it. If the same design plan would survive unchanged for an unrelated topic, revise it before coding.

Read [visual-design.md](visual-design.md) before changing page structure or CSS. The bundled template demonstrates an editorial technical-dossier direction, not a universal brand. Preserve its hierarchy and craft level while replacing its subject-specific metaphor.

## Implement

- Keep all visible article copy in `src/content.ts` when it is static.
- Put topic-specific state and causal calculations in a dedicated component under `src/components/`.
- Keep experiment parameters deterministic when comparison matters.
- Use CSS and SVG for visual state; use Canvas only when hundreds of moving marks make DOM/SVG impractical.
- Use real buttons and inputs. Announce result changes through `aria-live`.
- Use inline SVG or generated HTML; do not add remote images or fonts.

## Build and verify

Run:

```bash
scripts/build_explainer.sh <project-directory>
node scripts/validate_html.mjs <project-directory>/explainer.html
scripts/serve_explainer.sh <project-directory> [port]
```

The build script installs pinned dependencies when needed, runs type checking, builds with Vite, and copies the single-file bundle to `explainer.html`.

Use the printed local URL to test the production `explainer.html` in a real browser. The local server is an acceptance surface, not a viewing-time dependency; the validator separately proves the delivered file is self-contained. Verify:

1. the complete default narrative from orientation through mechanism, evidence, and limits;
2. every experiment control, reset, and final textual result;
3. keyboard focus order and visible focus;
4. viewport widths around 390 px and 1280 px;
5. reduced-motion output;
6. source links and evidence labels;
7. no network requests are required after the file opens.
