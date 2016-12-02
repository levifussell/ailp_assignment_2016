# used for testing on a computer without Carneades available
IMPORT_CARNEADES = True

if IMPORT_CARNEADES:
    import carneades.src.carneades.caes as cs

from Markup.CodeFile import CodeFile
from Markup.Compilation.MarkupCompiler import MarkupCompiler
from Markup.FileReading.MarkupReader import MarkupReader, ErrorTypes

if IMPORT_CARNEADES:
    from Markup.CarneadesWrite.CarneadesWriter import CarneadesWriter

from _LoggerManager import _Logger_Thread

import re

class _MarkupManager:
    """Class for managing the sequence of events from reading to compiling to
    writing of a Carneades markup script"""
    @staticmethod
    def run(codeFile, testProp, expectedTestResult):
        """
        begin the process given:
        codeFile: markup code script Object
        testProp: the proposition to test at the end of the carneades process
        expectedTestResult: the expected truth value of the testProp
        """

        # create a markup reader
        mlreader = MarkupReader()
        # add the regEx error searches to the markup reader
        mlreader.addErrorType(ErrorTypes.ERR_MATCHINGBRACKETS)
        mlreader.addErrorType(ErrorTypes.ERR_UNKNOWNCHARACTER)
        mlreader.addErrorType(ErrorTypes.ERR_NONMATCHINGLIST)

        # run the markup reader only if no errors found
        if _Logger_Thread.count_errors == 0:
            classObjs = mlreader.run(codeFile)

        # create a markup compiler
        mlcompiler = MarkupCompiler()
        # create a list for each caesClass class type
        caesProps = []
        caesArgs = []
        caesProofStnd = []
        caesArgWeights = []
        caesCAES = []
        # run the markup compiler only if no errors found
        if _Logger_Thread.count_errors == 0:
            caesProps, caesArgs, caesProofStnd, caesArgWeights, caesCAES = mlcompiler.run(classObjs)

        if IMPORT_CARNEADES:
            # create a new cs writer
            csWriter = CarneadesWriter()
            # run the writer only if no errors found
            if _Logger_Thread.count_errors == 0:
                csWriter.build(caesProps, caesArgs, caesProofStnd, caesArgWeights, caesCAES)
                # run test on the Carneades system
                csWriter.testBuild(testProp, expectedTestResult)
                return csWriter.propositions.values(), csWriter.argumentSet, csWriter.audiences[0], csWriter.proofOfStandards[0], csWriter.propositions[testProp]
