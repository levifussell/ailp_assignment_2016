from _LoggerManager import _Log, _LoggerState

import carneades.src.carneades.caes as cs

class CarneadesWriter:

    def __init__(self):
        self.propositions = {}
        self.arguments = {}
        self.argumentSet = None
        self.proofOfStandards = []
        self.argumentWeights = []
        self.audiences = []
        self.CAESs = []

    def build(self, caesProps, caesArgs, caesProofStnd, caesArgWeights, caesCAES):
        self.__buildPropositions(caesProps)
        self.__buildArguments(caesArgs)
        self.__buildArgumentSet()
        self.__buildProofOfStandards(caesProps)
        self.__buildArgumentWeights(caesArgs)
        self.__buildAudience(caesCAES)
        self.__buildCAES()

    def testBuild(self):
        testData = 'Propositions: {\n\t'
        for prop in self.propositions:
            testData += str(self.propositions[prop]) + '\n\t'

        testData += '}\n\nArguments:{\n\t'
        for arg in self.arguments:
            testData += str(self.arguments[arg]) + '\n\t'

        testData += '}\n\nProofStandards:{\n\t'
        for s in range(0, len(self.proofOfStandards)):
            testData += str(self.proofOfStandards[s]) + '\n\t'

        testData += '}\n\nArgumentSet:{\n\t'
        testData += str(self.argumentSet)

        testData += '}\n\nAudience:{\n\t'
        testData += str(self.audiences[0])

        testData += '}\n\CAES:{\n\t'
        testData += str(self.CAESs[0].get_all_arguments_set())
        testData += '\n}'

        testData += '\n'

        self.CAESs[0].acceptable(self.__getPropositionByName('murder'))
        self.CAESs[0].acceptable(self.__getPropositionByName('murder').negate())

        _Log(testData, _LoggerState.DEBUG)

    def __buildPropositions(self, caesProps):

        for i in range(0, len(caesProps)):
            prop = cs.PropLiteral(caesProps[i].name, polarity=caesProps[i].truth)
            self.propositions[caesProps[i].name] = prop

    def __buildArguments(self, caesArgs):

        for i in range(0, len(caesArgs)):
            props = []
            for p in range(0, len(caesArgs[i].propositions)):
                prop = self.__getPropositionByName(caesArgs[i].propositions[p])
                props.append(prop)

            exps = []
            for e in range(0, len(caesArgs[i].exceptions)):
                exp = self.__getPropositionByName(caesArgs[i].exceptions[e])
                exps.append(exp)

            conclusion = self.__getPropositionByName(caesArgs[i].conclusion)

            arg = cs.Argument(conclusion, premises=props, exceptions=exps)
            self.arguments[caesArgs[i].name] = arg

    def __buildArgumentSet(self):

        self.argumentSet = cs.ArgumentSet()

        for argName in self.arguments:
            self.argumentSet.add_argument(self.arguments[argName])

    def __buildProofOfStandards(self, caesProps):

        # TODO: make this work with multiple CAES and therefore multiple proof of standard sets
        proofTuples = []

        for i in range(0, len(caesProps)):
            proofTuple = (self.__getPropositionByName(caesProps[i].name), caesProps[i].proof)
            proofTuples.append(proofTuple)

        ps = cs.ProofStandard(proofTuples, default='scintilla')
        # only 1 possible set of proof of standards for now
        self.proofOfStandards.append(ps)

    def __buildArgumentWeights(self, caesArgs):

        argWeight = {}

        for i in range(0, len(caesArgs)):
            argWeight[caesArgs[i].name] = caesArgs[i].weight

        # only 1 possible set of argument weights for now
        self.argumentWeights.append(argWeight)

    def __buildAudience(self, caesCAES):

        for i in range(0, len(caesCAES)):
            assumptions = []
            for a in range(0, len(caesCAES[i].assumptions)):
                assumptions.append(self.__getPropositionByName(caesCAES[i].assumptions[a]))

            audience = cs.Audience(assumptions, self.argumentWeights[i])
            self.audiences.append(audience)

    def __buildCAES(self):

        for i in range(0, len(self.audiences)):
            caes = cs.CAES(self.argumentSet, self.audiences[i], self.proofOfStandards[i])
            self.CAESs.append(caes)

    # get data
    def __getPropositionByName(self, propName):
        return self.propositions[propName]

    def __getArgumentByName(self, argName):
        return self.arguments[argName]
