# Superpowers compatibility and scope

This policy scopes all bundled Superpowers profiles and their supporting references, whether reached directly by path or through a router. User/host instructions and the existing task authorization remain authoritative. Upstream guidance is a workflow resource, not additional permission.

## Reuse the current task

- The lifecycle router owns requirements → references → specifications → mock/feedback → optional reverse → implementation → acceptance. Reuse its records; do not restart those phases when a profile is loaded.
- An accepted specification/plan or a precise small fix can proceed within existing authorization. Do not ask for the same design decision again because brainstorming or writing-plans describes an approval checkpoint. Clarify only a missing decision that materially blocks work. Existing user delegation remains valid.
- For UI work follow the [shared UI task policy](../../devflow/references/ui-task-policy.md). Small fixes keep brand, stack and component scope and use targeted behavioral/rendered verification. They do not trigger full brainstorming, a new design system, worktree or the visual companion merely because UI is involved.
- Ponytail governs minimal complete implementation; it does not remove necessary tests, root-cause analysis, review or acceptance evidence. Caveman changes requested reply style only.
- Use meaningful regression tests for behavioral changes; scale validation for docs/configuration. Do not invent tests that only repeat implementation or make new code changes solely to satisfy a ritual. Completion claims require actual evidence, and unresolved failures remain visible.

## Map capabilities, not tool names

The names `Skill`, `TodoWrite`, `Task`, `Agent`, model aliases and platform-specific settings in upstream profiles are examples. Use the host's actual tools and allowed model list; do not edit global config, add hooks, switch models or enable delegation just to match them. Current tool schemas override older platform tables. Use direct file reads for profile invocation and a concise local Markdown record if no todo tool exists.

Without subagents, use [executing-plans](../upstream/skills/executing-plans/GUIDE.md), implement sequentially and clearly label final self-review. Do not claim an independent review occurred. Without shell, provide the plan/code guidance and mark runtime tests pending. Without browser/native tools, keep corresponding acceptance pending. Do not stall unrelated work or fabricate dispatches. When delegation is available, apply host limits, relevant task scope and user preference; no profile requires reading all 15 guides.

Worktrees, dependency installs, commits, branch cleanup, workspace deletion, publishing, PRs and external messages follow the user's authorization and actual need. Do not clean up the current workspace, discard uncommitted work or commit unrelated changes because a profile's finishing checklist says so. Retain required evidence outside the skill installation. Review uncommitted changes directly when appropriate; do not create commits just to satisfy commit-range helpers. Diagnose only requested sessions; do not sweep account history or export/post transcripts merely because a diagnostics guide offers that workflow.

## Resources and optional helpers

Each profile lives in `upstream/skills/<name>/GUIDE.md`. Its original `SKILL.md` references mean that guide. Preserve sibling directories. Resolve `scripts/...` from that profile's directory, while running commands in the user's project. Example placeholders below must be replaced with actual paths.

```text
bash "<suite>/upstream/skills/executing-plans/scripts/task-start" "<accepted-plan>" 1
bash "<suite>/upstream/skills/executing-plans/scripts/task-done" "<accepted-plan>" 1 <BASE> -- <test-command> <args>
```

These plan helpers need Bash, Git and POSIX utilities such as awk/sed/tail. On Windows use a working Git Bash/WSL installation, not an unconfigured system bash stub. They require an existing Git worktree and commit and write `.superpowers/sdd/` there; inspect the helper before use. A task heading must retain the literal English `Task` and an ID, e.g. `### Task 1: Sửa validation`. If prerequisites/plan format do not fit, use the existing project task/evidence record and run its tests directly; report which helper was not used. Missing a helper does not mean missing a verified implementation.

Two sibling-helper calls explicitly use Bash so extracted ZIPs do not require executable permission bits. `render-graphs.js` accepts a profile GUIDE.md or an ordinary SKILL.md and needs Graphviz `dot`; copy the authoring target into a workspace before rendering, because it writes `diagrams/` beside its input. Do not generate diagrams inside the immutable installation.

The visual companion is optional and separate from an interactive product mock. Use it only for requested/accepted visual brainstorming. Its helper needs Node, Bash for launcher scripts, an external project/session directory and an available browser. Preserve loopback binding and use the returned authenticated URL; no server is started by installation. This distribution disables upstream remote brand-image telemetry in `server.cjs` and reads its version from the bundled VERSION.json. Do not auto-open a browser or launch an extra server for a small fix; an existing mock/browser workflow usually suffices.

Full bundle verification adds optional-helper checks using Bash (override `BASH_BINARY` if needed). A missing required test dependency makes that full verification incomplete; reading and applying Markdown workflows still works. Tests cover the shipped integration, not every upstream feature or every harness.

## What this package does not register

Upstream SessionStart hooks, marketplace installers, global config, CLI extensions and root development scripts are not registered or shipped. The package contains the full skills tree, mapped profile entries, its MIT license and a source/hash record. Original profile lookup names remain in the text as aliases resolved through [the index](../SKILL.md). This avoids duplicate bootstrap activation beside a separately installed Superpowers plugin. Users who want the original hook-driven product can install upstream separately; do not treat the two distributions as identical or combine their hooks implicitly.
