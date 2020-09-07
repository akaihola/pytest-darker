"""Run ``setup.py check --metadata --restructuredtext`` on the package"""

from distutils.command.check import check  # type: ignore
from distutils.core import run_setup


def test_package(capsys):
    """The package metadata and description are valid"""
    distribution = run_setup("setup.py", stop_after="config")
    command = check(distribution)
    command.restructuredtext = 1
    command.run()
    assert capsys.readouterr().err == ''
