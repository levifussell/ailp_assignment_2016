from MarkupReader_.MarkupErrors_.MarkupErrorFactory import MarkupError, MarkupErrorFactory, ErrorHandlingTypes, ErrorTypes

from .GenericClass.ClassObject import ClassObject

from _LoggerManager import _Log, _LoggerState

class CaernadesObjectLayouts:

    allObjHashesCache = []

    @staticmethod
    def checkObjIsCaernadesObj(objAttrList):

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
        propositionHash = CaernadesObjectLayouts.__hashObj(['Proposition', 'name', 'truth'])
        argumentHash = CaernadesObjectLayouts.__hashObj(['Argument', 'name', 'propositions', 'exceptions'])

        allObjHashes = [propositionHash, argumentHash] 

        return allObjHashes

    @staticmethod
    def __hashObj(objAttrList):
        hashTotal = 0
        for i in range(0, len(objAttrList)):
            hashTotal += hash(objAttrList[i])

        return hashTotal

class MarkupCompiler:

    def __init__(self):
        self.__errorFactory = MarkupErrorFactory()
        # self.thrownErrors = []

    def run(self, classObjects):

        # if classObjects == None or len(classObjects) == 0:
        #     mErr = self.__errorFactory.createError(ErrorTypes.ERR_NULLDATA)
        #     self.__createThrowError(mErr, 'compiler', 'unk.')

        try:
            _Log('...begin compiling...', _LoggerState.WARNING)

            propNamesList = []

            for cObj in classObjects:
                
                # check each object against its name

                cDefList = cObj.getDefinitionList()
                isCaeObj = CaernadesObjectLayouts.checkObjIsCaernadesObj(cDefList)
                
                if isCaeObj == False:
                    mErr = self.__errorFactory.createError(ErrorTypes.ERR_HASHCLASSOBJECT)
                    self.__createThrowError(mErr, cObj.name, 'unk.')

            
            _Log('...compilation successful...\n', _LoggerState.WARNING)

        except:
            if classObjects == None or len(classObjects) == 0:
                mErr = self.__errorFactory.createError(ErrorTypes.ERR_NULLDATA)
                self.__createThrowError(mErr, 'compiler', 'unk.')

            # if cObj.name == 'Proposition':
            #     # get name of attribute
            #     try:
            #         attrName = cObj.findAttributeByName('name')
            #         propNamesList.append(attrName.value)
            #     except:
            #         # print('error')
            #         propErr = self.__errorFactory.createError(ErrorTypes.ERR_PROPOSITION)
            #         self.__createThrowError(propErr, 'name', 'unk.')

            #     try:
            #         attr

            # elif cObj.name == 'Argument':

    def __createThrowError(self, markupError, error_item, line):
        errorText = markupError.toString() + '  ' + '\'' + error_item + '\' at line ' + str(line)
        # self.thrownErrors.append(errorText)
        _Log(errorText, _LoggerState.ERROR) 