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

IMPORT_CARNEADES = True

if IMPORT_CARNEADES:
    import carneades.src.carneades.caes as cs

from Markup.CodeFile import CodeFile
from Markup.Compilation.MarkupCompiler import MarkupCompiler
from Markup.FileReading.MarkupReader import MarkupReader, ErrorTypes
from Markup.MarkupClass.Attribute import AttributeTupleList

if IMPORT_CARNEADES:
    from Markup.CarneadesWrite.CarneadesWriter import CarneadesWriter

from _LoggerManager import _Logger_Thread, _Log

import re
from copy import copy, deepcopy

import time

import curses
from curses.textpad import Textbox, rectangle

# SIMULATE A FILE READ HERE----
# REGEX FOR GENERIC MARK UP LANGUAGE--------------------------------------

def beginMarkupRead(codeFile):

    # start error thread
    _THREAD_log = _Logger_Thread()
    _THREAD_log.start()

    # create a CodeFile object
    codeFile = CodeFile(codeFile)

    mlreader = MarkupReader()
    mlreader.addErrorType(ErrorTypes.ERR_MATCHINGBRACKETS)
    mlreader.addErrorType(ErrorTypes.ERR_UNKNOWNCHARACTER)
    mlreader.addErrorType(ErrorTypes.ERR_NONMATCHINGLIST)

    if _Logger_Thread.count_errors == 0:
        classObjs = mlreader.run(codeFile)

    mlcompiler = MarkupCompiler()
    caesProps = []
    caesArgs = []
    caesProofStnd = []
    caesArgWeights = []
    caesCAES = []
    if _Logger_Thread.count_errors == 0:
        caesProps, caesArgs, caesProofStnd, caesArgWeights, caesCAES = mlcompiler.run(classObjs)

    if IMPORT_CARNEADES:
        csWriter = CarneadesWriter()
        if _Logger_Thread.count_errors == 0:
            csWriter.build(caesProps, caesArgs, caesProofStnd, caesArgWeights, caesCAES)
            csWriter.testBuild()

    _Logger_Thread.programOverTime = time.time()
    _Logger_Thread.programOver = True


#MAIN----------------------------------------------------

if __name__ == '__main__':

    # file_read = open('codeTest2.txt', 'r')
    # fileData = file_read.read()
    #
    # print('parsing code file: ')
    # print(fileData + '\n\n')
    # print('PARSED:')
    # readInputFileString(fileData)
    # fileData = re.sub('[\\n]|[\\s]', '', fileData)
    # # fileData = re.sub('\\s', '', fileData)
    # print(fileData)

    # TODO: UNCOMMENT TO RUN COMPILER ON TEXT
    beginMarkupRead('codeTest2.txt')

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
