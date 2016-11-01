# READING FILES INTO CAES:
# 
# --PROPOSITIONS:
# <Proposition>
#   <name>NAME</name>
#   <truth>TRUE</truth>
# </Proposition>
# 
# --ARGUEMENTS:
# <Argument>
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
from CodeFile import CodeFile

import re
from copy import copy, deepcopy

import curses
from curses.textpad import Textbox, rectangle

# SIMULATE A FILE READ HERE----
# REGEX FOR GENERIC MARK UP LANGUAGE--------------------------------------

def beginMarkupRead(dataString):

    # create a CodeFile object
    codeFile = CodeFile(dataString)

    # find all linebreak locations
    # linebreakIndices = []
    # lineIndex = 0
    # while lineIndex >= 0:
    #     lineIndex = dataString.find('\n', lineIndex + 1)
    #     if lineIndex != -1:
    #         linebreakIndices.append(lineIndex)
    #         # print(lineIndex)

    # for i in range(0, len(linebreakIndices)):
    #     print(linebreakIndices[i])

    # remove extra spaces and newlines from text file
    # dataString = re.sub('[\\n]|[\\s]', '', dataString)
    # record the extracted data in a stack
    stackData = []
    # recursively extract markup data
    regFindNextMarkupObj(codeFile.getCleanCodeText(), 0, stackData)

    # for i in range(0, len(stackData)):
    #     print(stackData[i].toString())

    # convert the markup data stack to class objects
    errorList = regFindSyntaxErrors(codeFile)

    if len(errorList) == 0:
        listClassObjs = convertMarkupStackToObjects(stackData)

        for i in range(0, len(listClassObjs)):
            listClassObjs[i].print()

    else:
        print('ERRORS FOUND: ')
        for i in range(0, len(errorList)):
            print(errorList[i])

def regFindSyntaxErrors(codeFile):

    dataString = codeFile.getCleanCodeText()
    errorsList = []

    try:
        # check all '<>' are matching and NOT embedded
        error_matchingBrackets = re.search('(<[^<|^>]*<[^<|^>]*)|(>[^<|^>]*>[^<|^>]*)', dataString, re.DOTALL)

        errorValue = error_matchingBrackets.group(0)
        errorsList.append('error \'' + errorValue + '\' found at line ' + str(codeFile.getLineOfText(errorValue)))
    except:
        print('NO BRACKET ERRORS')

    return errorsList

def regFindNextMarkupObj(dataString, depth, stackData):
    while len(dataString) > 0:

        # get the name of the next markup obj
        try:
            regMarkupObjName = re.search('<[\w|!]+?>', dataString, re.DOTALL).group(0)
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
            # return
    

def convertMarkupStackToObjects(stackData):

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

    # TODO: UNCOMMENT TO RUN COMPILER ON TEXT
    beginMarkupRead(fileData)

    # -----------------------------------------
    # stdscr = curses.initscr()
    # stdscr.keypad(True)
    # curses.cbreak()
    # curses.noecho()

    # stdscr.addstr(0, 0, "Enter IM message: (hit Ctrl-G to send)")

    # editwin = curses.newwin(5,30, 2,1)
    # rectangle(stdscr, 1,0, 1+20+1, 1+30+1)
    # stdscr.refresh()

    # box = Textbox(editwin)

    # # Let the user edit until Ctrl-G is struck.
    # box.edit()

    # # Get resulting contents
    # message = box.gather()

    # curses.nocbreak()
    # stdscr.keypad(False)
    # curses.echo()
    # curses.endwin()
    # -----------------------------------------

    # while True:
    #     curses.echo()
    #     c = stdscr.getch()
    #     if c == curses.KEY_BACKSPACE:
    #         stdscr.addch(' ')
    #         [y, x] = curses.getsyx()
    #         if x > 0:
    #             stdscr.move(y, x)
    #         elif y > 0:
    #             stdscr.move(y - 1, x)

    #         stdscr.refresh()

    #     if c == curses.KEY_ENTER or c == 10 or c == 13:
    #         [y, x] = curses.getsyx()
    #         stdscr.move(y + 1, 0)
    #     elif c == ord('q'):
    #         curses.nocbreak()
    #         stdscr.keypad(False)
    #         curses.echo()
    #         curses.endwin()
    #         break

    # attr1 = AttributeFactory.createAttribute('hello', 'false')
    # print(attr1.toString())

    # readInputFileString(data_input)

    # objc = ClassObject("class")
    # attr1 = AttributeNumber('attr1', 20)
    # attr2 = AttributeTruthValue('attr1', True)
    # objc.addAttribute(attr1)
    # objc.addAttribute(attr2)
    # objc.print()
