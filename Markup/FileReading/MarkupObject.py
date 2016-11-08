class MarkupObject:
    """Placeholder class used to organise the markup as it is read by the reader.
    Organised by depth, type string and content (data)"""

    def __init__(self, dataString, dataDepth, dataType):
        self.data = dataString
        self.depth = dataDepth
        self.type = dataType

    def toString(self):
        return '{' + self.data + ', ' + self.type + ', ' + str(self.depth) + '}'