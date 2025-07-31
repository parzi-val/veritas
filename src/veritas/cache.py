# veritas/cache.py
import inspect
import functools
from collections.abc import Callable
from typing import Any, Optional, Union

from veritas.exceptions import VeritasCacheError


def _default_key_builder(args: tuple, kwargs: dict) -> Any:
    try:
        return hash((args, frozenset(kwargs.items())))
    except TypeError:
        raise VeritasCacheError("Unhashable arguments passed to cache. Use 'experimental=True' or provide a custom key.")


def _experimental_hash(value: Any) -> Any:
    if isinstance(value, dict):
        return frozenset((k, _experimental_hash(v)) for k, v in value.items())
    elif isinstance(value, (list, tuple)):
        return tuple(_experimental_hash(v) for v in value)
    elif isinstance(value, set):
        return frozenset(_experimental_hash(v) for v in value)
    return value  # base case


def _build_key_from_explicit_args(func: Callable, key_fields: list, args: tuple, kwargs: dict) -> Any:
    bound = inspect.signature(func).bind_partial(*args, **kwargs)
    bound.apply_defaults()
    try:
        return tuple(bound.arguments[field] for field in key_fields)
    except KeyError as e:
        raise VeritasCacheError(f"Missing argument '{e.args[0]}' for cache key computation.")


def cache(key: Optional[Union[list[str], Callable]] = None, experimental: bool = False):
    def decorator(func):
        cache_store = {}

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if key is None:
                key_val = None
                try:
                    key_val = _default_key_builder(args, kwargs)
                except VeritasCacheError:
                    if experimental:
                        key_val = hash(_experimental_hash((args, kwargs)))
                    else:
                        raise
            elif isinstance(key, list):
                key_val = _build_key_from_explicit_args(func, key, args, kwargs)
            elif callable(key):
                key_val = key(*args, **kwargs)
            else:
                raise VeritasCacheError("Invalid 'key' parameter for @cache decorator.")

            if key_val in cache_store:
                return cache_store[key_val]

            result = func(*args, **kwargs)
            cache_store[key_val] = result
            return result

        wrapper._veritas_cache = cache_store  # for inspection / manual control
        return wrapper
    return decorator
