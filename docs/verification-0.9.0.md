# DevFlow Kit 0.9.0 — verification record

Date: 2026-11-10 (Asia/Bangkok). Scope: Open Code Review and Security Audit integration, eleven-component packaging, documentation and harness checks. Environment: Windows, Python 3.12.14, Node.js 24.22.1, Codex 0.159.2, Git Bash and Playwright Chromium.

## Result

The final extracted portable ZIP passed every verifier group: bundle regression, catalog helper, security validators and the sample application lifecycle. **182 checks passed, zero failed, and 19 upstream security tests were explicitly capability-skipped.** Skipped cases are not counted as passing or as evidence of cross-platform execution.

| Suite | Passed | Skipped |
|---|---:|---:|
| Bundle, adapters, resources and integrations | 52 | 0 |
| Catalog helper | 28 | 0 |
| Security schema, coverage and stdin transport | 54 | 19 |
| Sample backend | 12 | 0 |
| Interactive mock browser flow | 12 | 0 |
| Real backend browser flow | 15 | 0 |
| Concurrency scenarios | 2 | 0 |
| UI state scenarios | 7 | 0 |
| **Total** | **182** | **19** |

File integrity passed before and after execution: 590 portable manifest entries and 587 release entries. The sample also passed mock/database isolation, persistence, restart and bounded local backup/restore checks.

## Issues found and resolved

1. **Unsupported protected file opening on Windows.** Upstream's findings CLI tests included seven cases that assumed `O_NOFOLLOW`/`O_NONBLOCK`. The production readers correctly rejected input when these flags were unavailable. The bundle preserves that behavior, marks those test prerequisites explicitly and adds a bounded trusted-parent stdin transport using the same schema, structural preflight and semantic validation. Eight new stdin tests cover valid records, malformed data, UTF-8, size/depth limits, forbidden fields, path-argument rejection and diagnostic escaping. A separate live process check confirmed the 10-second input timeout (observed approximately 10.12 seconds). The 19 skipped cases include upstream's existing OS-dependent file tests; they remain unverified on this Windows host.
2. **CRLF in an executable upstream script.** The first archive failed the shebang/LF regression check for the coverage validator. Only its line endings were normalized; logic and original protected reader are unchanged. Provenance hashes distinguish original Git bytes from distributed bytes. The corrected archive was rebuilt and the full verifier rerun successfully.

stdin validation is for serialized JSON already owned by the trusted parent. It is not a workaround for unverified scratch artifacts, an execution sandbox, or proof that a finding is true. The upstream target-execution and independent-verification requirements remain in force.

## OCR runtime probe

An existing native **Open Code Review v1.13.6 (`891df1b`)** executable ran `delegate preview --format json` and `delegate rule --format json` against a disposable local Git fixture. Preview identified exactly two expected entries: one modified file and one untracked added file. Rule resolution returned the configured rule group.

No OCR model provider or paid review endpoint was invoked by that fixture. This verifies deterministic preparation, not LLM review quality. The packaged guides are pinned to upstream revision `04deca6721ec4fe2f74a6a0eb069d2a01b3d31cb`; the installed runtime revision is recorded separately. The executable is not bundled or installed by the portable installer.

## Installation and Codex behavior

All five project adapters (`codex`, `claude-code`, `dsh`, `trae`, `trae-cn`) installed **591 files / 11 components** and passed dry-run, repeated installation, source comparison and installed-copy integrity checks. Both archive CRC/source comparisons passed. Native Codex discovery from the final extracted installation returned **12 entries**: the outer router and eleven components, with no discovery errors.

A fresh read-only model probe read the project-local outer entry, shared review coordination, both new adapters and their compatibility references. For a diff-only review without OCR, it chose a labeled host-native fallback and rejected automatic installation, provider setup, fixes and publishing. For a full audit without execution isolation or independent review, it allowed source inspection while marking execution blocked and full-audit completion unavailable. It did not execute the hypothetical review or audit. All six instruction files read by the probe were byte-compared with the final archive after the line-ending correction and matched.

Existing local Codex component links were preserved; two additional links expose the new components. A fresh host session may be required to refresh discovery.

## Documentation

README remains English and retains the requested hero artwork. It now describes eleven skills, review examples and runtime limits. Architecture and portability diagrams include the new review/security role. Structural checks, geometry checks, SVG exports and Chromium rendering passed for all three technical diagrams. At 390 px, diagrams scroll within their container without overflowing the page. The README's four images loaded in desktop/mobile previews. Local documentation and component links were checked.

## Final archives

| Archive | Bytes | SHA-256 |
|---|---:|---|
| `devflow-kit-v0.9.0.zip` | 3,407,440 | `ec74d4838da99ce5c22de7b3fa5a4c4cab5b6aeff27ff35fe88d18fda792203d` |
| `devflow-kit-plugin-v0.9.0.zip` | 3,361,991 | `24aae719caa4157c0be13b874569da4335d1079ef68e7aa401c0cddf9fcb99f7` |

Root documentation and images are repository artifacts outside the installable payload. Creation metadata can change archive checksums on a later rebuild.

## Limits

This is integration verification, not a completed security audit of a target system. It does not certify vulnerability-detection quality, safe production deployment, independent human acceptance, authenticated execution in Claude Code/DSH/Trae, or macOS/Linux runtime behavior. No target-code audit sandbox is supplied. The optional Taste inspector and Python Playwright PNG helper were not executed. Full audit completion still requires the upstream workflow's evidence, independent reviewers and applicable execution controls.

Reproduce with `python plugin/verify_bundle.py --with-example --report .local/verification.json` and the prerequisites in the installation guide. Raw local logs remain outside Git because they contain environment-specific paths.
