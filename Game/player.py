from pawns import Color

class Player:
    def __init__(self, color: Color, *name: str):
        self.color = color
        self.name = name
        
    