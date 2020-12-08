========
Usage
========

This extension shows the default values in autodoc-formatted docstrings.

The default behaviour of `autodoc <https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html>`_ is to turn this:

	.. code-block:: python

		def namedlist(name: str = "NamedList") -> Callable:
			"""
			A factory function to return a custom list subclass with a name.

			:param name: The name of the list.
			:default name: :py:obj:`True`

			:return:
			"""

into this:

	.. image:: before.png

With ``default_values`` enabled, the documentation will now look like this:

	.. image:: after.png


Default values are taken from the function/class signature.
They can be overridden using the ``:default <argname>: <default value>`` option in the docstring:

	.. code-block:: rest

		:param name: The name of the list.
		:default name: :py:obj:`True`

which will produce:

	.. image:: override.png

The value must be formatted how you would like it to be displayed in Sphinx.
This can be useful when the default value in the signature is :py:obj:`None`
and the true default value is assigned in the function body,
such as for a mutable default argument.

The default value can be suppressed using the ``:no-default <argname>`` option:

	.. code-block:: rest

		:param name: The name of the list.
		:no-default name:

	.. image:: before.png

This allows for default values to be suppressed on a per-argument basis.

|

No default value is shown if the argument does not have a default value.

The formatting of the default value can be customised using the
``default_description_format`` option in ``conf.py``.
By default this is ``'Default %s'``.
