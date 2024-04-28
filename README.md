# protocol_implements_decorator

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
