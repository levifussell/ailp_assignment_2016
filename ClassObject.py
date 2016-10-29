class ClassObject:

    def __init__(self, name):
        self.name = name
        self.attributes = []

    def addAttribute(self, attribute):
        self.attributes.append(attribute)

    def print(self):
        print('CLASS: ' + self.name)

        for i in range(0, len(self.attributes)):
            print('\tATTR_' + str(i) + ': ' + self.attributes[i].toString())