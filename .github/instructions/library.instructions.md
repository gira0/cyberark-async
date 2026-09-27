---
applyTo: "cyberark_async/**/*.py"
---

# Library code (`cyberark_async/`)

- `cyberark.py` owns authentication, sessions, request handling and concurrency. Feature modules (`accounts.py`, `safe.py`, `users.py`, `platforms.py`, ...) receive the `EPV` instance as `self.epv` and must call `self.epv.handle_request(method, "API/...", data=..., params=...)` rather than building their own sessions or URLs.
- `config.py` owns configuration parsing, defaults and validation. Flag transport settings (timeouts, TLS, retries) implemented inside feature modules.
- Query parameter values must be `str`, `int` or `float`. Convert booleans explicitly, for example `str(include_accounts)`, as `search_safe_paginate()` and `get_safe_details()` in `safe.py` do.
- Flag `print()` in library code. Use the `cyberark_async` logger (`logging.getLogger("cyberark_async")`) and never log response bodies from AIM/CCP or authentication calls.
- Flag bare `except:` and `except Exception: pass` that hide API errors. Errors from the PVWA should surface as `CyberarkAPIException` or `CyberarkException`.
- Changing a public function's name, parameters or return shape is a breaking change: it needs a deprecation path or an explicit note in `CHANGELOG.md`.
