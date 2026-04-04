"""Custom Stack implementation for educational purposes.

This module provides a basic stack data structure implementation
to demonstrate low-level data structure usage in SCC algorithms.
"""

class Stack:
    """A simple stack implementation using a list."""

    def __init__(self):
        """Initialize an empty stack."""
        self.items = []

    def isEmpty(self) -> bool:
        """Check if the stack is empty.

        Returns:
            True if the stack is empty, False otherwise.
        """
        return self.items == []

    def push(self, item):
        """Push an item onto the stack.

        Args:
            item: The item to push onto the stack.
        """
        self.items.append(item)

    def pop(self):
        """Pop an item from the stack.

        Returns:
            The item at the top of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        return self.items.pop()

    def peek(self):
        """Peek at the top item of the stack without removing it.

        Returns:
            The item at the top of the stack.

        Raises:
            IndexError: If the stack is empty.
        """
        return self.items[len(self.items) - 1]

    def size(self) -> int:
        """Get the size of the stack.

        Returns:
            The number of items in the stack.
        """
        return len(self.items)

    def contains(self, item) -> bool:
        """Check if an item is in the stack.

        Args:
            item: The item to check for.

        Returns:
            True if the item is in the stack, False otherwise.
        """
        return item in self.items