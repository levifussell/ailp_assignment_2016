import threading
import atexit
import time
import sys
from enum import Enum

# create a thread lock between the two threads
threadLock = threading.Lock()

class _LoggerState(Enum):
    ERROR = 1
    WARNING = 2
    DEBUG = 3

# when calling this class it should create an error and add it to the global errors list
class _Log (threading.Thread):
    """Calling this class locks the thread and adds a log to the logThrowList to be printed to the screen"""

    def __init__(self, errorText, logState):
        threading.Thread.__init__(self)

        # set the thread to daemon so that it will close when the main thread is closed
        self.daemon = True
        self.errorText = errorText
        self.logState = logState
        # start the thread immediately
        self.start()

    def run(self):
        """lock the thread and add this Log object to the list of logs to throw"""
        threadLock.acquire()
        try:
            # add this log to the log list
            _Logger_Thread.logsToThrowList.append(self)
        finally:
            threadLock.release()

class _Logger_Thread (threading.Thread):
    """A thread for synchronously managing the Log output onto the cmd for errors, warnings and debug statements"""

    # data for setting the end of the program
    programOver = False
    programOverTime = time.time()
    # time to wait before closing this thread to make sure all processes have finished
    programOverTimeElapsedWait = 0.1

    # logging state; whatever the state is, all states below it will be printed.
    #  DEBUG is the highest, ERROR is the lowest
    currentLogState = _LoggerState.DEBUG

    # dynamic list of log objects to print to the cmd
    logsToThrowList = []

    # record list of all errors
    errorsList = []

    # recording the types of logs thrown
    count_errors = 0
    count_warnings = 0
    count_debugs = 0

    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        """Run a looping thread that prints Log objects to the cmd screen dynamically after locking the thread"""

        # record when the thread has started
        print("running: Logger Thread")

        # loop the thread while the program is running, the throw list contains Logs or the closing time hasn't ended
        while _Logger_Thread.programOver == False or (len(_Logger_Thread.logsToThrowList) > 0) or ((time.time() - _Logger_Thread.programOverTime) < _Logger_Thread.programOverTimeElapsedWait):

            # lock the thread if the there are logs in the list
            if len(_Logger_Thread.logsToThrowList) > 0:
                threadLock.acquire()

                # use a try/catch so that the lock will not be lost if the thread crashes
                try:
                    # itterate over the list of Logs to throw
                    for i in range(0, len(_Logger_Thread.logsToThrowList)):

                        # get the state of the log
                        errLogState = _Logger_Thread.logsToThrowList[i].logState

                        # if the current allowed logging state is greater than the log state, print the log
                        if _Logger_Thread.getLogState().value >= errLogState.value:
                            print(_Logger_Thread.logsToThrowList[i].errorText)

                        # document the log states processed
                        if errLogState == _LoggerState.ERROR:
                            _Logger_Thread.count_errors += 1
                            _Logger_Thread.errorsList.append(_Logger_Thread.logsToThrowList[i].errorText)
                        elif errLogState == _LoggerState.WARNING:
                            _Logger_Thread.count_warnings += 1
                        elif errLogState == _LoggerState.DEBUG:
                            _Logger_Thread.count_debugs += 1
                finally:
                    # empty the list of logs to throw
                    _Logger_Thread.logsToThrowList.clear()
                    # release the lock for this thread
                    threadLock.release()

                    if _Logger_Thread.count_errors > 0:
                        print('\n---------------------\n---------------------\nERROR THROWN (see cmd output)\n---------------------\n---------------------\n')
                        for i in range(0, len(_Logger_Thread.errorsList)):
                            print(_Logger_Thread.errorsList[i] + '\n')
                        _Logger_Thread.printLoggingStats()
                        sys.exit()

        # at the end of this thread, print out the logging stats
        _Logger_Thread.printLoggingStats()

    @staticmethod
    def printLoggingStats():
        """Write out the count of errors/warnings/debugs during the logging period"""
        print('LOGGER OUTPUT:\n\tERRORS: {}\n\tWARNINGS: {}\n\tDEBUGS: {}\n'.
            format(_Logger_Thread.count_errors, _Logger_Thread.count_warnings, _Logger_Thread.count_debugs))

    @staticmethod
    def setLogState(logState):
        """Set the allowed logging state"""
        _Logger_Thread.currentLogState = logState

    @staticmethod
    def getLogState():
        """Get the allowed logging state"""
        return _Logger_Thread.currentLogState
