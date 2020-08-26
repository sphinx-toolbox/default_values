#!/usr/bin/env python3
#
#  __init__.py
"""
A Sphinx directive to specify that a module has extra requirements, and show how to install them.
"""
#
#  Copyright © 2020 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#
# Based on https://github.com/agronholm/sphinx-autodoc-typehints
# Copyright (c) Alex Grönholm
# MIT Licensed
#

# stdlib
import inspect
import re
import string
import typing
from typing import Any, Dict, Union

# 3rd party
from docutils.nodes import document
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.parsers import RSTParser
from sphinx.util.inspect import signature as Signature

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"

__license__: str = "MIT"
__version__: str = "0.0.8"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = ["process_docstring", "process_default_format", "setup"]


def process_docstring(app: Sphinx, what, name, obj, options, lines: typing.List[str]) -> None:
	"""
	Add default values to the docstring.

	:param app:
	:param what:
	:type what:
	:param name:
	:type name:
	:param obj:
	:type obj:
	:param options:
	:type options:
	:param lines: List of strings representing the current contents of the docstring.
	"""

	# Size varies depending on docutils config
	a_tab = " " * app.config.docutils_tab_width  # type: ignore

	if isinstance(obj, property):
		return None

	if callable(obj):
		if inspect.isclass(obj):
			obj = getattr(obj, "__init__")

		obj = inspect.unwrap(obj)

		try:
			signature = Signature(obj)
		except ValueError:
			return None

		default_description_format: str = app.config.default_description_format  # type: ignore

		for argname, param in signature.parameters.items():
			if argname.endswith('_'):
				argname = f"{argname[:-1]}\\_"

			default_value = param.default
			formatted_annotation = None

			# Get the default value from the signature
			if default_value is not inspect._empty:  # type: ignore

				if isinstance(default_value, bool):
					formatted_annotation = f":py:obj:`{default_value}`"
				elif default_value is None:
					formatted_annotation = f":py:obj:`None`"
				elif isinstance(default_value, str):
					formatted_annotation = f"``'{default_value.replace(' ', '␣')}'``"
				else:
					formatted_annotation = f"``{default_value!r}``"

			# Check if the user has overridden the default value in the docstring
			default_searchfor = [f":{field} {argname}:" for field in ("default", "Default")]

			for i, line in enumerate(lines):
				for search_string in default_searchfor:
					if line.startswith(search_string):
						formatted_annotation = line.split(search_string)[-1].lstrip(" ")
						lines.remove(line)
						break

			# Check the user hasn't turned the default argument off
			no_default_searchfor = re.compile(fr"^:(No|no)[-_](default|Default) {argname}:")

			for i, line in enumerate(lines):
				if no_default_searchfor.match(line):
					formatted_annotation = None
					break

			# Add the default value
			searchfor = [f":{field} {argname}:" for field in ("param", "parameter", "arg", "argument")]
			insert_index = None

			for i, line in enumerate(lines):
				if any(line.startswith(search_string) for search_string in searchfor):
					insert_index = i
					break

			if formatted_annotation is not None:
				if insert_index is not None:

					# Look ahead to find the index of the next unindented line, and insert before it.
					for idx, line in enumerate(lines[insert_index + 1:]):
						if not line.startswith("    "):

							# Ensure the previous line has a fullstop at the end.
							if lines[insert_index + idx][-1] not in ".,;:":
								lines[insert_index + idx] += '.'

							lines.insert(
									insert_index + 1 + idx,
									f"{a_tab}{default_description_format % formatted_annotation}."
									)
							break

		# Remove all remaining :default *: lines
		for i, line in enumerate(lines):
			if re.match(r"^:(default|Default) ", line):
				lines.remove(line)

		# Remove all remaining :no-default *: lines
		for i, line in enumerate(lines):
			if re.match(r"^:(No|no)[-_](default|Default) ", line):
				lines.remove(line)

	return None


def process_default_format(app: Sphinx) -> None:
	"""
	Prepare the formatting of the default value.

	:param app:
	:type app:
	"""

	default_description_format: str = app.config.default_description_format  # type: ignore

	# Check the substitution is in the string and is preceded by whitespace, or is at the beginning of the string
	if "%s" in default_description_format:
		if re.search(r"[^\s]%s", default_description_format) and not default_description_format.startswith("%s"):
			default_description_format = default_description_format.replace("%s", " %s")
	else:
		# Add the substitution to the end.
		if default_description_format[-1] not in string.whitespace:
			default_description_format += " %s"
		else:
			default_description_format += "%s"

	app.config.default_description_format = default_description_format  # type: ignore


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app:

	:return:
	"""

	# Custom formatting for the default value indication
	app.add_config_value("default_description_format", "Default %s", "env")
	app.connect("builder-inited", process_default_format)
	app.connect("autodoc-process-docstring", process_docstring)

	# Hack to get the docutils tab size, as there doesn't appear to be any other way
	class CustomRSTParser(RSTParser):

		def parse(self, inputstring: Union[str, StringList], document: document) -> None:
			app.config.docutils_tab_width = document.settings.tab_width  # type: ignore
			super().parse(inputstring, document)

	app.add_source_parser(CustomRSTParser, override=True)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
