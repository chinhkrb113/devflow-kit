---
name: devflow
description: Develop software from reference systems through requirements, specifications, interactive mock UI, optional reverse analysis, construction and acceptance. Also use for reference-tool discovery, frontend design or review, disciplined engineering with Superpowers, focused implementation with Ponytail, or requested concise replies with Caveman.
license: See bundle/THIRD_PARTY_NOTICES.md for component licenses.
compatibility: Requires a host that can read local Markdown and referenced files. Optional helpers need Python or Node; browser and native checks require the corresponding tools. Plain chat can provide guidance but cannot execute these checks.
---

# DevFlow Kit — AI Development Skills

This entry contains eight components in one self-contained skill; Superpowers contains 15 on-demand workflow profiles. Resolve all links relative to this installed SKILL.md, never relative to the project's working directory or another personal installation. Load only the component needed for the user's task:

| Task | Read |
|---|---|
| Requirements, reference lookup, complete lifecycle or continuing an existing project | [Lifecycle router](bundle/skills/devflow/SKILL.md) |
| Interactive mock, frontend construction or UI review | [UI coordination](bundle/skills/devflow/references/ui-workflow.md), then relevant component files |
| Coding, fixes or review with minimal complete changes | [Coding coordination](bundle/skills/devflow/references/coding-communication.md) and [Ponytail](bundle/skills/ponytail/SKILL.md) |
| Requested concise replies / Caveman | [Caveman](bundle/skills/caveman/SKILL.md); installation/auditing is not mode activation |
| Superpowers, implementation planning, TDD, debugging or evidence-based review | [Superpowers](bundle/skills/superpowers/SKILL.md), then its relevant profile; continue accepted work and preserve the focused UI route |

The UI components are [Frontend Design](bundle/skills/frontend-design/SKILL.md), [UI/UX Pro Max](bundle/skills/ui-ux-pro-max/SKILL.md), [Leonxlnx Taste](bundle/skills/taste-skill/SKILL.md), and [Uizze UI Taste](bundle/skills/ui-taste/SKILL.md). They share one accepted design, existing brand and actual stack. Direct calls and this router follow the same [UI task policy](bundle/skills/devflow/references/ui-task-policy.md); small fixes use its focused route, without restarting discovery or redesign. The lifecycle remains requirements → references → feasibility/specifications → interactive mock → feedback → optional reverse → implementation → verification/acceptance. Resume existing work; do not restart or ask for decisions already given.

## Adapt to this harness

Use the host's real file-reading, shell, browsing, image and test capabilities. No Codex-only API or special tool name is required. `${...}`, `<skill-root>` and sample paths in component examples must be resolved from the component's actual directory before execution; do not execute unresolved placeholders. Host policy and the user's scope take precedence. A slash command or `$skill` spelling is only an invocation convention, not a required tool or assumed global state.

Before a phase needs a capability, establish whether it is available. Missing web access means current external facts are unverified; missing shell means scripts were not run; missing browser means no interaction/visual pass; missing native runner means native acceptance is pending. Uizze MCP is optional. Read local guidance and continue independent work when a capability is absent, keeping dependent claims pending. Do not invent tool output or silently replace required checks with text advice.

AI chat without file access can use pasted instructions as guidance only. Ask for the specific referenced content needed; never pretend that inaccessible bundle files were loaded. A screenshot is not an interactive prototype, a mock is not a backend, and an evidence hash check is not visual inspection or owner approval.

For setup and portability checks, see [START-HERE.md](START-HERE.md). Core Caveman only is included, not its ultra/wenyan companion skills; installing this package sets up no proxy, hooks, paid services or deployment.
