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
from types import BuiltinFunctionType, FunctionType, ModuleType
from typing import Any, Callable, Dict, Iterator, List, Mapping, Optional, Pattern, Tuple, Type, Union

# 3rd party
from docutils.nodes import document
from docutils.statemachine import StringList
from sphinx.application import Sphinx
from sphinx.parsers import RSTParser
from sphinx.util.inspect import signature as Signature

try:
	# 3rd party
	import attr
except ImportError:  # pragma: no cover
	# attrs is used in a way that it is only required in situations
	# where it is available to import, so its fine to do this.
	pass

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020 Dominic Davis-Foster"

__license__: str = "MIT"
__version__: str = "0.3.1"
__email__: str = "dominic@davis-foster.co.uk"

__all__ = [
		"process_docstring",
		"process_default_format",
		"setup",
		"get_class_defaults",
		"get_function_defaults",
		"default_regex",
		"no_default_regex",
		"get_arguments",
		"format_default_value",
		]

#: Regular expression to match default values declared in docstrings.
default_regex: Pattern = re.compile(r"^:(default|Default) ")

#: Regular expression to match flags in docstrings to suppress default values.
no_default_regex: Pattern = re.compile(r"^:(No|no)[-_](default|Default) ")


def escape_trailing__(string: str) -> str:
	"""
	Returns the given string with trailing underscores escaped to prevent Sphinx treating them as references.

	:param string:
	"""

	if string.endswith('_'):
		return f"{string[:-1]}\\_"
	return string


def format_default_value(value: Any) -> Optional[str]:
	"""
	Format the value as a string.

	:param value:

	.. versionadded:: 0.3.1
	"""

	if value is not inspect.Signature.empty and value is not Ellipsis:

		if isinstance(value, ModuleType):
			return f":mod:`{value.__name__}`"
		elif isinstance(value, BuiltinFunctionType):
			return f":py:func:`{value.__name__}`"
		elif isinstance(value, FunctionType):
			return f":py:func:`{value.__module__}.{value.__name__}`"
		elif inspect.isclass(value):
			if value.__module__ == "builtins":
				return f":py:class:`{value.__name__}`"
			else:
				return f":py:class:`{value.__module__}.{value.__name__}`"
		elif isinstance(value, bool):
			return f":py:obj:`{value}`"
		elif value is None:
			return ":py:obj:`None`"
		elif isinstance(value, str):
			return f"``{value.replace(' ', '␣')!r}``"
		else:
			return f"``{value!r}``"

	return None


def process_docstring(
		app: Sphinx,
		what: str,
		name: str,
		obj: Any,
		options: Dict[str, Any],
		lines: List[str],
		) -> None:
	"""
	Add default values to the docstring.

	:param app: The Sphinx app.
	:param what:
	:param name: The name of the object being documented.
	:param obj: The object being documented.
	:param options: Mapping of autodoc options to values.
	:param lines: List of strings representing the current contents of the docstring.
	"""

	if isinstance(obj, property):
		return None

	# Size varies depending on docutils config
	a_tab = " " * app.config.docutils_tab_width  # type: ignore

	if callable(obj):

		if not lines or lines[-1]:
			lines.append('')

		default_getter: Union[Callable[[Type], _defaults], Callable[[Callable], _defaults]]

		if inspect.isclass(obj):
			default_getter = get_class_defaults
		else:
			default_getter = get_function_defaults

		default_description_format: str = app.config.default_description_format  # type: ignore

		for argname, default_value in default_getter(obj):
			argname = escape_trailing__(argname)

			# Get the default value from the signature
			formatted_annotation = format_default_value(default_value)

			# Check if the user has overridden the default value in the docstring
			default_searchfor = re.compile(fr"^:[dD]efault {re.escape(argname)}:")
			for i, line in enumerate(lines):
				if default_searchfor.match(line):
					formatted_annotation = ":".join(line.split(":")[2:]).lstrip()
					lines.remove(line)
					break

			# Check the user hasn't turned the default argument off
			no_default_searchfor = re.compile(fr"^:(No|no)[-_](default|Default) {re.escape(argname)}:")
			for i, line in enumerate(lines):
				if no_default_searchfor.match(line):
					formatted_annotation = None
					break

			# Add the default value
			insert_index = None

			# TODO: sphinx.domains.python.PyObject.doc_field_types
			param_searchfor = re.compile(fr"^:(param|parameter|arg|argument) {re.escape(argname)}:")
			for i, line in enumerate(lines):
				if param_searchfor.match(line):
					insert_index = i
					break

			if formatted_annotation is not None:
				if insert_index is not None:

					# Look ahead to find the index of the next unindented line, and insert before it.
					for idx, line in enumerate(lines[insert_index + 1:]):
						if not line.startswith(a_tab):

							# Ensure the previous line has a fullstop at the end.
							line_content = ":".join(lines[insert_index + idx].split(":")[2:]).strip()
							if line_content and line_content[-1] not in ".,;:":
								lines[insert_index + idx] += '.'

							lines.insert(
									insert_index + 1 + idx,
									f"{a_tab}{default_description_format % formatted_annotation}."
									)
							break

		# Remove all remaining :default *: lines
		for i, line in enumerate(lines):
			if default_regex.match(line):
				lines.remove(line)

		# Remove all remaining :no-default *: lines
		for i, line in enumerate(lines):
			if no_default_regex.match(line):
				lines.remove(line)

	return None


_defaults = Iterator[Tuple[str, Any]]


def get_class_defaults(obj: Type) -> _defaults:
	"""
	Obtains the default values for the arguments of a class.

	:param obj: The class.

	:return: An iterator of 2-element tuples comprising the argument name and its default value.
	"""

	# TODO: handle __new__

	for argname, param in get_arguments(getattr(obj, "__init__")).items():
		default_value = param.default

		if hasattr(obj, "__attrs_attrs__"):
			# Special casing for attrs classes
			if default_value is attr.NOTHING:
				for value in obj.__attrs_attrs__:
					if value.name == argname and isinstance(value.default, attr.Factory):  # type: ignore
						default_value = value.default.factory()

		yield argname, default_value

	return None


def get_function_defaults(obj: Callable) -> _defaults:
	"""
	Obtains the default values for the arguments of a function.

	:param obj: The function.

	:return: An iterator of 2-element tuples comprising the argument name and its default value.
	"""

	for argname, param in get_arguments(obj).items():
		yield argname, param.default

	return None


def get_arguments(obj: Callable) -> Mapping[str, inspect.Parameter]:
	"""
	Returns a dictionary mapping argument names to parameters/arguments for a function.

	:param obj: A function (can be the ``__init__`` method of a class).
	"""

	try:
		signature = Signature(inspect.unwrap(obj))
	except ValueError:  # pragma: no cover
		return {}

	return signature.parameters


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
	app.add_config_value("default_description_format", "Default %s", "env", [str])
	app.connect("builder-inited", process_default_format)
	app.connect("autodoc-process-docstring", process_docstring)

	# Hack to get the docutils tab size, as there doesn't appear to be any other way
	class CustomRSTParser(RSTParser):

		def parse(self, inputstring: Union[str, StringList], document: document) -> None:  # pragma: no cover
			app.config.docutils_tab_width = document.settings.tab_width  # type: ignore
			super().parse(inputstring, document)

	app.add_source_parser(CustomRSTParser, override=True)

	return {
			"version": __version__,
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}
