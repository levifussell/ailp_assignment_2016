from _LoggerManager import _Log, _LoggerState

import carneades.src.carneades.caes as cs

class CarneadesWriter:
    """
    class for converting Skeleton Carneades classes directly to Carneades objects.
    Also runs a caernades simulation of the data

    @param propositions: dictionary of all Carneades propositions
    @param argument: list of all Carneades arguments (no dictionary so arguments retain order)
    @param argumentSet: a Carneades argument set of all arguments
    @param proofOfStandards: a list of Carneades proofStandard of the propositions (only support for one at the moment)
    @param agumentWeights: a list of argument weight dictionaries (only support for one at the moment)
    @param audiences: a list of Carneades audiences (only support for one at the moment)
    @param CAESs: a list of Carneades CAES objects (only support for one at the moment)
    """
    def __init__(self):
        self.propositions = {}
        self.arguments = []
        self.argumentSet = None
        self.proofOfStandards = []
        self.argumentWeights = []
        self.audiences = []
        self.CAESs = []

    def build(self, caesProps, caesArgs, caesProofStnd, caesArgWeights, caesCAES):
        """begin the sequential build of all Carneades object"""
        self.__buildPropositions(caesProps)
        self.__buildArguments(caesArgs)
        self.__buildArgumentSet(caesArgs)
        self.__buildProofOfStandards(caesProps)
        self.__buildArgumentWeights(caesArgs)
        self.__buildAudience(caesCAES)
        self.__buildCAES()

    def testBuild(self):
        """Writes out the values of the Carneades objets for debugging and also simulates
        test on a specific argument to test the CAES system is working"""

        testData = 'Propositions: {\n\t'
        for prop in self.propositions:
            testData += str(self.propositions[prop]) + '\n\t'

        testData += '}\n\nArguments:{\n\t'
        for i in range(0, len(self.arguments)):
            testData += str(self.arguments[i]) + '\n\t'

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

        # test the CAES system
        self.CAESs[0].acceptable(self.__getPropositionByName('ticket_revoked'))
        self.CAESs[0].acceptable(self.__getPropositionByName('ticket_revoked').negate())

        _Log(testData, _LoggerState.WARNING)

    def __buildPropositions(self, caesProps):
        """Create Carneades Proposition objects from all proposition caesClass objects"""
        for i in range(0, len(caesProps)):
            # make sure that negative propositions are added the same as their positive
            #  counterpart
            if caesProps[i].negateTag != None:
                prop = cs.PropLiteral(caesProps[i].negateTag, polarity=caesProps[i].truth)
                self.propositions[caesProps[i].name] = prop
            else:
                prop = cs.PropLiteral(caesProps[i].name, polarity=caesProps[i].truth)
                self.propositions[caesProps[i].name] = prop

    def __buildArguments(self, caesArgs):
        """Create Carneades Argument objects from all arguments caesClass objects"""
        for i in range(0, len(caesArgs)):
            # get premises and organise into a list
            props = []
            for p in range(0, len(caesArgs[i].propositions)):
                prop = self.__getPropositionByName(caesArgs[i].propositions[p])
                props.append(prop)

            # get exceptions and organise into a list
            exps = []
            for e in range(0, len(caesArgs[i].exceptions)):
                exp = self.__getPropositionByName(caesArgs[i].exceptions[e])
                exps.append(exp)

            # get the conclusion from the set of Caernades Propositions
            conclusion = self.__getPropositionByName(caesArgs[i].conclusion)

            # create the Caernades Argument and add to list
            arg = cs.Argument(conclusion, premises=props, exceptions=exps)
            self.arguments.append(arg)

    def __buildArgumentSet(self, caesArgs):
        """Create Carneades ArgumentSet objects from Carneades Arguments.
        Note: this method could be merged with __buildArguments, but it is
        left seperate for readability"""
        self.argumentSet = cs.ArgumentSet()

        # add arguments in reverse order, so that they are recorded in the original order in the CAES
        for i in range(0, len(self.arguments)):
            self.argumentSet.add_argument(self.arguments[len(self.arguments) - i - 1], arg_id=caesArgs[len(self.arguments) - i - 1].name)

    def __buildProofOfStandards(self, caesProps):
        """Create Carneades ProofStandards objects from all proposition caesClass objects"""
        # TODO: make this work with multiple CAES and therefore multiple proof of standard sets
        proofTuples = []

        for i in range(0, len(caesProps)):
            # make sure negative propositions use the correct name
            if caesProps[i].proof != None:
                proofTuple = (self.__getPropositionByName(caesProps[i].name), caesProps[i].proof)
                proofTuples.append(proofTuple)

        ps = cs.ProofStandard(proofTuples, default='scintilla')
        # only 1 possible set of proof of standards for now
        self.proofOfStandards.append(ps)

    def __buildArgumentWeights(self, caesArgs):
        """Create ArgumentWeight dictionaries from all argument caesClass objects"""
        argWeight = {}

        for i in range(0, len(caesArgs)):
            argWeight[caesArgs[i].name] = caesArgs[i].weight

        # only 1 possible set of argument weights for now
        self.argumentWeights.append(argWeight)

    def __buildAudience(self, caesCAES):
        """Create Carneades Audience objects from all Carneades Propositions
        and the CAES caesClass object"""
        for i in range(0, len(caesCAES)):
            # get the propositions corresponding to each CAES assumption
            assumptions = []
            for a in range(0, len(caesCAES[i].assumptions)):
                assumptions.append(self.__getPropositionByName(caesCAES[i].assumptions[a]))

            # create an audience object and add to list
            audience = cs.Audience(assumptions, self.argumentWeights[i])
            self.audiences.append(audience)

    def __buildCAES(self):
        """Create Carneades CAES objects from all audience, proofStandards and argumentSets"""
        for i in range(0, len(self.audiences)):
            caes = cs.CAES(self.argumentSet, self.audiences[i], self.proofOfStandards[i])
            self.CAESs.append(caes)

    # get data
    def __getPropositionByName(self, propName):
        """get a proposition from the dictionary given a name key"""
        return self.propositions[propName]
