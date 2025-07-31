class VeritasError(Exception):
    """Base exception for all Veritas-related errors."""
    pass

class UnsafeSharedArgumentError(VeritasError):
    """Raised when a function decorated with @veritas uses an unsafe mutable default."""
    def __init__(self, message):
        super().__init__(message)

class MissingSharedArgumentError(VeritasError):
    """Raised when a function decorated with @veritas is missing a 'shared' argument."""
    def __init__(self, message="No 'shared' default provided, or not set. Use unsafe=True to bypass."):
        super().__init__(message)

class VeritasCacheError(VeritasError):
    """Raised when caching fails due to bad keys or configuration."""
    def __init__(self, message):
        super().__init__(message)
