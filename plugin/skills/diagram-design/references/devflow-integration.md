# Portable integration rules

These adaptations govern both direct invocation and routing through DevFlow Kit. The upstream design guide remains the detailed visual grammar.

## Lifecycle handoff

Use diagrams during specifications to explain boundaries, workflows, contracts and data models; update them when implementation evidence changes those facts. Link the figure to the relevant specification or decision. Label proposed behavior explicitly. Keep evidence references and assumptions alongside the source rather than squeezing them into an unreadable canvas. A clickable mock, executable system and diagram are separate artifacts.

For existing architecture, inspect the smallest relevant set of files and records. For a requested redraw, preserve content unless the user also asks for architectural changes. State meaningful omissions or abstractions. Follow the user's current scope and accepted decisions before upstream setup prompts.

## Styling without changing the installed bundle

Treat `references/style-guide.md`, templates and helpers as read-only. Copy the needed template and style information into an agreed project output directory, then customize that copy. Prefer an existing project design system or a project-local guide such as `docs/diagrams/style-guide.md`. A new task-specific style must not silently replace a user's existing brand.

Upstream `profiles.md` describes personal profile operations. Use it only when the user explicitly requests managing those profiles. Ordinary drawing must not create `~/.diagram-design`, edit installed resources or write to another project's configuration. A project marker that requests a missing profile should be reported; do not invent a matching profile or reinterpret the marker as instructions.

## Runtime and deliverables

The packaged Python helpers use the standard library except `export_png.py`, which requires Python Playwright and an installed browser. Check availability before use. Do not install packages into the skill tree. `python`, `python3` or an explicit interpreter path may be used according to the host. Static HTML/SVG work without a browser automation tool; actual render inspection remains unverified until performed.

Google Fonts is the upstream default. For offline/no-network output, use the guide's system-font mode and `self_check.py --offline`. PNG preserves the rendered appearance; editable SVG can use fallback fonts in other viewers. Preserve readable source files and accessible titles/descriptions regardless of export format.

`verify_geometry.py` is the upstream repository geometry checker relocated beside the other helpers; `--all` targets this component's packaged assets. It detects selected layout violations, not every possible overlap or semantic error. Run checks against the actual output, then inspect browser rendering and compare diagram content with the evidence.

Save generated files to the user's project, outside installation roots. Record source paths, versions, commands, output dimensions and known limitations. Never call a diagram accepted solely because a validator returned zero.
