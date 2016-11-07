from enum import Enum

class ErrorHandlingTypes(Enum):
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

    def __init__(self, errorText, errorLevel):
        self.errorText = errorText
        self.errorLevel = errorLevel

    def toString(self):
        return 'error (' + ErrorHandlingTypes.toString(self.errorLevel) + '): ' + self.errorText

class MarkupErrorRegEx(MarkupError):

    def __init__(self, regularExpression, errorText, errorLevel):
        MarkupError.__init__(self, errorText, errorLevel)
        self.regularExpression = regularExpression
        self.errorText = errorText
        self.errorLevel = errorLevel

    def toString(self):
        return 'error (' + ErrorHandlingTypes.toString(self.errorLevel) + '): ' + self.errorText