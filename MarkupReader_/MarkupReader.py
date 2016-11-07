# from MarkupErrors.MarkupErrorFactory import MarkupErrorFactory
# from MarkupObject import MarkupObject
from .MarkupErrors_.MarkupErrorFactory import MarkupError, MarkupErrorFactory, ErrorHandlingTypes, ErrorTypes
from .MarkupObject import MarkupObject
# import sys
# sys.path.append('../Compilation/GenericClass')
from Compilation.GenericClass.ClassObject import ClassObject
from Compilation.GenericClass.AttributeFactory import AttributeFactory

from _LoggerManager import _Log, _Logger_Thread, _LoggerState

import re

class MarkupReader:

    def __init__(self):
        self.error_types = []
        self.__errorFactory = MarkupErrorFactory()

    def run(self, codeFile):

        _Log('...begin reading file...', _LoggerState.WARNING)

        self.__computeErrors(codeFile)

        # if NO errors, continue processing the Markup
        if _Logger_Thread.count_errors == 0:
            
            stackData = []
            # recursively extract markup data
            self.__regFindNextMarkupObj(codeFile.getCleanCodeText(), 0, stackData, codeFile)

            if _Logger_Thread.count_errors == 0:
                listClassObjs = self.__convertMarkupStackToObjects(stackData)

                totalListLog = ''
                for i in range(0, len(listClassObjs)):
                    totalListLog += listClassObjs[i].toString() + '\n'

                _Log(totalListLog, _LoggerState.DEBUG)

                if _Logger_Thread.count_errors == 0:
                    _Log('...reading file successful...', _LoggerState.WARNING)
                    return listClassObjs
                
        _Log('...reading file failed...', _LoggerState.ERROR)

        return None
        # if len(errorList) == 0:
        #     listClassObjs = convertMarkupStackToObjects(stackData)

        #     for i in range(0, len(listClassObjs)):
        #         listClassObjs[i].print()

        # else:
        #     print('ERRORS FOUND: ')
        #     for i in range(0, len(errorList)):
        #         print(errorList[i])

    def __convertMarkupStackToObjects(self, stackData):

        queueAttributes = [] # Attribute is a Variable with a Value below it in depth
        listClassObjs = [] # Class is a Variable with multiple Variables below it in depth

        while len(stackData) > 0:

            _a = stackData.pop()
            if _a.type == 'value':
                variable = stackData.pop()
                # first check the variable is not a comment
                if variable.data == '!':
                    #TODO: do something if it is a comment
                    _Log('COMMENT FOUND', _LoggerState.DEBUG)
                else:
                    # add the value/variable object to a queue
                    queueAttributes.append([variable.data, _a.data])
            elif _a.type == 'variable':
                # get all attributes and below in queue and make a class
                classObj = ClassObject(_a.data)
                
                while len(queueAttributes) > 0:
                    attrML = queueAttributes.pop()
                    attrObj = AttributeFactory.createAttribute(attrML[0], attrML[1])
                    classObj.addAttribute(attrObj)

                listClassObjs.append(classObj)
                
        return listClassObjs

    def __regFindNextMarkupObj(self, codeString, depth, stackData, codeFile):

        while len(codeString) > 0:

            # get the name of the next markup obj
            try:
                regMarkupObjName = re.search('<[\w|!]+?>', codeString, re.DOTALL).group(0)
                markupObjName = regMarkupObjName[1:len(regMarkupObjName) - 1]
                codeString = codeString[len(regMarkupObjName):len(codeString)]
                # print('E:')
                # print(codeString)
                stackData.append(MarkupObject(markupObjName, depth, 'variable'))
                # print(markupObjName + ':')
            except:
                # print('D:')
                # print(codeString)
                stackData.append(MarkupObject(codeString, depth, 'value'))
                # print(codeString)
                return

            try:
                # implement that name into the next regEx search
                regMarkupObjData = re.search('.+?</' + markupObjName + '>', codeString, re.DOTALL).group(0)
                # print('SD:' + regMarkupObjData)
                startIdx = 0
                endIdx = len(regMarkupObjData) - len(markupObjName) - 3
                markupObjData = regMarkupObjData[startIdx:endIdx]
                # print('D: ' + markupObjData)
                self.__regFindNextMarkupObj(markupObjData, depth + 1, stackData, codeFile)
                
                codeString = codeString[len(regMarkupObjData):len(codeString)]
                # print('D:' + codeString)
            except:
                errOB = self.__errorFactory.createError(ErrorTypes.ERR_MATCHINGNAME)
                self.__createThrowError(errOB, regMarkupObjName, codeFile.getLineOfText(regMarkupObjName))
                # return

    def __createThrowError(self, markupError, error_item, line):
        errorText = markupError.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line)
        # self.thrownErrors.append(errorText) 
        _Log(errorText, _LoggerState.ERROR)

    def __computeError(self, codeFile, markupError):

        error_throw = ' '

        try:
            codeString = codeFile.getCleanCodeText()
            # print(markupError.regularExpression)
            error_re = re.search(markupError.regularExpression, codeString, re.DOTALL)

            error_item = error_re.group(0)

            self.__createThrowError(markupError, error_item, codeFile.getLineOfText(error_item))
        except:
            _Log('failed to throw error in markup reader', _LoggerState.DEBUG)

    def __computeErrors(self, codeFile):

        for i in range(0, len(self.error_types)):
            self.__computeError(codeFile, self.error_types[i])

    def addErrorType(self, errorType):
        mError = self.__errorFactory.createError(errorType)
        # print('ADDING ERROR: ' + str(mError.errorLevel))
        self.error_types.append(mError)