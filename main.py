# READING FILES INTO CAES:
#
# <!>PROPOSITIONS:<!>
# <Proposition>
#   <name>NAME</name>
#   <truth>TRUE</truth>
# </Proposition>
#
# <!>ARGUEMENTS:<!>
# <Argument>
#   <propositions>[P1, P2, P3]</propositions>
#   <exceptions>[P1, P2, P3]</exceptions>
#   <outcome>PROPOSITION</outcome>
# </Arguement>
#
# --
#
# -----------------------------------
# -----------------------------------
# see README.md for more information
# -----------------------------------
# -----------------------------------

from Markup._MarkupManager import _MarkupManager
from Markup.CodeFile import CodeFile
from _LoggerManager import _Logger_Thread

import time

# SIMULATE A FILE READ HERE----
# REGEX FOR GENERIC MARK UP LANGUAGE--------------------------------------

def beginMarkupRead(codeFile):

    # start error thread
    _THREAD_log = _Logger_Thread()
    _THREAD_log.start()

    # create a CodeFile object
    codeFile = CodeFile(codeFile)

    # read, compile and process the markup file to Carneades system
    _MarkupManager.run(codeFile)

    # end the process and give the threads time to close
    _Logger_Thread.programOverTime = time.time()
    _Logger_Thread.programOver = True


#MAIN----------------------------------------------------

if __name__ == '__main__':

    beginMarkupRead('codeTest1.txt')
