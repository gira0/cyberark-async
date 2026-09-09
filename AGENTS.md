# AIObastion

## Project Shape

- This is an asynchronous Python 3.12+ library for the CyberArk API, built on `asyncio` and `aiohttp`.
- `aiobastion/cyberark.py` owns the `EPV` facade, authentication, HTTP sessions, request handling, concurrency, serialization, and lifecycle.
- Feature modules are initialized by `EPV` and keep a reference to it: `accounts.py`, `safe.py`, `users.py`, `platforms.py`, `accountgroup.py`, `applications.py`, `session_management.py`, and `system_health.py`.
- `config.py` owns configuration parsing, defaults, validation, and compatibility aliases. Keep transport concerns in `EPV` rather than duplicating them in feature modules.
- `utilities.py` contains higher-level bulk helpers; `exceptions.py` defines the public exception hierarchy; `api_options.py` holds compatibility/deprecation options.

## Development Workflow

- Use `uv` for dependencies and tooling. Run `uv sync` before local checks.
- Run the default offline suite with `uv run --group test pytest`.
- Run formatting and lint checks with `uv run --group dev ruff format .` and `uv run --group dev ruff check .`.
- Install and run all repository hooks with `uv run --group dev pre-commit install` and `uv run --group dev pre-commit run --all-files`.
- Refresh `uv.lock` with `uv lock` after dependency changes. Resolution is intentionally limited by `exclude-newer` in `pyproject.toml`.
- Make focused changes and run the narrowest relevant test file first, then the full offline suite when practical.

## Collaboration

- Call out clear typos, naming mismatches, and other obvious inconsistencies before applying the requested change, especially when they could create confusing filenames, commands, or public references.

## Versioning and Releases

- Use calendar versioning for releases: `YYYY.MM.DD`, with PEP 440 prerelease suffixes such as `a1`, `b1`, or `rc1` when needed.
- The current initial alpha version is `2026.09.09a2`; its Git tag is `v2026.09.09a2`.
- The GitHub release workflow requires the tag to exactly match the version in `pyproject.toml`.
- Publish through GitHub Releases and PyPI Trusted Publishing; do not add PyPI API tokens to the repository or workflow.

## Code Conventions

- Keep public APIs asynchronous: await library operations and use `asyncio.run()` only at an application boundary.
- Prefer `async with EPV(...)` so sessions are closed reliably. Preserve the existing `EPV.handle_request` transport path and shared concurrency controls.
- Follow the existing model and exception patterns in neighboring feature modules before introducing new abstractions.
- Use canonical configuration names such as `api_host`, `max_concurrent_tasks`, and `verify`; retain legacy aliases only for compatibility.
- Do not commit credentials, certificates, private test configuration, generated artifacts, or environment-specific settings.
- Update documentation when behavior or public APIs change. Start with the relevant page under `docs/` and [CONTRIBUTING.md](CONTRIBUTING.md).

## Testing Constraints

- Most tests are offline. Live CyberArk tests are opt-in and require a working Vault/PVWA environment.
- Enable live tests only with `AIOBASTION_RUN_INTEGRATION_TESTS=1`; optional test config and user overrides are documented in [CONTRIBUTING.md](CONTRIBUTING.md).
- Integration tests can be slow, destructive, permission-sensitive, or skipped when prerequisites are absent. Never add real secrets to test files.

## Documentation Map

- [README.md](README.md): installation, quick start, development commands, and integration-test switches.
- [docs/started.rst](docs/started.rst): async usage, batching, concurrency, and examples.
- [docs/login.rst](docs/login.rst): configuration, authentication, AIM, and lifecycle.
- [docs/index.rst](docs/index.rst): full documentation index; use the feature-specific pages linked there instead of duplicating API guidance here.
- [docs/compatibility.rst](docs/compatibility.rst) and [docs/faq.rst](docs/faq.rst): compatibility and troubleshooting guidance.