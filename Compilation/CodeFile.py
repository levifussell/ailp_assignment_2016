import re

class CodeFile:

    def __init__(self, text):

        self.text_unclean = text
        self.text_formatted = self.__createFormattedCodeText(self.text_unclean)
        self.linebreakIndices = self.__calculateLines(self.text_unclean)

    def __createFormattedCodeText(self, textUnformatted):
        return re.sub('[\\n]|[\\s]', '', textUnformatted)

    def __calculateLines(self, textUnformatted):
        linebreakIndices = []
        lineIndex = 0
        while lineIndex >= 0:
            lineIndex = textUnformatted.find('\n', lineIndex + 1)
            if lineIndex != -1:
                linebreakIndices.append(lineIndex)
                # print(lineIndex)

        # for i in range(0, len(linebreakIndices)):
        #     print(linebreakIndices[i])
        return linebreakIndices

    def getLineOfText(self, textSnippet):
        
        try:
            indexOfText = self.text_unclean.find(textSnippet)

            # no line found, return -1 as item is not in file
            if indexOfText == -1:
                return -1

            for i in range(0, len(self.linebreakIndices)):
                if self.linebreakIndices[i] >= indexOfText:
                    return i + 1

            # no line found, return -1 as item is not in file
            return -1

        except:
            raise IndexError('text not found in code file')

    def getCleanCodeText(self):
        return self.text_formatted

