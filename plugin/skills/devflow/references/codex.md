# Codex discovery and activation

For all nine components, use the bundle [installation guide](../../../INSTALL.md) and installer. Keep the enclosing bundle together for sibling links and runtime resources. The single-skill instructions below still apply when only the catalog/system workflow is wanted, but the integrated UI path needs its four UI siblings; implementation/communication guidance uses Ponytail/Caveman.

The skill's source under `plugin/skills/` is not automatically a repository skill. Plugin marketplace metadata alone does not install it into Codex. For local development, expose this folder through a supported discovery root; keep one active copy to avoid duplicate names and stale instructions.

Codex's documented local roots include `<repo>/.agents/skills/` and `~/.agents/skills/`. The runtime may also expose legacy `~/.codex/skills/` locations. Check the actual client/runtime rather than assuming that a directory name means it is installed.

For this Windows checkout, a directory junction avoids stale copied files (adjust the source path for another checkout):

```powershell
$source = (Resolve-Path -LiteralPath './plugin/skills/devflow').Path
$destination = Join-Path $env:USERPROFILE '.agents\skills\devflow'
if (Test-Path -LiteralPath $destination) { throw 'Inspect the existing installation; do not overwrite it.' }
New-Item -ItemType Directory -Force -Path (Split-Path $destination) | Out-Null
New-Item -ItemType Junction -Path $destination -Target $source
```

The checkout must remain present for the junction to work. A copied installation must include SKILL.md, agents/, references/ and scripts/ together and must be refreshed after source changes. Do not include generated caches. On systems supporting symbolic links, the same single-source arrangement can use a directory symlink.

## Verify the three separate claims

1. **Discovery:** ask the installed app-server's `skills/list` with the target `cwds` and `forceReload: true`. Match the intended resolved SKILL.md path and its returned name, with enabled=true and no load errors. Some runtimes prefix the name with the enclosing plugin, for example `devflow-kit:devflow`, even for a user-scope link. An exact comparison with the short name alone can falsely report absence. Confirm one active installation and read UI metadata through the runtime result when available. Do not infer discovery from filesystem existence.
2. **Explicit activation:** in a fresh Codex session, invoke the name returned by discovery (for example `$devflow-kit:devflow`) with a scoped task; test the short `$devflow` alias separately when relying on it. Observe full instructions/references being loaded and the correct branch selected. A response merely repeating the name is insufficient.
3. **Implicit activation:** repeat a reference-led task without the name/path. Observe whether Codex selects and reads the skill. Also use an unrelated request to detect over-triggering. Record actual prompt, runtime/model, read/tool events and outcome; selection is probabilistic, not guaranteed by one passing example.

Use a disposable project and read-only activation probes. `codex exec --ephemeral --json` can preserve an event trace in an explicitly chosen report file without persisting a normal session. A CLI result establishes that runtime's behavior; do not claim that it proves the Desktop skill picker or another host's behavior. If runtime/model compatibility prevents a model turn, record discovery separately from the failed activation attempt.

Installed skills should be available on the next turn/new session. If the selector remains stale, refresh discovery or restart the client; never claim the current already-loaded conversation has refreshed without checking. After editing the source, verify the loaded path/content and repeat affected activation cases.

Official references: [local discovery and activation](https://learn.chatgpt.com/docs/build-skills), [app-server skills/list](https://learn.chatgpt.com/docs/app-server), [skill evaluations](https://developers.openai.com/blog/eval-skills). Recheck runtime-specific schemas when commands or fields differ.
