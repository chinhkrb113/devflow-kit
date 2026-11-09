# Tool lookup and integration

Read this for a standalone lookup, acquisition or integration, or a tool subtask inside the system workflow. Shared trust rules remain in [SKILL.md](../SKILL.md). Return to the enclosing product task after resolving a subtask.

## Workflow

1. **Define the outcome and scope.** Use the user's existing requirements: task, platform/runtime, local versus cloud operation, constraints, and an observable success condition. Ask only about missing information that changes the choice. Distinguish research/comparison from acquisition/integration. A research request does not authorize installing or running candidate code; existing authorization remains valid without asking again.

2. **Check official options first.** Determine whether an official API/SDK meets that outcome. If it does, recommend or use it within scope and stop this search. Otherwise record the specific gap, such as cloud-only access when local control is required. If this check is incomplete, say so.

3. **Find a shortlist.** Read [usage and failure handling](usage.md) before running the helper. Search with 1–4 product/vendor/task words; apply category, language, stars and archived filters as useful. Broaden the query when empty. Results can include partial matches; inspect each candidate instead of treating ranking as approval. Record the data source and freshness when known.

4. **Verify, then select.** Read the relevant README sections, current project status, compatibility/dependencies and license files at an identified revision before making the final choice. Check suitability first, then maintenance and stack; use stars only as a tie-breaker. A blank index license is **unknown**, not a licensing conclusion. An 80-line excerpt or successful command exit does not prove documentation was retrieved or reviewed. Use another read-only route when necessary. Report unresolved compatibility or licensing; do not proceed with integration while a material requirement remains unknown.

5. **Branch by scope.** For research/comparison, report the recommendation and stop. For authorized acquisition/integration, first state a short plan: selected version/revision, destination/environment, dependencies and files/settings affected, acceptance checks, and cleanup/recovery where changes require it. Scale this to the task; do not create a full product lifecycle for a lookup. Clarify only actions that exceed existing authorization.

6. **Acquire and verify within scope.** Review relevant code and installation hooks before execution; reading alone does not establish trust. Pin the selected version/revision, use an isolated environment where practical, and avoid unrelated changes. If only acquisition was requested, record the obtained revision and stop without executing candidate code. For integration, run the smallest meaningful smoke test against the stated outcome using test data. Include relevant failure cases, inspect errors/diff, and compare actual results with acceptance checks. Failed or unavailable checks mean incomplete verification, not success. Use independent review when the change's risk warrants it.

7. **Report evidence.** State the outcome/mode, official-option decision, chosen project and revision, source/freshness, license evidence, actions performed, commands/results, and remaining limits. Label observations as executed, read/inferred, or unverified. Never describe a recommendation, README read, clone or installation as a tested integration. Reuse the project's existing report/task conventions for integration evidence; a brief answer is enough for research.

