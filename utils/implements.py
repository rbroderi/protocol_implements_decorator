from typing import Protocol
import inspect


class Printable(Protocol):
    def to_string(self):
        pass


def implements(protocol: Protocol):
    def add_bar_impl(cls):
        implements: set[str] = set()
        protocol_implements: set[str] = set()
        for name, method in inspect.getmembers(cls):
            if (not inspect.ismethod(method) and not inspect.isfunction(method)) or inspect.isbuiltin(method) or name.startswith("_"):
                continue
            implements.add(name)
        for name, method in inspect.getmembers(protocol):
            if (not inspect.ismethod(method) and not inspect.isfunction(method)) or inspect.isbuiltin(method) or name.startswith("_"):
                continue
            protocol_implements.add(name)
            if implements != protocol_implements:
                raise NotImplementedError(f"{protocol.__qualname__} requires implentation of {list(set(protocol_implements) - set(implements))!r}")
        return cls
    return add_bar_impl


@implements(Printable)
class Example:
    """Test class that should implement printable but doesn't."""
