from Markup.MarkupClass.Attribute import Attribute

from abc import ABCMeta, abstractmethod

# TODO: CHECK THAT ATTRIBUTES PROVIDED ARE OF THE RIGHT OBJECT TYPE!!
#   OTHERWISE THROW ERROR

class CaesClass:
    """An abstract Caernades class used to build Caernades skeleton objects
    from markup data"""
    __metaclass__ = ABCMeta

    def __init__(self, attributes):

        for i in range(0, len(attributes)):
            self.processAttribute(attributes[i])

    @abstractmethod
    def processAttribute(self, attribute): 
        """Abstract method to process a single attribute from markup to Caernades"""
        raise NotImplementedError( "CaesClass method processAttribute not implemented" )

    @abstractmethod
    def toString(self):
        """Convert this object to a printable string format for debugging"""
        raise NotImplementedError( "CaesClass method toString not implemented" )

class CaesProposition(CaesClass):
    """Caernades Proposition skeleton class that converts markup to a managable
    format to be used in caernades"""

    def __init__(self, attributes):
        self.name = None
        self.truth = True
        self.proof = 'scintilla'
        self.negateTag = None

        CaesClass.__init__(self, attributes)

    def processAttribute(self, attribute):

        if attribute.name == 'name':
            self.name = attribute.value

        elif attribute.name == 'negate':
            self.negateTag = attribute.value
            self.truth = None

        elif attribute.name == 'truth':
            self.truth = attribute.value

        elif attribute.name == 'proof':
            self.proof = attribute.value

    def toString(self):
        return 'Proposition: ' + str(self.name) + '=' + str(self.truth) + ', proof =' + str(self.proof) + ', negate =' + str(self.negateTag)

class CaesArgument(CaesClass):
    """Caernades Argument skeleton class that converts markup to a managable
    format to be used in caernades"""

    def __init__(self, attributes):
        self.name = None
        self.conclusion = None
        self.propositions = None
        self.exceptions = []
        self.weight = None

        CaesClass.__init__(self, attributes)

    def processAttribute(self, attribute):

        if attribute.name == 'name':
            self.name = attribute.value

        elif attribute.name == 'conclusion':
            self.conclusion = attribute.value

        elif attribute.name == 'propositions':
            self.propositions = attribute.value

        elif attribute.name == 'exceptions':
            self.exceptions = attribute.value
        
        elif attribute.name == 'weight':
            self.weight = attribute.value

    def toString(self):
        return 'Argument: ' + str(self.name) + ': ' + str(self.propositions) + ', ' + str(self.exceptions) + ' => ' + str(self.conclusion) + ' (' + str(self.weight) + ')' 

class CaesProofOfStandards(CaesClass):
    """Caernades ProofOfStandard skeleton class that converts markup to a managable
    format to be used in caernades"""

    def __init__(self, attributes):
        self.name = None
        self.proofPairs = None

        CaesClass.__init__(self, attributes)

    def processAttribute(self, attribute):

        if attribute.name == 'name':
            self.name = attribute.value
        
        elif attribute.name == 'proofPairs':
            self.proofPairs = attribute.value

    def toString(self):
        return 'ProofOfStandard: ' + str(self.name) + ': ' + str(self.proofPairs)

class CaesArgumentWeights(CaesClass):
    """Caernades ArgumentWeights skeleton class that converts markup to a managable
    format to be used in caernades"""

    def __init__(self, attributes):
        self.name = None
        self.weights = None

        CaesClass.__init__(self, attributes)

    def processAttribute(self, attribute):
        if attribute.name == 'name':
            self.name = attribute.value
        
        elif attribute.name == 'weights':
            self.weights = attribute.value

    def toString(self):
        return 'ArgumentWeights: ' + str(self.name) + ': ' + str(self.weights)

class CaesCAES(CaesClass):
    """Caernades CAES skeleton class that converts markup to a managable
    format to be used in caernades"""

    def __init__(self, attributes):
        self.name = None
        self.assumptions = None
        self.argWeights = None
        self.proofOfStandards = None

        CaesClass.__init__(self, attributes)

    def processAttribute(self, attribute):

        if attribute.name == 'name':
            self.name = attribute.value

        elif attribute.name == 'assumptions':
            self.assumptions = attribute.value

        # elif attribute.name == 'argWeights':
        #     self.argWeights = attribute.value

        # elif attribute.name == 'proofs':
        #     self.proofOfStandards = attribute.value

    def toString(self):
        return 'CAES: ' + str(self.name) + ': asmp=' + str(self.assumptions) + ', argwgt=' + str(self.argWeights) + ', proofs=' + str(self.proofOfStandards)
