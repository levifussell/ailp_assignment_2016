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

    @staticmethod
    def run(codeFile):

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
