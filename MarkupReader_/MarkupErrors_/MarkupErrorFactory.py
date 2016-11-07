from .MarkupError import ErrorHandlingTypes, MarkupError, MarkupErrorRegEx

from enum import Enum

class ErrorTypes(Enum):
    ERR_UNKNOWN = 1
    ERR_MATCHINGBRACKETS = 2
    ERR_UNKNOWNCHARACTER = 3
    ERR_MATCHINGNAME = 4
    ERR_HASHCLASSOBJECT = 5
    ERR_NULLDATA = 6

class MarkupErrorFactory:

    def __init__(self):
        self.initialised = True

    def createError(self, errorType):
        err_regExp = ''
        err_text = ''
        err_level = ErrorHandlingTypes.UNKNOWN

        # Regular Expression Errors
        if(errorType == ErrorTypes.ERR_UNKNOWN):
            return MarkupErrorRegEx('', 'unkown error found', ErrorHandlingTypes.UNKNOWN)
        elif(errorType == ErrorTypes.ERR_MATCHINGBRACKETS):
            return MarkupErrorRegEx('(<[^<|^>]*<[^<|^>]*)|(>[^<|^>]*>[^<|^>]*)', 'non-matching brackets found', ErrorHandlingTypes.SYNTAX)
        elif(errorType == ErrorTypes.ERR_UNKNOWNCHARACTER):
            return MarkupErrorRegEx('[^<|^>|^\/|^\w|^\[|^\]|^!|\,]', 'illegal character found', ErrorHandlingTypes.SYNTAX)
        # Non-RegEx Errors
        elif(errorType == ErrorTypes.ERR_MATCHINGNAME):
            return MarkupError('Markup does not have matching opening and closing name', ErrorHandlingTypes.SYNTAX)
        elif(errorType == ErrorTypes.ERR_HASHCLASSOBJECT):
            return MarkupError('Object is not a valid Caernades class', ErrorHandlingTypes.COMPILER)
        elif(errorType == ErrorTypes.ERR_NULLDATA):
            return MarkupError('Null object during compilation', ErrorHandlingTypes.COMPILER)

        return MarkupError('unkown error found', ErrorHandlingTypes.UNKNOWN)