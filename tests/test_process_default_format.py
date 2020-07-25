# 3rd party
import pytest

# this package
from sphinxcontrib.default_values import process_default_format


class MockConfig(dict):

	def __getattr__(self, item):
		return self[item]

	def __setattr__(self, key, value):
		self[key] = value


class MockApp:

	def __init__(self, format_):
		self.config = MockConfig()
		self.config.default_description_format = format_


@pytest.mark.parametrize(
		"value, expects",
		[
				("Default %s", "Default %s"),
				("Default%s", "Default %s"),
				("Default", "Default %s"),
				("Default: %s", "Default: %s"),
				("Default:%s", "Default: %s"),
				("Default:", "Default: %s"),
				("default %s", "default %s"),
				("default%s", "default %s"),
				("default", "default %s"),
				("The default value is %s", "The default value is %s"),
				("The default value is%s", "The default value is %s"),
				("The default value is", "The default value is %s"),
				("The default value is\t", "The default value is\t%s"),
				("The default value is  ", "The default value is  %s"),
				("%s is the default value", "%s is the default value"),
				# TODO: Does it fail if there's no space after %s?
				]
		)
def test_process_default_format(value, expects):
	app = MockApp(value)
	process_default_format(app)
	assert app.config.default_description_format == expects
