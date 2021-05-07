###############
default_values
###############

.. start short_desc

.. documentation-summary::

.. end short_desc

.. start shields

.. only:: html

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
		  - |codefactor| |actions_flake8| |actions_mypy|
		* - Other
		  - |license| |language| |requires|

	.. |docs| rtfd-shield::
		:project: default_values
		:alt: Documentation Build Status

	.. |docs_check| actions-shield::
		:workflow: Docs Check
		:alt: Docs Check Status

	.. |actions_linux| actions-shield::
		:workflow: Linux
		:alt: Linux Test Status

	.. |actions_windows| actions-shield::
		:workflow: Windows
		:alt: Windows Test Status

	.. |actions_macos| actions-shield::
		:workflow: macOS
		:alt: macOS Test Status

	.. |actions_flake8| actions-shield::
		:workflow: Flake8
		:alt: Flake8 Status

	.. |actions_mypy| actions-shield::
		:workflow: mypy
		:alt: mypy status

	.. |requires| requires-io-shield::
		:alt: Requirements Status

	.. |coveralls| coveralls-shield::
		:alt: Coverage

	.. |codefactor| codefactor-shield::
		:alt: CodeFactor Grade

	.. |pypi-version| pypi-shield::
		:project: default_values
		:version:
		:alt: PyPI - Package Version

	.. |supported-versions| pypi-shield::
		:project: default_values
		:py-versions:
		:alt: PyPI - Supported Python Versions

	.. |supported-implementations| pypi-shield::
		:project: default_values
		:implementations:
		:alt: PyPI - Supported Implementations

	.. |wheel| pypi-shield::
		:project: default_values
		:wheel:
		:alt: PyPI - Wheel

	.. |conda-version| image:: https://img.shields.io/conda/v/domdfcoding/default_values?logo=anaconda
		:target: https://anaconda.org/domdfcoding/default_values
		:alt: Conda - Package Version

	.. |conda-platform| image:: https://img.shields.io/conda/pn/domdfcoding/default_values?label=conda%7Cplatform
		:target: https://anaconda.org/domdfcoding/default_values
		:alt: Conda - Platform

	.. |license| github-shield::
		:license:
		:alt: License

	.. |language| github-shield::
		:top-language:
		:alt: GitHub top language

	.. |commits-since| github-shield::
		:commits-since: v0.4.3
		:alt: GitHub commits since tagged version

	.. |commits-latest| github-shield::
		:last-commit:
		:alt: GitHub last commit

	.. |maintained| maintained-shield:: 2021
		:alt: Maintenance

	.. |pypi-downloads| pypi-shield::
		:project: default_values
		:downloads: month
		:alt: PyPI - Downloads

.. end shields

Overview
-----------

This extension shows the default values in autodoc-formatted docstrings.

The default behaviour of :mod:`~sphinx.ext.autodoc` is to turn this:

	.. code-block:: python

		def namedlist(name: str = "NamedList") -> Callable:
			"""
			A factory function to return a custom list subclass with a name.

			:param name: The name of the list.

			:return:
			"""

into this:

	.. image:: usage/before.png

With ``default_values`` enabled, the documentation will now look like this:

	.. image:: usage/after.png


Default values are taken from the function/class signature.
They can be overridden using the :rst:field:`default` option in the docstring.
The default value can be suppressed using the :rst:field:`no-default` option.

No default value is shown if the argument does not have a default value.

The formatting of the default value can be customised using the
:confval:`default_description_format` option in ``conf.py``.
By default this is ``'Default %s'``.


.. _autodoc: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html

Contents
-----------

.. html-section::

.. toctree::
	:hidden:

	Home<self>

.. toctree::
	:maxdepth: 3

	usage/installation
	usage/configuration
	docs
	demo
	Source

.. toctree::
	:caption: Links
	:hidden:

	GitHub <https://github.com/sphinx-toolbox/default_values>
	PyPI <https://pypi.org/project/default_values>
	Contributing Guide <https://contributing-to-sphinx-toolbox.readthedocs.io/en/latest/>

.. start links

.. only:: html

	View the :ref:`Function Index <genindex>` or browse the `Source Code <_modules/index.html>`__.

	:github:repo:`Browse the GitHub Repository <sphinx-toolbox/default_values>`

.. end links
