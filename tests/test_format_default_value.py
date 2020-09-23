# stdlib
import inspect
import json
import re

# 3rd party
import pytest

# this package
import sphinxcontrib.default_values
from sphinxcontrib.default_values import format_default_value


@pytest.mark.parametrize(
		"value, expects",
		[
				(json, ":mod:`json`"),
				(pytest, ":mod:`pytest`"),
				(sphinxcontrib.default_values, ":mod:`sphinxcontrib.default_values`"),
				(format_default_value, ":py:func:`sphinxcontrib.default_values.format_default_value`"),
				(json.dumps, ":py:func:`json.dumps`"),
				(json.JSONEncoder, ":py:class:`json.encoder.JSONEncoder`"),
				(str, ":py:class:`str`"),
				(chr, ":py:func:`chr`"),
				(True, ":py:obj:`True`"),
				(False, ":py:obj:`False`"),
				(None, ":py:obj:`None`"),
				("True", "``'True'``"),
				("False", "``'False'``"),
				("None", "``'None'``"),
				("Hello", "``'Hello'``"),
				("Hello World", "``'Hello World'``"),
				(" ", "``'␣'``"),
				("\t", "``'\\t'``"),
				(1234, "``1234``"),
				("1234", "``'1234'``"),
				(Ellipsis, None),
				(inspect.Signature.empty, None),
				(re.compile(".*"), "``re.compile('.*')``"),
				(re.compile(".*", flags=re.ASCII), "``re.compile('.*', re.ASCII)``"),
				]
		)
def test_format_default_value(value, expects):
	assert format_default_value(value) == expects
