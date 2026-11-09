---
name: superpowers
description: Use for disciplined software implementation with planning, TDD, root-cause debugging, code review and evidence-based completion, or when the user requests the bundled Superpowers workflows. Includes sequential and supported subagent execution; reuse accepted requirements and existing UI design.
license: MIT; see LICENSE.
---

# Superpowers — bundled development workflows

This is an adapted, pinned Superpowers 7.0.2 suite, not the upstream auto-bootstrap plugin. Read [compatibility and scope](references/compatibility.md), then only the relevant profile below. There are 15 profiles behind this one discoverable entry. Profiles are `GUIDE.md` files so hosts do not auto-load an additional global `using-superpowers` entry. The upstream body, supporting references, prompts and helpers are retained with documented adaptations.

For an approved task, continue from the unresolved work. For a bug, investigate the cause and reproduce it, fix it, and verify. For an accepted plan, execute it directly; choose sequential execution if the host lacks subagents. For new product decisions, use brainstorming, then a plan sized to the task. [The lifecycle router](../devflow/SKILL.md) owns reference discovery, specifications, mock/reverse and acceptance; Superpowers supplies the engineering steps within that lifecycle. [Ponytail](../ponytail/SKILL.md) keeps the implementation focused, and the [shared UI policy](../devflow/references/ui-task-policy.md) keeps UI scope and brand intact.

| Profile | When to load |
|---|---|
| [using-superpowers](upstream/skills/using-superpowers/GUIDE.md) | How the suite selects relevant workflows; use the bundle capability rules below. |
| [brainstorming](upstream/skills/brainstorming/GUIDE.md) | Clarify unresolved product/design decisions; reuse accepted requirements. |
| [writing-plans](upstream/skills/writing-plans/GUIDE.md) | Break an accepted design into verifiable implementation tasks. |
| [executing-plans](upstream/skills/executing-plans/GUIDE.md) | Execute an accepted plan sequentially; also the no-subagent fallback. |
| [subagent-driven-development](upstream/skills/subagent-driven-development/GUIDE.md) | Delegate implementation/review when supported and appropriate. |
| [dispatching-parallel-agents](upstream/skills/dispatching-parallel-agents/GUIDE.md) | Independent investigations with no shared mutable work. |
| [test-driven-development](upstream/skills/test-driven-development/GUIDE.md) | Reproduce meaningful behavior/bugs, then verify the correction. |
| [systematic-debugging](upstream/skills/systematic-debugging/GUIDE.md) | Find the root cause before changing code. |
| [requesting-code-review](upstream/skills/requesting-code-review/GUIDE.md) | Review a concrete change with sufficient code and evidence. |
| [receiving-code-review](upstream/skills/receiving-code-review/GUIDE.md) | Check feedback against requirements and reproduce findings. |
| [verification-before-completion](upstream/skills/verification-before-completion/GUIDE.md) | Run relevant checks before claiming success. |
| [using-git-worktrees](upstream/skills/using-git-worktrees/GUIDE.md) | Isolate work when needed, preserving current user work. |
| [finishing-a-development-branch](upstream/skills/finishing-a-development-branch/GUIDE.md) | Prepare tested changes for the authorized delivery action. |
| [writing-skills](upstream/skills/writing-skills/GUIDE.md) | Create or refine skill instructions using realistic scenarios. |
| [diagnosing-superpowers](upstream/skills/diagnosing-superpowers/GUIDE.md) | Requested session diagnosis using scoped evidence; no automatic transcript export. |

Resolve `superpowers:<profile>` mentions by this table even if the host has no Skill tool. Read the linked file directly. Never substitute an older personal copy just because its name matches. Explicit use: ask the installed `superpowers` entry to apply `systematic-debugging`, or ask the outer `devflow` router to use Superpowers for the accepted task. Actual skill names/prefixes depend on discovery.

Helper prerequisites are optional for reading: Bash + Git/POSIX tools for plan helpers, Node for the visual companion, Graphviz for diagram rendering. See [execution boundaries and portable commands](references/compatibility.md). Installation starts no server, injects no hook and edits no account configuration. Missing capabilities must be reported, never simulated as a successful run.
