# DevFlow Kit — Installation

Version 0.9.0 provides a portable self-contained `devflow` entry for Codex, Claude Code, DeepSeek Harness, Trae and generic Agent Skills hosts. From the portable ZIP root, follow `START-HERE.md` and run `python bundle/install.py --target <harness> --project <existing-project>`. It copies all eleven components without symlinks or personal-configuration edits. See [compatibility and evidence boundaries](HARNESS-COMPATIBILITY.md). The eleven-entry plugin/junction installation below remains a legacy alternative; do not mix both forms unless duplicate discovery is intended.

The bundle contains eleven components: the reference-led workflow, Frontend Design, UI/UX Pro Max, Taste (`design-taste-frontend`), Ponytail, Caveman, UI Taste (`ui-taste`, Uizze), Superpowers (15 workflow profiles), Diagram Design (architecture and technical visuals), Open Code Review, and Security Audit. Keep the entire `plugin` directory together: the workflow resolves the four UI skills as siblings, and their scripts read adjacent data, libraries and assets.

Start with the Vietnamese [quick start](BAT-DAU.md). On Windows, open a terminal in the extracted `plugin` directory:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\install-codex.ps1
```

For a downloaded archive, extract it to a permanent directory and run `install-codex.ps1` from the extracted `plugin` directory. The installer adds directory junctions under `~/.agents/skills`, points them at this bundle and refuses to overwrite conflicting entries. It skips a skill already linked to the same source. Keep that source directory in place. Personal skills under `~/.codex/skills` remain untouched.

On macOS/Linux, create directory symlinks under `~/.agents/skills` to each of the eleven folders in `plugin/skills`, using distinct link names such as `devflow-kit-frontend-design`. Inspect existing entries first; do not overwrite another installation or create a duplicate link to the same source. Preserve the enclosing bundle directory for sibling references and plugin namespacing.

From the extracted `plugin` directory on macOS/Linux (instructions supplied, not execution-tested in this Windows release):

```sh
bundle_dir="$PWD"
bundle_skills='devflow frontend-design ui-ux-pro-max taste-skill ponytail caveman ui-taste superpowers diagram-design open-code-review security-audit'
mkdir -p "$HOME/.agents/skills"
for skill in $bundle_skills; do
  destination="$HOME/.agents/skills/devflow-kit-$skill"
  if [ -e "$destination" ] || [ -L "$destination" ]; then
    printf 'Inspect existing entry before installing: %s\n' "$destination" >&2
    exit 1
  fi
done
for skill in $bundle_skills; do
  ln -s "$bundle_dir/skills/$skill" "$HOME/.agents/skills/devflow-kit-$skill"
done
```

The preflight refuses any existing destination, including a dangling symlink, before creating links. Do not remove this guard or add a force flag: plain `ln -s` can otherwise create a nested link inside an existing directory.

## Updating or removing an installation

For a portable copy, run the **new release's** `install.py --check` with the original target/project arguments. It checks expected bytes and the complete file inventory. Missing/changed/extra files or linked directories fail with exit 2; checks never remove user files. To upgrade, preserve the old installation outside the harness discovery root, then install the new version into an empty destination. Do not merge versions. Keep legacy links separate from portable copies.

In an extracted/installed bundle, runtime exceptions are limited to `verification-report.json`, flat `examples/appointment-demo/evidence/*.{json,log,png,webm,mp4}` files, and Python `.pyc` files directly under `__pycache__` directories. These generated files are not release-hashed or trusted proof of execution. Arbitrary `SKILL.md`, scripts, `.git`, `node_modules` and `.taste-skill` outputs are not exempt. Put custom reports, generated design artifacts and dependencies outside the installation; use `--report` and `--playwright-module` with external paths. A source checkout has no release manifest, so its archive inventory is not certified until packaging/extraction.

The sample's UI-state suite also writes these exact nested outputs under `examples/appointment-demo/evidence/ui-redesign/`: `ui-states.json`, `mock-320.png`, `mock-390.png`, `mock-768.png`, and `mock-1440.png`. These five names are allowed; arbitrary nested files remain rejected. The verifier rechecks integrity after running the suites.

Do not move the source while its junctions/symlinks are in use. For a new extracted version, first inspect the existing link and its target. Remove only a verified junction/symlink that you intend to replace, then run the new installer. Never recursively delete the skills root or the linked source directory.

For one Windows link, replace the example name deliberately; this command refuses a regular folder:

```powershell
$skillLink = Get-Item -LiteralPath (Join-Path $env:USERPROFILE '.agents\skills\devflow-kit-frontend-design') -Force
$skillLink | Select-Object FullName, LinkType, Target
# After verifying the displayed path/target belongs to the installation being removed:
if ($skillLink.LinkType -ne 'Junction') { throw 'Expected a junction; leave this entry untouched.' }
[System.IO.Directory]::Delete($skillLink.FullName)
```

This is non-recursive removal of that junction. Repeat only for the other verified bundle links. A standalone linked lifecycle skill may use `devflow` without the prefix; inspect actual discovery rather than guessing. On macOS/Linux inspect `readlink` and remove only the intended symlink with `unlink`.

Python 3 is needed for UI/UX Pro Max's local search. Use Node.js 22+ for the complete Taste toolset, including browser inspection; draw/lint alone support Node.js 18+. Frontend Design itself has no script dependencies. Taste's browser inspection also needs Chrome/Edge/Chromium; remote asset retrieval needs network access. Installing the bundle does not install a product framework or browser.

## Use and verify

The current plugin exposes `devflow-kit:ponytail`, `devflow-kit:caveman` and `devflow-kit:ui-taste` on hosts that use the plugin prefix. Ponytail contributes focused implementation guidance; Caveman is a requested concise voice and is not activated merely by installation. Uizze UI Taste supplies local web/iOS playbooks and an optional Node evidence-integrity checker. Its paid MCP is not installed or required. The core Ponytail/Caveman skills are included; their separate companion skills, proxy and hooks are not. See [coding and communication](skills/devflow/references/coding-communication.md).

Start a fresh Codex turn/session and inspect discovery. Hosts that namespace plugin entries may return `devflow-kit:devflow`, `devflow-kit:frontend-design`, `devflow-kit:ui-ux-pro-max` and `devflow-kit:design-taste-frontend`. Match the returned name and source path rather than assuming every host adds the same prefix. See [discovery checks](skills/devflow/references/codex.md).

Example: `$devflow-kit:devflow Build an interactive appointment admin mock using the bundled UI skills, keeping our existing brand and HTML stack.`

The workflow's [UI guide](skills/devflow/references/ui-workflow.md) assigns UX research, visual implementation and Taste critique to one shared design decision. Existing brand and user requirements take precedence over generic style defaults. Mock interaction, real backend behavior and human acceptance remain separate checks.

Use Python 3.12+ and run `python verify_bundle.py` from this directory for package and catalog-helper checks. Use `--node` when Node is not on PATH; add `--with-example` after installing the optional Playwright dependency as described in the [sample README](examples/appointment-demo/README.md). Missing prerequisites/skipped required tests are incomplete, not full success. The release manifest hashes packaged files; verification outputs are generated separately. See [third-party notices](THIRD_PARTY_NOTICES.md) and the revision/hash lock before updating vendored sources. Update intentionally from a pinned revision; rerunning an unpinned upstream installer can discard this integration.

## Superpowers 7.0.2 integration

Since version 0.6.0 the bundle includes [the Superpowers suite](skills/superpowers/SKILL.md), pinned at `22f0b463e7a5e579904dd6211a520321035526f7`. Its 15 original skill bodies are shipped as on-demand `GUIDE.md` profiles with sibling resources. One scoped entry is discoverable; there are eleven bundle components, with internal profiles loaded on demand. The original SessionStart hooks, marketplace installers and global configuration are not installed. This is an adapted distribution, not the upstream plugin.

Use the detected `superpowers` entry or ask `devflow` to apply a named profile such as `systematic-debugging`. With no Skill tool, read the entry and linked profile directly. Read the [capability and scope policy](skills/superpowers/references/compatibility.md) for sequential fallback, accepted-plan reuse, optional Bash/Node/Graphviz helpers, output paths and disabled companion telemetry. Full helper verification also needs a working Bash/POSIX tool environment (Git Bash on Windows, `BASH_BINARY` override available).

## Upgrade from reverse-engineered (0.6.x and earlier)

DevFlow Kit is the bundle name (`devflow-kit`); the callable skill and installed portable directory are `devflow`. The portable ZIP is `devflow-kit-v0.9.0.zip`, with outer directory `devflow/`. Plugin discovery may expose `devflow-kit:devflow` and `devflow-kit:<component>` instead of the short names. Resolve the name and path actually returned by your harness.

Before upgrading, inspect project and user discovery roots for `reverse-engineered`, `find-reverse-engineered`, or `reverse-engineered-*` entries. Back up the exact old bundle outside all discovery roots. For junctions/symlinks, inspect and remove only the verified link, preserving its target and other personal skills. Do not merge versions, rename an old manifest to fake an upgrade, or recursively delete a link target. Install the new capsule into the empty `devflow` destination, run `--check`, and refresh discovery in a new session. The installers reject old names in the selected skills root without changing them; they cannot detect disabled/remote installations or every other root.

To roll back, archive the new capsule outside discovery and restore the intact old installation with its original folder structure. Repository/catalog URLs, the catalog cache `~/.cache/awesome-reverse-engineered`, original authors, licenses and upstream revision hashes retain their factual identities. DevFlow Kit is maintained independently at https://github.com/chinhkrb113/devflow-kit; the original catalog repository is still the external data source. Skill workflow behavior and all eleven components / fifteen Superpowers profiles are retained.

## Review and security components (0.9.0)

Open Code Review and Security Audit bring the total to eleven components. OCR's CLI is an optional external dependency; the installer does not configure providers or install binaries. Host delegation needs Git and a compatible `ocr` command but no separate OCR model endpoint. Security guidance can be read on every host; complete audit claims still require independent verification and appropriate target-execution isolation.

Security JSON validation uses the original protected file readers where supported, or the bounded trusted-parent stdin adapter. Windows lacks the upstream Node file flags in the tested runtime; corresponding file tests are explicitly capability-skipped, while stdin and semantic checks run. This transport does not weaken sandbox or retained-artifact requirements. See [review coordination](skills/devflow/references/review-security.md), [OCR runtime](skills/open-code-review/references/compatibility.md) and [security runtime](skills/security-audit/references/compatibility.md).
