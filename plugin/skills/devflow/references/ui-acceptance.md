# Interactive UI acceptance

Use for mock and real frontend changes. Select checks that apply to the actual controls and data; a CLI task does not need UI tests. Preserve the user's scope, brand, stack and earlier design decisions. These checks came from observed sample failures, but their purpose is to verify invariants, not impose the sample's colors, layout, dates or database.

## State transitions to exercise

| Boundary | Executed check and expected outcome |
|---|---|
| Identity/workspace change | Enter a draft as A, switch to B. No private draft, old selection, details or stale response from A appears under B. Preserve only fields explicitly intended to be shared. |
| Invalid input | Try blank, malformed, out-of-range and boundary values. Clear dependent selections/actions before rendering new availability. Mock validation follows the agreed contract; HTTP validation is tested independently. |
| Mutation in flight | Delay the request and try submit again, reset, identity/date changes and navigation. Disable or safely coordinate conflicting actions; no duplicate write, accidental reset or completion applied to another context. Use handler guards as well as visual disabled states. |
| Async reads | Release old success and error responses after a newer mutation, date change, view change or identity switch. They must not replace current state or resurrect old errors. |
| Recovery | Test empty data, all options unavailable, network failure, denied access and malformed local mock storage where applicable. Show an actionable explanation and working retry/reset. Reset affects only owned mock data, not the real database. |
| Correcting a field | Trigger an error, correct the field, then submit. Inline error, aria-invalid and any matching summary agree; unrelated server errors are not silently cleared. |
| Keyboard after rerender | Focus a dynamic control, activate with Enter/Space, and continue with Tab. Focus stays on a meaningful control after DOM replacement; a CSS focus ring alone does not establish this. |
| Shared facts | Selection summary, labels, counts and outgoing request derive from the same state. Assert totals against displayed rows and verify dates/timezones explicitly. |

Use isolated fixtures and controlled delayed responses. Record a genuine failing reproduction before fixing a discovered defect, then its passing regression. Never corrupt the user's storage to simulate an error. Synthetic authorization tests do not prove server-side enforcement; run real HTTP permission tests when a backend is in scope.

## Rendered UI checks

Test the target desktop, tablet and phone widths, including the narrowest supported width. Do not turn the sample's breakpoint into a universal requirement. Assert document-level overflow and inspect screenshots: a grid can keep two columns while making a form unusably narrow. Confine intentional horizontal scrolling to the relevant strip/table; keep keyboard access and touch targets usable.

Measure relevant contrast in normal, hover, selected, disabled and error states. Disabled controls are not automatically WCAG contrast failures, but their purpose and label should remain understandable. Tests should assert the intended behavior/contrast, not the previous design's exact RGB value. Keep precise token checks only when those tokens are an explicit requirement.

For full visual work, run the applicable Taste lint and browser inspector, then inspect screenshots yourself. For a focused fix, follow the [shared task policy](ui-task-policy.md): targeted interaction/rendered checks suffice; the full Taste inspector is not mandatory. A zero-finding inspector is not interaction, accessibility certification or user acceptance. Record justified design exceptions individually; do not blanket-allow findings to make a report green. If the in-app browser is unavailable, an available browser automation/inspection tool may supply execution evidence. State the actual tool used and any unexecuted check.

## One repeatable acceptance command

Maintain a top-level runner that actually invokes every required regression suite, including newly added UI tests. It must propagate failures, report missing dependencies/skips as incomplete, and identify the tested source revision or hashes. A green old runner does not cover a new test file sitting beside it.

Keep prototype execution separate from UI → HTTP → storage checks. Assert that mock actions leave the real database unchanged; for a real mutation, verify persisted state, permissions, conflict handling and restart/recovery where required. Run in temporary databases, ports and browser contexts; close resources before Windows cleanup.

After the final code change, rerun affected checks and the relevant integrated runner. Preserve first failures, fixes, final logs and screenshots, then ensure the hashes identify the final delivered code. Distinguish test counts from exhaustive coverage. Update specs, README and acceptance records together; report local technical acceptance, human acceptance and release authorization separately.
