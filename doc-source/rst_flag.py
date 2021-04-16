# stdlib
import re
from typing import Any, Dict, cast

# 3rd party
from sphinx import addnodes
from sphinx.addnodes import desc_signature
from sphinx.application import Sphinx
from sphinx.domains import ObjType
from sphinx.domains.rst import ReSTDomain, ReSTMarkup
from sphinx.locale import _
from sphinx.roles import XRefRole
from sphinx.util.nodes import make_id


class ReSTFlag(ReSTMarkup):
	"""
	Description of a reST directive.
	"""

	def handle_signature(self, sig: str, signode: desc_signature) -> str:
		try:
			name, argument = re.split(r'\s*:\s+', sig.strip(), 1)
		except ValueError:
			name, argument = sig, None

		signode += addnodes.desc_name(f':{name}:', f':{name}:')
		if argument:
			signode += addnodes.desc_annotation(' ' + argument, ' ' + argument)
		if self.options.get("type"):
			text = f' ({self.options["type"]})'
			signode += addnodes.desc_annotation(text, text)
		return name

	def add_target_and_index(self, name: str, sig: str, signode: desc_signature) -> None:
		domain = cast(ReSTDomain, self.env.get_domain("rst"))

		prefix = self.objtype
		objname = re.match("([A-Za-z-_]*) <([A-Za-z-_]*)>", name).group(1)

		node_id = make_id(self.env, self.state.document, prefix, name)
		signode["ids"].append(node_id)

		# Assign old styled node_id not to break old hyperlinks (if possible)
		# Note: Will be removed in Sphinx-5.0 (RemovedInSphinx50Warning)
		old_node_id = self.make_old_id(name)
		if old_node_id not in self.state.document.ids and old_node_id not in signode["ids"]:
			signode["ids"].append(old_node_id)

		self.state.document.note_explicit_target(signode)
		domain.note_object(self.objtype, objname, node_id, location=signode)

		key = name[0].upper()
		text = _(":%s: (flag)") % name
		self.indexnode["entries"].append(("single", text, node_id, '', key))


def setup(app: Sphinx) -> Dict[str, Any]:
	"""
	Setup Sphinx Extension.

	:param app: The Sphinx app.
	"""

	app.add_directive_to_domain("rst", "flag", ReSTFlag)
	app.add_role_to_domain("rst", "flag", XRefRole())
	ReSTDomain.object_types["flag"] = ObjType(_("flag"), "flag")

	return {"parallel_read_safe": True}
