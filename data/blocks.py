from constants import COLOR
class BLOCK():
    def __init__(self, id, name, color, colissionable, mineable, data=[]):
        self.id = id
        self.name = name
        self.color = color
        self.colissionable = colissionable
        self.mineable = mineable
        self.data = data

BLOCKS = [
    BLOCK("air","Aire", COLOR.transparent, False, False),
    BLOCK("barrier", "Barrera", COLOR.gray.light, True, False),
    BLOCK("grass","Tierra", COLOR.green.light, True, True),
    BLOCK("wood","Madera", COLOR.brown, True, True),
    BLOCK("stone","Piedra", COLOR.gray.dark, False, True),
    BLOCK("water", "Agua", COLOR.blue.dark, False, False)
]

class block():
    def __init__(self, value, rect, data=[]):
        self.value = value
        self.rect = rect
        self.data = data