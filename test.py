class Zoom:
    def __init__(self):
        self.value = 1

    def __str__(self):
        return str(self.value)

    def __set__(self, instance, value):
        print("entering __ep__")


foo = Zoom()
foo = "string"
print(type(foo), foo)