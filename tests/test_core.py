import pytest
from veritas import veritas
from veritas.exceptions import UnsafeSharedArgumentError, MissingSharedArgumentError

def test_unsafe_shared_argument_raises_error():
    with pytest.raises(UnsafeSharedArgumentError, match="'shared' must be of type .* but got <class 'dict'>. Use unsafe=True to bypass this check."):
        @veritas
        def unsafe_function(shared={}):
            pass

def test_missing_shared_argument_raises_error():
    with pytest.raises(MissingSharedArgumentError, match="No 'shared' default provided, or not set. Use unsafe=True to bypass."):
        @veritas
        def missing_shared_function():
            pass

def test_unsafe_veritas_bypasses_check():
    try:
        @veritas(unsafe=True)
        def unsafe_function(shared={}):
            pass
    except (UnsafeSharedArgumentError, MissingSharedArgumentError):
        pytest.fail("veritas(unsafe=True) should not raise an error for unsafe shared arguments.")
