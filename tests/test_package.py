import pathlib
import unittest
import warnings

import cyberark_async


class TestPackage(unittest.TestCase):
    """Offline checks on the package surface and source hygiene (issue #10)."""

    def test_all_names_are_exported(self):
        self.assertIn("EPV", cyberark_async.__all__)
        for name in cyberark_async.__all__:
            with self.subTest(name=name):
                self.assertTrue(hasattr(cyberark_async, name))

    def test_star_import_matches_all(self):
        namespace = {}
        exec("from cyberark_async import *", namespace)
        namespace.pop("__builtins__")
        self.assertEqual(set(namespace), set(cyberark_async.__all__))

    def test_old_exception_names_are_aliases(self):
        self.assertIs(
            cyberark_async.AiobastionException, cyberark_async.CyberarkAsyncException
        )
        self.assertIs(
            cyberark_async.AiobastionConfigurationException,
            cyberark_async.CyberarkAsyncConfigurationException,
        )
        self.assertNotIn("AiobastionException", cyberark_async.__all__)

    def test_sources_compile_without_syntax_warnings(self):
        package_dir = pathlib.Path(cyberark_async.__file__).parent
        for path in sorted(package_dir.glob("*.py")):
            with self.subTest(path=path.name), warnings.catch_warnings():
                warnings.simplefilter("error", SyntaxWarning)
                compile(path.read_text(encoding="utf-8"), str(path), "exec")


if __name__ == "__main__":
    unittest.main()
