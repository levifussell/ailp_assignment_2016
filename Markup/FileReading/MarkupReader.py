from Markup.ErrorManagement.MarkupErrorFactory import MarkupError, MarkupErrorFactory, ErrorHandlingTypes, ErrorTypes
from Markup.MarkupClass.ClassObject import ClassObject
from Markup.MarkupClass.AttributeFactory import AttributeFactory

from .MarkupObject import MarkupObject

from _LoggerManager import _Log, _Logger_Thread, _LoggerState

import re

class MarkupReader:
    """This class reads a markup file and converts the markup data to markup objects
    for easy compilation into Caernades via the compiler"""

    def __init__(self):
        self.error_types = []

    def run(self, codeFile):
        """Begin reading a markup code file"""

        _Log('...begin reading file...', _LoggerState.WARNING)

        # first check the file for any obvious syntactical errors
        self.__computeErrors(codeFile)

        # if NO errors, continue processing the Markup
        if _Logger_Thread.count_errors == 0:
            
            # recursively extract markup data into a markup stack
            stackData = []
            self.__regFindNextMarkupObj(codeFile.getCleanCodeText(), 0, stackData, codeFile)

            # check that no errors have been created since extracting data
            if _Logger_Thread.count_errors == 0:

                # re-read the markup stack to create markup objects
                listClassObjs = self.__convertMarkupStackToObjects(stackData)

                # create a log of the output markup objects created for debugging
                totalListLog = ''
                for i in range(0, len(listClassObjs)):
                    totalListLog += listClassObjs[i].toString() + '\n'
                _Log(totalListLog, _LoggerState.DEBUG)

                # if no errors since reading markup data, reading is successful
                if _Logger_Thread.count_errors == 0:
                    _Log('...reading file successful...', _LoggerState.WARNING)
                    return listClassObjs
                
        # failed to read markup via some error
        _Log('...reading file failed...', _LoggerState.ERROR)
        return None

    def __convertMarkupStackToObjects(self, stackData):
        """Convert a markup data stack read from the file to markup objects by reading
        off the stack and dynamically creating markup objects"""

        # Attribute is defined in the stack as: a Variable with a Value below it in depth
        queueAttributes = []
        # Class is defined in the stack as: a Variable with multiple Variables below it in depth
        listClassObjs = []

        # itterate through stack until end
        while len(stackData) > 0:

            # get top value from stack
            _a = stackData.pop()

            # value and variables are defined as:
            # 
            #  <variable>value</variable>
            # 
            # ...or they can be:
            # 
            # <variables>
            #   <variable>
            #       value
            #   </variable>
            # </variable

            if _a.type == 'value':
                # if value, get the next object in stack, which should
                #  be the variable for the value
                variable = stackData.pop()

                # first check the variable is not a comment
                if variable.data == '!':
                    #TODO: do something if it is a comment
                    _Log('COMMENT FOUND', _LoggerState.DEBUG)
                elif variable.type == 'value': pass
                    # TODO: throw error for having value, value pair
                else:
                    # add the value/variable object to a queue
                    queueAttributes.append([variable.data, _a.data])

            elif _a.type == 'variable':

                # get all attributes and below in queue and make a class
                classObj = ClassObject(_a.data)
                
                while len(queueAttributes) > 0:
                    # get value, variable pair from queue as a class attribute
                    #  and add it to the class
                    attrML = queueAttributes.pop()
                    attrObj = AttributeFactory.createAttribute(attrML[0], attrML[1])
                    classObj.addAttribute(attrObj)

                listClassObjs.append(classObj)
                
        return listClassObjs

    def __regFindNextMarkupObj(self, codeString, depth, stackData, codeFile):
        """given some markup code string, use regular expressions to read the string
        and convert it to a markup data stack via depth-first recursion"""

        # itterate through the whole code file
        while len(codeString) > 0:

            try:
                # get the name of the next markup obj
                regMarkupObjName = re.search('<[\w|!]+?>', codeString, re.DOTALL).group(0)
                # trim the '< >' edges of the object
                markupObjName = regMarkupObjName[1:len(regMarkupObjName) - 1]
                # remove that object from the code string
                codeString = codeString[len(regMarkupObjName):len(codeString)]
                # add the object to the markup data stack as a variable
                stackData.append(MarkupObject(markupObjName, depth, 'variable'))
                # print(markupObjName + ':')
            except:
                # if no markup object was found, then must be at the bottom of the recursion
                #  of markup objects, so add the final code string data as a value
                stackData.append(MarkupObject(codeString, depth, 'value'))
                return

            try:
                # implement the found markup object name into the next regEx search
                #  to find where the object ends
                regMarkupObjData = re.search('.+?</' + markupObjName + '>', codeString, re.DOTALL).group(0)
                # record bounds of the total markup object to trim from end
                startIdx = 0
                endIdx = len(regMarkupObjData) - len(markupObjName) - 3
                # get the inner code inside the markup object
                markupObjData = regMarkupObjData[startIdx:endIdx]
                
                # continue down the tree depth to find the next markup object
                self.__regFindNextMarkupObj(markupObjData, depth + 1, stackData, codeFile)
                
                # remove the markup object from the codestring after processing
                codeString = codeString[len(regMarkupObjData):len(codeString)]
            except:
                # markup objects must have a opening and closing. No closing should throw an error
                self.__createThrowError(ErrorTypes.ERR_MATCHINGNAME, regMarkupObjName, codeFile.getLineOfText(regMarkupObjName))

    def __createThrowError(self, errorType, error_item, line):
        markupError = MarkupErrorFactory.createError(errorType)
        errorText = markupError.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line)
        # self.thrownErrors.append(errorText) 
        _Log(errorText, _LoggerState.ERROR)

    def __createThrowErrorReg(self, markupErrorReg, error_item, line):
        errorText = markupErrorReg.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line)
        # self.thrownErrors.append(errorText) 
        _Log(errorText, _LoggerState.ERROR)

    def __computeError(self, codeFile, markupError):
        """Run a regular expression error over a code file to check for syntax errors"""
        error_throw = ' '

        try:
            # get the code string without spaces or returns or tabs
            codeString = codeFile.getCleanCodeText()
            
            # search for syntax error
            error_re = re.search(markupError.regularExpression, codeString, re.DOTALL)

            # if the error is found, throw it
            error_item = error_re.group(0)
            self.__createThrowErrorReg(markupError, error_item, codeFile.getLineOfText(error_item))
        except:
            # report debug info
            _Log('failed to throw error in markup reader: GOOD', _LoggerState.DEBUG)

    def __computeErrors(self, codeFile):
        """Run some regular expression errors over a code file to check for syntax errors"""
        for i in range(0, len(self.error_types)):
            self.__computeError(codeFile, self.error_types[i])

    def addErrorType(self, errorType):
        """Determine which errors to search for during the reading of markup files"""
        mError = MarkupErrorFactory.createError(errorType)
        _Log('ADDING ERROR: ' + str(mError.errorLevel), _LoggerState.DEBUG)
        self.error_types.append(mError)