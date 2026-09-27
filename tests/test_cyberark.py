import sys
import asyncio
import os
import unittest
from unittest import IsolatedAsyncioTestCase, mock
import aiobastion
import tests


class TestEPV(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        tests.require_integration_tests(tests.CONFIG, "AIOBASTION_TEST_CONFIG")
        self.vault = aiobastion.EPV(tests.CONFIG)
        await self.vault.login()

    async def asyncTearDown(self):
        try:
            await self.vault.logoff()
        except Exception:
            # test_logoff
            pass

    async def test_logoff(self):
        await self.vault.logoff()
        self.assertFalse(await self.vault.check_token())

    async def test_login(self):
        await self.vault.login()
        self.assertTrue(await self.vault.check_token())

    async def test_login_aim(self):
        if (
            tests.AIM_CONFIG is None
            or tests.AIM_CONFIG == ""
            or not os.path.exists(tests.AIM_CONFIG)
        ):
            self.skipTest("AIM_CONFIG is not set in init file")
        await self.vault.logoff()
        self.assertFalse(await self.vault.check_token())
        self.vault = aiobastion.EPV(tests.AIM_CONFIG)
        await self.vault.login()
        self.assertTrue(await self.vault.check_token())
        await self.vault.close_session()

    async def test_check_token(self):
        self.assertTrue(await self.vault.check_token())

    async def test_inline_conf(self):
        self.skipTest("Need harcoded credentials")
        config = {"api_host": "pvwa.acme.fr"}

        production_vault = aiobastion.EPV(serialized=config)
        await production_vault.login("admin", "Cyberark1")
        async with production_vault as epv:
            print(await epv.safe.list())

    async def test_login_pvwa_only(self):
        self.skipTest("Need harcoded credentials")
        PVWA_CONFIG = "../../confs/config_test_pvwa_only.yml"
        self.vault = aiobastion.EPV(PVWA_CONFIG)
        await self.vault.login(
            username="admin", password=os.getenv("AIOBASTION_TEST_PASSWORD", "")
        )
        print(await self.vault.safe.list())
        self.assertTrue(await self.vault.check_token())

    def test_get_url(self):
        addr, head = self.vault.get_url("Accounts")
        self.assertIn("PasswordVault", addr)
        self.assertIn("Authorization", head)
        # self.fail()

    def test_to_json(self):
        serialized = self.vault.to_json()
        self.assertIsInstance(serialized, dict)
        # self.fail()

    async def test_handle_request(self):
        ret = await self.vault.handle_request(
            "get",
            "WebServices/PIMServices.svc/User",
            filter_func=lambda x: x["AgentUser"],
        )

        self.assertFalse(ret)


class _FakeResponse:
    status = 200

    async def read(self):
        return b""

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return False


class TestSerializedTokenOffline(IsolatedAsyncioTestCase):
    """Offline regression tests for EPV instances built from a serialized token (issue #2)."""

    async def test_check_token_sets_up_request_params(self):
        vault = aiobastion.EPV(
            serialized={"api_host": "pvwa.example.invalid", "token": "abc"}
        )
        self.assertIsNone(vault.request_params)

        calls = []

        def fake_request(session, method, url, **kwargs):
            calls.append((method, url, kwargs))
            return _FakeResponse()

        with mock.patch("aiohttp.ClientSession.request", new=fake_request):
            try:
                self.assertTrue(await vault.check_token())
            finally:
                await vault.close_session()

        self.assertEqual(len(calls), 1)
        method, url, kwargs = calls[0]
        self.assertEqual(method, "get")
        self.assertTrue(url.endswith("api/LoginsInfo"))
        self.assertIn("ssl", kwargs)
        self.assertIn("timeout", kwargs)

    async def test_context_manager_with_valid_serialized_token(self):
        with mock.patch(
            "aiohttp.ClientSession.request", new=lambda *a, **kw: _FakeResponse()
        ):
            async with aiobastion.EPV(
                serialized={"api_host": "pvwa.example.invalid", "token": "abc"}
            ) as vault:
                self.assertIsNotNone(vault.request_params)


if __name__ == "__main__":
    if sys.platform == "win32":
        # Turned out, using WindowsSelectorEventLoop has functionality issues such as:
        #     Can't support more than 512 sockets
        #     Can't use pipe
        #     Can't use subprocesses
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    unittest.main()
