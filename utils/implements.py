"""Adds the implements and protocol decorators."""
import inspect
from typing import Any, Callable, Protocol, List


def protocol(cls: type[Any]):
    """A class decorator that signifies that this class is a protocol and adds
    the __protocols_implemented__ attribute."""
    try:
        protocols_implemented: set[str] = getattr(
            cls, "__protocols_implemented__"
        )
        protocols_implemented.add(protocol.__qualname__)
    except AttributeError:
        setattr(cls, "__protocols_implemented__", {protocol.__qualname__})
    return cls


def implements(protocol: type[Any]) -> Callable[..., Any]:
    """A class decorator that signifies that this class implements the
    specified protocol."""

    def inner(cls: type[Any]):
        """Inner wrapper."""
        implements: set[str] = set()
        protocol_implements: set[str] = set()
        NO_NEED_TO_IMPLEMENT: List[str] = []
        for name, method in inspect.getmembers(Protocol):
            if inspect.isbuiltin(method):
                continue
            NO_NEED_TO_IMPLEMENT.append(name)
        NO_NEED_TO_IMPLEMENT.append("__subclasshook__")

        # set implented protocols appending if needed.
        try:
            protocols_implemented: set[str] = getattr(
                cls, "__protocols_implemented__"
            )
            protocols_implemented.add(protocol.__qualname__)
        except AttributeError:
            setattr(cls, "__protocols_implemented__", {protocol.__qualname__})

        # get set of methods and attributes implemented by class
        for name, method in inspect.getmembers(cls):
            if inspect.isbuiltin(method) or name in NO_NEED_TO_IMPLEMENT:
                continue
            implements.add(name)

        # get set of methods and attributes implemented by protocol
        for name, method in inspect.getmembers(protocol):
            if inspect.isbuiltin(method) or name in NO_NEED_TO_IMPLEMENT:
                continue
            protocol_implements.add(name)

        # if the set of protocol methods and attributes is not a subset of
        # implemented methods and attributes raise error
        if not protocol_implements.issubset(implements):
            raise NotImplementedError(
                f"{protocol.__qualname__} requires implentation of"
                f" {list(set(protocol_implements) - set(implements))!r}"
            )
        return cls

    return inner


# ***********************************


def main():
    """Run some tests on the functionality of the decorators."""

    @protocol
    class Printable(Protocol):
        """A test protocol that requires a to_string method."""

        def to_string(self) -> str:
            return ""

    @protocol
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

    assert fail

    @implements(Printable)
    class Example2:
        """Test class that does implement Printable."""

        def to_string(self) -> str:
            return str(self)

    @implements(Otherable)
    @implements(Printable)
    class Example3:
        """Test class that should implements printable but doesn't use
        dectorator."""

        def to_string(self) -> str:
            return str(self)

        def other(self) -> str:
            return str(self)

    def testUsage(o: Printable):
        print(o.to_string())
        pass

    test = Example3()
    # TODO any way to fix has no attribute "__protocols_implemented__ mypy error?
    print(test.__protocols_implemented__)
    testUsage(test)


if __name__ == "__main__":
    main()
