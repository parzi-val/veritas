from collections.abc import MutableMapping
import threading
import asyncio

class ThreadSafeDict(MutableMapping):
    def __init__(self):
        self._data = {}
        self._lock = threading.RLock()
    
    def set(self, key, value):
        with self._lock:
            self._data[key] = value

    def __getitem__(self, key):
        with self._lock:
            return self._data[key]

    def __setitem__(self, key, value):
        with self._lock:
            self._data[key] = value

    def __delitem__(self, key):
        with self._lock:
            del self._data[key]

    def __iter__(self):
        with self._lock:
            return iter(self._data.copy())

    def __len__(self):
        with self._lock:
            return len(self._data)

    def __contains__(self, key):
        with self._lock:
            return key in self._data

    def clear(self):
        with self._lock:
            self._data.clear()

    def items(self):
        with self._lock:
            return list(self._data.items())

    def __repr__(self):
        with self._lock:
            return f"<ThreadSafeDict {self._data!r}>"


class AsyncSafeDict(MutableMapping):
    def __init__(self):
        self._data = {}
        self._lock = asyncio.Lock()

    def set(self, key, value):
        with self._lock:
            self._data[key] = value

    async def __getitem__(self, key):
        async with self._lock:
            return self._data[key]

    async def __setitem__(self, key, value):
        async with self._lock:
            self._data[key] = value

    async def __delitem__(self, key):
        async with self._lock:
            del self._data[key]

    async def __contains__(self, key):
        async with self._lock:
            return key in self._data

    async def __len__(self):
        async with self._lock:
            return len(self._data)

    async def items(self):
        async with self._lock:
            return list(self._data.items())

    async def clear(self):
        async with self._lock:
            self._data.clear()

    def __aiter__(self):
        # for `async for key in dict`
        async def gen():
            async with self._lock:
                for k in self._data:
                    yield k
        return gen()

    def __repr__(self):
        return f"<AsyncSafeDict {id(self)}>"
