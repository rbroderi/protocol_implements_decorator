Protocol Implements Decorator
================================================
<!-- [![GitHub License](https://img.shields.io/github/license/rbroderi/Verbex)](https://github.com/rbroderi/Verbex/blob/master/LICENSE) -->
[![Generic badge](https://img.shields.io/badge/license-GPL‐3.0-orange.svg)](https://github.com/rbroderi/protocol_implements_decorator/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/protocol_implements_decorator)](https://pypi.python.org/pypi/ansicolortags/)
[![Generic badge](https://img.shields.io/badge/mypy-typed-purple.svg)](http://mypy-lang.org/)
[![Generic badge](https://img.shields.io/badge/beartype-runtime_typed-cyan.svg)](https://github.com/beartype/beartype)
[![Generic badge](https://img.shields.io/badge/bandit-checked-magenta.svg)](https://bandit.readthedocs.io/en/latest/)
[![Generic badge](https://img.shields.io/badge/uv-requirements-yellow.svg)](https://github.com/astral-sh/uv)
[![Dynamic TOML Badge](https://img.shields.io/badge/dynamic/toml?url=https%3A%2F%2Fraw.githubusercontent.com%2Frbroderi%2FVerbex%2Fmaster%2Fpyproject.toml&query=%24.project.version&label=Version)](https://github.com/rbroderi/protocol_implements_decorator/releases)


Adds the "implements" decorator to make using protocols easier and more explicit


## Description

Adds the @implements decorator.
This will cause a runtime NotImplementedError if the class does not implement all parts of the protocol.
Also adds the get_protocols_implemented method to the class providing a list of all protocols the decorated class adhears to.

Usage:
---
Two example protocols

```python
class Printable(Protocol):
  """A test protocol that requires a to_string method."""

  def to_string(self) -> str:
    return ""

class Otherable(Protocol):
  """Another example."""

  def other(self) -> str:
    return "
```

---
Example of one protocol

```python
@implements(Printable)
class Example2:

  def to_string(self) -> str:
    return str(self)
```

For multiple protocols you can chain dectorator or include in a list in one dectorator
```python
@implements(Printable)
@implements(Otherable)
class Example1:
  """Test class that uses multiple protocols."""

  def to_string(self) -> str:
    return str(self)

  def other(self) -> str:
    return str(self)


@implements(Printable, Otherable)
class Example2:
  """Test class that uses multiple protocols."""

  def to_string(self) -> str:
    return str(self)

  def other(self) -> str:
    return str(self)
```

Errors
---
This will cause a runtime error as it doesn't implement the Printable protocol

```python
@implements(Printable, Otherable)
class Example2:
  """Test class that uses multiple protocols."""

  def other(self) -> str:
    return str(self)
```
```text
NotImplementedError: test.<locals>.Printable requires implentation of ['to_string']
```
