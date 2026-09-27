---
applyTo: "tests/**/*.py"
---

# Tests (`tests/`)

- The default suite is offline. Tests that need a live Vault/PVWA must call `tests.require_integration_tests(...)` in their setup so they skip unless `AIOBASTION_RUN_INTEGRATION_TESTS=1` is set.
- Prefer offline regression tests for bug fixes: patch `EPV.handle_request` or `aiohttp.ClientSession.request` with `unittest.mock` instead of calling a real server. See `TestSerializedTokenOffline` in `tests/test_cyberark.py` and `TestSafeDetailsOffline` in `tests/test_safe.py`.
- Flag real hostnames, usernames, passwords, tokens or certificates. Use placeholders such as `pvwa.example.invalid`.
- Flag assertions that cannot fail, such as `assertIn(x, x)`, and `self.assertRaises(SomeError)` called with only the exception, outside a `with` block, which asserts nothing. The callable form `self.assertRaises(SomeError, func, *args)` is fine, and async code needs `await` inside the `with` block.
- Do not skip, disable or loosen an existing test to make a change pass.
