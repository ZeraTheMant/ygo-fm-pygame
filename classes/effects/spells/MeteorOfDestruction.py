#import jewgeeoh.classes.card 
from ..change_lp import LifePointsChanger

class MeteorOfDestruction(LifePointsChanger):
    POSITIVE_CHANGE = False
    AFFECTS_OPPONENT = True
    OPPONENT_LP_CHANGE = -0.2

