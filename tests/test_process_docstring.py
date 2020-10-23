# stdlib
from decimal import Decimal
from textwrap import dedent
from typing import Any, Callable, Dict, List, Optional, Tuple

# 3rd party
import attr
import pytest
from domdf_python_tools.utils import strtobool

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
		self.config.docutils_tab_width = 4
		self.config.default_description_format = format_


def namedlist(name: str = "NamedList") -> Callable:
	pass


@pytest.fixture()
def app():
	return MockApp("Default %s")


def test_process_docstring(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list.",
			'',
			":return:",
			]

	process_docstring(app, '', '', namedlist, {}, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list.",
			"    Default ``'NamedList'``.",
			'',
			":return:",
			'',
			]


def test_process_docstring_override(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list.",
			":default name: py:obj:`True`",
			'',
			":return:",
			]

	process_docstring(app, '', '', namedlist, {}, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list.",
			"    Default py:obj:`True`.",
			'',
			":return:",
			'',
			]


def test_process_docstring_suppress(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list.",
			":no-default name:",
			'',
			":return:",
			]

	process_docstring(app, '', '', namedlist, {}, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list.",
			'',
			":return:",
			'',
			]


def test_process_docstring_missing_fullstop(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list",
			'',
			":return:",
			]

	process_docstring(app, '', '', namedlist, {}, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list.",
			"    Default ``'NamedList'``.",
			'',
			":return:",
			'',
			]


def test_process_docstring_redundant_defaults(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list",
			":default foo: bar",
			'',
			":return:",
			]

	process_docstring(app, '', '', namedlist, {}, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			'',
			":param name: The name of the list.",
			"    Default ``'NamedList'``.",
			'',
			":return:",
			'',
			]


def test_process_docstring_underscores(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			'',
			r":param name\_: The name of the list",
			":default foo: bar",
			'',
			":return:",
			]

	def underscore(name_: str = "NamedList") -> Callable:
		pass

	process_docstring(app, '', '', underscore, {}, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			'',
			r":param name\_: The name of the list.",
			"    Default ``'NamedList'``.",
			'',
			":return:",
			'',
			]


def test_process_docstring_underscores_class(app):
	lines = [
			"A factory function to return a custom list subclass with a name.",
			'',
			r":param name\_: The name of the list",
			":default foo: bar",
			'',
			":return:",
			]

	class Underscore:

		def __init__(self, name_: str = "NamedList"):
			pass

	process_docstring(app, '', '', Underscore, {}, lines)

	assert lines == [
			"A factory function to return a custom list subclass with a name.",
			'',
			r":param name\_: The name of the list.",
			"    Default ``'NamedList'``.",
			'',
			":return:",
			'',
			]


def test_process_docstring_multiple_arguments(app):
	lines = [
			"Does something.",
			'',
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			'',
			]

	def my_func(foo, bar=None, show=True, coloured_output=False):
		pass

	process_docstring(app, '', '', my_func, {}, lines)

	assert lines == [
			"Does something.",
			'',
			":param foo: An argument.",
			":param bar: Another argument.",
			"    Default :py:obj:`None`.",
			":param show: Whether to print the result.",
			"    Default :py:obj:`True`.",
			":param coloured_output: Whether to use coloured output.",
			"    Default :py:obj:`False`.",
			'',
			]


def test_process_docstring_no_final_newline(app):
	lines = [
			"Does something.",
			'',
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			]

	def my_func(foo, bar=None, show=True, coloured_output=False):
		pass

	process_docstring(app, '', '', my_func, {}, lines)

	assert lines == [
			"Does something.",
			'',
			":param foo: An argument.",
			":param bar: Another argument.",
			"    Default :py:obj:`None`.",
			":param show: Whether to print the result.",
			"    Default :py:obj:`True`.",
			":param coloured_output: Whether to use coloured output.",
			"    Default :py:obj:`False`.",
			'',
			]


def test_process_docstring_property(app):
	lines = [
			"Does something.",
			'',
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			'',
			]

	class MyClass:

		@property
		def my_prop(self) -> None:
			return None

	process_docstring(app, '', '', MyClass.my_prop, {}, lines)

	assert lines == [
			"Does something.",
			'',
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			'',
			]


def test_process_docstring_class(app):
	lines = [
			"Does something.",
			'',
			":param foo: An argument.",
			":param bar: Another argument.",
			":param show: Whether to print the result.",
			":param coloured_output: Whether to use coloured output.",
			'',
			]

	class MyClass:

		def __init__(self, foo, bar=None, show=True, coloured_output=False):
			pass

	process_docstring(app, '', '', MyClass, {}, lines)

	assert lines == [
			"Does something.",
			'',
			":param foo: An argument.",
			":param bar: Another argument.",
			"    Default :py:obj:`None`.",
			":param show: Whether to print the result.",
			"    Default :py:obj:`True`.",
			":param coloured_output: Whether to use coloured output.",
			"    Default :py:obj:`False`.",
			'',
			]


def test_process_docstring_demo(app):
	lines = [
			":param a: No default.",
			":param b: A float.",
			":param c: An empty string.",
			":param d: A space (or a smiley face?)",
			":param e: A string.",
			":param f: A Tuple.",
			":param g: A Decimal.",
			":param h: An int.",
			":param i: Default None.",
			":param j: Overridden default.",
			":default j: ``[]``",
			":param k: Suppressed default.",
			":no-default k:",
			":param l: This is a really long description.",
			"    It spans multiple lines.",
			"    The quick brown fox jumps over the lazy dog.",
			"    The default value should be added at the end regardless.",
			":param m: Tab.",
			":param n: This argument's default value is undefined.",
			'',
			]

	def demo(
			a: Any,
			b: float = 0.0,
			c: str = '',
			d: str = ' ',
			e: str = "hello world",
			f: Tuple = (),
			g: Decimal = Decimal("12.34"),
			h: int = 1234,
			i: Optional[List[str]] = None,
			j: Optional[List[str]] = None,
			k: Optional[List[str]] = None,
			l: str = '',
			m: str = "\t",
			n: Any = ...,
			):
		pass

	process_docstring(app, '', '', demo, {}, lines)

	assert lines == [
			":param a: No default.",
			":param b: A float.",
			"    Default ``0.0``.",
			":param c: An empty string.",
			"    Default ``''``.",
			":param d: A space (or a smiley face?).",
			"    Default ``'␣'``.",
			":param e: A string.",
			"    Default ``'hello world'``.",
			":param f: A Tuple.",
			"    Default ``()``.",
			":param g: A Decimal.",
			"    Default ``Decimal('12.34')``.",
			":param h: An int.",
			"    Default ``1234``.",
			":param i: Default None.",
			"    Default :py:obj:`None`.",
			":param j: Overridden default.",
			"    Default ``[]``.",
			":param k: Suppressed default.",
			":param l: This is a really long description.",
			"    It spans multiple lines.",
			"    The quick brown fox jumps over the lazy dog.",
			"    The default value should be added at the end regardless.",
			"    Default ``''``.",
			":param m: Tab.",
			r"    Default ``'\t'``.",
			":param n: This argument's default value is undefined.",
			'',
			]


@attr.s(slots=True)
class Device:
	"""
	Represents a device in a :class:`~.AcqMethod:`.

	:param device_id: The ID of the device
	:param display_name: The display name for the device.
	:param rc_device: Flag to indicate the device is an RC Device. If :py:obj:`False` the device is an SCIC.
	:param configuration: List of key: value mappings for configuration options.
	"""

	device_id: str = attr.ib(converter=str)
	display_name: str = attr.ib(converter=str)
	rc_device: bool = attr.ib(converter=strtobool, default=False)
	configuration: List[Dict[str, Any]] = attr.ib(converter=list, default=attr.Factory(list))


def test_process_docstring_attrs(app):
	lines = dedent(Device.__doc__).split("\n")  # type: ignore

	process_docstring(app, '', '', Device, {}, lines)

	assert lines == [
			'',
			"Represents a device in a :class:`~.AcqMethod:`.",
			'',
			":param device_id: The ID of the device",
			":param display_name: The display name for the device.",
			":param rc_device: Flag to indicate the device is an RC Device. If :py:obj:`False` the device is an SCIC.",
			"    Default :py:obj:`False`.",
			":param configuration: List of key: value mappings for configuration options.",
			"    Default ``[]``.",
			'',
			]
