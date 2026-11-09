# 0.7.1 — Independent repository maintained by chinhkrb113

- Extracted the self-contained skill bundle into https://github.com/chinhkrb113/devflow-kit, with a dedicated Git history, README and packaging script.
- Updated package author/marketplace owner and project URLs; preserved original copyright notices, source pins, vendor licenses and modification history.
- Retained all eight components, fifteen Superpowers profiles, installers and regression tests. The catalog remains an external source; the website, MCP service and catalog refresh workflows are not part of this repository.

# 0.7.0 — DevFlow Kit — AI Development Skills

- Renamed the bundle/plugin/marketplace to `devflow-kit`, portable entry and lifecycle router to `devflow`, and portable ZIP root to `devflow/`.
- Synced component links, UI metadata, installers, verifier, manifest format, documentation generator and current installation instructions. Original upstream names, licenses, source URLs and historical release notes remain factual.
- Added migration guards for known old names in the selected discovery root; existing content is preserved. See INSTALL.md for backup, migration and rollback.
- Preserved all eight components, fifteen Superpowers profiles and focused UI behavior. Refreshed distributed hashes separately from upstream provenance.

# 0.6.0 — Superpowers development workflows

- Added Superpowers 7.0.2 at commit `22f0b463e7a5e579904dd6211a520321035526f7`: all 15 profile bodies, references, prompts, runtime helpers and MIT license.
- Added one scoped `superpowers` entry with on-demand GUIDE.md profiles, preserving sibling resources while avoiding global bootstrap duplication. Original hooks/installers are omitted and no user config is edited.
- Integrated accepted-plan reuse, focused UI scope, sequential fallback, review/evidence boundaries and existing Ponytail guidance.
- Adapted two helper calls to Bash after ZIP extraction, made the renderer accept GUIDE.md, disabled companion remote branding telemetry, and fixed ephemeral-port URLs to use the actual bound port.
- Updated installer component counting, eight-entry legacy install, docs/provenance and helper regression checks. Harness discovery/model execution and cross-platform limitations remain separately reported.

# 0.5.1 — M1 integrity and consistent UI routing

- Installer checks and archive verification now reject unexpected files and linked paths, including hidden/cache/evidence directories; no files are deleted or overwritten.
- Explicit runtime exceptions cover the default verification report, flat demo evidence files, the five named UI-state outputs in `evidence/ui-redesign/`, and Python bytecode caches. All other output belongs outside the installation. Use a separate project/dependency directory for experiments. Integrity is checked again after tests.
- All four UI entries and the router use one task policy: preserve accepted brand/stack, separate focused fixes from new screens/redesigns, and distinguish aesthetic lint from functional acceptance.
- Taste now has a compact entry; its full upstream workflow is retained as an on-demand reference. Small fixes skip full app chapters, new design-system generation, draws and image work.
- Updated quick starts, installation/evidence boundaries, vendor adaptation records and regression coverage. This release does not add authenticated DSH/Trae/Claude or non-Windows runtime proof.

# 0.5.0 — portable harness delivery

- Added a standard outer `reverse-engineered` entry containing all seven components with preserved relative resource paths, source pins and licenses.
- Added a cross-platform Python copy installer for Codex, Claude Code, DeepSeek Harness, Trae/Trae CN and documented custom skills roots, with dry-run/check, no overwrite and integrity checks.
- Added a no-installer manual copy path, portable upload layout and a guidance-only mode for AI without filesystem/shell/browser tools.
- Kept legacy seven-entry plugin packaging available with `--format plugin`; default release packaging now produces the self-contained portable archive.
- Added copy/idempotence/conflict/source-integrity/resource-independence regressions. Native discovery/model execution is reported separately from filesystem installation and format checks.

# 0.4.0 — focused coding, concise replies and Uizze UI Taste

- Added pinned Ponytail and Caveman core skills with their licenses and documented compatibility edits. No proxy, hooks, global mode or companion suite is installed.
- Added the complete hosted UI Taste package (26 files), verified against its upstream checksums, with licenses, notices and provenance. Hosted snapshots use content hashes, not a fabricated Git revision.
- Coordinated four UI skills around one accepted design. Distinguished target images, interactive mocks, rendered evidence and native-device verification; optional Uizze MCP does not block local work.
- Expanded installation to seven skills and regression checks to cover missing/stale evidence and the browser/native boundary. The example remains a web appointment demo, not evidence of native iOS execution.

# 0.3.0 — lessons from the interactive appointment sample

- Added reusable checks for identity/draft ownership, invalid prerequisites, reset during mutation, stale async responses, corrected-error summaries and keyboard focus after rerender.
- Added actual viewport/overflow/contrast inspection and requirement-based assertions, rather than tests tied to old visual colors.
- Required final acceptance runners to invoke new suites and identify the delivered source revision; missing dependencies/skips cannot silently mean full pass.
- Added distribution verification from an extracted archive, a Vietnamese quick start and a clean runnable appointment example with backend/browser/recovery tests.
- Kept the three upstream UI skills pinned at the same revisions and hashes as 0.2.0. Lessons belong to the integration workflow; they do not alter upstream assets or impose the sample's brand/layout on other projects.

Observed sample failures were reproduced and fixed before these rules were written. Instruction scenario reviews, archive/helper tests, Codex discovery/activation and live example execution remain separate verification claims. See the release verification report accompanying the ZIP for the actual results and tested platform.
