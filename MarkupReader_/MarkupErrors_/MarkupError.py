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

    def __init__(self, regularExpression, errorText, errorLevel):
        self.regularExpression = regularExpression
        self.errorText = errorText
        self.errorLevel = errorLevel
        # self.lineNum = lineNum

    # def getFullErrorStatement(self):
    #     return self.errorText

    def toString(self):
        return 'error (' + ErrorHandlingTypes.toString(self.errorLevel) + '): ' + self.errorText