# Review and security coordination

Use one scope and one evidence record across the engineering workflow. Inspect the request, accepted requirements, exact source/diff and available tools before choosing a reviewer.

| Task | Route | Completion evidence |
|---|---|---|
| Review a change, commit or branch | [Open Code Review](../../open-code-review/SKILL.md), preferably host-model delegation | Previewed files accounted for, source-backed findings, skipped/failed coverage disclosed |
| Explain or investigate a security concern | [Security Audit](../../security-audit/SKILL.md), focused guidance | Trust boundary, reachable path, evidence and concrete unknowns |
| Explicit comprehensive audit/report | Security Audit six-phase workflow | Coverage ledger, independent validation, structured records, final report or explicit incomplete status |
| Fix accepted findings | Superpowers debugging/verification and Ponytail implementation | Reproduction where possible, narrow fix and affected regression checks |

Superpowers owns planning, debugging and review discipline; these specialists supply review mechanics. Avoid running overlapping whole-repository passes just because multiple skills are installed. Keep small UI changes on the focused UI path. Security-relevant changes warrant proportionate scrutiny, not an automatic full audit.

An OCR security comment is a candidate, not a confirmed vulnerability. Link it to the same source revision and trace before handing it to Security Audit. Preserve contrary evidence and rejected candidates; do not raise severity to make a finding more persuasive. Missing OCR, provider access, execution isolation or independent reviewers must be named precisely.

Direct and router calls use the same rules. Review-only requests leave source unchanged. Existing authorization for fixes, commits or delivery remains valid, but review tooling does not grant new permission to publish comments, configure providers, create CI workflows or probe live endpoints.

At handoff, record revision, scope/mode, tool versions, actual commands, coverage, findings, validation status and remaining limitations. Keep actionable evidence in the requested language. Do not expose raw model reasoning, credentials or unrelated private data. A completed code review, a validated report schema, an independent security audit and human product acceptance are separate claims.
