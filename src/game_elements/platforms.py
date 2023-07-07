# @author: javie and angy

from game_elements.onboard import OnBoard

''' This class defines all the platforms in the game '''

class Platform(OnBoard):
    
    # It sets the determined values for x and y:
    def __init__(self, x, y):
        super().__init__(x, y)
   

