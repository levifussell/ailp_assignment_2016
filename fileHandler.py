# READING FILES INTO CAES:
# 
# --PROPOSITIONS:
# <Proposition>
#   <name>NAME</name>
#   <truth>TRUE</truth>
# </Proposition>
# 
# --ARGUEMENTS:
# <Arguement>
#   <propositions>[P1, P2, P3]</propositions>
#   <exceptions>[P1, P2, P3]</exceptions>
#   <outcome>PROPOSITION</outcome>
# </Arguement>
# 
# --
# 
# 

# data_input = "<Argument>\n" + "\t<name>Arg1</name>\n" + "</Argument>" + "\n<Argument>\n" + "\t<name>Arg2</name>\n" + "</Argument>"

from ClassObject import ClassObject
from Attribute import AttributeFactory
from MarkupObject import MarkupObject

import re
from copy import copy, deepcopy

# SIMULATE A FILE READ HERE----
# start reading the file here for regExp
def readInputFileString(input):

    regClasses = regFindAllClassObjects(input)

    classObjs = []

    for i in range(0, len(regClasses)):
        classObj = regBuildClassObject(regClasses.pop())
        classObjs.append(classObj)
        # regFindClassAttributeObjects(regClasses.pop())

    # TEMP: print the classes that have been found
    for i in range(0, len(classObjs)):
        classObjs[i].print()

# REGEX FOR GENERIC MARK UP LANGUAGE--------------------------------------

def beginMarkupRead(dataString):

    # remove extra spaces and newlines from text file
    dataString = re.sub('[\\n]|[\\s]', '', dataString)
    # record the extracted data in a stack
    stackData = []
    # recursively extract markup data
    regFindNextMarkupObj(dataString, 0, stackData)

    # for i in range(0, len(stackData)):
    #     print(stackData[i].toString())

    # convert the markup data stack to class objects
    listClassObjs = convertMarkupStackToObjects(stackData)

    for i in range(0, len(listClassObjs)):
        listClassObjs[i].print()

def regFindNextMarkupObj(dataString, depth, stackData):
    while len(dataString) > 0:
        # get the name of the next markup obj
        try:
            regMarkupObjName = re.search('<[\w].+?>', dataString, re.DOTALL).group(0)
            markupObjName = regMarkupObjName[1:len(regMarkupObjName) - 1]
            dataString = dataString[len(regMarkupObjName):len(dataString)]
            # print('E:')
            # print(dataString)
            stackData.append(MarkupObject(markupObjName, depth, 'variable'))
            # print(markupObjName + ':')
        except:
            # print('D:')
            # print(dataString)
            stackData.append(MarkupObject(dataString, depth, 'value'))
            # print(dataString)
            return

        try:
            # implement that name into the next regEx search
            regMarkupObjData = re.search('.+?</' + markupObjName + '>', dataString, re.DOTALL).group(0)
            # print('SD:' + regMarkupObjData)
            startIdx = 0
            endIdx = len(regMarkupObjData) - len(markupObjName) - 3
            markupObjData = regMarkupObjData[startIdx:endIdx]
            # print('D: ' + markupObjData)
            regFindNextMarkupObj(markupObjData, depth + 1, stackData)
            
            dataString = dataString[len(regMarkupObjData):len(dataString)]
            # print('D:' + dataString)
        except:
            print('NO DATA')
            return
    

def convertMarkupStackToObjects(stackData):

    queueAttributes = [] # Attribute is a Variable with a Value below it in depth
    listClassObjs = [] # Class is a Variable with multiple Variables below it in depth

    while len(stackData) > 0:

        _a = stackData.pop()
        if _a.type == 'value':
            variable = stackData.pop()
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

#REGEX EXTRA----------------------------------------------------

def displayRegResults(listRegItems, nameOfIemTypes):
# diplay as a vertical list the results of a regular expression search
# NOTE: make sure to hand in a deepcopy of the regExp results so that
# the items are not removed from the original queue

    print(nameOfIemTypes + ':')
    while len(listRegItems) > 0:
        print(listRegItems.pop() + '\n\n')

#MAIN----------------------------------------------------

if __name__ == '__main__':

    file_read = open('codefile.txt', 'r')
    fileData = file_read.read()

    print('parsing code file: ')
    print(fileData + '\n\n')
    print('PARSED:')
    # readInputFileString(fileData)
    # fileData = re.sub('[\\n]|[\\s]', '', fileData)
    # # fileData = re.sub('\\s', '', fileData)
    # print(fileData)
    beginMarkupRead(fileData)

    # attr1 = AttributeFactory.createAttribute('hello', 'false')
    # print(attr1.toString())

    # readInputFileString(data_input)

    # objc = ClassObject("class")
    # attr1 = AttributeNumber('attr1', 20)
    # attr2 = AttributeTruthValue('attr1', True)
    # objc.addAttribute(attr1)
    # objc.addAttribute(attr2)
    # objc.print()
