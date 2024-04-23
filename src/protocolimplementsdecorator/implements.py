"""Adds the implements and protocol decorators."""

import functools
import inspect
from collections.abc import Callable
from typing import Any
from typing import Protocol
from typing import TypeVar

FuncT = TypeVar("FuncT", bound=Callable[..., Any])


def __implements(protocol: FuncT) -> Callable[[FuncT], FuncT]:  # noqa: C901
    @functools.wraps(protocol)
    def inner(cls: FuncT) -> FuncT:  # noqa: C901, PLR0912
        """Inner wrapper."""
        implements_set: set[tuple[str, Any]] = set()
        protocol_implements: set[tuple[str, Any]] = set()
        no_need_to_implement: list[str] = []
        for name, method in inspect.getmembers(Protocol):
            if inspect.isbuiltin(method):
                continue
            no_need_to_implement.append(name)
        no_need_to_implement.extend(
            (
                "__subclasshook__",
                "__annotations__",
                "__weakref__",
                "__dict__",
            ),
        )

        # set implemented protocols appending if needed.
        temp = getattr(
            cls,
            "__protocols_implemented__",
            None,
        )
        if temp is None:
            temp = {protocol.__qualname__}
        protocols_implemented: set[str] = temp
        protocols_implemented.add(protocol.__qualname__)
        cls.__protocols_implemented__ = protocols_implemented  # type:ignore[attr-defined]

        def get_protocols_implemented(cls: type[Any]) -> tuple[str, ...]:
            return tuple(sorted(cls.__protocols_implemented__))

        cls.get_protocols_implemented = get_protocols_implemented  # type:ignore[attr-defined]

        sig: Any
        # get set of methods and attributes implemented by class
        for name, method in inspect.getmembers(cls):
            # special case __str__ and __repr__
            if (
                name == "__str__"
                and cls.__str__ != object.__str__
                or name == "__repr__"
                and cls.__repr__ != object.__repr__
            ):
                sig = inspect.signature(method)

            elif inspect.isbuiltin(method) or name in no_need_to_implement:
                continue
            elif inspect.isfunction(method) or inspect.ismethod(method):
                sig = inspect.signature(method)
            else:
                sig = "ATTRIBUTE"
            implements_set.add((name, sig))

        # get set of methods and attributes implemented by protocol
        for name, method in inspect.getmembers(protocol):
            # special case __str__ and __repr__
            if (
                name == "__str__"
                and protocol.__str__ != object.__str__
                or name == "__repr__"
                and protocol.__repr__ != object.__repr__
            ):
                sig = inspect.signature(method)
            elif inspect.isbuiltin(method) or name in no_need_to_implement:
                continue
            elif inspect.isfunction(method) or inspect.ismethod(method):
                sig = inspect.signature(method)
            else:
                sig = "ATTRIBUTE"
            protocol_implements.add((name, sig))

        # if the set of protocol methods and attributes is not a subset of
        # implemented methods and attributes raise error
        if not protocol_implements.issubset(implements_set):
            msg = (
                f"{protocol.__qualname__} requires implementation of"
                f" {list(set(protocol_implements) - set(implements_set))!r}"
            )
            raise NotImplementedError(
                msg,
            )
        return cls

    return inner


def implements(*args: Any) -> Callable[[FuncT], FuncT]:
    """Check if a class implements a given protocol.

    :param args: The protocols to check for implementation.
    :type args: Any

    :return: The inner wrapper function.
    :rtype: Callable[[FuncT], FuncT]

    :raises NotImplementedError: If the class does not implement all the methods and
            attributes required by the protocol.

    """

    def wrapped(func: FuncT) -> FuncT:
        for arg in reversed(args):
            func = __implements(arg)(func)
        return func

    return wrapped
