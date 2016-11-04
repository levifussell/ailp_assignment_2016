# from MarkupErrors.MarkupErrorFactory import MarkupErrorFactory
# from MarkupObject import MarkupObject
from .MarkupErrors_.MarkupErrorFactory import MarkupError, MarkupErrorFactory, ErrorHandlingTypes, ErrorTypes
from .MarkupObject import MarkupObject
# import sys
# sys.path.append('../Compilation/GenericClass')
from Compilation.GenericClass.ClassObject import ClassObject
from Compilation.GenericClass.AttributeFactory import AttributeFactory

import re

class MarkupReader:

    def __init__(self):
        self.error_types = []
        self.__errorFactory = MarkupErrorFactory()

    def run(self, codeFile):

        thrownErrors = self.__computeErrors(codeFile)

        # print('errors found: ' + str(len(thrownErrors)))

        for i in range(0, len(thrownErrors)):
            print(thrownErrors[i])

        # if NO errors, continue processing the Markup
        if len(thrownErrors) == 0:
            
            stackData = []
            # recursively extract markup data
            self.__regFindNextMarkupObj(codeFile.getCleanCodeText(), 0, stackData)

            listClassObjs = self.__convertMarkupStackToObjects(stackData)

            for i in range(0, len(listClassObjs)):
                listClassObjs[i].print()

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
                    print('COMMENT FOUND')
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

    def __regFindNextMarkupObj(self, codeString, depth, stackData):

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
                self.__regFindNextMarkupObj(markupObjData, depth + 1, stackData)
                
                codeString = codeString[len(regMarkupObjData):len(codeString)]
                # print('D:' + codeString)
            except:
                print('NO DATA')
                # return

    def __createThrowError(self, markupError, error_item, line):
        return markupError.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line) 

    def __computeError(self, codeFile, markupError):

        is_thrown = False
        error_throw = ' '

        try:
            codeString = codeFile.getCleanCodeText()
            # print(markupError.regularExpression)
            error_re = re.search(markupError.regularExpression, codeString, re.DOTALL)

            error_item = error_re.group(0)

            error_throw = self.__createThrowError(markupError, error_item, codeFile.getLineOfText(error_item))
            is_thrown = True
        except:
            error_throw = 'NONE'
            is_thrown = False

        return is_thrown, error_throw

    def __computeErrors(self, codeFile):

        thrown_errors = []

        for i in range(0, len(self.error_types)):
            isThrown, error_throw = self.__computeError(codeFile, self.error_types[i])

            if isThrown:
                thrown_errors.append(error_throw)

        return thrown_errors

    def addErrorType(self, errorType):
        mError = self.__errorFactory.createError(errorType)
        # print('ADDING ERROR: ' + str(mError.errorLevel))
        self.error_types.append(mError)