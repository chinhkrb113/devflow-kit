# Helper usage and failure handling

## Invoke from the skill directory

Resolve this skill's directory from the SKILL.md you loaded. The helper is its `scripts/re_index.py`, not the consuming project's `scripts/` directory. Run from the skill directory or substitute the resolved absolute script path below. Use Python 3.9 or newer; `python3` is a common alternative to `python`.

```bash
python scripts/re_index.py search tuya local --limit 5
python scripts/re_index.py search psd parser --lang Python --json
python scripts/re_index.py categories
python scripts/re_index.py info jasonacox/tinytuya --lines 160
```

The helper reads JSON and writes CLI output as UTF-8, including on Windows; `-X utf8` is optional. Use `--category TEXT`, `--lang NAME`, `--min-stars N`, `--include-archived`, `--limit N` and search `--json` as needed. Full matches precede partial matches; JSON contains entries without per-result match labels or provenance. Limits must be positive; minimum stars and README line counts must be non-negative. `info --lines 0` explicitly requests index metadata only, with no README request.

Only when acquisition is authorized:

```bash
python scripts/re_index.py clone jasonacox/tinytuya
git -C ~/.cache/awesome-reverse-engineered/clones/tinytuya rev-parse HEAD
```

Without `--dest` the clone goes to `~/.cache/awesome-reverse-engineered/clones/<name>`, outside the project, so a harness does not load the clone's CLAUDE.md, AGENTS.md or skills as project instructions. Pass a `--dest` inside the project only when the user asks to vendor the code there. Resolve a relative destination against the current working directory and state it in the plan. The clone helper takes the default branch tip, not a pinned revision. If a revision was selected, use an explicit Git checkout/fetch procedure that obtains it and verify HEAD before execution. Do not assume a shallow clone contains an older tag or commit.

## Data and authentication

- `RE_INDEX_DATA` selects and validates a local entries.json. An invalid override fails instead of silently selecting different data. Otherwise a valid disk cache is used for 24 hours. An expired or corrupt cache triggers a refresh; only valid UTF-8 JSON with the required entry fields replaces it, using an atomic file replacement. Failed downloads leave a valid old cache intact, with a stale-data warning; otherwise the helper tries bundled data. The bundled fallback is available in a full repository checkout; do not assume it ships in a standalone skill install.
- If cache persistence fails (for example, a Windows file lock), valid downloaded data can still be used for this invocation, with a warning. A later invocation may need to download again.
- Cache mtime indicates download time, not when each project's metadata was verified. Report unknown freshness honestly.
- README requests use `GITHUB_TOKEN` when set, otherwise try `gh auth token`. This is GitHub authentication, not authorization to give credentials to a candidate tool. Do not print token values. Public README reading can use another unauthenticated route if needed.

## Known limits and recovery

| Exit code | Meaning |
|---|---|
| 0 | Requested operation completed; an empty search result is valid. This does not certify a candidate tool works. |
| 1 | Data, network, file or Git operation failed; inspect stderr. info may have printed metadata before a README failure. |
| 2 | Invalid arguments or repository URL. |
| 3 | info is incomplete: README fetching is unsupported for this host, README is empty, or metadata-only lookup found no entry. |

| Observation | Required response |
|---|---|
| No matches | Broaden terms/vendor or inspect categories; this is not proof no tool exists. |
| README fetch error (exit 1) or incomplete info (exit 3) | Mark README unverified. Obtain the necessary sections another way before selecting/integrating; inspect content as well as exit status. Older helper versions can print a README error with exit 0: treat the error as failure. |
| Non-GitHub project | Full HTTP(S) URLs retain their host and path. Index metadata lookup is supported; README fetching supports GitHub only. Use a read-only browser/API route for other hosts. |
| No usable index or invalid override (exit 1) | Use `RE_INDEX_DATA` pointing to a valid local copy when available; otherwise report blocked retrieval. Do not delete the only good copy. |
| Clone fails (exit 1) | Inspect stderr and any partial destination before retrying; do not remove a pre-existing directory automatically. |
| Partial/old/missing metadata | Check repository facts; distinguish index metadata from current observations. |

Use owner/repo for GitHub shorthand, or an HTTP(S) URL for another host. Embedded URL credentials and non-HTTP(S) schemes are rejected. A default-branch clone remains unpinned until its actual revision is checked; an index match, successful install or README excerpt is not functional verification.
