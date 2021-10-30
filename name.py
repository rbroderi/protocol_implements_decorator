"""A class that holds a name."""
from __future__ import annotations

from dataclasses import dataclass
from functools import total_ordering
from typing import List, Tuple, ClassVar


@total_ordering
@dataclass
class Name:
    parts: List[str]
    sort_order: Tuple[int, ...]
    seperator: ClassVar[str] = " "
    case_sensitive: ClassVar[bool] = False

    def __init__(
        self, parts: List[str], sort_order: None | Tuple[int, ...] = None
    ):
        if sort_order is None:
            self.sort_order = tuple(range(0, len(parts)))
        else:
            self.sort_order = sort_order
        self.parts = parts

    def _sort_str(self) -> str:
        ret = ""
        for index in self.sort_order:
            ret += "".join([x for x in self.parts[index]])
        return ret if Name.case_sensitive else ret.lower()

    def __eq__(self, other: Name):
        return self._sort_str() == other._sort_str()

    def __lt__(self, other: Name):
        return self._sort_str() < other._sort_str()

    def __str__(self) -> str:
        return Name.seperator.join(self.parts)

    def __repr__(self) -> str:
        return f"Name(parts={self.parts!r},sort_order={self.sort_order!r})"
