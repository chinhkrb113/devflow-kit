# Documentation visuals

The README uses a generated brand hero and three editable technical diagrams. They have separate rendering paths so rebuilding diagrams never overwrites the hero.

| Asset / source | Purpose | Format |
|---|---|---|
| [hero.png](../assets/hero.png) | Product identity and positioning | Generated raster artwork; see [art direction and prompt](hero-artwork.md) |
| [architecture.html](architecture.html) | Harness, router and nine complementary components | Architecture; eight nodes and seven connectors |
| [workflow.html](workflow.html) | Work, constraints and outputs across five lifecycle stages | Process with consistent semantic rows |
| [portability.html](portability.html) | Complete capsule, installer and target roots | Distribution architecture |

## Technical diagram sources

Diagram Design is bundled at [plugin/skills/diagram-design](../../plugin/skills/diagram-design/SKILL.md), pinned to revision `6a7f19fcc132b39b126bea90167679b46b14bcc4`. Its compact entry selects the relevant references and keeps project styles outside the installed bundle. The original guide, templates and helpers remain available on demand.

The diagrams use a 1280 × 720 editorial canvas with project-specific [style tokens](style-guide.md). Each HTML file has accessible inline SVG and a local horizontal scroller for narrow screens. Google Fonts is its only external dependency. PNG exports preserve the rendered appearance; editable SVG may use fallback fonts in other viewers.

## Rebuild

From the repository root:

```text
python scripts/draw_readme_diagrams.py
```

Run the following for `architecture`, `workflow` and `portability`, replacing `<name>`:

```text
python plugin/skills/diagram-design/scripts/self_check.py docs/diagrams/<name>.html
python plugin/skills/diagram-design/scripts/verify_geometry.py docs/diagrams/<name>.html
python plugin/skills/diagram-design/scripts/export_svg.py docs/diagrams/<name>.html docs/assets/<name>.svg
node scripts/export_readme_assets.cjs
```

The last command renders all three PNGs using Node Playwright and Chromium. Set `PLAYWRIGHT_MODULE` to an external installation if required. This host's existing Node browser runtime is used instead of the optional upstream Python Playwright PNG helper.

The exporter waits for Instrument Serif, Geist and Geist Mono, outputs 2560 × 1440 PNGs, checks canvas text bounds, and verifies that a 390 px viewport scrolls inside the diagram container without overflowing the document. Its local report is written under ignored `.local/`.

## Validation

For version 0.8.0, all three technical diagrams passed the bundled structural and geometry checks, SVG export and Chromium render checks. The generated PNGs were inspected visually. The raster hero is checked separately for text accuracy, legibility and README rendering; SVG geometry checks do not apply to that artwork.

These checks establish the reported properties, not a universal aesthetic score or architectural correctness. See the [release verification record](../verification-0.8.0.md).
