# @author: javie and angy

from onboard import OnBoard

''' This class defines all the ladders in the game '''

class Ladder(OnBoard):
    
    # It sets the determined values for x and y:
    def __init__(self, x, y):
        super().__init__(x, y)
            