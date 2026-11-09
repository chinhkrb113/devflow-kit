# Bundled UI skills

First read the [shared UI task policy](ui-task-policy.md). Direct component calls and this router use the same task classification, precedence and focused-fix route. For a small UI fix, follow that route and load only the relevant component guidance; the full workflow below is for broader UI work.

Use this branch for interactive prototypes and frontend construction. It complements the system workflow; backend-only tasks and catalog searches do not need these skills. Resolve the links below relative to this file and load the bundled copy, rather than an unrelated personal installation with the same short name.

| Skill | Role in this workflow |
|---|---|
| [UI/UX Pro Max](../../ui-ux-pro-max/SKILL.md) | Search relevant interaction, accessibility, responsive and existing-stack guidance; identify important screen states and constraints. |
| [Frontend Design](../../frontend-design/SKILL.md) | Develop the visual direction, typography, composition and implementation within the agreed brief. |
| [Taste](../../taste-skill/SKILL.md) (`design-taste-frontend`) | Explore compatible composition when needed and critique visual quality. Use its app-screen mode for dashboards, admin, tables and settings; use site mode for public/marketing pages. |
| [UI Taste by Uizze](../../ui-taste/SKILL.md) (`ui-taste`) | Apply the relevant web/iOS playbook, target-to-render comparison and evidence receipt. This is a different skill from Leonxlnx Taste above. Local playbooks work without an account or paid MCP. |

## One design decision, four complementary inputs

Inspect existing screens, brand tokens, components, stack and accepted decisions first. Record screen purpose, users, primary actions, important states and target viewports. Keep existing project conventions unless the requested redesign changes them. The user's requirements and brand, accessibility and working interactions take priority over a skill's default palette, font bans, animation, image quotas or framework recommendation. Do not install a UI framework or motion library merely because a reference mentions it.

1. Read the relevant UI/UX Pro Max rules and query its local data for the actual interface. Recommendations are candidates, not evidence that the result meets accessibility or product acceptance criteria. For an existing design system, search targeted UX/stack guidance instead of generating replacement colors and type.
2. Read Frontend Design and choose one coherent direction that fits the content and constraints. Keep a concise design record with tokens, components, layout, interaction and responsive behavior; reuse it through prototype and production.
3. Read Taste and its applicable references. For a new direction, its draw helper can supply candidates; reconcile them with the same design record rather than generating a second competing theme. For an established brand or approved mock, use the applicable critique guidance and preserve the accepted direction. When drawing, `--keep palette,type` preserves those brand decisions. For a full new design/redesign, app/admin screens use Taste's `references/app-screens.md` and `--app`; focused fixes skip that full chapter and new screens reuse the accepted direction; do not apply landing-page photography or section quotas to a working admin screen.

4. Read Uizze UI Taste and load the matching action/platform playbook. Reuse the same research and design record. For new visual work or an approved redesign, follow its image-to-UI guidance when an authorized image tool is available; inspect the target before implementation. Preserve an approved mock or existing system for extensions and small fixes. If image tooling is unavailable, state the limitation and use existing targets/conventions. A target image is not an interactive mock or proof that the application renders. Native iOS acceptance requires simulator/device evidence; a browser mock verifies only the web prototype.

Read only the relevant supporting references. A narrow UI fix does not need four complete redesigns. Generated script output is design guidance, not authority to override the brief or add unrelated work. If a resource/helper is unavailable, identify it and use the readable references with an explicit limitation; do not claim the missing helper ran.

Uizze MCP is optional. Use local playbooks and available authorized references when it is absent; do not request a paid account or add a connection as a prerequisite. If using a connected service, distinguish observed results, related examples, no match and service errors. No MCP token belongs in the bundle or evidence. Overdrive is an explicit mode, not the default. A read-only audit remains read-only unless fixes are requested.

The local search can legitimately return zero matches for a broad phrase. Refine the query with an actual component/API term, use the relevant UX domain or read the applicable reference; report no match instead of inventing guidance. Dataset version/date fields are upstream claims: check recommendations against the project's installed versions and current official documentation before relying on version-specific behavior.

## Portable helper execution

Resolve `<ui-root>` and `<taste-root>` to the absolute sibling skill directories above, replacing the placeholders before execution. UI/UX search needs Python 3; the complete Taste toolset needs Node.js 22+ (draw/lint alone support 18+). These helpers do not require npm/pip installation. Use the project's working directory and an explicit private artifact location; do not write internal design records into a public site's documentation tree.

```text
python "<ui-root>/scripts/search.py" "keyboard focus forms validation" --domain ux --json
python "<ui-root>/scripts/search.py" "appointment booking admin" --design-system --json
node "<taste-root>/scripts/draw.mjs" --app --list kinds
node "<taste-root>/scripts/draw.mjs" --app --kind <listed-kind> --brief "the agreed screen purpose" --keep palette,type --options 3
node "<taste-root>/scripts/lint.mjs" "<project-ui-directory>" --app --json
```

Use the locally available interpreter command (`python3`, `python`, or its absolute path). To persist a UI/UX design system, add `--persist --output-dir "<private-project-design-directory>"`; to save a Taste draw, omit `--options` and supply `--out "<private-project-design-directory>/taste"`. Read the applicable helper usage before selecting options or styles. Taste normally keeps cross-project history under the user's home; for reproducible tests set `TASTE_SKILL_HISTORY` to a disposable file and use `--seed`. Never overwrite the user's design records to run a test.

Taste's browser inspection requires an available browser/CDP environment. Its asset helpers may fetch external images; verify provenance and suitability before using them. The bundle contains metadata and code, not a blanket license to linked photos, fonts or reference-site branding. Do not claim remote assets were downloaded or visually inspected when only the local libraries were queried.

## Prototype, implementation and verification

Use the [interactive UI acceptance checks](ui-acceptance.md) when implementing or reviewing UI behavior. They cover cross-identity drafts, in-flight resets, stale responses, focus after rerender, error recovery, responsive layout and inclusion of new tests in the actual acceptance runner.

Build the agreed interactive mock with synthetic fixtures, real navigation/input/state changes and explicit simulated operations. Exercise empty, loading, success, invalid-input, error and denied states as applicable; check keyboard focus, reduced motion and intended viewports. Record browser steps and actual outcomes. Apply Taste's critique to the rendered screen; treat automated style lint as advisory where it conflicts with the accepted brand or interface purpose, documenting the reason. Lint does not replace browser interaction or measured accessibility checks.

Carry the accepted direction, components and states into the real vertical slice. Replace simulated calls with agreed contracts; verify server permissions and persisted behavior separately. Keep visual critique, interaction tests, technical acceptance and actual owner feedback distinct. These skills do not advance handbook gates or authorize deployment by themselves.

When using Uizze's finish workflow, save its [visual evidence receipt](../../ui-taste/references/uizze-visual-verification.md) with the actual source/capture hashes and required states/viewports. Run `node "<uizze-root>/scripts/verify-visual-evidence.mjs" "<private-artifacts>/visual-evidence.json"` after replacing placeholders. Its exit code 0 checks file integrity and declared coverage only; it does not establish visual quality, actual inspection, interaction execution or owner approval. Re-render and inspect affected states after later edits before updating the receipt. Reuse existing evidence records where possible instead of inventing a parallel approval process.
