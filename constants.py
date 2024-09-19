from libs.colorCreate import newColor
class SIZES:
    width = 720
    height = 480
    gridSize = 20
class PHYSICS:
    speed = SIZES.gridSize/5
class COLOR: 
    white = (255, 255, 255)
    black = (0,0,0)
    brown = (139,69,19)
    transparent = (0,0,0,0)
    blue = newColor((0, 0, 255), (0, 0, 255), (0, 0, 255))
    green = newColor((0, 255, 0), (0, 255, 0), (0, 255, 0))
    gray = newColor((169,169,169), (211,211,211), (128, 128, 128))
