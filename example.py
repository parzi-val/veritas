from veritas import veritas
from veritas.cache import cache
from veritas.datastructs import ThreadSafeDict


shared = ThreadSafeDict()

@cache()
def multiply(x, y, shared=shared):
    """multiply shi"""
    print("⛏️  Multiply computing...")
    return x * y


@cache(key=["x"])
@veritas
def increment(x, noise, shared=shared):
    print("🛠️  Increment computing...")
    return x + 1


@cache()
@veritas
def flatten(data, shared=shared):
    print("🧪 Flatten computing...")
    return sum(data)


from inspect import signature

print(multiply.__name__)       # multiply
print(multiply.__doc__)        # whatever docstring you wrote
print(signature(multiply))     # (x, y, shared=...)


multiply(2, 5)  # miss
multiply(2, 5)  # hit

increment(1, noise=99)  # miss
increment(1, noise=100)  # hit (same x)

flatten([1, 2, 3])  # miss
flatten([1, 2, 3])  # hit
flatten([4, 5, 6])  # miss


