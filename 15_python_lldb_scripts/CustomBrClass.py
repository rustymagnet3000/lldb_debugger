class CustomBrClass:
  def __init__(self, name, age):
    self.name = name
    self.age = age

    def myfunc(self):
        print("Hello: " + self.name)