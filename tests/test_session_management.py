import sys
import asyncio
import random
import secrets
import unittest
from unittest import TestCase, IsolatedAsyncioTestCase
import aiobastion
from aiobastion.exceptions import CyberarkAPIException, CyberarkException, AiobastionException
from aiobastion.accounts import PrivilegedAccount
import tests
import time


@unittest.skipUnless(tests.INTEGRATION_TESTS_ENABLED, "Integration tests are disabled. Set AIOBASTION_RUN_INTEGRATION_TESTS=1.")
class TestSessionManagement(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        tests.require_integration_tests(tests.AIM_CONFIG, "AIOBASTION_TEST_AIM_CONFIG")
        self.vault = aiobastion.EPV(tests.AIM_CONFIG)
        await self.vault.login()

    async def asyncTearDown(self):
        await self.vault.close_session()

    async def test_get_all_connection_components(self):
        all_cc = await self.vault.session_management.get_all_connection_components()
        self.assertGreater(all_cc["Total"], 5)

if __name__ == '__main__':
    if sys.platform == 'win32':
        # Turned out, using WindowsSelectorEventLoop has functionality issues such as:
        #     Can't support more than 512 sockets
        #     Can't use pipe
        #     Can't use subprocesses
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    unittest.main()
