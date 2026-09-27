# Copilot instructions for cyberark-async

cyberark-async (import name `aiobastion`) is an asynchronous Python 3.12+ client for the CyberArk PVWA REST API, built on `asyncio` and `aiohttp`. `AGENTS.md` describes the project layout, workflow and conventions; read it for context. This file lists what matters most when reviewing a pull request.

## Review priorities

Report problems in this order, and say which category each finding belongs to:

1. **Secret exposure.** Passwords, tokens, AIM/CCP response bodies or certificates that reach logs, `print`, exception messages or test files. The body of a CCP (`aim.py`) response can contain the retrieved password.
2. **Correctness of API calls.** Wrong HTTP method or path, query parameters or JSON bodies whose values aiohttp/yarl cannot encode (for example `bool` query values must be sent as strings), and missing error handling for non-2xx responses.
3. **Async and lifecycle bugs.** Blocking calls in async code, un-awaited coroutines, `asyncio.run()` inside library code, and sessions that are not closed.
4. **Behaviour changes without tests or docs.** Anything user-visible needs an offline test and a `CHANGELOG.md` entry under `## [Unreleased]`, and public API changes need the matching page under `docs/`.
5. Everything else. Formatting and lint are enforced by `ruff` in CI, so do not comment on style that ruff accepts.

## Project rules

- Feature modules must send HTTP requests through `self.epv.handle_request()`. Flag any direct `get_session()`, `aiohttp.ClientSession(...)` or session HTTP call (`session.request(...)` or any verb method such as `.get`, `.post`, `.put`, `.patch`, `.delete`, `.head`, `.options`) use outside the EPV transport and authentication code (`cyberark.py`, `http_session.py`, `aim.py`): it bypasses the shared concurrency semaphore, TLS and timeout settings, and the normalised non-2xx error handling. Existing bypasses are tracked in #12; new ones should not be added.
- Keep public APIs `async`. Do not add synchronous wrappers.
- Raise the exceptions from `aiobastion/exceptions.py` (`AiobastionException`, `CyberarkException`, `CyberarkAPIException`, ...) instead of bare `Exception` or `ValueError`, following the neighbouring functions.
- Use the canonical configuration names `api_host`, `max_concurrent_tasks` and `verify`. Legacy aliases stay only for compatibility and must not appear in new examples or docs.
- New exported names belong in `aiobastion/__init__.py` `__all__`.
- Dependencies are managed with uv (0.9.17 or newer). A `uv.lock` change is only expected when `pyproject.toml` dependencies change; otherwise ask why it changed.
- Never suggest disabling TLS verification (`verify: False`) as a fix.

## Checking against the CyberArk API

- `tests/test_data/cyberark-pvwa-swagger.json` is the PVWA OpenAPI (Swagger 2.0) spec. Use its `paths` to check that every new or changed HTTP call, whether through `handle_request()` or a direct session (whose route comes from `self.epv.get_url("API/...")`), uses an existing route, the right method and valid parameter names. For body parameters, follow the `schema` `$ref` into `definitions` and check the JSON body keys against that model's `properties`.
- `tests/test_data/support_manifest.json` lists the implemented operations as `[METHOD, "/api/..."]` pairs, and `tests/test_data/support_manifest_baseline.json` is the regression baseline that `tests/test_api_support_report.py` checks for removals. A PR that adds a supported operation should add it to both files; a PR that removes one should remove it from both and note the breaking change in `CHANGELOG.md` (see CONTRIBUTING.md).
