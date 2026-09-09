"""Shared aiohttp session lifecycle and TLS configuration."""

import asyncio
import logging
import os
import ssl
from typing import Optional

import aiohttp

from .config import Config
from .exceptions import AiobastionException


logger = logging.getLogger("aiobastion")


class HttpSession:
    """Manage one endpoint's aiohttp session and concurrency limit."""

    def __init__(
        self,
        max_concurrent_tasks: int = Config.CYBERARK_DEFAULT_MAX_CONCURRENT_TASKS,
        timeout: int = Config.CYBERARK_DEFAULT_TIMEOUT,
    ):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.timeout = timeout
        self._session: Optional[aiohttp.ClientSession] = None
        self._sema: Optional[asyncio.Semaphore] = None
        self.request_params: Optional[dict] = None

    @property
    def semaphore(self) -> asyncio.Semaphore:
        if self._sema is None:
            self._sema = asyncio.Semaphore(self.max_concurrent_tasks)
        return self._sema

    def setup_ssl(self, verify: Optional[object] = None) -> None:
        """Build request SSL parameters from a CA setting."""
        if verify is None:
            verify = Config.CYBERARK_DEFAULT_VERIFY
        if not isinstance(verify, (str, bool)):
            raise AiobastionException(
                f"Invalid type for parameter 'verify': {type(verify)} value: {verify!r}"
            )

        if isinstance(verify, str):
            if not os.path.exists(verify):
                raise AiobastionException(f"CA certificate file not found {verify!r}")
            if os.path.isdir(verify):
                ssl_context = ssl.create_default_context(capath=verify)
            else:
                ssl_context = ssl.create_default_context(cafile=verify)
        elif verify:
            ssl_context = ssl.create_default_context()
        else:
            ssl_context = False

        self.request_params = {"timeout": self.timeout, "ssl": ssl_context}

    def setup_ssl_with_client_cert(
        self,
        verify: Optional[object],
        cert: str,
        key: Optional[str] = None,
        passphrase: Optional[str] = None,
    ) -> None:
        """Build request SSL parameters with an AIM client certificate."""
        if not os.path.exists(cert):
            raise AiobastionException(f"Public certificate file not found: {cert!r}")
        if key and not os.path.exists(key):
            raise AiobastionException(f"Private key certificate file not found: {key!r}")

        self.setup_ssl(verify)
        ssl_context = self.request_params["ssl"]
        if ssl_context is False:
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
        ssl_context.load_cert_chain(cert, keyfile=key, password=passphrase)
        self.request_params["ssl"] = ssl_context

    def get_session(
        self,
        token: Optional[str] = None,
        cookies: Optional[object] = None,
    ) -> aiohttp.ClientSession:
        """Return or create an authenticated or login-phase session."""
        if self._session is None or self._session.closed:
            headers = {
                "Content-type": "application/json",
                "Authorization": "None" if token is None else token,
            }
            self._session = aiohttp.ClientSession(headers=headers, cookies=cookies)
            logger.debug("Created HTTP session: %s", self._session)
        self.semaphore
        return self._session

    def get_anonymous_session(self) -> aiohttp.ClientSession:
        """Return or create a session without an Authorization header."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession()
            logger.debug("Created anonymous HTTP session: %s", self._session)
        self.semaphore
        return self._session

    async def close(self) -> None:
        """Close the endpoint session and reset its concurrency limiter."""
        if self._session is not None and not self._session.closed:
            await self._session.close()
        self._session = None
        self._sema = None