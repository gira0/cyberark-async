import sys
import asyncio
import os
import random
import secrets
import unittest
from unittest import TestCase, IsolatedAsyncioTestCase
import aiobastion
from aiobastion.exceptions import CyberarkAPIException, CyberarkException, AiobastionException
from aiobastion.accounts import PrivilegedAccount
from aiobastion.utilities import clone_privileged_account, case_insensitive_getattr
import tests
import time


class TestUtilitiesPure(TestCase):
    def test_case_insensitive_getattr(self):
        class Dummy:
            SomeValue = 123

        self.assertEqual(case_insensitive_getattr(Dummy(), "somevalue"), 123)

    def test_clone_privileged_account_does_not_mutate_original(self):
        account = PrivilegedAccount(
            "name",
            "platform",
            "safe",
            address="1.2.3.4",
            userName="admin",
            platformAccountProperties={"foo": "bar"},
        )

        cloned = clone_privileged_account(account, {"address": "5.6.7.8", "custom": "value"})

        self.assertEqual(account.address, "1.2.3.4")
        self.assertEqual(cloned.address, "5.6.7.8")
        self.assertEqual(cloned.platformAccountProperties["custom"], "value")
        self.assertEqual(cloned.name, "5.6.7.8-admin")

    def test_privileged_account_rejects_invalid_secret_type(self):
        with self.assertRaises(AiobastionException):
            PrivilegedAccount("name", "platform", "safe", secretType="invalid")


class TestUtilities(IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        tests.require_integration_tests(tests.CONFIG, "AIOBASTION_TEST_CONFIG")
        self.vault = aiobastion.EPV(tests.CONFIG)
        await self.vault.login()

        self.test_safe = "sample-it-dept"

    async def asyncTearDown(self):
        # await self.vault.close_session()
        await self.vault.logoff()

    async def get_random_account(self, n=1):
        accounts = await self.vault.account.search_account_by(
            safe=self.test_safe
        )
        self.assertGreaterEqual(len(accounts), 1)
        if n == 1:
            return random.choice(accounts)
        else:
            return random.choices(accounts, k=n)

    async def test_clone_account(self):
        account = await self.get_random_account()

        await self.vault.utils.clone_address(account.address, {"address": "new_add", "IPCible": "127"})

    async def test_semaphore(self):
        self.skipTest("This test is not relevant for daily usage")
        for i in (1, 10, 20, 30, 40, 50):
            tasklist = []
            start = time.time()
            # await self.vault.account.search_account_by(safe=self.test_safe)

            for _ in range(0, i):
                tasklist.append(self.vault.account.search_account_by(safe=self.test_safe))

            await asyncio.gather(*tasklist)
            end = time.time()

            print(f"Took {end - start} for {i} requests")


    async def test_dump_all_users_details(self):
        start = time.time()

        all_user_list = await self.vault.user.list()
        all_user_details = await asyncio.gather(*[self.vault.user.details(_u) for _u in all_user_list])
        end = time.time()

        print(f"Good logic took {end - start} seconds")

        start = time.time()
        all_user_list = await self.vault.user.list()
        for _u in all_user_list:
            await self.vault.user.details(_u)

        end = time.time()

        print(f"Bad logic took {end - start} seconds")


class TestPlatformUtilies(IsolatedAsyncioTestCase):

    async def test_count_platform(self):
        self.skipTest("This test takes too long to execute")
        qualif = aiobastion.EPV(tests.AIM_CONFIG)

        async with qualif:
            for c in await qualif.utils.platform.count_platforms():
                print(c)

    async def test_connection_component_usage(self):
        self.skipTest("This test takes too long to execute")
        qualif = aiobastion.EPV(tests.AIM_CONFIG)

        async with qualif:
            for c in await qualif.utils.platform.connection_component_usage():
                print(c)

if __name__ == '__main__':
    if sys.platform == 'win32':
        # Turned out, using WindowsSelectorEventLoop has functionality issues such as:
        #     Can't support more than 512 sockets
        #     Can't use pipe
        #     Can't use subprocesses
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    unittest.main()
