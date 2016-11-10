from _LoggerManager import _Log, _LoggerState

from enum import Enum

class ErrorHandlingTypes(Enum):
    """Different points in the compiler where errors can be thrown"""
    UNKNOWN = 1
    SYNTAX = 2
    COMPILER = 3
    RUNTIME = 4

    @staticmethod
    def toString(errorType):
        if errorType == ErrorHandlingTypes.SYNTAX:
            return 'syntax'
        elif errorType == ErrorHandlingTypes.COMPILER:
            return 'compiler'
        elif errorType == ErrorHandlingTypes.RUNTIME:
            return 'runtime'
        elif errorType == ErrorHandlingTypes.UNKNOWN:
            return 'unknown'
        else:
            return 'unknown'

class MarkupError:
    """Class for creating new errors during Markup reading/compilation to Caernades"""
    def __init__(self, errorText, errorLevel):
        self.errorText = errorText
        self.errorLevel = errorLevel

    def toString(self):
        return 'error (' + ErrorHandlingTypes.toString(self.errorLevel) + '): ' + self.errorText

class MarkupErrorRegEx(MarkupError):
    """Class for creating new errors during Markup reading to Caernades with a
    specific regular expression errors to search for in the markup"""
    def __init__(self, regularExpression, errorText, errorLevel):
        MarkupError.__init__(self, errorText, errorLevel)
        self.regularExpression = regularExpression
        self.errorText = errorText
        self.errorLevel = errorLevel

    def toString(self):
        return 'error (' + ErrorHandlingTypes.toString(self.errorLevel) + '): ' + self.errorText

class ErrorThrowable:
    """Interface for a class that can throw errors dynamically"""

    def __createThrowError(self, errorType, error_item, line):
        """throw a new error via the _Log and given a predefined error type"""
        markupError = MarkupErrorFactory.createError(errorType)
        errorText = markupError.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line)
        _Log(errorText, _LoggerState.ERROR)
