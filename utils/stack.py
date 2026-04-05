"""Custom stack implementation used by the SCC algorithms."""


class Stack[T]:
    """A small typed stack wrapper around a list."""

    def __init__(self) -> None:
        self._items: list[T] = []

    def is_empty(self) -> bool:
        """Return ``True`` when the stack contains no items."""
        return not self._items

    def push(self, item: T) -> None:
        """Push an item onto the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item."""
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it."""
        return self._items[-1]

    def size(self) -> int:
        """Return the number of items currently on the stack."""
        return len(self._items)

    def contains(self, item: T) -> bool:
        """Return ``True`` if the item is currently stored in the stack."""
        return item in self._items
