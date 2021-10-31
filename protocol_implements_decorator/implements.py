"""Adds the implements and protocol decorators."""
import inspect
from typing import Any, Callable, Protocol, List, Tuple, Type, Set


def __implements(protocol: Type[Any]) -> Callable[..., Any]:
    """A class decorator that signifies that this class implements the
    specified protocol."""

    def inner(cls: Type[Any]):
        """Inner wrapper."""
        implements: Set[Tuple[str, Any]] = set()
        protocol_implements: Set[Tuple[str, Any]] = set()
        NO_NEED_TO_IMPLEMENT: List[str] = []
        for name, method in inspect.getmembers(Protocol):
            if inspect.isbuiltin(method):
                continue
            NO_NEED_TO_IMPLEMENT.append(name)
        NO_NEED_TO_IMPLEMENT.append("__subclasshook__")

        # set implented protocols appending if needed.
        try:
            protocols_implemented: Set[str] = getattr(
                cls, "__protocols_implemented__"
            )
            protocols_implemented.add(protocol.__qualname__)
        except AttributeError:
            setattr(cls, "__protocols_implemented__", {protocol.__qualname__})

        def get_protocols_implemented(cls: Type[Any]) -> Tuple[str, ...]:
            return tuple(sorted(cls.__protocols_implemented__))

        setattr(cls, "get_protocols_implemented", get_protocols_implemented)

        sig: Any
        # get set of methods and attributes implemented by class
        for name, method in inspect.getmembers(cls):
            if inspect.isbuiltin(method) or name in NO_NEED_TO_IMPLEMENT:
                continue
            if inspect.isfunction(method) or inspect.ismethod(method):
                sig = inspect.signature(method)
            else:
                sig = "ATTRIBUTE"
            implements.add((name, sig))

        # get set of methods and attributes implemented by protocol
        for name, method in inspect.getmembers(protocol):
            if inspect.isbuiltin(method) or name in NO_NEED_TO_IMPLEMENT:
                continue
            if inspect.isfunction(method) or inspect.ismethod(method):
                sig = inspect.signature(method)
            else:
                sig = "ATTRIBUTE"
            protocol_implements.add((name, sig))

        # if the set of protocol methods and attributes is not a subset of
        # implemented methods and attributes raise error
        if not protocol_implements.issubset(implements):
            raise NotImplementedError(
                f"{protocol.__qualname__} requires implentation of"
                f" {list(set(protocol_implements) - set(implements))!r}"
            )
        return cls

    return inner


def implements(*args: Type[Any]):
    def wrapped(func: Callable[..., Any]):
        for arg in reversed(args):
            func = __implements(arg)(func)
        return func

    return wrapped


# ***********************************
