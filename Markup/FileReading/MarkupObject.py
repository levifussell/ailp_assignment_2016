class MarkupObject:
    """
    Placeholder class used to organise the markup as it is read by the reader.
    Organised by depth, type string and content (data)
    @param data: a piece of data in a string
    @param depth: markup depth layer
    @param type: string description of type of data
    """

    def __init__(self, dataString, dataDepth, dataType):
        self.data = dataString
        self.depth = dataDepth
        self.type = dataType

    def toString(self):
        """convert the markup object to loggable string representation"""
        return '{' + self.data + ', ' + self.type + ', ' + str(self.depth) + '}'
