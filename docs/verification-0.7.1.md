# DevFlow Kit 0.7.1 — verification record

Date: 2026-11-09. Scope: independent repository extraction, portable distribution and documentation. Environment: Windows, Python 3.12.14, Node.js 24.22.1, Codex 0.159.2, Git Bash and Playwright Chromium.

## Automated checks

The full verifier ran against the extracted portable ZIP. All checks returned exit code 0. File integrity passed before and after execution: 257 portable manifest entries and 254 release manifest entries.

| Suite | Passing tests |
|---|---:|
| Bundle, adapters, UI resources and Superpowers integration | 42 |
| Catalog helper, URL handling, cache and exit codes | 28 |
| Sample backend | 12 |
| Interactive mock browser flow | 12 |
| Real backend browser flow | 15 |
| Concurrency scenarios | 2 |
| UI state scenarios | 7 |
| **Total** | **118** |

The sample verifier additionally confirmed that mock mode did not write the database, a real UI operation persisted, records survived a server restart, and a local one-row backup/restore fixture worked. This is not a production recovery-time benchmark.

## Installation and activation

Each of the five project adapters (`codex`, `claude-code`, `dsh`, `trae`, `trae-cn`) copied 258 files and passed repeated installation, comparison with source and installed-copy integrity checking. Archive CRC and payload/source comparisons passed for both distribution formats.

Codex native discovery found the outer `devflow` entry and all eight namespaced components in the isolated project installation. A fresh, read-only model run explicitly invoked `$devflow`, read the outer entry, lifecycle router and shared UI task policy, and chose the focused route for a small modal-focus fix. Its response retained the existing visual identity/stack and explicitly said no implementation tests had run. This activation probe verifies routing; it is not an end-to-end autonomous project build.

## Distribution checksums

| Archive | Bytes | SHA-256 |
|---|---:|---|
| `devflow-kit-v0.7.1.zip` | 1,824,513 | `ccfc27daeb6b3ef7813cdc737b3862602d31f05d7efc4a5132b4ec08850fc5ca` |
| `devflow-kit-plugin-v0.7.1.zip` | 1,800,841 | `ab71ac53002f2667f1381bee55a8ab427e831f86bc9374e7bc6e9184f960d69b` |

These are the locally built artifacts. Root README and diagram files are repository documentation, outside the installable plugin payload. Regenerating an archive changes creation metadata and can change its checksum without changing source content.

## Documentation visuals

Four new figures were produced using Diagram Design 2.6: project overview, architecture, development flow and installation. Static checks, geometry verification and SVG export all passed. PNGs were rendered at 2560 × 1440 with the expected fonts and inspected visually. At a 390 px viewport, the HTML diagrams scroll locally without overflowing the document. See [diagram sources and reproduction](diagrams/README.md).

## Boundaries

- Claude Code, DSH and Trae received filesystem/integrity tests, not authenticated model execution tests.
- macOS and Linux execution were not tested in this run.
- Discovery, activation, application checks, human acceptance and deployment are separate states.
- No production deployment, human acceptance or cloud skill upload was performed.
- The optional Taste browser inspector was not executed in the full verifier.
- Upstream skill bytes, licenses and provenance are retained; imported upstream whitespace is not normalized merely to satisfy a first-import diff check.

Reproduce the application and bundle checks with `python plugin/verify_bundle.py --with-example --report .local/verification.json` after installing the dependencies described in the [sample README](../plugin/examples/appointment-demo/README.md). Local raw logs are excluded from Git because they contain machine-specific paths.
