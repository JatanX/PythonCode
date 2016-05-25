from enum import Enum
class SignID(Enum):
    Stop = 0
    Forward = 1
    Left = 2
    Right = 3
    Wait = 4

class EngineDirection(Enum):
    Stop = 0
    Forward = 1
    Backward = 2

class EngineIntensity(Enum):
    Speed0 = 0
    Speed1 = 1
    Speed2 = 2
    Speed3 = 3
    Speed4 = 4
    Speed5 = 5
    Speed6 = 6
    Speed7 = 7
    Speed8 = 8
    Speed9 = 9
    Speed10 = 10
    Speed11 = 11
    Speed12 = 12
    Speed13 = 13
    Speed14 = 14
    Speed15 = 15

class PriorityEnum(Enum):
    Stop = 1
    MoBa = 2
    MoFo = 3
    TuLe = 4
    TuRi = 5
