import re
from pathlib import Path
from typing import Any, Optional, Tuple, Union, cast

import py
import pytest
import toml
from _pytest._code.code import ExceptionInfo, TerminalRepr
from _pytest.cacheprovider import Cache
from _pytest.config import Config
from _pytest.config.argparsing import Parser
from darker.__main__ import main

HISTKEY = "darker/mtimes"
PYTEST_7 = int(pytest.__version__.split(".")[0]) >= 7


class DarkerError(Exception):
    pass


class DarkerItem(pytest.Item):
    def __init__(self, path: Path, parent: pytest.Collector):
        if PYTEST_7:
            relative_path = path.relative_to(parent.config.rootpath)
        else:
            relative_path = Path(path).relative_to(parent.config.rootpath)
        super(DarkerItem, self).__init__(
            "DARKER", parent=parent, nodeid=f"{relative_path}::DARKER"
        )
        self.add_marker("darker")
        try:
            with open("pyproject.toml") as toml_file:
                self.pyproject = toml.load(toml_file)["tool"]["darker"]
        except Exception:
            self.pyproject = {}

    def setup(self) -> None:
        pytest.importorskip("darker")
        mtimes = getattr(self.config, "_darkermtimes", {})
        self._darkermtime = self.fspath.mtime()
        old = mtimes.get(str(self.fspath), 0)
        if self._darkermtime == old:
            pytest.skip("file(s) previously passed darker format checks")

        if self._skip_test():
            pytest.skip("file(s) excluded by pyproject.toml")

    def runtest(self) -> None:
        retval = main(
            [
                "--check",
                "--diff",
                "--quiet",
                str(self.fspath),
            ]
        )
        if retval != 0:
            raise DarkerError("Edited lines are not Black formatted")

        mtimes = getattr(self.config, "_darkermtimes", {})
        mtimes[str(self.fspath)] = self._darkermtime

    def repr_failure(  # type: ignore[override]
        self, excinfo: ExceptionInfo[BaseException]
    ) -> Union[str, TerminalRepr]:
        if excinfo.errisinstance(DarkerError):
            return cast(TerminalRepr, excinfo.value)
        return super(DarkerItem, self).repr_failure(excinfo)

    def reportinfo(self) -> Tuple[Union[py.path.local, str], Optional[int], str]:
        return self.fspath, -1, "Darker format check"

    def _skip_test(self) -> bool:
        return self._excluded() or (not self._included())

    def _included(self) -> bool:
        if "include" not in self.pyproject:
            return True
        return bool(re.search(self.pyproject["include"], str(self.fspath)))

    def _excluded(self) -> bool:
        if "exclude" not in self.pyproject:
            return False
        return bool(re.search(self.pyproject["exclude"], str(self.fspath)))


def pytest_addoption(parser: Parser) -> None:
    group = parser.getgroup("general")
    group.addoption(
        "--darker", action="store_true", help="enable format checking with darker"
    )


if PYTEST_7:

    def pytest_collect_file(
        file_path: Path, parent: pytest.Collector
    ) -> Optional[DarkerItem]:
        if parent.config.option.darker and file_path.suffix == ".py":
            return DarkerItem.from_parent(path=file_path, parent=parent)
        else:
            return None

else:

    def pytest_collect_file(
        path: py.path.local, parent: pytest.Collector
    ) -> Optional[DarkerItem]:
        if parent.config.option.darker and path.ext == ".py":
            return DarkerItem.from_parent(path=path, parent=parent)
        else:
            return None


def pytest_configure(config: Config) -> None:
    # load cached mtimes at session startup
    if config.option.darker and hasattr(config, "cache"):
        assert isinstance(config.cache, Cache)
        config._darkermtimes = config.cache.get(  # type: ignore[attr-defined]
            HISTKEY, {}
        )
    config.addinivalue_line("markers", "darker: enable format checking with darker")


def pytest_unconfigure(config: Config) -> None:
    # save cached mtimes at end of session
    if hasattr(config, "_darkermtimes"):
        assert isinstance(config.cache, Cache)
        config.cache.set(HISTKEY, config._darkermtimes)  # type: ignore[attr-defined]
