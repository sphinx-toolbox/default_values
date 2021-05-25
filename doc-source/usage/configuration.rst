================
Configuration
================

.. confval:: default_description_format
	:type: :class:`str`
	:required: False
	:default: Default %s

	The format string for the default value.

Fields
---------

These fields can be used in docstrings for classes, functions, methods etc., alongside other fields such as ``:param:``.

.. rst:field:: default <name>: value

	Overrides the default value for ``<name>``.

	The value must be formatted how you would like it to be displayed in Sphinx.
	This can be useful when the default value in the signature is :py:obj:`None`
	and the true default value is assigned in the function body,
	such as for a mutable default argument.

	**Example:**

	.. code-block:: rest

		:param name: The name of the list.
		:default name: :py:obj:`True`

	.. function:: domdf_python_tools.bases.namedlist (name='NamedList')
		:noindex:

		A factory function to return a custom list subclass with a name.

		:param name: The name of the list. Default :py:obj:`True`.
		:type name: :class:`str`

		:rtype: :class:`~typing.Callable`

..	.. image:: override.png


.. rst:field:: no-default <name>: value

	Suppresses display of the default value for ``<name>``.

	This allows for default values to be suppressed on a per-argument basis.

	**Example:**

	.. code-block:: rest

		:param name: The name of the list.
		:no-default name:

	.. function:: domdf_python_tools.bases.namedlist (name='NamedList')
		:noindex:

		A factory function to return a custom list subclass with a name.

		:param name: The name of the list.
		:type name: :class:`str`

		:rtype: :class:`~typing.Callable`

..	.. image:: before.png
