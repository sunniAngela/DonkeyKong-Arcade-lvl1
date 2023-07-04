# @author: javie and angy

import random
import constants
from onboard import OnBoard

''' This class defines all the barrels in the game '''

class Barrel(OnBoard):
    
    # It sets the determined values for x and y and declares the attributes
    # neccesary for the movement of the barrel down the ladder:
    def __init__(self, x, y):
        super().__init__(x, y)
        self.__in_ladder = False
        self.__index = 0
        self.points_gained = False
    
    
    def move_barrel(self):
        ''' This function allows the movement of the barrel through the platforms '''
        
        __bounds_x = (184,26)
        __bounds_y = (73,153)
       
        for number in range(2):
            if self.x < __bounds_x[0] and self.y == __bounds_y[number]:
                self.x += 2
            elif self.x >= __bounds_x[0] and \
            (self.y < __bounds_y[number] + 40 and self.y > __bounds_y[number] - 14):
                self.y += 2
                self.x += 1
            elif self.x > __bounds_x[1] and self.y == __bounds_y[number] + 40:
                self.x -= 2
            elif self.x <= __bounds_x[1] and \
            (self.y < __bounds_y[number] + 80 and self.y > __bounds_y[number] + 26):
                self.y += 2
                self.x -= 1
        if self.y == 233:
            self.x += 2
    
    
    def go_down_ladders(self):
        ''' This function checks if the barrel is passing above  
            a ladder and determines if is going down or not '''
        
        __value_for_going_down = 1
        __found = False
        __random_number = 0
        
        if self.__in_ladder:
            self.going_down()
        else:
            for index in range(3, len(constants.POSITION_LADDER)):
                if self.x == constants.POSITION_LADDER[index][0] - 4 and \
                self.y == constants.POSITION_LADDER[index][1] - 23:
                    __random_number = random.randint(1,4)
                    self.__index = index
                    __found = True
            if __random_number == __value_for_going_down and __found:
                self.__in_ladder = True
                self.going_down()
    
    
    def going_down(self):
        ''' This function makes the barrel move down the ladder '''
        
        if self.y < constants.POSITION_LADDER[self.__index][1] + 17:
            self.y += 1
        elif self.y == constants.POSITION_LADDER[self.__index][1] + 17:
            self.__in_ladder = False
            
    