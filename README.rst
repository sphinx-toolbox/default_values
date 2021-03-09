###############
default_values
###############

.. start short_desc

**Sphinx extension to show default values in documentation.**

.. end short_desc


.. start shields

.. list-table::
	:stub-columns: 1
	:widths: 10 90

	* - Docs
	  - |docs| |docs_check|
	* - Tests
	  - |actions_linux| |actions_windows| |actions_macos| |coveralls|
	* - PyPI
	  - |pypi-version| |supported-versions| |supported-implementations| |wheel|
	* - Anaconda
	  - |conda-version| |conda-platform|
	* - Activity
	  - |commits-latest| |commits-since| |maintained| |pypi-downloads|
	* - QA
	  - |codefactor| |actions_flake8| |actions_mypy| |pre_commit_ci|
	* - Other
	  - |license| |language| |requires|

.. |docs| image:: https://img.shields.io/readthedocs/default_values/latest?logo=read-the-docs
	:target: https://default_values.readthedocs.io/en/latest
	:alt: Documentation Build Status

.. |docs_check| image:: https://github.com/sphinx-toolbox/default_values/workflows/Docs%20Check/badge.svg
	:target: https://github.com/sphinx-toolbox/default_values/actions?query=workflow%3A%22Docs+Check%22
	:alt: Docs Check Status

.. |actions_linux| image:: https://github.com/sphinx-toolbox/default_values/workflows/Linux/badge.svg
	:target: https://github.com/sphinx-toolbox/default_values/actions?query=workflow%3A%22Linux%22
	:alt: Linux Test Status

.. |actions_windows| image:: https://github.com/sphinx-toolbox/default_values/workflows/Windows/badge.svg
	:target: https://github.com/sphinx-toolbox/default_values/actions?query=workflow%3A%22Windows%22
	:alt: Windows Test Status

.. |actions_macos| image:: https://github.com/sphinx-toolbox/default_values/workflows/macOS/badge.svg
	:target: https://github.com/sphinx-toolbox/default_values/actions?query=workflow%3A%22macOS%22
	:alt: macOS Test Status

.. |actions_flake8| image:: https://github.com/sphinx-toolbox/default_values/workflows/Flake8/badge.svg
	:target: https://github.com/sphinx-toolbox/default_values/actions?query=workflow%3A%22Flake8%22
	:alt: Flake8 Status

.. |actions_mypy| image:: https://github.com/sphinx-toolbox/default_values/workflows/mypy/badge.svg
	:target: https://github.com/sphinx-toolbox/default_values/actions?query=workflow%3A%22mypy%22
	:alt: mypy status

.. |requires| image:: https://requires.io/github/sphinx-toolbox/default_values/requirements.svg?branch=master
	:target: https://requires.io/github/sphinx-toolbox/default_values/requirements/?branch=master
	:alt: Requirements Status

.. |coveralls| image:: https://img.shields.io/coveralls/github/sphinx-toolbox/default_values/master?logo=coveralls
	:target: https://coveralls.io/github/sphinx-toolbox/default_values?branch=master
	:alt: Coverage

.. |codefactor| image:: https://img.shields.io/codefactor/grade/github/sphinx-toolbox/default_values?logo=codefactor
	:target: https://www.codefactor.io/repository/github/sphinx-toolbox/default_values
	:alt: CodeFactor Grade

.. |pypi-version| image:: https://img.shields.io/pypi/v/default_values
	:target: https://pypi.org/project/default_values/
	:alt: PyPI - Package Version

.. |supported-versions| image:: https://img.shields.io/pypi/pyversions/default_values?logo=python&logoColor=white
	:target: https://pypi.org/project/default_values/
	:alt: PyPI - Supported Python Versions

.. |supported-implementations| image:: https://img.shields.io/pypi/implementation/default_values
	:target: https://pypi.org/project/default_values/
	:alt: PyPI - Supported Implementations

.. |wheel| image:: https://img.shields.io/pypi/wheel/default_values
	:target: https://pypi.org/project/default_values/
	:alt: PyPI - Wheel

.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/default_values?logo=anaconda
	:target: https://anaconda.org/domdfcoding/default_values
	:alt: Conda - Package Version

.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/default_values?label=conda%7Cplatform
	:target: https://anaconda.org/domdfcoding/default_values
	:alt: Conda - Platform

.. |license| image:: https://img.shields.io/github/license/sphinx-toolbox/default_values
	:target: https://github.com/sphinx-toolbox/default_values/blob/master/LICENSE
	:alt: License

.. |language| image:: https://img.shields.io/github/languages/top/sphinx-toolbox/default_values
	:alt: GitHub top language

.. |commits-since| image:: https://img.shields.io/github/commits-since/sphinx-toolbox/default_values/v0.4.3
	:target: https://github.com/sphinx-toolbox/default_values/pulse
	:alt: GitHub commits since tagged version

.. |commits-latest| image:: https://img.shields.io/github/last-commit/sphinx-toolbox/default_values
	:target: https://github.com/sphinx-toolbox/default_values/commit/master
	:alt: GitHub last commit

.. |maintained| image:: https://img.shields.io/maintenance/yes/2021
	:alt: Maintenance

.. |pypi-downloads| image:: https://img.shields.io/pypi/dm/default_values
	:target: https://pypi.org/project/default_values/
	:alt: PyPI - Downloads

.. |pre_commit_ci| image:: https://results.pre-commit.ci/badge/github/sphinx-toolbox/default_values/master.svg
	:target: https://results.pre-commit.ci/latest/github/sphinx-toolbox/default_values/master
	:alt: pre-commit.ci status

.. end shields

|

Installation
--------------

.. start installation

``default_values`` can be installed from PyPI or Anaconda.

To install with ``pip``:

.. code-block:: bash

	$ python -m pip install default_values

To install with ``conda``:

	* First add the required channels

	.. code-block:: bash

		$ conda config --add channels http://conda.anaconda.org/conda-forge
		$ conda config --add channels http://conda.anaconda.org/domdfcoding

	* Then install

	.. code-block:: bash

		$ conda install default_values

.. end installation
