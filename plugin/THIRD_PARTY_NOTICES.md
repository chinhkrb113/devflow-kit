# Bundled third-party skills

DevFlow Kit is assembled and maintained by [chinhkrb113](https://github.com/chinhkrb113/devflow-kit). This identifies the bundle maintainer, not authorship of all included third-party work. Original author and license notices remain in their respective files.

DevFlow Kit includes a lifecycle router derived from the original reverse-engineered skill under the root [MIT license](LICENSE), plus the components below. Their licenses remain applicable to their respective files; the bundle is not entirely MIT. Exact revisions, packaged file hashes and local adaptations are recorded in [third-party-skills.lock.json](third-party-skills.lock.json).

| Component | Upstream | License | Included scope |
|---|---|---|---|
| frontend-design | [Anthropic skills](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5/skills/frontend-design) | [Apache-2.0](skills/frontend-design/LICENSE.txt) | SKILL.md with bundle task-policy adaptation; license unchanged. |
| ui-ux-pro-max | [NextLevelBuilder](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/713eef51b04efc98d6fa565323b495f7c9c89fd4/.claude/skills/ui-ux-pro-max) | [MIT](skills/ui-ux-pro-max/LICENSE), Copyright (c) 2024 NextLevelBuilder | Skill, Python runtime scripts, local datasets and references. Repository-dependent upstream tests omitted. |
| design-taste-frontend | [Leonxlnx taste-skill](https://github.com/Leonxlnx/taste-skill/tree/12af471f627f866411b4bd785b19646d3672784c/skills/taste-skill) | [MIT](skills/taste-skill/LICENSE), Copyright (c) 2026 Leonxlnx | Complete skill directory, including libraries, helpers, references, assets and evaluation prompts. |

Local adaptation on 2026-11-03: UI/UX Pro Max's SKILL.md replaces Claude-specific script roots with a documented absolute-path placeholder, clarifies existing-project defaults and replaces a missing README pointer with interpreter fallback guidance. Python runtime code and datasets are unchanged. Repository-level MIT license files were copied alongside the two MIT skills. Bundle routing and installation documentation are maintained separately from upstream content.

Third-party image/font URLs and reference-site names in the datasets are references, not copied media or an endorsement. Their inclusion does not transfer rights to external assets. Anthropic repository tools such as FFmpeg and imageio are not included in this frontend-design-only package.
# Sources added in 0.4.0

- **Ponytail**, Dietrich Gebert: [upstream](https://github.com/DietrichGebert/ponytail), commit `96608e078b2d5ea607c5c3b8b5a54d1c1fba6846`, core `skills/ponytail`, [MIT license](skills/ponytail/LICENSE). Added a scoped activation/workflow note; upstream license copied into the standalone folder.
- **Caveman**, Julius Brussee: [upstream](https://github.com/JuliusBrussee/caveman), commit `2e068f735253cce28256744804785f01887d9646`, core `skills/caveman`, [Apache-2.0 license](skills/caveman/LICENSE). Added a compatibility note and clarified unavailable ultra/wenyan companion skills. No proxy, hooks or other repository tooling included. The current upstream repository uses Apache-2.0; an older MIT license file is not substituted for it. Names do not imply endorsement.
- **UI Taste by Uizze**: complete 26-file hosted snapshot from [official distribution](https://uizze.sh/.well-known/skills/ui-taste/SKILL.md), retrieved 2026-11-04, manifest version `uizze-design-v14`. The original 0.4.0 snapshot was unmodified; 0.5.1 adds a task-policy adapter to SKILL.md. [License](skills/ui-taste/LICENSE), [NOTICE](skills/ui-taste/NOTICE), [upstream modifications](skills/ui-taste/MODIFICATIONS.md) and [source manifest](skills/ui-taste/MANIFEST.json) are retained, including Apache-2.0/MIT notices for Impeccable, Platform Design Skills and Appllama. Exact snapshot and file hashes are in the lock; the design-stack Git commit is not misrepresented as the hosted package revision.

The lock schema v2 accepts either a Git revision or a hosted content snapshot. Linked external images, paid materials and MCP services are not redistributed or licensed by this bundle.

Caveman also retains its [NOTICE](skills/caveman/NOTICE), historical [LICENSE-MIT](skills/caveman/LICENSE-MIT), and [licensing explanation](skills/caveman/LICENSING.md). These preserve the original contributions' notices alongside the current Apache-2.0 license. The full upstream NOTICE mentions engine, CLI, browser tooling, binaries and fonts; none of those components is shipped in this core-skill bundle.


# Local adaptations in 0.5.1 (2026-11-04)

The four UI entry points now link to one shared task policy for scope, accepted design and focused fixes. Taste's original body is preserved in `skills/taste-skill/references/full-workflow.md`, behind a compact entry; resource paths there remain relative to the skill root. Runtime scripts, datasets and licenses are unchanged.

Uizze's `CHECKSUMS.sha256` and `MANIFEST.json` are retained as upstream provenance, not checksums of the locally adapted entry. The lock records its original `SKILL.md` hash in `upstream_sha256` and hashes every distributed file in `sha256`. Its `snapshot_sha256` describes the adapted distribution; `upstream_snapshot_sha256` preserves the prior hosted snapshot aggregate. Tests verify unchanged files against upstream checksums and adapted files against the lock.

# Superpowers added in 0.6.0

[obra/superpowers](https://github.com/obra/superpowers/tree/22f0b463e7a5e579904dd6211a520321035526f7), version 7.0.2, copyright (c) 2025 Jesse Vincent, [MIT license](skills/superpowers/LICENSE). Retrieved 2026-11-05. Includes the complete `skills/` runtime tree, with 15 entry files renamed to GUIDE.md and a local task/capability adapter, index and VERSION.json. The original skill bodies remain below the marked adapter notes; resource directory relationships are preserved.

Local helper changes: task-start/task-done invoke sibling helpers through Bash; graph rendering accepts GUIDE.md or SKILL.md; the visual companion disables remote brand-image telemetry, reads VERSION.json and reports the actual bound ephemeral port. The diagnostics timeline prompt recognizes mapped GUIDE.md reads and profiles.json inventory while retaining original SKILL.md support. Hooks, harness plugin manifests/installers, root developer tooling and upstream repository test harnesses are omitted. No claim of an unchanged upstream plugin or its automatic bootstrap behavior is made. The lock contains original source hashes and all distributed file hashes; local tests cover the integration.

For Superpowers, `upstream_sha256` hashes the original Git blobs at the pinned revision. `upstream_checkout_sha256` records the retrieved working-tree bytes; ten files differ only in line endings, listed in `checkout_line_ending_differences`. `sha256` always hashes the actual distributed bytes after documented adaptations. This distinction makes the source pin reproducible across checkout platforms.

## Diagram Design

- Source: https://github.com/cathrynlavery/diagram-design
- Revision: `6a7f19fcc132b39b126bea90167679b46b14bcc4`; source directory `skills/diagram-design`, plus the repository geometry verifier.
- License: MIT; original notice is included in `skills/diagram-design/LICENSE`.
- Adaptations: compact DevFlow entry, upstream body retained as `GUIDE.md`, project-local styling and host capability rules, geometry helper relocation and corrected local assets root. See the component `NOTICE` and lock record.
- Upstream Git-blob SHA-256 and distributed SHA-256 are distinct; the project's customized documentation style is not substituted for the upstream default.

## Open Code Review

Source: https://github.com/alibaba/open-code-review at `04deca6721ec4fe2f74a6a0eb069d2a01b3d31cb`. Apache-2.0 license retained. Both upstream skill guides are preserved as references behind one adapted entry. The executable, providers, extensions and CI examples are not included. See the component NOTICE and provenance lock.

## Security Audit

Source: https://github.com/cloudflare/security-audit-skill at `c1c8a8c1471069fb0e188eeaff69b8e8db6564a8`. MIT license retained. The original guide, companions, schema, validators and tests are included. The bundle adds a compact entry and trusted-parent stdin transport, exposes the existing findings text preflight and marks seven POSIX-dependent test prerequisites. The original file-input protection is unchanged. See the component NOTICE for detail.
