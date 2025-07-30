from collections.abc import MutableMapping
import threading
import asyncio

class ThreadSafeDict(MutableMapping):
    """A dictionary that provides thread-safe access to its contents."""
    def __init__(self):
        """Initializes the ThreadSafeDict with a re-entrant lock."""
        self._data = {}
        self._lock = threading.RLock()

    def __getitem__(self, key):
        """Retrieves an item from the dictionary in a thread-safe manner."""
        with self._lock:
            return self._data[key]

    def __setitem__(self, key, value):
        """Sets an item in the dictionary in a thread-safe manner."""
        with self._lock:
            self._data[key] = value

    def __delitem__(self, key):
        """Deletes an item from the dictionary in a thread-safe manner."""
        with self._lock:
            del self._data[key]

    def __iter__(self):
        """Returns an iterator over a copy of the dictionary items."""
        with self._lock:
            return iter(self._data.copy())

    def __len__(self):
        """Returns the number of items in the dictionary."""
        with self._lock:
            return len(self._data)

    def __contains__(self, key):
        """Checks if a key is in the dictionary in a thread-safe manner."""
        with self._lock:
            return key in self._data

    def __repr__(self):
        """Returns a string representation of the dictionary."""
        with self._lock:
            return f"<ThreadSafeDict {self._data!r}>"

    def set(self, key, value):
        """Alias for __setitem__ for more explicit API."""
        with self._lock:
            self._data[key] = value

    def clear(self):
        """Removes all items from the dictionary."""
        with self._lock:
            self._data.clear()

    def items(self):
        """Returns a list of the dictionary's items."""
        with self._lock:
            return list(self._data.items())


class AsyncSafeDict(MutableMapping):
    """A dictionary that provides async-safe access to its contents for asyncio applications."""
    def __init__(self):
        """Initializes the AsyncSafeDict with an asyncio Lock."""
        self._data = {}
        self._lock = asyncio.Lock()

    async def __getitem__(self, key):
        """Retrieves an item from the dictionary in an async-safe manner."""
        async with self._lock:
            return self._data[key]

    async def __setitem__(self, key, value):
        """Sets an item in the dictionary in an async-safe manner."""
        async with self._lock:
            self._data[key] = value

    async def __delitem__(self, key):
        """Deletes an item from the dictionary in an async-safe manner."""
        async with self._lock:
            del self._data[key]

    def __aiter__(self):
        """Returns an async iterator over the dictionary keys."""
        async def gen():
            async with self._lock:
                for k in self._data:
                    yield k
        return gen()

    async def __len__(self):
        """Returns the number of items in the dictionary."""
        async with self._lock:
            return len(self._data)

    async def __contains__(self, key):
        """Checks if a key is in the dictionary in an async-safe manner."""
        async with self._lock:
            return key in self._data

    def __repr__(self):
        """Returns a string representation of the dictionary."""
        return f"<AsyncSafeDict {id(self)}>"

    def __iter__(self):
        """Raises a TypeError, as this dictionary is for async contexts only."""
        raise TypeError("AsyncSafeDict cannot be used in a synchronous context.")

    def set(self, key, value):
        """Alias for __setitem__ for a more explicit API."""
        with self._lock:
            self._data[key] = value

    async def items(self):
        """Returns a list of the dictionary's items."""
        async with self._lock:
            return list(self._data.items())

    async def clear(self):
        """Removes all items from the dictionary."""
        async with self._lock:
            self._data.clear()

