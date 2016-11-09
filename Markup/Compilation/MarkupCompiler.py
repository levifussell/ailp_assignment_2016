from Markup.ErrorManagement.MarkupErrorFactory import MarkupError, MarkupErrorFactory, ErrorHandlingTypes, ErrorTypes
from Markup.MarkupClass.ClassObject import ClassObject
from Markup.MarkupClass.AttributeFactory import AttributeFactory

from .CaesClassFactory import CaesClassFactory, CaesProposition, CaesArgument, CaesCAES

from _LoggerManager import _Log, _LoggerState

class CaernadesObjectLayouts:
    """Static class that defines the skeleton structure of different Caernades classes"""

    # hashe codes are not loaded on compile but when they are first requested
    allObjHashesCache = []

    @staticmethod
    def checkObjIsCaernadesObj(objAttrList):
        """Determine whether a markup object has a layout that matches some Caernades
        class; returns true if so, otherwise false"""

        # hash the attributes list
        hashedObj = CaernadesObjectLayouts.__hashObj(objAttrList)

        # check if the hashes are already made, if not, create it and cache it
        if len(CaernadesObjectLayouts.allObjHashesCache) == 0:
            CaernadesObjectLayouts.allObjHashesCache = CaernadesObjectLayouts.__getHashCodes()

        # compare each hash against the object hash to make sure at least one is right
        #  and therefore the object is a legal object to be made
        for i in range(0, len(CaernadesObjectLayouts.allObjHashesCache)):
            if CaernadesObjectLayouts.allObjHashesCache[i] == hashedObj:
                return True

        # no matched object hash, therefore this is not a legal object
        return False

    @staticmethod
    def __getHashCodes():
        """Static definition of different Caernades class constructors (each possible constructor
        for each class). Note that only Proposition, Argument and CAES are present; this is because
        classes Audience and ProofOfStandard are made dynamically during compilation with the
        attributes from Proposition/Argument objects. This makes the writing of scenarios more
        intuitive to the user. NOTE: at the moment the markup only allows for single-value weights
        and proof-of-standards for Propositions and Arguments, therefore a user can only create a
        single CAES object. This is to be extended with lists so that foreach value in the list a
        new CAES object is made; therefore the markup has the same capabilities as Caernades."""

        hashObjs = []

        # Proposition Constructors
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['Proposition', 'name', 'truth']))
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['Proposition', 'name', 'truth', 'proof']))
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['Proposition', 'name']))
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['Proposition', 'name', 'proof']))
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['Proposition', 'name', 'proof', 'negate']))
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['Proposition', 'name', 'negate']))

        # Argument Constructors
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['Argument', 'name', 'conclusion', 'propositions', 'exceptions', 'weight']))
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['Argument', 'name', 'conclusion', 'propositions', 'weight']))

        # CAES Constructors
        hashObjs.append(CaernadesObjectLayouts.__hashObj(['CAES', 'name', 'assumptions']))

        return hashObjs

    @staticmethod
    def __hashObj(objAttrList):
        """given a unordered list of attribute names, create a unique hashcode for these
        specific set of attributes"""
        hashTotal = 0
        for i in range(0, len(objAttrList)):
            # sum hashes so that list is position invariant
            hashTotal += hash(objAttrList[i])

        return hashTotal

class MarkupCompiler:
    """Class for compiling markup objects into Caernades-managable classes. This class
    also does a second order of checking for errors with consistent naming of objects, etc."""

    def __init__(self):
        self.__attrFactory = AttributeFactory()
        self.__caesClassFactory = CaesClassFactory()

    def run(self, classObjects):
        """Perform compilation on a list of markup objects"""

        try:
            _Log('...begin compiling...', _LoggerState.WARNING)

            # lists of different compiled classes
            #  TODO: make dictionary?
            caesProps = []
            caesArgs = []
            caesProofStnd = []
            caesArgWeights = []
            caesCAES = []

            # itterate through each markup object
            for cObj in classObjects:

                # determine if a markup object is able to compile to a Caernades class
                cDefList = cObj.getDefinitionList()
                isCaeObj = CaernadesObjectLayouts.checkObjIsCaernadesObj(cDefList)

                # create unknown-object error if object isn't made with correct constructor
                if isCaeObj == False:
                    self.__createThrowError(ErrorTypes.ERR_HASHCLASSOBJECT, cObj.name, 'unk.')
                    _Log('...compilation failed...\n', _LoggerState.ERROR)
                    return None
                else:
                    # else, create a caernades object instance
                    caesClass = self.__caesClassFactory.createCaesClass(cObj.name, cObj.attributes)

                    # add the caernades object to the corresponding list
                    if caesClass != None:
                        if isinstance(caesClass, CaesProposition):
                            caesProps.append(caesClass)
                        elif isinstance(caesClass, CaesArgument):
                            caesArgs.append(caesClass)
                        elif isinstance(caesClass, CaesCAES):
                            caesCAES.append(caesClass)
                    else: pass
                    # TODO: throw exception here

            # process each proposition
            for i in range(0, len(caesProps)):
                self.__propositionCompile(i, caesProps)

            # process each argument to check names
            for i in range(0, len(caesArgs)):
                self.__argumentCompile(i, caesProps, caesArgs)

            # create ProofOfStandard from propositions
            self.__proofOfStandardCompile(caesProps, caesProofStnd)

            # create ArgumentWeights from propositions
            self.__argumentWeightsCompile(caesArgs, caesArgWeights)

            # process and create final CAES
            self.__caesCompile(caesCAES, caesProofStnd, caesArgWeights)

            # print objects
            for prop in caesProps:
                _Log(prop.toString(), _LoggerState.DEBUG)

            for args in caesArgs:
                _Log(args.toString(), _LoggerState.DEBUG)

            for pos in caesProofStnd:
                _Log(pos.toString(), _LoggerState.DEBUG)

            for argWght in caesArgWeights:
                _Log(argWght.toString(), _LoggerState.DEBUG)

            for caes in caesCAES:
                _Log(caes.toString(), _LoggerState.DEBUG)

            return caesProps, caesArgs, caesProofStnd, caesArgWeights, caesCAES

            _Log('...compilation successful...\n', _LoggerState.WARNING)

        except:
            # throw error because markup reader failed to get data from file
            if classObjects == None or len(classObjects) == 0:
                self.__createThrowError(ErrorTypes.ERR_NULLDATA, 'compiler', 'unk.')

    # compile all propositions (used epecially for the negated oness)
    def __propositionCompile(self, i, caesProps):
        """compile all propositions by checking for no name duplicates and
        negated appropriate propositions"""

        BadNegTagNaming = True
        for j in range(0, len(caesProps)):

            # two props cannot have the same name and truth value
            if i != j and caesProps[i].name == caesProps[j].name:
                self.__createThrowError(ErrorTypes.ERR_SAMENAME, 'Proposition: ' + caesProps[i].name, 'unk.')

            # if this is a negated prop:
            if caesProps[i].negateTag != None:
                 if isinstance(caesProps[i], CaesProposition) and i != j:
                    if caesProps[i].negateTag == caesProps[j].name:
                        caesProps[i].truth = not(caesProps[j].truth)
                        caesProps[i].proof = None
                        # caesProps[i].negateTag = None
                        BadNegTagNaming = False
                        break

        #  if negtag but no proposition was found, create the positive proposition
        if BadNegTagNaming and caesProps[i].negateTag != None:
            propPos = CaesProposition([])
            propPos.name = caesProps[i].negateTag
            caesProps.append(propPos)
            self.__propositionCompile(i, caesProps)
            # self.__createThrowError(ErrorTypes.ERR_BADNEGATION, 'Proposition: ' + caesProps[i].name, 'unk.')

    def __argumentCompile(self, i, caesProps, caesArgs):
        """compile all arguments by checking for no name duplicates and
        that all prop/exceptions have a corresponding proposition with
        that name"""

        # check no duplicate names
        for j in range(0, len(caesArgs)):
            if caesArgs[i].name == caesArgs[j].name and i != j:
                self.__createThrowError(ErrorTypes.ERR_SAMENAME, 'Argument: ' + caesArgs[i].name, 'unk.')

        # check for correct naming of prop/exp
        numCorrectProps = 0
        numCorrectExps = 0

        # check that all propositions exits
        for p in range(0, len(caesArgs[i].propositions)):
            propExists = False
            for j in range(0, len(caesProps)):
                if caesProps[j].name == caesArgs[i].propositions[p]:
                    numCorrectProps += 1
                    propExists = True

            if propExists == False:
                propDynamic = CaesProposition([])
                propDynamic.name = caesArgs[i].propositions[p]
                if propDynamic.name[0:4] == 'neg_':
                    propDynamic.negateTag = propDynamic.name[4:len(propDynamic.name)]

                caesProps.append(propDynamic)
                self.__propositionCompile(len(caesProps) - 1, caesProps)

        # check that all exceptions exits
        for p in range(0, len(caesArgs[i].exceptions)):
            expExists = False
            for j in range(0, len(caesProps)):
                if caesProps[j].name == caesArgs[i].exceptions[p]:
                    numCorrectExps += 1
                    expExists = True

            if expExists == False:
                expDynamic = CaesProposition([])
                expDynamic.name = caesArgs[i].exceptions[p]
                if expDynamic.name[0:4] == 'neg_':
                    expDynamic.negateTag = expDynamic.name[4:len(expDynamic.name)]

                caesProps.append(expDynamic)
                self.__propositionCompile(len(caesProps) - 1, caesProps)

        # check that conclusion exists
        concExists = False
        for j in range(0, len(caesProps)):
            if caesProps[j].name == caesArgs[i].conclusion:
                concExists = True

        if concExists == False:
            concDynamic = CaesProposition([])
            concDynamic.name = caesArgs[i].conclusion
            if concDynamic.name[0:4] == 'neg_':
                concDynamic.negateTag = concDynamic.name[4:len(concDynamic.name)]

            caesProps.append(concDynamic)
            self.__propositionCompile(len(caesProps) - 1, caesProps)

        # throw errors if the number of prop/excep found are not the amount expected
        # if numCorrectProps != len(caesArgs[i].propositions):
        #     self.__createThrowError(ErrorTypes.ERR_NULLDATA, 'Argument - propositions: ' + caesArgs[i].name, 'unk.')
        #
        # if numCorrectExps != len(caesArgs[i].exceptions):
        #     self.__createThrowError(ErrorTypes.ERR_NULLDATA, 'Argument - exceptions: ' + caesArgs[i].name, 'unk.')

    def __proofOfStandardCompile(self, caesProps, caesProofStnd):
        """compile all ProofsOfStandard by getting the propositions and
        taking their 'proof' attribute defined in the markup"""

        # create a string tuple list
        proofTuples = '['

        for i in range(0, len(caesProps)):
            p_name = caesProps[i].name
            p_proof = caesProps[i].proof
            proofTuples += '(' + str(p_name) + ',' + str(p_proof) + ')'

        proofTuples += ']'

        # generate appropriate attributes to hand-make a markup object
        attrProofStnds = []
        attrProofStnds.append(self.__attrFactory.createAttribute('proofPairs', proofTuples))
        attrProofStnds.append(self.__attrFactory.createAttribute('name', 'PoS'))

        # create proof of standard Caernades skeleton class
        caesClass = self.__caesClassFactory.createCaesClass('ProofOfStandard', attrProofStnds)
        caesProofStnd.append(caesClass)

    def __argumentWeightsCompile(self, caesArgs, caesArgWeights):
        """compile all ArgumentWeights by getting the arguments and
        taking their 'weight' attribute defined in the markup"""

        # create a string dictionary
        weights = '{'

        for i in range(0, len(caesArgs)):
            a_name = caesArgs[i].name
            a_weight = caesArgs[i].weight
            weights += '(' + str(a_name) + ',' + str(a_weight) + ')'

        weights += '}'

        # generate appropriate attributes to hand-make a markup object
        attrArgWeights = []
        attrArgWeights.append(self.__attrFactory.createAttribute('weights', weights))
        attrArgWeights.append(self.__attrFactory.createAttribute('name', 'argWeights'))

        # create argument weight Caernades skeleton class
        caesClass = self.__caesClassFactory.createCaesClass('ArgumentWeights', attrArgWeights)
        caesArgWeights.append(caesClass)

    def __caesCompile(self, caesCAES, caesProofStnd, caesArgWeights):
        """compile all CAESs by getting proofsOfStandard and argumentWeights
        TODO: for now only 1 CAES item can be made; extend this to itterate through
        lists of argWeights and proofStnds"""

        caesCAES[0].argWeights = caesArgWeights[0].weights
        caesCAES[0].proofOfStandards = caesProofStnd[0].proofPairs

    def __createThrowError(self, errorType, error_item, line):
        markupError = MarkupErrorFactory.createError(errorType)
        errorText = markupError.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line)
        # self.thrownErrors.append(errorText)
        _Log(errorText, _LoggerState.ERROR)
