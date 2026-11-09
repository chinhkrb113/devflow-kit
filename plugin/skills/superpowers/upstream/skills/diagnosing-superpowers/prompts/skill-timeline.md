Read `prompts/analyst-common.md` first; it gives your role, inputs,
context-safety rules, and the return format. This file adds the dimension.

Dimension: Skill timeline

Bundle adaptation: for a DevFlow Kit Superpowers installation, locate
`<suite-root>/profiles.json` from the case's verified install root. It maps profile
names to `upstream/skills/<name>/GUIDE.md`. Use that inventory and the suite's
`references/compatibility.md` when interpreting trigger scope. A GUIDE.md read
is a profile read, not evidence of a native Skill-tool invocation or execution.
For an original upstream installation retain its SKILL.md inventory instead.
Do not substitute a personal installation or assume bootstrap hooks ran.

Build the per-human-turn record of skill and plugin use, then look for gaps.

1. List the human prompts with line numbers and timestamps.
2. Using the skill-invocation and attribution meanings established in the case
   file, list every explicit invocation, active-skill attribution, or read of a
   file named `SKILL.md` or a `GUIDE.md` mapped by the installed profiles.json.
   Record the line, the skill/profile name, and the human turn it
   happened in.
3. List every non-superpowers plugin, skill, agent type, MCP server, or
   hook used. Use only the evidenced tool, attribution, agent-dispatch, MCP,
   and hook meanings recorded in the case file; identify values associated
   with something other than `superpowers`.
4. For each human turn, compare the request text against the trigger
   descriptions of the superpowers skills installed (read
   the profile files from profiles.json for this bundle, or
   `<install root>/skills/*/SKILL.md` for original upstream installations;
   inspect their frontmatter `description` lines and the applicable scope policy).
   The install root is in the case file. Report as findings:
   - a skill invoked, with the request that preceded it (one finding per
     invocation is fine when there are few; group by skill when many);
   - a turn whose request matches a skill's trigger description with no
     invocation in that turn (state which description matched and quote
     the request);
   - a skill invoked one or more turns after the matching request (late);
   - each non-superpowers plugin/skill/tool used, with where.

Do not say whether a missed or late trigger was wrong. Report the match
and the absence; the reader decides.
