import inspect
import queue
import asyncio
from veritas.datastructs import ThreadSafeDict, AsyncSafeDict
from veritas.exceptions import UnsafeSharedArgumentError, MissingSharedArgumentError

SAFE_MUTABLE_TYPES = (queue.Queue, asyncio.Queue, ThreadSafeDict, AsyncSafeDict)

class VeritasWrapper:
    """
    A wrapper that enforces safe usage of a shared mutable default argument.

    This class inspects the decorated function for a `shared` parameter with a
    mutable default. It validates the type of the default argument to ensure it is
    thread-safe or async-safe, depending on the function type.
    """
    def __init__(self, func, unsafe=False):
        """
        Initializes the VeritasWrapper.

        Args:
            func (callable): The function to wrap.
            unsafe (bool): If True, bypasses the safety checks for the shared argument.
        """
        self._func = func
        self._unsafe = unsafe
        self._state = self._extract_mutable_default()

    def _extract_mutable_default(self):
        """
        Extracts and validates the shared mutable default argument from the wrapped function.

        Raises:
            MissingSharedArgumentError: If no `shared` parameter with a default is found.
            UnsafeSharedArgumentError: If the default value is not of a recognized safe type.

        Returns:
            The shared mutable object if validation passes.
        """
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

        pretty_safe_types = ''.join(f'  - {t.__module__}.{t.__name__}' for t in SAFE_MUTABLE_TYPES)
        raise UnsafeSharedArgumentError(
            f"Invalid type for 'shared' argument: found {type(shared_value).__name__}."
            f"Please use one of the following safe mutable types: {pretty_safe_types}"
            f"To bypass this check, use @veritas(unsafe=True)."
        )


    def __call__(self, *args, **kwargs):
        """Calls the original wrapped function."""
        return self._func(*args, **kwargs)

    @property
    def state(self):
        """Provides direct access to the shared mutable state."""
        return self._state

def veritas(_func=None, *, unsafe=False):
    """
    A decorator to safely manage shared mutable default arguments in functions.

    It ensures that any function using a `shared` mutable default argument uses a
    thread-safe or async-safe type.

    Args:
        unsafe (bool): If True, allows the use of non-validated mutable defaults.

    Returns:
        A decorator that wraps the function.
    """
    def decorator(func):
        return VeritasWrapper(func, unsafe=unsafe)
    return decorator if _func is None else decorator(_func)
