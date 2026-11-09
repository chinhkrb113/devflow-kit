# DevFlow Kit 0.8.0 — verification record

Date: 2026-11-10 (Asia/Bangkok). Scope: Diagram Design integration, nine-component distribution, English README and new hero artwork. Runtime: Windows, Python 3.12.14, Node.js 24.22.1, Codex 0.159.2, Git Bash and Playwright Chromium.

## Bundle and example checks

The full verifier ran against the extracted portable ZIP. All suites returned exit code 0. Before and after execution, integrity checks verified 556 portable manifest entries and 553 release entries.

| Suite | Passing tests |
|---|---:|
| Bundle, adapters, resources and integration | 48 |
| Catalog helper, URL handling, cache and exit codes | 28 |
| Sample backend | 12 |
| Interactive mock browser flow | 12 |
| Real backend browser flow | 15 |
| Concurrency scenarios | 2 |
| UI state scenarios | 7 |
| **Total** | **124** |

Six new Diagram Design tests run from a copied component in an independent temporary directory. They cover packaged routing/resources, valid offline HTML, rejection of missing accessibility metadata, rejection of diagonal connectors, acceptance of orthogonal connectors and accessible SVG export. The tests exercise rejection paths as well as successful output.

The sample lifecycle also passed its mock/database isolation, real persistence, server restart and local backup/restore checks. These are local fixtures, not production recovery benchmarks.

## Installation and native discovery

All five project adapters (`codex`, `claude-code`, `dsh`, `trae`, `trae-cn`) copied 557 files with nine components and passed dry-run, repeat installation, source comparison and installed-copy integrity checks. ZIP CRC and source/payload comparisons passed for both distribution formats.

Native Codex discovery found **10 project entries**: the outer `devflow` entry and nine components, including `devflow-kit:diagram-design`, with no discovery errors.

Two fresh read-only model probes completed successfully:

| Probe | Observed behavior |
|---|---|
| Explicit `$devflow` routing | Read the outer entry, lifecycle entry, Diagram Design adapter and integration reference; distinguished current facts, assumptions and proposals; kept style files project-local; named structural, geometry and browser checks without claiming execution |
| Direct Diagram Design entry | Read the adapter and integration reference; preserved established content/brand, chose offline system fonts, and correctly left PNG/render inspection pending when browser tools were unavailable |

These probes establish entry selection and instruction handling. They do not establish a fully autonomous architecture audit or drawing session. The router probe enumerated the local bundle before reading its four relevant instruction files; enumeration did not imply reading every guide.

## Documentation and visuals

- Root README is English and the requested ownership/provenance section is absent. Component license files, notices and integrity metadata remain in the distribution.
- Hero artwork was generated with the built-in image tool and inspected for product-name/tagline accuracy and readability. Its [prompt and art direction](diagrams/hero-artwork.md) are recorded separately.
- Three technical diagrams passed the bundled structural and geometry checks, SVG export and Chromium rendering. All three expected web-font families loaded; no text fell outside the canvas.
- HTML diagrams use a local horizontal scroller at a 390 px viewport without document overflow.
- GitHub-rendered README Markdown was previewed locally at desktop and mobile widths; all four images loaded and the document had no mobile overflow.
- Diagram Design's local Markdown links were checked; none referenced missing files.

## Archives

| Archive | Bytes | SHA-256 |
|---|---:|---|
| `devflow-kit-v0.8.0.zip` | 3,262,676 | `aec74b1f508ae8f301a5c648dbb1ad27f02fce5dc0884e71be043d8feed89fc6` |
| `devflow-kit-plugin-v0.8.0.zip` | 3,219,904 | `5cd2f6d5702c12b3006937b008fcda9a56c65b983f87f503e9cf5ae311e2305e` |

These are the locally built archives. Root documentation and images are repository artifacts outside the installable payload. Archive creation metadata can change checksums when rebuilding.

## Limits

Claude Code, DSH and Trae were tested at the installation/integrity layer, not through authenticated model execution. macOS/Linux, cloud uploads, human acceptance and production deployment were not tested. The new Diagram Design checks sample supported helpers; they do not cover every upstream diagram type or importer. The optional Python Playwright PNG helper was not run; documentation PNGs used the existing Node Playwright runtime. The optional Taste inspector is outside this verifier run.

Reproduce with `python plugin/verify_bundle.py --with-example --report .local/verification.json` after installing the documented prerequisites. Local raw logs are excluded from Git because they contain environment-specific paths.
