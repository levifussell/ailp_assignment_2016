"""READING FILES INTO CAES:

<!>PROPOSITIONS:<!>
<Proposition>
  <name>NAME</name>
  <truth>TRUE</truth>
</Proposition>

<!>ARGUEMENTS:<!>
<Argument>
  <propositions>[P1, P2, P3]</propositions>
  <exceptions>[P1, P2, P3]</exceptions>
  <outcome>PROPOSITION</outcome>
</Arguement>

--

--------------------------------------
--------------------------------------
**see README.md for more information**
--------------------------------------
--------------------------------------

"""

from Markup._MarkupManager import _MarkupManager
from Markup.CodeFile import CodeFile
from BurdenOfProof._BurdenOfProofManager import _BurdenOfProofManager, _ArgumentSearchHeuristic
from _LoggerManager import _Logger_Thread, _LoggerState, _Log

import time

# SIMULATE A FILE READ HERE----
# REGEX FOR GENERIC MARK UP LANGUAGE--------------------------------------

def beginMarkupRead(codeFile, testProp, expectedTestResult, searchHeuristic = _ArgumentSearchHeuristic.DJIKSTRA, prosName='PROSECUTION', defName='DEFENSE'):

    # start error thread
    _THREAD_log = _Logger_Thread()
    _THREAD_log.start()

    # create a CodeFile object
    codeFile = CodeFile(codeFile)

    # read, compile and process the markup file to Carneades system
    allPropositions, allArgumentSet, allAudience, allProofOfStandard, targetArgProp = _MarkupManager.run(codeFile, testProp, expectedTestResult)

    burdenProofSim = _BurdenOfProofManager(allPropositions, allArgumentSet, allAudience, allProofOfStandard, targetArgProp, searchHeuristic, prosName, defName)

    # do 5 steps for now
    state = 0
    while state == 0:
        state = burdenProofSim.step()

    _Log("\n\nARGUMENT OVER. WINNER: {}\n\n".format(burdenProofSim.nameFromState(state)), _LoggerState.WARNING)

    # end the process and give the threads time to close
    _Logger_Thread.programOverTime = time.time()
    _Logger_Thread.programOver = True


#MAIN----------------------------------------------------

if __name__ == '__main__':

    testNum = input('1, 2, 3, 4 or e to run test 1, 2, 3, or 4, or error testing: ')

    # begin process
    if testNum == '1':
        beginMarkupRead('CodeTests/codeTest1.txt', 'ticket_revoked', True, prosName='TICKET', defName='NO TICKET')
    elif testNum == '2':
        beginMarkupRead('CodeTests/codeTest2.txt', 'give_citizenship', False, prosName='NO CITIZENSHIP', defName='CITIZENSHIP')
    elif testNum == '3':
        beginMarkupRead('CodeTests/codeTest3.txt', 'shoplifting', True, prosName='NO SHOPLIFTING', defName='SHOPLIFTING')
    elif testNum == '4':
        heuristic = input('choose argument search heuristic:\n d = depth-first\n b = breadth-first\n m = min-weight-first\n k = djikstra\n')
        argSearchHeuristic = _ArgumentSearchHeuristic.DEPTH_FIRST
        if heuristic == 'd':
            argSearchHeuristic = _ArgumentSearchHeuristic.DEPTH_FIRST
        if heuristic == 'b':
            argSearchHeuristic = _ArgumentSearchHeuristic.BREADTH_FIRST
        if heuristic == 'm':
            argSearchHeuristic = _ArgumentSearchHeuristic.MIN_WEIGHT_FIRST
        if heuristic == 'k':
            argSearchHeuristic = _ArgumentSearchHeuristic.DJIKSTRA

        beginMarkupRead('CodeTests/codeTest4.txt', 'T', True, argSearchHeuristic)
    elif testNum == 'e':
        errorNum = input('1, 2, 3, 4, 5, 6, 7, 8, 9 to run error tests: ')
        # we only care about the state in error mode, so preset it
        _Logger_Thread.currentLogState = _LoggerState.ERROR

        if errorNum == '1':
            beginMarkupRead('CodeErrorTests/codeError1_brackets.txt', '', True)
        elif errorNum == '2':
            beginMarkupRead('CodeErrorTests/codeError2_brackets.txt', '', True)
        elif errorNum == '3':
            beginMarkupRead('CodeErrorTests/codeError3_nonmatchingname.txt', '', True)
        elif errorNum == '4':
            beginMarkupRead('CodeErrorTests/codeError4_badcomments.txt', '', True)
        elif errorNum == '5':
            beginMarkupRead('CodeErrorTests/codeError5_badconstructor.txt', '', True)
        elif errorNum == '6':
            beginMarkupRead('CodeErrorTests/codeError6_badlists.txt', '', True)
        elif errorNum == '7':
            beginMarkupRead('CodeErrorTests/codeError7_badmarkuplayers.txt', '', True)
        elif errorNum == '8':
            beginMarkupRead('CodeErrorTests/codeError8_samename.txt', '', True)
        elif errorNum == '9':
            beginMarkupRead('CodeErrorTests/codeError9_wrongassumptions.txt', 'prop1', True)
        else:
            print('not a valid input')
    else:
        print('not a valid input')
