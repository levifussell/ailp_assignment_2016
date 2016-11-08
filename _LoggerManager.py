import threading

import atexit

import time

from enum import Enum

threadLock = threading.Lock()

class _LoggerState(Enum):
    ERROR = 1
    WARNING = 2
    DEBUG = 3

# when calling this class it should create an error and add it to the global errors list
class _Log (threading.Thread):
    
    def __init__(self, errorText, logState):
        threading.Thread.__init__(self)
        self.errorText = errorText
        self.logState = logState
        self.start()

    def run(self):
        threadLock.acquire()
        try:
            _Logger_Thread.logsToThrowList.append(self)
        finally:
            threadLock.release()

class _Logger_Thread (threading.Thread):

    programOver = False
    programOverTime = time.time()
    programOverTimeElapsedWait = 0.1

    currentLogState = _LoggerState.DEBUG
    logsToThrowList = []

    count_errors = 0
    count_warnings = 0
    count_debugs = 0

    def __init__(self):
        threading.Thread.__init__(self)
        # stop this thread from running once the main thread has closed
        # self.daemon = True

    def run(self):
        print("running: Logger Thread")

        while _Logger_Thread.programOver == False or (len(_Logger_Thread.logsToThrowList) > 0) or ((time.time() - _Logger_Thread.programOverTime) < _Logger_Thread.programOverTimeElapsedWait):

            # print(time.time() - _Logger_Thread.programOverTime)
            # print(_Logger_Thread.programOverTimeElapsedWait)

            if len(_Logger_Thread.logsToThrowList) > 0:
                threadLock.acquire()

                try:
                    for i in range(0, len(_Logger_Thread.logsToThrowList)):

                        # threadLock.acquire()
                        errLogState = _Logger_Thread.logsToThrowList[i].logState
                        if _Logger_Thread.getLogState().value >= errLogState.value:
                            print(_Logger_Thread.logsToThrowList[i].errorText)

                        if errLogState == _LoggerState.ERROR:
                            _Logger_Thread.count_errors += 1
                        elif errLogState == _LoggerState.WARNING:
                            _Logger_Thread.count_warnings += 1
                        elif errLogState == _LoggerState.DEBUG:
                            _Logger_Thread.count_debugs += 1

                        # _Logger_Thread.logsToThrowList.remove(_Logger_Thread.logsToThrowList[i])
                finally:
                    # if threadLock.locked():
                    threadLock.release()
                    _Logger_Thread.logsToThrowList.clear()

        print('LOGGER OUTPUT:\n\tERRORS: {}\n\tWARNINGS: {}\n\tDEBUGS: {}'.
            format(_Logger_Thread.count_errors, _Logger_Thread.count_warnings, _Logger_Thread.count_debugs))

    # def exit_handler():
    #     print('LOGGER OUTPUT:\n\tERRORS: {}\n\tWARNINGS: {}\n\tDEBUGS: {}'.
    #         format(_Logger_Thread.count_errors, _Logger_Thread.count_warnings, _Logger_Thread.count_debugs))

    # atexit.register(exit_handler)

    @staticmethod
    def setLogState(logState):
        _Logger_Thread.currentLogState = logState

    @staticmethod
    def getLogState():
        return _Logger_Thread.currentLogState
        