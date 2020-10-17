#import jewgeeoh.classes.card 
from ..change_lp import LifePointsChanger

class DianKeto(LifePointsChanger):
    POSITIVE_CHANGE = True
    AFFECTS_OPPONENT = False
    OWNER_LP_CHANGE = 0.2

