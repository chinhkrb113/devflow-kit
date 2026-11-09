---
name: security-audit
description: Source-first security guidance, focused vulnerability review and explicitly scoped full audits with trust-boundary evidence, coverage records and independent verification. Applies to code, APIs, services and local tools; does not automatically authorize live probing or target-code execution.
license: MIT
---

# Security Audit — DevFlow Kit

Use [review coordination](../devflow/references/review-security.md) to select scope. Read the [upstream audit guide](GUIDE.md), then only the relevant reconnaissance, hunting, validation and domain companions. This entry adapts host capabilities and packaging; it preserves the upstream evidence and execution boundaries.

## Choose the mode

- For a security question, a suspicious diff or a specific candidate: use focused guidance. Do not create full audit artifacts or automatically inspect the entire codebase.
- For an explicit comprehensive security audit, penetration-test request or audit report: use the six-phase guide with scope, source revision, output ownership, coverage ledger and applicable budget. Source review does not authorize probing live systems.
- Integration or installation of this skill is not an audit request. Follow the user's current scope and do not fix source unless that work is separately requested or already authorized.

Record observations, assumptions, blockers and rejected candidates separately. Keep `confirmed`, `needs_validation` and `rejected` records distinct. A source-grounded candidate with an unresolved decisive fact stays `needs_validation` without severity; an incomplete review is not a security pass.

## Preserve execution and independence boundaries

The guide requires OS-enforced isolation for target-controlled execution: no external network, allowlisted clean environment, read-only target/toolchain, scratch-only writes and bounded resources/time. If these controls are unavailable, continue useful source inspection and record the exact execution blocker; do not run target builds, tests, scripts, fixture processing or live probes as a substitute.

Full audit confirmation requires fresh independent verification. Use actual supported delegation only when the audit calls for it. Without independent reviewers, provide a clearly labeled source-review result and mark the full audit incomplete; sequential self-review must not be renamed independent verification. A plain-chat host can interpret supplied evidence but cannot claim tool execution.

Keep target code, agent scratch and retained artifacts isolated as specified upstream. Do not replace race-safe promotion with ordinary recursive copying. If promotion controls cannot be enforced, retain a needs-validation blocker. Existing source authority never grants access to deployed accounts or other users' data.

## Validate final records

Read [validation and reporting](VALIDATION-AND-REPORTING.md) and `report-schema.json` before writing records. With supported OS file-opening protections:

```text
node <skill-dir>/validate-findings.cjs <output-dir>/findings.json
node <skill-dir>/validate-coverage-ledger.cjs <output-dir>/coverage-ledger.json
```

On hosts where those file APIs are unavailable, their CLI intentionally fails closed. For JSON already held by the trusted parent agent, the bundled [stdin validator](references/compatibility.md) applies the same semantic contracts without opening an input path:

```text
node <skill-dir>/validate-stdin.cjs findings
node <skill-dir>/validate-stdin.cjs coverage
```

Send bounded serialized parent-owned JSON through stdin and close the stream. This transport is not an artifact-promotion mechanism and must not be fed unverified target-controlled files. It does not supply the sandbox or reviewer independence missing from the host. Validators establish record shape and invariants; they do not prove a vulnerability or complete coverage.

The final report states source revision, scope, coverage gaps, verification performed, findings, remaining blockers and remediation proposals. Mark a full audit complete only when its applicable phases, independent checks and both validators succeed; otherwise record `run_status: incomplete` and why.
