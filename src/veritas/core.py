import inspect
import queue
import asyncio
from veritas.datastructs import ThreadSafeDict, AsyncSafeDict
from veritas.exceptions import UnsafeSharedArgumentError, MissingSharedArgumentError

SAFE_MUTABLE_TYPES = (queue.Queue, asyncio.Queue, ThreadSafeDict, AsyncSafeDict)

class VeritasWrapper:
    def __init__(self, func, unsafe=False):
        self._func = func
        self._unsafe = unsafe
        self._state = self._extract_mutable_default()

    def _extract_mutable_default(self):
        sig = inspect.signature(self._func)
        is_async = inspect.iscoroutinefunction(self._func)

        shared_param = sig.parameters.get("shared")
        if shared_param is None or shared_param.default is inspect.Parameter.empty:
            if self._unsafe:
                return None
            raise MissingSharedArgumentError()

        shared_value = shared_param.default
        if self._unsafe:
            return shared_value

        if is_async and isinstance(shared_value, (AsyncSafeDict, asyncio.Queue)):
            return shared_value
        elif not is_async and isinstance(shared_value, (ThreadSafeDict, queue.Queue)):
            return shared_value

        pretty_safe_types = '\n'.join(f'  - {t.__module__}.{t.__name__}' for t in SAFE_MUTABLE_TYPES)
        raise UnsafeSharedArgumentError(
            f"Invalid type for 'shared' argument: found {type(shared_value).__name__}.\n"
            f"Please use one of the following safe mutable types:\n{pretty_safe_types}\n\n"
            f"To bypass this check, use @veritas(unsafe=True)."
        )


    def __call__(self, *args, **kwargs):
        return self._func(*args, **kwargs)

    @property
    def state(self):
        return self._state

def veritas(_func=None, *, unsafe=False):
    def decorator(func):
        return VeritasWrapper(func, unsafe=unsafe)
    return decorator if _func is None else decorator(_func)
