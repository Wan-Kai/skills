---
name: draw
description: Create and edit native draw.io diagrams, architecture diagrams, flowcharts, sequence diagrams, mind maps, and other editable visual canvases. Use when the user asks to draw, visualize a system or process, create or modify a .drawio file, or open an editable diagram in the Codex side browser. Always use draw.io; for a new diagram, recommend a visual style and ask the user to choose, defaulting to product-blueprint when no preference is given. Do not use Excalidraw.
---

# Draw

Create native, locally saved `.drawio` diagrams and open them in the draw.io web editor when the user wants to review or continue editing.

## Tool and output rules

1. Always use draw.io. Never route diagram work to Excalidraw.
2. Author native draw.io XML directly by default so the light-sketch style and collision-free routing remain deterministic.
3. Save a descriptive lowercase hyphenated `.drawio` file locally before delivery.
4. Keep all output editable. Do not flatten the diagram into an image unless the user explicitly requests PNG, SVG, or PDF.
5. Preserve an existing local diagram unless the user explicitly asks to replace or clear it.
6. Validate generated XML with `xmllint --noout <file>` when available.

## Optional draw.io Desktop capabilities

Use the draw.io Desktop CLI only when it adds value. On macOS, check `command -v drawio` and `/Applications/draw.io.app/Contents/MacOS/draw.io`. If unavailable, continue with native XML and explain only the missing optional capability.

### Mermaid conversion

- Use Mermaid when the user explicitly requests Mermaid or prefers rapid authoring of a standard flowchart, sequence, class, state, ER, gantt, mind map, timeline, journey, C4, or git graph over the default precise visual style.
- Convert Mermaid to native `.drawio` before any export:

  ```bash
  drawio -x -f xml -o diagram.drawio diagram.mmd
  ```

- Never export `.mmd` directly to PNG/SVG/PDF; direct Mermaid export can fail during embedded-XML processing.
- Remove the temporary `.mmd` after successful conversion, but keep the resulting `.drawio` as the persistent source.
- If the CLI is unavailable or conversion fails, author the same diagram as native XML.

### ELK layout and edge routing

- Apply layout only before final styling and manual connector routing; automatic layout can replace intentional geometry.
- Available presets include `verticalFlow`, `horizontalFlow`, `verticalTree`, `horizontalTree`, `radialTree`, and `organic`:

  ```bash
  drawio -x -f xml --layout horizontalFlow -o diagram.drawio diagram.drawio
  ```

- Use `--layout libavoid` as an optional first pass to route edges around fixed shapes without moving nodes. Then reopen the result and enforce the explicit-port and gutter rules below; never assume automatic routing is collision-free.
- For custom ELK configuration, pass a JSON array such as `'[{"layout":"elkLayered","config":{"elk.direction":"RIGHT"}}]'`.

### Editable exports

- Export only when the user requests PNG, SVG, or PDF. Keep the local `.drawio` source even after export.
- Use `-e` to embed diagram XML and a double extension that signals editability:

  ```bash
  drawio -x -f png -e -b 10 -o diagram.drawio.png diagram.drawio
  ```

- PNG, SVG, and PDF support embedded XML; JPG does not.
- Useful flags: `-t` for transparent PNG, `-s` for scale, `--width`/`--height` for fitting, `-a` for all PDF pages, and `-p` for a 1-based page index.
- If export fails, keep the valid `.drawio` and return its absolute path.

## Visual-style selection

For every **new diagram**, select its visual direction before authoring.

1. If the user explicitly names a supported style, use it without asking again.
2. Otherwise, recommend the best-fitting style in one short sentence, show the four supported choices below, and ask the user which style they want.
3. If the user asks to proceed without a choice, gives no preference, or the task must continue without an answer, use `product-blueprint` as the default and state that assumption.
4. For an edit to an existing diagram, preserve its current visual style unless the user asks for a restyle.

Supported choices:

- `light-sketch` — friendly hand-drawn diagrams for ideation, training, and early proposals.
- `product-blueprint` — the default; polished product maps, domain blueprints, and solution-planning diagrams.
- `clean-architecture` — restrained technical architecture, C4 views, and durable engineering documentation.
- `dark-ops` — high-contrast runtime, observability, and presentation-screen diagrams.

Never offer or imply a `roadmap-status` style. Convey roadmap status inside `product-blueprint` with badges and semantic colours when needed.

## Style specifications

### `product-blueprint` (default)

Use this clean card-based style by default. It is the reference style for product/solution blueprints: a soft white canvas, restrained semantic colour, section boundaries, and information-rich cards.

- Use an off-white canvas with a very subtle square grid when it helps spatial orientation; do not let the grid compete with labels.
- Use `sketch=0;rounded=1;shadow=1;strokeWidth=2;fontFamily=PingFang SC;fontColor=#1e293b` on business cards. Use white or very pale fills and a soft grey shadow.
- Use large rounded rectangles for business cards; arrange their content as title, optional top-right status badge, and compact bottom explanation or risk note.
- Use dashed rounded containers for domains, phases, and ownership boundaries. Give each container a small, left-aligned title in its semantic colour.
- Use semantic accent borders and fills consistently: blue `#2563eb` / `#eff6ff` for key or entry items; green `#16a34a` / `#f0fdf4` for converged or complete items; amber `#d97706` / `#fffbeb` for pending decisions; violet `#8b5cf6` / `#f5f3ff` for MVP or comparison items; slate `#94a3b8` / `#f8fafc` with a dashed border for planned items; red `#ef4444` only for risks or blocking boundaries.
- Render statuses as compact pill badges with a pale semantic fill, matching border, bold 11–12px text, and no separate legend when badge text is self-explanatory.
- Use thin orthogonal connectors with filled or classic arrowheads. Green may mark a confirmed primary path; coral/red dashed lines may mark unresolved dependencies. Add a compact legend whenever line colour or dash semantics are not evident from labels.
- Prefer generous whitespace and a horizontal or top-down reading direction. Use nested boundaries and highlighted paths instead of cramming every relationship into one node.

### `light-sketch`

- Use `sketch=1;curveFitting=1;jiggle=2` on nodes and connectors.
- Use `jiggle=1` on large containers and section frames so the layout remains calm.
- Use a shared charcoal outline: `strokeColor=#475569;strokeWidth=2`.
- Use soft pastel fills by semantic role:
  - user/client: `#dbeafe`
  - gateway/entry: `#fef3c7`
  - service/compute: `#dcfce7`
  - database/storage: `#f3e8ff`
  - neutral/container: `#fffdf5` or `#f8fafc`
- Use `PingFang SC` for Chinese labels and `Comic Sans MS` for short Latin labels when available.
- Use rounded rectangles for services, ellipses for people or clients, and `shape=cylinder3` for databases.
- Use orthogonal connectors with open arrowheads: `edgeStyle=orthogonalEdgeStyle;rounded=1;endArrow=open;endFill=0`.
- Keep shadows off, avoid gradients, and avoid saturated multicolour outlines.
- Use short labels, generous whitespace, even spacing, and one abstraction level per diagram.
- Keep titles clear and professional; do not append labels such as “草图版” unless requested.

### `clean-architecture`

Use this restrained, documentation-first style for technical architecture and C4-like diagrams.

- Use a white or `#f8fafc` canvas, `sketch=0`, no gradients, and no shadows.
- Use `strokeColor=#475569;strokeWidth=1.5;fontColor=#0f172a;fontFamily=PingFang SC` with 8–12px rounded corners.
- Use `#dbeafe` for people/clients, `#fef3c7` for gateways, `#dcfce7` for services, `#f3e8ff` for storage, and `#f8fafc` for neutral/external systems. Pair every non-obvious colour with an explicit type label or concise legend.
- Use solid grey orthogonal connectors for normal calls. Encode protocol, sync/async, or trust boundaries through labels and line styles; do not rely only on colour.
- Use recognised shapes only when they improve meaning: rounded rectangles for systems/services, ellipses for people, and `shape=cylinder3` for data stores. Keep every diagram to one C4 abstraction level.

### `dark-ops`

Use this high-contrast style for runtime topology, observability, incident paths, and large-screen presentations.

- Use `#0f172a` or `#111827` canvas, `sketch=0`, no grid, and no gradients.
- Use dark card fills (`#1e293b` or `#172554`), `strokeColor=#64748b;strokeWidth=1.5`, and high-contrast text (`#f8fafc` title, `#cbd5e1` body).
- Use a limited bright semantic palette: cyan `#22d3ee` for traffic, green `#4ade80` for healthy paths, amber `#fbbf24` for degraded paths, and red `#fb7185` for incidents. Do not use more than these four accents in one diagram.
- Use 2px orthogonal connectors with clear arrowheads. Keep connector labels in compact dark-backed chips so they remain legible over lines.
- Preserve ample spacing and avoid dense tables, pale text, or low-contrast dashed lines; this style must remain readable in a meeting-room display.

## Authoring workflow

1. For a new diagram, complete the visual-style selection workflow above. Choose exactly one abstraction level—domain map, entity relationship, flow, or architecture—per page. Split complex work into overview and detail pages before drawing.
2. Before XML, make the coordinate table described in [layout-and-routing.md](references/layout-and-routing.md): target viewport/side-panel budget, canvas, container and node bboxes, gutters, and every cross-domain edge. Use root coordinates for planned waypoints.
3. For standard flows, architecture diagrams, and small diagrams, author native `mxGraphModel` XML directly. Include root cells `id="0"` and `id="1"`; give every cell a unique ID.
4. Give every edge an expanded `<mxGeometry relative="1" as="geometry"/>`, escape XML attribute content, and never emit XML comments.
5. Use parent-child containment for architecture boundaries rather than placing a large rectangle behind unrelated nodes. Order cells: containers/frames, connectors, then nodes/labels.
6. For structural reflow of an existing diagram, preserve the source first: patch in place only for local changes; create a sibling backup or a new page before changing containers, abstraction level, or several cross-domain edges. Never overwrite unsaved browser work.
7. Write the `.drawio` file with `apply_patch`, run `xmllint --noout <file>` and `python3 skills/draw/scripts/check_geometry.py <file>`, then complete the dual-scale visual check in the reference before delivery.

## Connector routing and occlusion

Treat readable routing as a correctness requirement, not optional polish.

1. Never rely on automatic orthogonal routing when an edge could pass through another node, label, or layer title.
2. Connect at node boundaries with explicit `exitX`, `exitY`, `entryX`, and `entryY`; do not let lines visibly begin or end at node centres.
3. Reserve horizontal gutters between node rows and vertical gutters between columns as routing corridors. For a cross-domain edge, reserve a 48px corridor, cross the boundary perpendicularly, and add explicit `<mxPoint>` waypoints under `<Array as="points">` to keep segments inside it.
4. Calculate waypoint positions in root coordinates, including the offsets of parent containers.
5. For every connector, check each horizontal and vertical segment against the bounding boxes of all non-endpoint nodes. If a segment intersects one, reroute through the nearest clear gutter.
6. Route long cross-layer edges around intermediate nodes. For example, a left-to-right edge between nodes in the same row should travel above or below the row when another node lies between them.
7. Separate connectors that would otherwise share the same segment by using adjacent corridors or small offsets. Avoid stacked arrows that look like one ambiguous line.
8. Keep long explanatory text in a card or separate label chip; retain only short action labels on an edge, never on a domain boundary.
9. Keep containers below edges and nodes above edges, but do not use stacking as a substitute for collision-free routing. Run the bundled geometry check after each reflow.
10. Reopen and visually inspect dense areas at 35–45% and 65–80%. Fix any connector that crosses text, a node interior, a layer title, a boundary, or an unrelated connector junction.

## Codex side-browser delivery

When the user asks to see or edit the diagram in the Codex side browser:

1. Use the bundled in-app Browser skill and show the browser.
2. Keep the local `.drawio` file as the persistent source of truth.
3. Compress the XML with Node.js `zlib.deflateRawSync(encodeURIComponent(xml))`, encode it with Base64, and open:

   ```text
   https://app.diagrams.net/?splash=0&local=1#R<url-encoded-base64>
   ```

4. Do not use `#create=...` or `edit=_blank`; those forms can transfer or close the controlled Codex browser tab.
5. Open a new draw.io tab for a new artifact. Do not overwrite an active canvas containing unsaved user edits.
6. Verify the rendered canvas visually with a screenshot when appearance matters.
7. Keep the final tab as a browser `deliverable`; tab finalization must be the last browser action.

## Editing workflow

- For a local `.drawio` file, patch only the requested cells or styles, validate the XML, and reopen the updated file using the `#R` workflow.
- Browser-only manual changes are not automatically synchronized back to the local file. If those changes must be preserved, ask the user to save or download the updated `.drawio` file before applying further local edits.
- For a style-only request, preserve node IDs, labels, topology, and geometry unless the user also requests layout changes.

## Quality checklist

- Primary direction is immediately obvious.
- Nodes are aligned and evenly spaced.
- Connectors attach at node boundaries and do not cross unrelated nodes, labels, or layer titles.
- Long connectors use explicit ports and waypoints through reserved gutters.
- Cell stacking is container → connector → node/label.
- Semantic shapes and colours are consistent.
- Text remains readable at the intended zoom level.
- At overview (35–45%), both horizontal extremes remain visible; at detail (65–80%), labels, titles, boundaries, and key corridors remain unobstructed.
- `check_geometry.py` passes, or every intentional exception is stated before delivery.
- The local `.drawio` file validates and the browser canvas visibly renders.

## Example prompts

- “使用 `$draw` 画一个用户到数据库的系统架构图，并在侧边栏打开。”
- “使用 `$draw` 用产品蓝图风格画一张报税产品的领域地图。”
- “使用 `$draw` 给现有架构图增加 Redis，保留其他内容。”
- “使用 `$draw` 画一个登录流程图，保存为本地 `.drawio` 文件。”
