# Reference-led system workflow

Use for a product or feature whose requirements are informed by reference systems. For a component lookup use [tool workflow](tool-workflow.md). Keep the user's requested scope and existing decisions authoritative; handbook gates below are a reference framework, not permission to deploy or contact people.

## 1. Clarify the outcome

Inspect existing work first. Capture target users, problem, platform, primary journey, MVP boundaries, exclusions, budget/time constraints, data sensitivity, roles and measurable success. Separate confirmed requirements from assumptions and questions. Give requirements and acceptance criteria stable IDs; write observable Given/When/Then criteria, including important failure cases.

Resolve decisions that affect product behavior with the owner; do useful independent work while awaiting answers. Reuse previous decisions rather than requesting repeated approvals. Do not silently choose a business model, data policy or acceptance threshold for the owner. For a full product, record the one-page brief and decision to proceed (G0); for a small feature, a concise task record suffices.

## 2. Find and compare reference systems

Search from requirements, not only a product name. Consider official APIs/SDKs, maintained open-source products, licensed components and permitted product demos. Use the index helper for relevant reverse-engineered components, with [usage and failure handling](usage.md); it does not search all possible systems. Search the web or connected sources when available and needed, recording actual links and retrieval dates. If unavailable, use supplied/local evidence, mark coverage limited and do not invent a shortlist.

Compare a small useful shortlist against must-have requirements, platform, integration effort, operating cost, maintenance, license and data constraints. Separate documented claims from observed behavior. Record the choice to reuse, customize, integrate, independently build, or combine approaches, with rejected alternatives and material unknowns. Stars are not fit or reliability evidence. An official SDK solving one feature does not end the full project.

Do a short feasibility check before expensive design: required integration access, authentication, supported operations, local/cloud restrictions, data portability and material technical risks. Use an authorized sandbox for execution. Unknowns can become explicitly provisional mock assumptions; unknowns that affect architecture, rights or core acceptance block dependent implementation. No candidate satisfying requirements is a valid finding: explain the gap and evaluate independent construction or an owner-approved scope change.

## 3. Write initial specifications

Use [artifact records](artifacts.md), following the project's existing locations and format. Keep native editable text for requirements and decisions. At minimum connect the brief, feature list, acceptance criteria, screen/state map, initial data model, roles, API/integration contracts, architecture choices and implementation risks. Include server-side permissions, validation and failure behavior, not just happy-path screens.

These are initial specifications, not frozen facts. Mark unknown reference behavior and proposed behavior of the new system separately. Define the new system's contract deliberately; never claim that a guessed endpoint or field was discovered in the reference. Use a machine-checkable API contract where applicable and keep mock fixtures aligned with it. A CLI/offline component can have command/module contracts instead; record why web screens or HTTP APIs are inapplicable.

Use [Diagram Design](../../diagram-design/SKILL.md) for architecture, sequence or data-flow views that clarify the specification. Retain editable sources, distinguish current/proposed behavior and inspect the rendered result. Reuse the project style; keep generated files outside the installed skill.

## 4. Build and exercise an interactive mock UI

Use the [bundled UI workflow](ui-workflow.md) to select relevant UX guidance, one visual direction and the appropriate app/site critique. Keep existing brand, stack and confirmed requirements authoritative across all four UI skills. Direct calls use the same [task policy](ui-task-policy.md); existing-component fixes take its focused route instead of restarting this lifecycle.

Deliver runnable prototype source, entry point/start command, fixture/reset instructions and known limitations. Match the target platform and existing stack where practical. A local HTML/JS prototype may suffice; do not add a framework solely for a mock. Use synthetic data and label simulated operations. No production credentials, payments, external messages or real mutations are needed for prototype validation.

Cover the agreed end-to-end journey with actual navigation, input, validation and state changes. Exercise relevant empty, loading, success, error and permission-denied states. Make in-scope actions work; explicitly identify excluded controls. Document whether state survives navigation or reload. Check the intended viewport sizes and basic keyboard access for web UIs.

Run it and use a browser/app interaction tool to follow the scenarios; record steps, expected versus actual outcomes, runtime/console errors and evidence. Screenshots support the record but do not prove interaction. If interaction tooling cannot run, provide the runnable artifact and manual steps, mark interaction verification pending and do not claim the prototype passed.

For UI state transitions and rendered checks, use [interactive UI acceptance](ui-acceptance.md), including identity changes, pending mutations, recovery and focus after DOM updates. Keep mock and real-system evidence distinct.

Present the working prototype and concrete decisions to the user. Record actual feedback/approval or an existing decision that covers it; silence or an AI role-play is not user acceptance. If the user has delegated design decisions, record that delegation and the decisions made, without claiming human testing. Revise specifications and prototype when feedback changes the flow. Continue independent work while a necessary decision is pending.

## 5. Analyze or reverse only when needed

Ask what unresolved question analysis will answer. Prefer available documentation, licensed source and authorized black-box observation. If sufficient, record reverse as not needed with the reason. Move a blocking analysis earlier when feasibility depends on it. Do not perform binary decompilation by default.

When reverse analysis is necessary, establish authorized source, permitted scope and purpose before accessing protected material. Record source/version, acquisition provenance, SHA-256 for acquired files, available/missing tools and an inventory of relevant features, screens, data, interfaces and resources. Inspect in isolation and distinguish observed results, inference and unknowns. Do not infer authorization from possession of a file or a README.

For reconstructing proprietary reference behavior, maintain a clean-room handoff: the implementation context receives only the sanitized behavioral specification, not decompiled code, secrets or unlicensed assets. If the current context has read such code, use a separate implementation context restricted to the specification; if unavailable, report that boundary cannot yet be established. Do not claim clean-room separation inside one contaminated context. Separately authorized reuse of licensed source follows its license and is documented as reuse, not clean-room reconstruction.

Do not copy the reference's branding or unlicensed content/assets, reproduce its UI one-for-one, bypass protections, or call its production API as part of reverse analysis. An explicitly authorized official API integration is a separate scoped path. Record reference observations in T14-style analysis and classify every inventoried feature as implemented, deferred or excluded in the T15-style comparison ledger; before construction use planned implementation with evidence pending, never falsely mark implemented.

## 6. Finalize design before construction

Feed analysis and mock feedback back into requirements, data, permissions, contracts and prototype scenarios. Resolve blocking questions. Record agreed scope and decisions, version the artifacts and check consistency between them. G1 requires completed specifications, data/role design, applicable API lint, exercised prototype scenarios and a recorded design decision. Evidence and authority for that decision must be explicit; an earlier approval counts only if it covers the current design. Do not skip this handoff because a reference implementation exists.

For tasks stopping at documents or prototype, deliver that outcome and remaining dependencies now. For an authorized build, prepare a short ordered plan with vertical slices, touched areas, dependencies, tests, rollback/recovery and completion conditions. Avoid generic infrastructure or an oversized architecture. A slice should implement a user outcome across the necessary UI, service and storage layers.

## 7. Construct and verify

For frontend slices, carry the prototype's accepted direction through the [bundled UI workflow](ui-workflow.md); do not restart visual exploration or replace established tokens simply because construction begins.

Follow repository instructions, inspect worktree state and preserve unrelated changes. Use an isolated branch/worktree/environment when needed, without forcing one for a trivial edit. Review dependencies and hooks before running candidate code; pin chosen versions. Implement against the agreed contracts and replace prototype simulations with real behavior in production paths.

First prove a thin end-to-end slice with actual data flow and permissions; then expand. Test the relevant units, integration contracts and complete user journey, including invalid input, denied access, retries/duplicates and persisted state where applicable. Check authorization on the server, not only through hidden UI controls. Validate migrations/recovery where data changes. Inspect the diff and obtain independent review proportionate to risk; fix blocking findings, update artifacts and rerun affected checks.

Use the gate evidence below honestly. If only local execution is authorized or available, report local implementation/tests separately and leave staging/release gates pending. Continue useful authorized work, but do not claim a handbook gate passed or production readiness from local tests. CI evidence may be relevant to the built product; this skill does not require GitHub Actions or modify the catalog's automation.

## 8. Accept and hand off

Trace every in-scope criterion to an executed test or actual user observation on an identified revision/artifact and environment. Compare the delivered behavior with the chosen references and resolve every ledger item. Record failures, deferred/excluded scope decisions and remaining risks. Reconcile changes back into specs, contracts, prototype notes and user instructions. A release candidate's user guide should match its current UI and be tried by a new human; agent simulation does not substitute for that evidence.

Present the actual runnable result, evidence report and acceptance checklist. Owner acceptance, technical verification and permission to release are separate recorded decisions. Do not manufacture user sign-off; when it is pending, say what passed technically and what remains. Deployment, sending external notifications and recurring operations require scope authorization. If release is included, use the exact tested artifact, run post-release smoke checks and prepare recovery; otherwise stop at the requested handoff.

## Handbook gates and resuming

| Gate | Evidence required for a full product |
|---|---|
| G0 — scope | User/problem, MVP journey, success measure, budget, stop conditions and recorded decision to proceed. |
| G1 — design | Specifications, data/permissions, applicable validated API contract, exercised interactive prototype, no blocking questions and recorded design decision. |
| G2 — foundation | Clean setup runs; failing checks block integration; thin slice on staging; measured restore against agreed RTO/RPO and alert receipt. Local fixtures alone do not meet this gate. |
| G3 — functionality | Every in-scope AC has evidence, definition of done met, staging E2E passed and no blocking defects. |
| G4 — release | Exact artifact that passed G3; smoke/recovery evidence, agreed human testing and product-owner acceptance. |
| G5 — operations | Only if in scope: metrics versus agreed thresholds, incident owner/process, scheduled recovery checks and decisions at stop thresholds. |

Use Pass, Fail, Pending, or N/A with evidence. N/A requires a specific applicability rationale and recorded scope decision; lack of access or a failed check is not N/A. Do not reduce acceptance scope just to make a gate pass. A small local tool needs applicable task acceptance, not fictional staging or UI. Keep a checkpoint with current stage, artifact paths/revisions, completed evidence, unresolved questions, decisions/authorization and next action. Resume from it after verifying that underlying code and assumptions have not changed.
