============================================================================
 pytest-darker – A pytest plugin for checking of modified code using Darker
============================================================================

|travis-badge|_ |license-badge|_ |pypi-badge|_ |downloads-badge|_ |black-badge|_ |changelog-badge|_

.. |travis-badge| image:: https://travis-ci.com/akaihola/pytest-darker.svg?branch=master
.. _travis-badge: https://travis-ci.com/akaihola/pytest-darker
.. |license-badge| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
.. _license-badge: https://github.com/akaihola/pytest-darker/blob/master/LICENSE.rst
.. |pypi-badge| image:: https://img.shields.io/pypi/v/pytest-darker
.. _pypi-badge: https://pypi.org/project/pytest-darker/
.. |downloads-badge| image:: https://pepy.tech/badge/pytest-darker
.. _downloads-badge: https://pepy.tech/project/pytest-darker
.. |black-badge| image:: https://img.shields.io/badge/code%20style-black-000000.svg
.. _black-badge: https://github.com/psf/black
.. |changelog-badge| image:: https://img.shields.io/badge/-change%20log-purple
.. _changelog-badge: https://github.com/akaihola/pytest-darker/blob/master/CHANGES.rst

Requirements
============

* Pytest_
* Darker_

There is a minimum requirement of Darker_ 1.1.0 later.


Installation
============

::

    $ pip install pytest-darker


Usage
=====

To run pytest with checks provided by Darker_::

    $ pytest --darker

The plugin will output a diff of suggested formatting changes from Black_ (if any exist).
Changes will _not_ be applied automatically.


Customizing Black and isort behavior
====================================

Project-specific default options for Black_ and isort_
are read from the project's ``pyproject.toml`` file in the repository root.
isort_ also looks for a few other places for configuration.

For more details, see:

- `Black documentation about pyproject.toml`_
- `Black example configuration`_
- `isort documentation about config files`_



Testing
=======

To run the tests against a selection of Python interpreters::

    $ tox

To run against a specific interpreter (e.g. Python 3.6)::

    $ tox -e py36

The ``tox.ini`` file in the root of this repository
is used to configure the test environment.


License
=======

Distributed under the terms of the ``BSD`` license,
`pytest-darker` is free and open source software.


Issues
======

If you encounter any problems, please file an issue
in the `pytest-darker issue tracker`_ along with a detailed description.

.. _Darker: https://github.com/akaihola/darker
.. _Pytest: https://docs.pytest.org/
.. _pytest-darker issue tracker: https://github.com/akaihola/pytest-darker/issues
.. _Black: https://github.com/python/black
.. _isort: https://pypi.org/project/isort/
.. _Black documentation about pyproject.toml: https://black.readthedocs.io/en/stable/pyproject_toml.html
.. _Black example configuration: https://github.com/ambv/black/blob/master/pyproject.toml
.. _isort documentation about config files: https://timothycrosley.github.io/isort/docs/configuration/config_files/
.. _command line arguments: https://black.readthedocs.io/en/stable/installation_and_usage.html#command-line-options

GitHub stars trend
==================

|stargazers|_

.. |stargazers| image:: https://starchart.cc/akaihola/pytest-darker.svg
.. _stargazers: https://starchart.cc/akaihola/pytest-darker
