# @author: javie and angy

import game_elements.constants as constants

""" This class defines all the inanimate objects that will be displayed on the board
    Ex: platforms, ladder, barrels.
    It sets the position for all its child classes """

class OnBoard:
    # It sets the determined values for x and y:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y
    
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,x):
        if x >= 0 and x <= constants.WIDTH:
            self.__x = x
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,y):
        if y >= 0 and y <= constants.HEIGHT:
            self.__y = y