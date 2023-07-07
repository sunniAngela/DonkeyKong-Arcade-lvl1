# @author: javie and angy

import game_elements.constants as constants

class Mario:
    ''' This class defines Mario'''
    
    def __init__(self,x,y):
        
        self.is_alive = True
        self.lives = 3
        self.score = 0
        self.jumping = False
        self.descending = False
        self.climbing = False
        self.__x = x
        self.__y = y
        self.jy = 0
        self.win_game = False
        self.game_over = False
        self.ground = 0
        self.falling = False
        
    def update_position(self, direction):
        """Sets the position of Mario """
        
        # Mario cannot move left and right while jumping or climbing
        if direction == 'right' and not (self.x == constants.WIDTH-16 or self.climbing or self.jumping or self.descending):
            self.x = self.x + constants.VEL
        if direction == 'left' and not (self.x == 0 or self.climbing or self.jumping or self.descending):
            self.x = self.x - constants.VEL
            
        # While climbing it must be able to move up or down
        # Mario can only move up and down on ladders, no need to restrict
        # movement inside height and width of the screen
        if direction == 'up':
            for index in range(len(constants.POSITION_LADDER)):
                if (abs(self.x - constants.POSITION_LADDER[index][0]) <= 4) \
                and (self.y > constants.POSITION_LADDER[index][1] - 24 and self.y <= constants.POSITION_LADDER[index][1] + 16):
                    self.climbing = True
                    self.y -= constants.CLIMB_VEL
                else:
                    self.climbing = False
        
        if direction == 'down':
            for index in range(len(constants.POSITION_LADDER)):
                if (abs(self.x - constants.POSITION_LADDER[index][0]) <= 4) \
                and (self.y >= constants.POSITION_LADDER[index][1] - 24 and self.y < constants.POSITION_LADDER[index][1] + 16):
                    self.climbing = True
                    self.y += constants.CLIMB_VEL
                else:
                    self.climbing = False
        
    def jump_motion(self):
        """Defines the jumping motion that consists of a jumping state and a
        descending state"""
        
        if self.jumping and self.jy < constants.JUMP_HEIGHT:
            self.y -= constants.JUMP_VEL
            self.jy += constants.JUMP_VEL
        elif self.jumping and self.jy == constants.JUMP_HEIGHT :
            self.descending = True
            self.jumping = False
        elif self.descending and self.jy > 0:
            self.y += constants.JUMP_VEL
            self.jy -= constants.JUMP_VEL
        elif self.descending and self.jy == 0:
            self.descending = False
                
    def platform_falling(self):
        """This function allows Mario to fall down from platforms"""
        
        __length = 0
        for index in range(len(constants.POSITION_PLATFORM)):
            if index == 0:
                __length = 60
            if 1 <= index <= 4:
                __length = 184
            if index == 5:
                __length = 224
            
            if self.falling:
                if self.y < constants.POSITION_PLATFORM[self.ground][1] - 16:
                    self.y += 0.5
                else:
                    self.falling = False
            elif self.y == constants.POSITION_PLATFORM[index][1] - 16:
                if (self.x <= constants.POSITION_PLATFORM[index][0] - 16 \
                or self.x >= constants.POSITION_PLATFORM[index][0] + __length):
                    self.falling = True
                    self.ground = index + 1
                else:
                    self.falling = False   
                    
    def death_event(self):
        """Determines what happens when Mario dies"""
        
        # When Mario dies, the score goes back to zero and he loses a life
        # If there are any remaining lives, he respawns
        # If no lives left, game over
        self.score = 0
        self.lives -= 1
        self.jumping=False
        self.climbing=False
        self.descending=False
        
        if self.lives > 0:
            # Respawns at initial point
            self.x = constants.INITIAL_X_MARIO
            self.y = constants.INITIAL_Y_MARIO
            self.is_alive = True
        if self.lives == 0:
            self.game_over = True
            
    def check_win(self):
        """Checks if Mario has arrived to the winning position"""
        
        if self.x <= constants.X_PAULINE + 25 and self.y == 32:
            self.win_game = True
            
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self,x):
        if (x>=0 or x<=constants.WIDTH):
            self.__x=x
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self,y):
        if (y>=0 or y<= constants.HEIGHT):
            self.__y=y
