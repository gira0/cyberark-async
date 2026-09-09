# Contributing

<!-- TOC -->
* [Contributing](#contributing)
  * [How to contribute](#how-to-contribute)
  * [Bugs and issues](#bugs-and-issues)
  * [Code contribution](#code-contribution)
  * [Test](#test)
    * [Prepare CyberArk to Run the Testing](#prepare-cyberark-to-run-the-testing)
      * [Test Accounts and Permissions](#test-accounts-and-permissions)
      * [Platforms and Apps](#platforms-and-apps)
    * [Troubleshoot Test Issues](#troubleshoot-test-issues)
  * [Update documentation](#update-documentation)
<!-- TOC -->
## How to contribute

Any kind of contribution is welcomed. Because this project is quite new the best way to contribute right now is to start to use this module and give feedback about it.
 

## Bugs and issues

If ou find an error, a bug or an issue, feel free to [log an issue][new-issue]

## Code contribution

If you wish to contribute with code the workflow is :
- Clone the Github repo
- Make any change
- Make sure [all tests are passed](#test)
- [Update documentation](#updating-documentation)
- Submit a pull request the dev branch

## Test

- Most tests are offline and run without a Vault or PVWA.
- To run the live CyberArk integration tests, set `AIOBASTION_RUN_INTEGRATION_TESTS=1` before invoking pytest.
- Optional overrides:
  - `AIOBASTION_TEST_CONFIG=/path/to/config_tests.yml`
  - `AIOBASTION_TEST_AIM_CONFIG=/path/to/config_aim_hp.yml`
  - `AIOBASTION_TEST_API_USER=admin_test_restapi`
- When the live tests are disabled or the config files are missing, the integration suites skip instead of failing.
- In order to test you need a working Vault and a PVWA.
- Then, generate some accounts with mockaroo and the following schemas : https://www.mockaroo.com/1e429890. See "Troubleshoot"
  section of some cleanup to avoid issues.
- Create the associated safes : sample-it-dept,sample-iaadmins,sample-coolteam
- Create safe "RENAME_ME", and grant user "admin_bot" (see below) to the "Safe Management" permissions (for safe
  rename testing)
- Import the data (with bulk upload)
- Create the configuration file for your testing Vault
- Check the \_\_init__.py file for the location of this file
- Ensure all tests are passed (or skipped)

### Offline test commands

Run the pure unit and config tests without any CyberArk environment:

```bash
uv run --group test pytest tests/test_config_value.py tests/test_utilities.py
```

Run the live integration tests only when the environment variables above are set:

```bash
uv run --group test pytest tests/test_accounts.py tests/test_cyberark.py tests/test_safe.py
```

Build the documentation locally with warnings treated as errors:

```bash
uv run --locked --extra docs sphinx-build -W -b html docs /tmp/aiobastion-docs
```

Documentation is built automatically for pushes and pull requests targeting
the `main` or `dev` branches. Read the Docs publishes the configured branch
after its build succeeds.

### Prepare CyberArk to Run the Testing
#### Test Accounts and Permissions
You need an API user, such as **"admin_bot"**, to run the testing. This account is similar to Administrator for
permissions, but you can't use "Administrator" itself (you will get "PASWS291E You cannot perform this
task with an Administrator user. Log on with a different user and try again" error)

The username of the API user you chose must be set in tests/__init__.py (and then just don't commit this file please.)

* In Private Ark Client:
  * Add to "Vault Admins" and "PVWAUsers" groups
  * Give "Add Safes, Audit Users, Add/Update Users, Reset Users' Passwords, Activate Users" authorizations rules.
  * Add to "admins" group (not sure this is needed)
  * Add as safe owners for the 3 test safes under user -> "Safe Ownership"
* In PVWA Browser:
  * Check "Advanced", "Safe Management", "Account Management" permissions for the 3 test safes.

Create more test accounts In PrivateArk client:
* Create "admin/Cyberark1" user
* Create "bastion_std_usr" and "bastion_test_usr" users with any random password
  * Add "bastion_test_usr" to "Vault Admins" group

In PVWA browser, add "bastion_test_usr" to "sample-it-dept" safe as Members, no special permission needed.

#### Platforms and Apps
With a freshly installed CyberArk,
* Activate "Oracle" platform
* Create and activate "sample_group" as a "group platform".

Finally, create two apps, "TestApp" and "TestApp2".

#### Load-balancer for Testing
You can use [HAproxy](https://www.haproxy.org/) as a load-balancer for testing. HAproxy supports both client IP hash
and affinity cookies, as shown below:
```aidl
backend my_backend
    mode http
    ## cookie based session affinity
    cookie SERVERID insert indirect nocache
    server backend1 ip_address_1:443 check cookie backend1 ssl verify none
    server backend2 ip_address_2:443 check cookie backend2 ssl verify none

#     ## hash based session affinity
#     stick-table type ip size 200k expire 30m
#     stick on src
#     server backend1 ip_address_1:443 check  ssl verify none
#     server backend2 ip_address_2:443 check ssl verify none
```
### Troubleshoot Test Issues
* `PASWS167E There are some invalid parameters`: The secrets should not include "," or "<".
* `PASWS159E Parameter [manualManagementReason] cannot be specified with parameter [enableAutomaticManagement]=[True]`: 
  all the test accounts the "manualManagementReason" need to be empty, if `enableAutomaticManagement == True`.
* `The number of concurrent dynamic sessions for user admin_bot has reached its limit (300)`: Make sure the tearDown
  logs off.
* `PASWS032E Platform [Oracle] is not active`: The Oracle platform is not activated.

## Update documentation

If your commit has an impact on documentation, please don't forget to update it accordingly.

## Releases

Releases are published to PyPI from GitHub Releases. Update the version in
`pyproject.toml`, merge the change, create a matching CalVer tag such as
`v2026.09.08a1`,
and publish the GitHub Release. The release workflow verifies that the tag and
package version match, builds both wheel and source distributions, checks them
with Twine, and publishes through PyPI Trusted Publishing.

The repository must be configured as a PyPI trusted publisher for the
`pypa/gh-action-pypi-publish` workflow, using the `pypi` GitHub environment.
No PyPI API token is stored in GitHub Actions.