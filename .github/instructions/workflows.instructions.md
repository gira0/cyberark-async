---
applyTo: ".github/workflows/**"
---

# GitHub Actions workflows

- Pin newly added third-party actions (outside `actions/` and `github/`) to a full commit SHA with the version in a comment, as in `tests.yml` (`astral-sh/setup-uv@<sha> # v6.6.1`).
- Keep `permissions:` minimal. Only the release workflow needs `id-token: write`.
- Publishing uses PyPI Trusted Publishing. Flag any PyPI API token, `TWINE_PASSWORD` or similar secret.
- Run Python tooling through uv with `--locked` (for example `uv run --locked --group test pytest`) so CI uses `uv.lock`. `setup-uv` reads the minimum uv version from `uv.toml`; do not pin an older one.
- Do not add `continue-on-error: true` to test or lint steps.
