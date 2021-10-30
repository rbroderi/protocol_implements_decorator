import inspect
from typing import Any, Callable, Protocol, Type, TypeVar

_T = TypeVar("_T", bound="object")
_Tp = TypeVar("_Tp", bound="Protocol")


class Printable(Protocol):
    def to_string(self):
        pass

    def _private_method(self):
        pass


def implements(
    protocol: Type[_Tp], require_private: bool = False
) -> Callable[..., Any]:
    def inner(cls: Type[_T]):
        implements: set[str] = set()
        protocol_implements: set[str] = set()
        NO_NEED_TO_IMPLEMENT = (
            "__class_getitem__",
            "__init__",
            "__subclasshook__",
            "__init_subclass__",
        )

        for name, method in inspect.getmembers(cls):
            if not require_private and name.startswith("_"):
                continue
            if (
                (
                    not inspect.ismethod(method)
                    and not inspect.isfunction(method)
                )
                or inspect.isbuiltin(method)
                or name in NO_NEED_TO_IMPLEMENT
            ):
                continue
            implements.add(name)
        for name, method in inspect.getmembers(protocol):
            if not require_private and name.startswith("_"):
                continue
            if (
                (
                    not inspect.ismethod(method)
                    and not inspect.isfunction(method)
                )
                or inspect.isbuiltin(method)
                or name in NO_NEED_TO_IMPLEMENT
            ):
                continue
            protocol_implements.add(name)
        if implements != protocol_implements:
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

        pass


except NotImplementedError:
    fail = True
    pass

assert fail

fail: bool = False
try:

    @implements(Printable)
    class Example2:
        """Test class that does implement Printable."""

        def to_string(self):
            return "str(self)"


except NotImplementedError:
    fail = True
    pass

assert not fail


fail: bool = False
try:

    @implements(Printable, require_private=True)
    class Example3:
        """Test class that does implement Printable but not private methods."""

        def to_string(self):
            return "str(self)"


except NotImplementedError:
    fail = True
    pass

assert fail
