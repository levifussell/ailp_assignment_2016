class MarkupObject:

    def __init__(self, dataString, dataDepth, dataType):
        self.data = dataString
        self.depth = dataDepth
        self.type = dataType

    def toString(self):
        return '{' + self.data + ', ' + self.type + ', ' + str(self.depth) + '}'