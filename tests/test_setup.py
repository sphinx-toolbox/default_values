# stdlib
from types import SimpleNamespace
from typing import Any, Tuple

# 3rd party
import sphinx
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


# https://github.com/sphinx-toolbox/sphinx-toolbox/blob/d1750cf9d19f8f5e7fc5e408f0b50164ac9fad63/tests/common.py#L32
def get_app_config_values(config: Any) -> Tuple[str, str, Any]:
	if sphinx.version_info >= (7, 3):
		valid_types = config.valid_types
		default = config.default
		rebuild = config.rebuild
	else:
		default, rebuild, valid_types = config

	if isinstance(valid_types, (set, frozenset, tuple, list)):
		valid_types = sorted(valid_types)

	if hasattr(valid_types, "_candidates"):
		new_valid_types = SimpleNamespace()
		new_valid_types.candidates = sorted(valid_types._candidates)
		valid_types = new_valid_types

	return (default, rebuild, valid_types)


def test_setup():

	app: Sphinx
	setup_ret, directives, roles, additional_nodes, app = run_setup(sphinxcontrib.default_values.setup)

	assert setup_ret == {
			"version": __version__,
			"parallel_read_safe": True,
			"parallel_write_safe": True,
			}

	assert get_app_config_values(app.config.values["default_description_format"]) == ("Default %s", "env", [str])

	assert app.events.listeners == {
			"builder-inited": [EventListener(id=0, handler=process_default_format, priority=500)],
			"autodoc-process-docstring": [EventListener(id=1, handler=process_docstring, priority=500)],
			}
