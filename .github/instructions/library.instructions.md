---
applyTo: "aiobastion/**/*.py"
---

# Library code (`aiobastion/`)

- `cyberark.py` owns authentication, sessions, request handling and concurrency. Feature modules (`accounts.py`, `safe.py`, `users.py`, `platforms.py`, ...) receive the `EPV` instance as `self.epv` and must call `self.epv.handle_request(method, "API/...", data=..., params=...)` rather than building their own sessions or URLs.
- `config.py` owns configuration parsing, defaults and validation. Flag transport settings (timeouts, TLS, retries) implemented inside feature modules.
- Query parameter values must be `str`, `int` or `float`. Convert booleans explicitly, for example `str(include_accounts)`, as `safe.search()` does.
- Flag `print()` in library code. Use the `aiobastion` logger (`logging.getLogger("aiobastion")`) and never log response bodies from AIM/CCP or authentication calls.
- Flag bare `except:` and `except Exception: pass` that hide API errors. Errors from the PVWA should surface as `CyberarkAPIException` or `CyberarkException`.
- Changing a public function's name, parameters or return shape is a breaking change: it needs a deprecation path or an explicit note in `CHANGELOG.md`.
