# 3rd party
from sphinx.events import EventListener
from sphinx_toolbox.testing import Sphinx, run_setup

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

	def add_source_parser(self, *args, **kwargs):
		pass


def test_setup():

	app: Sphinx
	setup_ret, directives, roles, additional_nodes, app = run_setup(sphinxcontrib.default_values.setup)

	assert setup_ret == {
			"version": __version__,
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}

	assert app.config.values["default_description_format"] == ("Default %s", "env", [str])

	assert app.events.listeners == {
			"builder-inited": [EventListener(id=0, handler=process_default_format, priority=500)],
			"autodoc-process-docstring": [EventListener(id=1, handler=process_docstring, priority=500)],
			}
