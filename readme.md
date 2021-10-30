The adds the @protocol and @implements decorators.

Usage:
---
Two example protocols

class Printable(Protocol):
  """A test protocol that requires a to_string method."""
  
  def to_string(self) -> str:
    return ""

class Otherable(Protocol):
  """Another example."""

  def other(self) -> str:
    return "

---
Example of one protocol

 @implements(Printable)
class Example2:

  def to_string(self) -> str:
    return str(self)

For multiple protocols you can chain dectorator or include in a list in one dectorator
@implements(Printable, Otherable)
class Example4:
  """Test class that uses multiple protocols."""

  def to_string(self) -> str:
    return str(self)

  def other(self) -> str:
    return str(self)

 
