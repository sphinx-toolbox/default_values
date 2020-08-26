# stdlib
from decimal import Decimal  # pragma: no cover
from typing import Any, List, Optional, Tuple  # pragma: no cover

__all__ = ["demo"]  # pragma: no cover


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
		):  # pragma: no cover
	"""

	:param a: No default.
	:param b: A float.
	:param c: An empty string.
	:param d: A space (or a smiley face?)
	:param e: A string.
	:param f: A Tuple.
	:param g: A Decimal.
	:param h: An int.
	:param i: Default None.
	:param j: Overridden default.
	:default j: ``[]``
	:param k: Suppressed default.
	:no-default k:
	:param l: This is a really long description.
		It spans multiple lines.
		The quick brown fox jumps over the lazy dog.
		The default value should be added at the end regardless.


	The description for ``d`` lacked a fullstop at the end, but one was added automatically.
	"""
