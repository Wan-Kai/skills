---
name: draw
description: Create and edit native draw.io diagrams, architecture diagrams, flowcharts, sequence diagrams, mind maps, and other editable visual canvases. Use when the user asks to draw, visualize a system or process, create or modify a .drawio file, or open an editable diagram in the Codex side browser. Always use draw.io and the default light-sketch visual style; do not use Excalidraw.
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

## Default visual style: light sketch

Apply this style unless the user explicitly requests another visual direction.

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

## Authoring workflow

1. Identify the diagram type, primary flow, groups, and semantic roles.
2. For standard flows, architecture diagrams, and small diagrams, author native `mxGraphModel` XML directly.
3. Include root cells `id="0"` and `id="1"`; give every cell a unique ID.
4. Give every edge an expanded `<mxGeometry relative="1" as="geometry"/>` child.
5. Escape XML attribute content and never emit XML comments.
6. Use parent-child containment for architecture boundaries rather than placing a large rectangle behind unrelated nodes.
7. Order cells by visual stack: large containers and frames first, connectors second, business nodes and labels last.
8. Write the `.drawio` file with `apply_patch`, validate it, then deliver it.

## Connector routing and occlusion

Treat readable routing as a correctness requirement, not optional polish.

1. Never rely on automatic orthogonal routing when an edge could pass through another node, label, or layer title.
2. Connect at node boundaries with explicit `exitX`, `exitY`, `entryX`, and `entryY`; do not let lines visibly begin or end at node centres.
3. Reserve horizontal gutters between node rows and vertical gutters between columns as routing corridors. Add explicit `<mxPoint>` waypoints under `<Array as="points">` to keep segments inside those corridors.
4. Calculate waypoint positions in root coordinates, including the offsets of parent containers.
5. For every connector, check each horizontal and vertical segment against the bounding boxes of all non-endpoint nodes. If a segment intersects one, reroute through the nearest clear gutter.
6. Route long cross-layer edges around intermediate nodes. For example, a left-to-right edge between nodes in the same row should travel above or below the row when another node lies between them.
7. Separate connectors that would otherwise share the same segment by using adjacent corridors or small offsets. Avoid stacked arrows that look like one ambiguous line.
8. Keep containers below edges and nodes above edges, but do not use stacking as a substitute for collision-free routing.
9. Reopen and visually inspect dense areas at a readable zoom. Fix any connector that crosses text, a node interior, a layer title, or an unrelated connector junction.

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
- The local `.drawio` file validates and the browser canvas visibly renders.

## Example prompts

- “使用 `$draw` 画一个用户到数据库的系统架构图，并在侧边栏打开。”
- “使用 `$draw` 给现有架构图增加 Redis，保留其他内容。”
- “使用 `$draw` 画一个登录流程图，保存为本地 `.drawio` 文件。”
