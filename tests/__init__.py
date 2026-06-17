import logging
import os
import unittest

def _env_flag(name: str) -> bool:
    return os.getenv(name, "").strip().lower() in {"1", "true", "yes", "on"}


INTEGRATION_TESTS_ENABLED = _env_flag("AIOBASTION_RUN_INTEGRATION_TESTS")

CONFIG = os.getenv("AIOBASTION_TEST_CONFIG", os.path.join("..", "..", "confs", "config_tests.yml")) if INTEGRATION_TESTS_ENABLED else None
AIM_CONFIG = os.getenv("AIOBASTION_TEST_AIM_CONFIG", os.path.join("..", "..", "confs", "config_aim_hp.yml")) if INTEGRATION_TESTS_ENABLED else None
API_USER = os.getenv("AIOBASTION_TEST_API_USER", "admin_test_restapi")


def require_integration_tests(config_path: str, env_var_name: str) -> str:
    if not INTEGRATION_TESTS_ENABLED:
        raise unittest.SkipTest(
            "Integration tests are disabled. Set AIOBASTION_RUN_INTEGRATION_TESTS=1 to enable them."
        )

    if not config_path:
        raise unittest.SkipTest(f"{env_var_name} is not set")

    if not os.path.exists(config_path):
        raise unittest.SkipTest(f"{env_var_name} does not exist: {config_path}")

    return config_path

logging.basicConfig(
    level=logging.DEBUG,
    # level=logging.INFO,
    format='%(asctime)s %(levelname)08s %(name)s %(message)s',
)