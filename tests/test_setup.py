# this package
import sphinxcontrib.default_values
from sphinxcontrib.default_values import __version__, process_default_format, process_docstring


class MockApp:

	def __init__(self):
		self.config_values = []
		self.directives = []
		self.connections = []

	def add_config_value(self, *args):
		self.config_values.append(args)

	def add_directive(self, *args):
		self.directives.append(args)

	def connect(self, *args):
		self.connections.append(args)


def test_setup():
	app = MockApp()

	assert sphinxcontrib.default_values.setup(app=app) == {  # type: ignore
		"version": __version__,
		"parallel_read_safe": True,
		"parallel_write_safe": True,
		}

	assert app.config_values == [("default_description_format", "Default %s", 'env')]
	assert app.connections == [
			("builder-inited", process_default_format),
			("autodoc-process-docstring", process_docstring),
			]
