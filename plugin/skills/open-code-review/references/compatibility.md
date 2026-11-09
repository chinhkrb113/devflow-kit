# Open Code Review compatibility

This component packages the two upstream skill guides behind one discoverable entry. It does not package the Go executable, model provider configuration, editor extensions, GitHub Actions, hooks or marketplace installers. Source is pinned in the bundle lock; the user's installed CLI can have a different version and must be checked separately.

The inspected upstream README requires Git 2.41+. Use a compatible `ocr` release with `delegate preview --format json` and `delegate rule --format json`. Provider-driven review additionally needs the user's configured provider. Inspect `ocr --version` and relevant help output; do not run `ocr llm test` as a setup check because it contacts the provider. Prefer an existing executable or a specifically requested installation location/version over global changes.

Upstream references contain convenience instructions for automatic global install/upgrade, API setup, broad default review, optional fixes and repeated commit approval. The DevFlow entry adapts those behaviors: preserve scope, check capabilities first, use existing authorization and keep installation/provider changes explicit. Model-generated comments are candidates until checked against source. Never publish review comments just because the upstream tool supports it.

The npm launcher can perform background update checks. For deterministic/offline preparation, prefer an already installed native binary or set `OCR_NO_UPDATE=1` for the launcher; do not treat launcher update traffic as an OCR model call.

Host delegation does not call a model from OCR. The host still uses its own configured model and permissions. Plain chat cannot run Git or OCR; it can explain a provided diff and must identify the coverage limit. Sequential review is valid; do not pretend self-review was independently verified.
