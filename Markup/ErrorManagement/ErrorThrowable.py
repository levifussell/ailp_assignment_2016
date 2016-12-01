from .MarkupErrorFactory import MarkupErrorFactory, ErrorTypes

from _LoggerManager import _Log, _LoggerState

class ErrorThrowable:
    """Interface for a class that can throw errors dynamically"""

    def createThrowError(self, errorType, error_item, line):
        """throw a new error via the _Log and given a predefined error type"""
        markupError = MarkupErrorFactory.createError(errorType)
        errorText = markupError.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line)
        _Log(errorText, _LoggerState.ERROR)

    def createThrowErrorReg(self, markupErrorReg, error_item, line):
        """throw a pre-built regExp error via the _Log"""
        errorText = markupErrorReg.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line)
        _Log(errorText, _LoggerState.ERROR)
