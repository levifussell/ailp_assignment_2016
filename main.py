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

from Compilation.CodeFile import CodeFile
from Compilation.MarkupCompiler import MarkupCompiler
from MarkupReader_.MarkupReader import MarkupReader, ErrorTypes

from _LoggerManager import _Logger_Thread, _Log

import re
from copy import copy, deepcopy

import curses
from curses.textpad import Textbox, rectangle

# SIMULATE A FILE READ HERE----
# REGEX FOR GENERIC MARK UP LANGUAGE--------------------------------------

def beginMarkupRead(dataString):

    # start error thread
    _THREAD_log = _Logger_Thread()
    _THREAD_log.start()

    # create a CodeFile object
    codeFile = CodeFile(dataString)

    mlreader = MarkupReader()
    mlreader.addErrorType(ErrorTypes.ERR_MATCHINGBRACKETS)
    mlreader.addErrorType(ErrorTypes.ERR_UNKNOWNCHARACTER)
    classObjs = mlreader.run(codeFile)

    mlcompiler = MarkupCompiler()
    mlcompiler.run(classObjs)


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
