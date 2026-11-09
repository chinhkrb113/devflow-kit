# DevFlow Kit — Harness compatibility

Adapter source review: 2026-11-04. Branding revision: 2026-11-09; Independent repository revision: 0.7.1; Diagram Design integration: 0.8.0 (2026-11-10). See the repository verification report for checks performed after extraction.

The portable delivery uses one standard `devflow/SKILL.md` with all nine components and their resources inside `bundle/`. A successful copy is not proof that a host discovers or executes the skill. Scripts are optional capabilities, not prerequisites for reading the guidance. User/host policy always controls tool use.

Version 0.7.0 renames the bundle to DevFlow Kit and its entry to `devflow`. Version 0.6.0 added the Superpowers suite behind one scoped entry and preserves existing harness adapters. Direct component discovery and the outer router share the same [UI task policy](skills/devflow/references/ui-task-policy.md). Keep the full capsule together; component-only copies lose sibling policy/resources. The release report distinguishes M1 execution evidence from historical discovery observations below.

| Target | Discovery location | Verification scope |
|---|---|---|
| Codex | Project/user `.agents/skills` | Release 0.5.1 discovery on 0.159.2 found the outer entry plus seven components; 0.6.0 adds Superpowers. See its release report for refreshed discovery evidence. Explicit fresh-session model execution is recorded separately in the release report. |
| Claude Code | Project/user `.claude/skills` | Copy adapter follows official documentation; local CLI is present but unauthenticated in this release environment. No authenticated model execution claimed. |
| DeepSeek Harness (DSH) | Project `.dsh/skills`, user `$DSH_HOME/skills` or `~/.dsh/skills` | Copy adapter follows the upstream filesystem provider; requires provider/registry/tool enabled. No DSH runtime execution claimed. |
| Trae / Trae CN | Project `.trae/skills`; user `.trae/skills` / `.trae-cn/skills` | Paths cross-checked against the Skills CLI's maintained Trae adapters. Trae documentation is client-rendered and not readable in this audit; no Trae runtime verification claimed. |
| Other Agent Skills hosts | Explicit `--target generic --skills-root ...` | Self-contained format; recipient must supply a documented directory and verify discovery. No guessed vendor path. |
| Claude.ai / upload-enabled AI | Portable ZIP containing `devflow/SKILL.md` (`name: devflow`) | Upload-compatible layout, not an actual account import test. Host limits, account access and code execution support still apply. |
| Plain chat / AI API | Attach or paste the entry and selected references | Guidance only unless the host supplies file reading and execution tools; no automatic install, activation or test claims. |

Source references used for the adapter design:

- [Agent Skills specification](https://agentskills.io/specification): root name matches folder, concise metadata, resource paths internal to the package.
- [Official Codex skill documentation](https://learn.chatgpt.com/docs/build-skills): local skills discovery roots and explicit invocation.
- [Claude Code skills](https://code.claude.com/docs/en/skills): local/project skills, supporting files, separate cloud/account behavior.
- [DeepSeek filesystem provider](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/skill-filesystem/README.md): default roots, configurable homes and provider requirements.
- [DeepSeek skill tool](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/skill/tool-skill/README.md): catalog loading and user/model invocation.
- [Skills CLI agent adapters](https://github.com/vercel-labs/skills/blob/main/src/agents.ts): maintained Trae and Trae CN directory mappings; this is installer-source evidence, not a native Trae execution test.
- [Trae skills documentation](https://docs.trae.ai/ide/skills): recipient-facing configuration reference.

The release report records actual tested OS/runtime versions. Windows execution does not establish macOS/Linux execution. Standard-library copy code avoids symlink privileges and machine-specific absolute paths; a recipient should still run the smoke test and relevant helper verification on their platform.

Existing component-entry installations remain available through the legacy plugin and `install-codex.ps1`. The portable route is additive and uses a different outer entry. Avoid installing both forms into the same working environment unnecessarily: hosts may display duplicate component names. In tests, match the resolved file path rather than a short skill name alone.

Superpowers profiles use local file links, not assumed plugin namespaces or a required Skill API. Sequential execution is supported when delegation is unavailable. Original hooks/configuration are not registered. Platform-specific tables remain reference material; actual host schemas, permissions, models and user scope win. Optional helper tests add Bash/POSIX dependencies, while Markdown reading does not. See [Superpowers compatibility](skills/superpowers/references/compatibility.md).
