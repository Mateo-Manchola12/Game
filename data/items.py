from constants import COLOR
class item():
    def __init__(self, id, name, color, data=[]):
        self.id = id
        self.name = name
        self.color = color
        self.data = data

items = [
    item("wood","Madera", COLOR.brown),
    item("stone","Piedra", COLOR.gray.dark)
]