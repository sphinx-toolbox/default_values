# stdlib
from typing import Callable

# 3rd party
import pytest

# this package
from sphinxcontrib.default_values import process_docstring


class MockConfig(dict):

	def __getattr__(self, item):
		return self[item]

	def __setattr__(self, key, value):
		self[key] = value


class MockApp:

	def __init__(self, format_):
		self.config = MockConfig()
		self.config.default_description_format = format_


def namedlist(name: str = "NamedList") -> Callable:
	pass


@pytest.fixture()
def app():
	return MockApp("Default %s")


def test_process_docstring(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list.",
			"",
			":return:",
			]

	process_docstring(app, None, None, namedlist, None, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list.",
			"\tDefault ``'NamedList'``.",
			"",
			":return:",
			]


def test_process_docstring_override(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list.",
			":default name: py:obj:`True`",
			"",
			":return:",
			]

	process_docstring(app, None, None, namedlist, None, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list.",
			"\tDefault py:obj:`True`.",
			"",
			":return:",
			]


def test_process_docstring_suppress(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list.",
			":no-default name:",
			"",
			":return:",
			]

	process_docstring(app, None, None, namedlist, None, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list.",
			"",
			":return:",
			]


def test_process_docstring_missing_fullstop(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list",
			"",
			":return:",
			]

	process_docstring(app, None, None, namedlist, None, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list.",
			"\tDefault ``'NamedList'``.",
			"",
			":return:",
			]


def test_process_docstring_redundant_defaults(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list",
			":default foo: bar",
			"",
			":return:",
			]

	process_docstring(app, None, None, namedlist, None, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name: The name of the list.",
			"\tDefault ``'NamedList'``.",
			"",
			":return:",
			]


def test_process_docstring_underscores(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name\\_: The name of the list",
			":default foo: bar",
			"",
			":return:",
			]

	def underscore(name_: str = "NamedList") -> Callable:
		pass

	process_docstring(app, None, None, underscore, None, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			"",
			":param name\\_: The name of the list.",
			"\tDefault ``'NamedList'``.",
			"",
			":return:",
			]


def test_process_docstring_multiple_arguments(app):
	lines = [
			"Does something.",
			"",
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			"",
			]

	def my_func(foo, bar=None, show=True, coloured_output=False):
		pass

	process_docstring(app, None, None, my_func, None, lines)

	assert lines == [
			"Does something.",
			"",
			":param foo: An argument.",
			":param bar: Another argument.",
			"\tDefault :py:obj:`None`.",
			":param show: Whether to print the result.",
			"\tDefault :py:obj:`True`.",
			":param coloured_output: Whether to use coloured output.",
			"\tDefault :py:obj:`False`.",
			"",
			]


def test_process_docstring_property(app):
	lines = [
			"Does something.",
			"",
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			"",
			]

	class MyClass:

		@property
		def my_prop(self) -> None:
			return None

	process_docstring(app, None, None, MyClass.my_prop, None, lines)

	assert lines == [
			"Does something.",
			"",
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			"",
			]


def test_process_docstring_class(app):
	lines = [
			"Does something.",
			"",
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			"",
			]

	class MyClass:

		def __init__(self, foo, bar=None, show=True, coloured_output=False):
			pass

	process_docstring(app, None, None, MyClass, None, lines)

	assert lines == [
			"Does something.",
			"",
			":param foo: An argument.",
			":param bar: Another argument.",
			"\tDefault :py:obj:`None`.",
			":param show: Whether to print the result.",
			"\tDefault :py:obj:`True`.",
			":param coloured_output: Whether to use coloured output.",
			"\tDefault :py:obj:`False`.",
			"",
			]
