class SomeClass:
    def __init__(self, propValue=0) -> None:
        self.setAttachedProperty(propValue)

    def setAttachedProperty(self, propValue):
        self.attachedProperty = propValue

    def getAttachedProperty(self):
        return self.attachedProperty

    def printContent(self):
        print(f'attached property value from class {self.attachedProperty}')


if __name__ == "__main__":
    obj = SomeClass(5)
    obj.printContent()
    print(f'value of attached property {obj.getAttachedProperty()}')
