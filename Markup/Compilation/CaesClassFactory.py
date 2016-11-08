from .CaesClass import CaesProposition, CaesArgument, CaesProofOfStandards, CaesArgumentWeights, CaesCAES

from _LoggerManager import _Log

class CaesClassFactory:
    """A factory class for creating different Caernades objects. Is not static so
    that it can be extended to create different factories for different compilation
    methods or Caernades sessions"""
    def __init__(self):

        self.initialised = True

    def createCaesClass(self, name, attributes):

        if name == 'Proposition':
            return CaesProposition(attributes)

        elif name == 'Argument':
            return CaesArgument(attributes)

        elif name == 'ProofOfStandard':
            return CaesProofOfStandards(attributes)

        elif name == 'ArgumentWeights':
            return CaesArgumentWeights(attributes)

        elif name == 'CAES':
            return CaesCAES(attributes)

        else: pass
            
