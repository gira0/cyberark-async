---
name: code-review
description: Review a cyberark-async pull request against the project's API, security and async rules. Use when reviewing pull requests in this repository.
---

Review the pull request in this order. The rules themselves are in `.github/copilot-instructions.md`, the path-specific files in `.github/instructions/` and `AGENTS.md`.

1. **Classify the change.** List the changed files and group them: library (`aiobastion/`), tests (`tests/`), CI (`.github/`), docs (`docs/`, `README.md`, `CONTRIBUTING.md`), dependencies (`pyproject.toml`, `uv.lock`, `uv.toml`). Say in the summary which groups are touched.
2. **Check every changed API call against the spec.** Find every added or changed HTTP call: `handle_request(...)`, and any direct `get_session()`, `aiohttp.ClientSession(...)` or session HTTP call (`session.request(...)` or any verb method: `get`, `post`, `put`, `patch`, `delete`, `head`, `options`) use. Outside the EPV transport and authentication code (`cyberark.py`, `http_session.py`, `aim.py`), report a direct session call as a finding and ask for it to go through `handle_request()` (see #12). For each call, look up the route in `tests/test_data/cyberark-pvwa-swagger.json` under `paths`. The spec's paths start with `/api/...` and the code passes them without the leading slash and with varying case (`"API/Accounts/{id}"`), so compare case-insensitively. Confirm that the method exists for that path and that query parameter and body field names match the spec's `parameters`. Report a mismatch as a bug.
3. **Check the support manifest.** If the PR adds, removes or renames an API call, `tests/test_data/support_manifest.json` should gain or lose the matching `[METHOD, "/api/..."]` entry. Point out when it does not.
4. **Look for secret exposure.** Search the diff for `print(`, logger calls, exception messages and test data that could include passwords, tokens or response bodies.
5. **Check tests and changelog.** A bug fix should come with an offline test that would fail without the fix. A user-visible change needs a `CHANGELOG.md` line under `## [Unreleased]`.
6. **Report.** Lead each comment with its category (Security, API correctness, Async, Tests/Docs). Do not comment on formatting or import order; ruff enforces those in CI.
