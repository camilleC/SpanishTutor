# spanishtutor/src/core/exceptions.py

class TutorError(Exception):
    """Base class for all tutor-related errors."""
    pass

class TutorBadRequest(TutorError):
    """Raised for user input or internal prompt errors."""
    pass

class TutorModelUnavailable(TutorError):
    """Raised when the LLM model is unavailable or unresponsive."""
    pass

class TutorInternalError(TutorError):
    """Raised for any unexpected internal errors."""
    pass