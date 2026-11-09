# Minimal artifact records

Use these fields when the system workflow needs durable handoffs. Reuse existing project records; combine sections for a small task. The T-codes map to the solo-with-AI handbook's template families, not mandatory filenames or additional bureaucracy. Keep records in the user's language and agreed format. Choose a private project documentation location if `docs/` is a published website. Never include credentials, private customer data or unlicensed source extracts.

## Brief and decisions — T1, T10

- Problem, users, platform and primary journey.
- MVP scope/exclusions; measurable success and stop conditions; budget/time constraints.
- Confirmed requirements versus assumptions and blocking questions.
- Decision ID, options, selected option, reason, scope/risks, owner, date and evidence of decision or delegation.

## Reference analysis and comparison — T14, T15

| Reference ID / source / version / date | Requirement covered | Observed behavior and evidence | Inference / unknown | Fit, cost, maintenance, license evidence | Reuse / customize / integrate / independent build decision |
|---|---|---|---|---|---|

For acquired reverse-analysis files add provenance, permission scope, SHA-256, tools/limits and the sanitized-specification handoff location. Record whether a fact was read in documentation or actually exercised.

| Reference feature ID | Product requirement / spec ID | Planned scope | Delivered status: implemented / deferred / excluded | Implementation/test evidence or decision/reason |
|---|---|---|---|---|

Use `pending` for delivery status before evidence exists; classify all items by final comparison. An implemented label requires verification, not a planned task.

## Specification and design — T2, T3

- Requirement/feature ID, actor, preconditions, normal flow, failure/edge cases and Given/When/Then AC IDs.
- Screen/state map, fields, validation, navigation, role visibility and server-side permissions.
- Data entities, constraints, retention, ownership and state transitions.
- API/command/module contract: input/output, errors, auth, side effects, retry/idempotency where relevant; contract file and validation result.
- Minimal architecture, dependencies, chosen versions, integration boundaries and material risks. Use [Diagram Design](../../diagram-design/SKILL.md) when a visual clarifies these relationships; retain editable sources, evidence links and current/proposed labels.
- Links to references and decisions; proposed new behavior clearly distinguished from observations.

## Interactive prototype record

- Source and revision; start command/entry point; test fixtures and reset procedure.
- Working journey, simulated operations, excluded actions, persistence behavior and known limitations.
- Scenario ID → AC IDs → interaction steps → expected outcome → actual result → screenshot/log evidence.
- Viewport/device, keyboard checks, runtime errors and tested version.
- Actual user feedback/decision, resulting changes, unresolved items and retest evidence. Record human review as pending if not performed.

## Construction plan and context — T4, T5, T6

- Ordered slices with requirement/AC IDs, dependencies, files/areas affected, acceptance checks and recovery.
- Task status and current checkpoint; decisions carried forward and questions still pending.
- Authoritative spec/contract paths, commands/environment, working scope and trust boundaries for the implementation context.
- For clean-room reconstruction: only sanitized behavioral specification crosses into implementation, with the boundary recorded.

## Evidence and acceptance — T8, T9

| AC / gate ID | Spec / UI / reference links | Revision/artifact and environment | Command or interaction / expected / actual | Evidence path | Pass / Fail / Pending / N/A | Reviewer or owner decision / date |
|---|---|---|---|---|---|---|

Include test counts/failures, commands actually run, relevant runtime logs, review findings and their resolution. Record each N/A rationale and scope decision; missing tests remain pending. Keep technical results separate from human acceptance and release authorization. List remaining limits and exact next actions.

On completion or interruption, include how to run the current result, changed files, current stage and artifact revisions, open dependencies, authorization already given and the next safe action. Do not report a plan, mock or successful installation as an executed end-to-end system.
