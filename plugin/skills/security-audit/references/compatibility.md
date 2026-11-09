# Security Audit portability

The original six-phase guide, domain companions, schema and dependency-free Node validators are bundled at a pinned revision. Upstream `SKILL.md` is retained as `GUIDE.md`, leaving one discoverable entry. Node.js 22+ is the bundle's tested baseline. Reading the guidance itself does not require Node.

## File validation versus trusted stdin

The upstream file readers require `O_NOFOLLOW` and `O_NONBLOCK`. On Windows runtimes without these flags, both commands reject input intentionally. DevFlow preserves that behavior rather than weakening file handling. Seven upstream CLI tests that assumed these flags now declare their capability prerequisite, alongside upstream's existing capability skips; report skipped cases explicitly.

`validate-stdin.cjs findings|coverage` accepts **only** a JSON byte stream, never a path argument. It bounds bytes to 5 MiB and input time to 10 seconds, decodes strict UTF-8, runs the original structural preflight and semantic validator, and emits a sanitized JSON result with a nonzero exit on failure. Empty valid arrays mean zero records, not that an audit found the system secure. The findings helper exposes its existing preflight function for this transport; its file reader and validation rules are unchanged.

The trusted parent can pass its serialized record object as a subprocess's stdin, for example using an argument array and the process API's `input` field. Keep credentials out of the object. Do not use this path to read or promote unverified hunter scratch files: sandbox, path/handle ownership and no-follow promotion rules still apply before any evidence is retained. stdin validation is not proof of safe artifact provenance.

## Capability limits

No sandbox, independent reviewer, cloud account, scanner service or hosted test environment is installed. Without the guide's execution controls, source analysis can continue but target-controlled execution remains blocked. Without independent verification, a complete audit cannot be claimed. Preserve that limit on every harness rather than silently substituting self-review.

No audit is launched by installation or ordinary implementation. Focused security questions use relevant guidance without six-phase artifacts. Full audit output belongs outside the target by default; a user-selected in-target location must be wholly ignored by version control, as required upstream. Review findings are proposed fixes, not permission to modify or publish source.
