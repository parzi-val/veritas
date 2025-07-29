# Veritas

Veritas is a minimal Python microframework that enables safe usage of shared mutable default arguments in functions. Designed with both async and sync contexts in mind, Veritas flips the conventional wisdom around "mutable defaults are bad" into a powerful feature for building lightweight stateful systems, in-memory caches, and inter-task communication channels.

## Core Philosophy

Mutable defaults, when used intentionally and safely, can act as implicit state carriers. Veritas enforces safety by requiring that shared mutable defaults be explicitly defined using thread-safe or async-safe structures. It validates their usage at function definition time and ensures consistent behavior across sync and async contexts.

## Features

- **ThreadSafeDict / AsyncSafeDict**: Built-in safe dictionaries for concurrent access.
- **Safe by Default**: Disallows unsafe usage unless explicitly opted-in.
- **Support for asyncio and threading**: Works seamlessly with both paradigms.
- **Introspective Design**: Automatically extracts and validates the shared object.
- **Direct Access to Internal State**: Use `.state` on wrapped functions to inspect or manipulate shared memory.

## Installation

```bash
pip install veritas
```

## Usage

```python
from veritas import veritas
from veritas.datastructs import ThreadSafeDict

shared = ThreadSafeDict()
shared.set("count", 0)

@veritas
def increment(shared=shared):
    val = shared.get("count")
    shared.set("count", val + 1)
    print(f"Count is now {val + 1}")

for _ in range(10):
    increment()

# Access shared state directly
print("Final count:", increment.state.get("count"))
```

## Example

See the [examples](examples/) directory for a multi-threaded shared status writer-reader.

## Why Not ContextVars?

Veritas is not a replacement for `contextvars`. Instead, it offers a different kind of shared memory: persistent, introspectable, and defined at function scope rather than dynamic execution context.

## Contributing

Feature requests, bug reports, and PRs are welcome. See the TODO list in the issues for roadmap.

---

_Veritas_ — because shared memory doesn’t have to be dangerous.
