# type:ignore  # noqa: PGH003
# pylint: skip-file
"""Test cases for the functionality of the protocolimplementsdecorator package."""

from typing import Protocol

from protocolimplementsdecorator import implements


def test() -> None:
    """Run some tests on the functionality of the decorators."""

    class Printable(Protocol):
        """A test protocol that requires a to_string method."""

        def to_string(self) -> str:
            return ""

    class Otherable(Protocol):
        """Another example."""

        def other(self) -> str:
            return ""

    fail: bool = False
    try:

        @implements(Printable)
        class Example:
            """Test class that should implement printable but doesn't."""

    except NotImplementedError:
        fail = True
        pass

    assert fail  # noqa: S101

    @implements(Printable)
    class Example2:
        """Test class that does implement Printable."""

        def to_string(self) -> str:
            return str(self)

    fail = False

    @implements(Printable, Otherable)
    class Example4:
        """Test class that uses multiple protocols."""

        __slots__ = ()

        def to_string(self) -> str:
            return str(self)

        def other(self) -> str:
            return str(self)

    test = Example4()

    print(test.get_protocols_implemented())
