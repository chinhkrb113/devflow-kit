# DevFlow Kit diagrams

Original diagrams authored for this repository using [Diagram Design](https://github.com/cathrynlavery/diagram-design), version 2.6, source revision `6a7f19fcc132b39b126bea90167679b46b14bcc4` (MIT). The upstream skill supplies design guidance and validation/export tools; it is not vendored into the skill bundle.

| Source | Purpose | Visual grammar |
|---|---|---|
| [hero.html](hero.html) | Project introduction | Editorial cover |
| [architecture.html](architecture.html) | Harness, routing and supporting capabilities | Architecture; 7 nodes, 6 connectors |
| [workflow.html](workflow.html) | Work, constraints and outputs across the lifecycle | Process; stage framework, 5 stages × 3 semantic rows |
| [portability.html](portability.html) | Complete capsule, installer and host roots | Distribution architecture |

Each source is self-contained HTML with inline SVG. Google Fonts is the only external resource. HTML provides a local horizontal scroller on narrow screens. PNG exports embed the rendered appearance for GitHub and offline reading. SVG remains editable; its font appearance can vary in viewers without the named fonts. All diagrams include accessible titles and descriptions.

## Design

The 1280 × 720 slide preset uses a warm paper background, restrained blue accent, thin rules, orthogonal connections and no shadows. See [style-guide.md](style-guide.md). Solid lines show routing relationships; dashed lines show optional extensions. Routing is guidance selection, not a running network service. The development flow groups detailed lifecycle steps into five readable phases and explicitly keeps reverse optional.

## Reproduce

Generate the HTML sources with Python 3.12+:

```text
python scripts/draw_readme_diagrams.py
```

From an external checkout of the pinned Diagram Design revision, run these commands for each of `hero`, `architecture`, `workflow`, and `portability` (replace `<name>` and `<diagram-design>`):

```text
python <diagram-design>/skills/diagram-design/scripts/self_check.py docs/diagrams/<name>.html
python <diagram-design>/scripts/verify-geometry.py docs/diagrams/<name>.html
python <diagram-design>/skills/diagram-design/scripts/export_svg.py docs/diagrams/<name>.html docs/assets/<name>.svg
```

Render PNG with Node.js, Playwright and Chromium:

```text
node scripts/export_readme_assets.cjs
```

Set `PLAYWRIGHT_MODULE` to an existing Playwright module location if it is not on the Node resolution path. The exporter uses Node Playwright because that runtime is available in this environment; the upstream Python Playwright PNG helper was not executed. It waits for all three font families, exports at 2× resolution (2560 × 1440), checks canvas text bounds and verifies the mobile scroll boundary. A local report is written under ignored `.local/`.

## Validation on 2026-11-09

- Upstream static self-check: 4/4 pass.
- Upstream geometry verifier: 4/4 pass, zero findings.
- SVG exports: 4/4 pass.
- Chromium rendering, expected fonts and canvas bounds: 4/4 pass.
- 390 px viewport: no document overflow; diagrams scroll within their container.
- Visual inspection of all four exported PNGs completed.

Automated geometry checks do not measure aesthetic quality. These results establish renderability and the specific checks above.
