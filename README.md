# aiobastion

> I'm currently updating the tooling, migrating and linting this repo.

**aiobastion** is a simple and fully asynchronous framework for [Cyberark API](https://docs.cyberark.com/Product-Doc/OnlineHelp/PAS/Latest/en/Content/WebServices/Implementing%20Privileged%20Account%20Security%20Web%20Services%20.htm) written in Python 3.12 with [asyncio](https://docs.python.org/3/library/asyncio.html) and [aiohttp](https://github.com/aio-libs/aiohttp).
It helps you to manage your Cyberark implementation faster and in an intuitive way.


## Examples
See [examples of usage](https://aiobastion.readthedocs.io/en/latest/started.html#examples) in the [documentation](https://aiobastion.readthedocs.io/en/latest/index.html)

## Quick (and dirty) start
### List safes

Here's a minimal python snippet to list safes

```python 
import aiobastion
import asyncio

from aiobastion import GetTokenException


async def main():
    # Define your PVWA host here
    pvwa_host = "pvwa.mycompany.fr"
    vault = aiobastion.EPV(serialized={'api_host': pvwa_host})
    
    # Define login and password
    login = input("Login: ")
    password = input("Password: ")

    # Login to the PVWA
    try:
        await vault.login(login, password)
    except GetTokenException as err:
        print(f"An error occured while login : {err}")
        await vault.close_session()
        exit(0)

    # Working with PVWA
    async with vault as epv:
        # For example, listing all safes
        safes = await epv.safe.list()
        for s in safes:
            print(s)

if __name__ == '__main__':
    asyncio.run(main())

```



## Getting started
[Define a config file](https://aiobastion.readthedocs.io/en/latest/login.html#define-a-configuration-file), and start using functions to avoid spending hours in annoying tasks in the PVWA :

* [Accounts manipulation](https://aiobastion.readthedocs.io/en/latest/accounts.html)
* [Safe manipulation](https://aiobastion.readthedocs.io/en/latest/safe.html)
* [User manipulation](https://aiobastion.readthedocs.io/en/latest/users.html)
* Check the documentation for more

## Support policy

This repository currently targets Python 3.12 and newer. The current maintenance line is validated against Python 3.12, 3.13, and 3.14.

## Integration tests

The live CyberArk tests are opt-in. Set the environment variable below to enable them:

```bash
export AIOBASTION_RUN_INTEGRATION_TESTS=1
```

You can override the default local test config paths with:

```bash
export AIOBASTION_TEST_CONFIG=/path/to/config_tests.yml
export AIOBASTION_TEST_AIM_CONFIG=/path/to/config_aim_hp.yml
export AIOBASTION_TEST_API_USER=admin_test_restapi
```

With those set, run the live suite with:

```bash
uv run --group test pytest tests/test_accounts.py tests/test_cyberark.py tests/test_safe.py
```

## Development with uv

This repository uses [uv](https://docs.astral.sh/uv/) for dependency management and local tooling.

Install the project dependencies with:

```bash
uv sync
```

Run the main developer tools with uv dependency groups:

```bash
uv run --group dev ruff check .
uv run --group dev ruff format .
uv run --group test pytest
```

If you need to refresh the lockfile after dependency changes, run:

```bash
uv lock
```

The project config currently limits resolution to packages uploaded at least one week ago, so `uv sync` and `uv lock` may intentionally avoid very new releases.

## Pre-commit hooks

The repository includes a [pre-commit](https://pre-commit.com/) configuration for formatting and hygiene checks.

Install the hooks once per clone:

```bash
uv run --group dev pre-commit install
```

Run the full hook set manually with:

```bash
uv run --group dev pre-commit run --all-files
```

The hooks run `ruff`, `ruff-format`, and basic checks like end-of-file, trailing whitespace, YAML, TOML, and merge-conflict detection.


## Documentation
The documention is hosted on readthedocs : https://aiobastion.readthedocs.io/en/latest/index.html

## Rationale

I've been working on Cyberark projects for years and I see everywhere a profusion of scripts, very often complicated and long to execute for very simple tasks (sometimes even with a "do not turn off" post-it on the screen).
This package makes it quick and easy to accomplish without having to deal with the specifics of the Cyberark API.
The acquisition time may be longer than for other well-known libraries, but, believe me, you will save this time very quickly.

# AI Disclaimer

This repo is helped with Github Copilot