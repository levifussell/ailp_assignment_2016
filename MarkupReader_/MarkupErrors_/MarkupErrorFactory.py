from .MarkupError import ErrorHandlingTypes, MarkupError

from enum import Enum

class ErrorTypes(Enum):
    ERR_UNKNOWN = 1
    ERR_MATCHINGBRACKETS = 2

class MarkupErrorFactory:

    def __init__(self):
        self.initialised = True

    def createError(self, errorType):
        err_regExp = ''
        err_text = ''
        err_level = ErrorHandlingTypes.UNKNOWN

        if(errorType == ErrorTypes.ERR_UNKNOWN):
            err_regExp = ''
            err_text = 'unkown error found'
            err_level = ErrorHandlingTypes.UNKNOWN
        elif(errorType == ErrorTypes.ERR_MATCHINGBRACKETS):
            err_regExp = '(<[^<|^>]*<[^<|^>]*)|(>[^<|^>]*>[^<|^>]*)'
            err_text = 'non-matching brackets found'
            err_level = ErrorHandlingTypes.SYNTAX

        return MarkupError(err_regExp, err_text, err_level)