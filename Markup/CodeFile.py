import re

class CodeFile:
    """Format for organising a markup string into a code class"""

    def __init__(self, text):
        self.text_unclean = text
        self.text_formatted = self.__createFormattedCodeText(self.text_unclean)
        self.linebreakIndices = self.__calculateLines(self.text_unclean)

    def __createFormattedCodeText(self, textUnformatted):
        """Remove extra spaces and return characters in the string"""
        return re.sub('[\\n]|[\\s]', '', textUnformatted)

    def __calculateLines(self, textUnformatted):
        """Calculate each return character in the string as a recorded line position in the code string"""
        linebreakIndices = []
        lineIndex = 0
        lineCount = 0
        while lineIndex >= 0:
            lineIndex = textUnformatted.find('\n', lineIndex + 1)
            if lineIndex != -1:
                lineCount += 1
                linebreakIndices.append(lineIndex)

        return linebreakIndices

    def getLineOfText(self, textSnippet):
        """Determine the location of a string snippet in the code text based on the pre-processed
        line (return) positions"""
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
        """Return the code string without extra characters"""
        return self.text_formatted

