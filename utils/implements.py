import inspect
from typing import Any, Callable, Protocol


def protocol(cls: type[Any]):
    try:
        protocols_implemented: set[str] = getattr(
            cls, "__protocols_implemented__"
        )
        protocols_implemented.add(protocol.__qualname__)
    except AttributeError:
        setattr(cls, "__protocols_implemented__", {protocol.__qualname__})
    return cls


@protocol
class Printable(Protocol):
    def to_string(self) -> str:
        return ""


@protocol
class Otherable(Protocol):
    def other(self) -> str:
        return ""


def implements(protocol: type[Any]) -> Callable[..., Any]:
    def inner(cls: type[Any]):
        implements: set[str] = set()
        protocol_implements: set[str] = set()
        NO_NEED_TO_IMPLEMENT = (
            "__class_getitem__",
            "__init__",
            "__subclasshook__",
            "__init_subclass__",
        )

        try:
            protocols_implemented: set[str] = getattr(
                cls, "__protocols_implemented__"
            )
            protocols_implemented.add(protocol.__qualname__)
        except AttributeError:
            setattr(cls, "__protocols_implemented__", {protocol.__qualname__})

        for name, method in inspect.getmembers(cls):
            if name.startswith("_") and name != "__protocols_implemented__":
                continue
            if inspect.isbuiltin(method) or name in NO_NEED_TO_IMPLEMENT:
                continue
            implements.add(name)
        for name, method in inspect.getmembers(protocol):
            if name.startswith("_") and name != "__protocols_implemented__":
                continue
            if inspect.isbuiltin(method) or name in NO_NEED_TO_IMPLEMENT:
                continue
            protocol_implements.add(name)
        if not protocol_implements.issubset(implements):
            raise NotImplementedError(
                f"{protocol.__qualname__} requires implentation of"
                f" {list(set(protocol_implements) - set(implements))!r}"
            )
        return cls

    return inner


fail: bool = False
try:

    @implements(Printable)
    class Example:
        """Test class that should implement printable but doesn't."""


except NotImplementedError:
    fail = True
    pass

assert fail

fail = False
try:

    @implements(Printable)
    class Example2:
        """Test class that does implement Printable."""

        def to_string(self) -> str:
            return str(self)


except NotImplementedError:
    fail = True
    pass

assert not fail


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
