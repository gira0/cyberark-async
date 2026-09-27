import os
from unittest.mock import patch

import pytest

import cyberark_async


@pytest.mark.asyncio
async def test_logins_info_contract_through_prism():
    prism_url = os.getenv("CYBERARK_ASYNC_PRISM_URL")
    if not prism_url:
        pytest.skip("CYBERARK_ASYNC_PRISM_URL is not set")

    vault = cyberark_async.EPV(serialized={"api_host": "example.invalid"})
    vault.request_params = {"timeout": 10, "ssl": None}
    url = f"{prism_url.rstrip('/')}/api/LoginsInfo"
    headers = {"Content-type": "application/json", "Authorization": "None"}

    try:
        with patch.object(vault, "get_url", return_value=(url, headers)):
            response = await vault.handle_request("get", "api/LoginsInfo")
        assert "LastSuccessLoginTime" in response
        assert "FailedLogins" in response
    finally:
        await vault.close_session()
