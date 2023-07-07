# @author: javie and angy

import pyxel
import datetime
import game_elements.constants as constants
from game_elements.mario import Mario
from game_elements.platforms import Platform
from game_elements.ladder import Ladder
from game_elements.barrel import Barrel


class Board:
    '''Class that represents the board including score and lives, Mario, 
    barrels, platforms, ladders, DK and Pauline's image and runs the game'''
    
    def __init__(self):
        
        pyxel.init(constants.WIDTH,constants.HEIGHT, title="DONKEY KONG")
        # Loading sprites from pyxres file
        pyxel.load("../assets/sprites.pyxres")
        
        # Creates the objects for the platforms
        self.__platforms = []
        for number in range(len(constants.POSITION_PLATFORM)):
            self.platform = Platform(constants.POSITION_PLATFORM[number][0],
            constants.POSITION_PLATFORM[number][1])
            self.__platforms.append(self.platform)
       
        # Creates the objects for the ladders
        self.__ladders = []
        for number in range(len(constants.POSITION_LADDER)):
            self.ladder = Ladder(constants.POSITION_LADDER[number][0],
            constants.POSITION_LADDER[number][1])
            self.__ladders.append(self.ladder)
            
        # Creates Mario object
        self.mario=Mario(constants.INITIAL_X_MARIO,
                         constants.INITIAL_Y_MARIO)
        self.__time_prev_jump = datetime.datetime.now()
        
        # Creates the objects for the barrels
        self.__sequence_barrels = 0
        self.__barrels = []
        self.__rotation_degree = 0
        
        # Creates the variables for Donkey Kong
        self.__sequence_DK = 0
        self.__position_DK = 0
        
        # Creates the variables for Pauline
        self.__sequence_Pauline = 0

        pyxel.run(self.update, self.draw)
        
    def update(self):
        ''' This function is executed every frame. It checks if the Q key 
        is pressed to finish the program, and updates Mario and the barrels'''
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
            
        else:
            # Allows mario to fall off the platforms
            self.mario.platform_falling()
            
            # Allows mario to jump
            if pyxel.btn(pyxel.KEY_SPACE) and not self.mario.climbing:
                # Button cooldown to prevent Mario from staying up in the air
                time_now = datetime.datetime.now()
                time_diff = time_now - self.__time_prev_jump
                self.__time_prev_jump = time_now
                if time_diff.total_seconds() > 0.5:
                    self.mario.jumping = True
                    
            self.mario.jump_motion()
        
            # Updates the position of mario
            self.update_mario_direction()
            
            # It checks if the barrel is passing above a ladder and its probability of falling down
            for barrel in self.__barrels:
                barrel.go_down_ladders()
            
            # This invokes the move function for each of the barrels
            for barrel in self.__barrels:
                barrel.move_barrel()
                
            # It invokes the make_barrel function to create barrels from time to time
            if pyxel.frame_count % 75 == 0:
                self.make_barrel()
            
            # It checks if Mario has died
            self.check_death()
            
            # Gains 100 points when Mario jumps over a barrel
            self.gain_score()
            
            # Checks if Mario's at the winning position
            self.mario.check_win()
                
    def make_barrel(self):
        """ This function creates the barrels"""
        self.barrel = Barrel(constants.INITIAL_X_BARREL,constants.INITIAL_Y_BARREL)
        self.__barrels.append(self.barrel)
        
    def update_mario_direction(self):
        """ Determines in which direction it is going to move based on the key pressed"""
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.mario.update_position('right')
        elif pyxel.btn(pyxel.KEY_LEFT):
            self.mario.update_position('left')
        elif pyxel.btn(pyxel.KEY_UP):
            self.mario.update_position('up')
        elif pyxel.btn(pyxel.KEY_DOWN):
            self.mario.update_position('down')
    
    def check_death(self):
        """ Defines when Mario dies (when touched by a barrel) comparing
        his position with the ones of each barrel object"""
        # There is certain range for their positions as their hitbox is larger
        # At initial position Mario is invincible to avoid dying immediatly when
        # the character reappears if a barrel is passing by
        for barrel in self.__barrels:
            if (abs(self.mario.x - barrel.x) <= 8) \
            and (abs(self.mario.y - barrel.y) <= 8) and not (self.mario.x == constants.INITIAL_X_MARIO and \
            self.mario.y == constants.INITIAL_Y_MARIO) and self.mario.is_alive:
                self.mario.is_alive = False
                self.mario.death_event()
    
    def gain_score(self):
        """ This method allows the player to obtain 100 points every time
        Mario jumps over a barrel"""
        # Gains points if Mario is higher than the barrel jumping or descending from
        # a jump and their relative position is correct (within a certain range)
        for barrel in self.__barrels:
            if (abs(self.mario.x - barrel.x) <= 8) and \
            (0 <= barrel.y - self.mario.y <= 30) and \
            (self.mario.jumping or self.mario.descending) and not barrel.points_gained:
                self.mario.score += 100
                # this avoids getting more than 100 points in a single jump, 
                # but will only let the player gain points once for each barrel
                barrel.points_gained = True
        
    def draw(self):
        """ Draws all elements of the game on the board"""
        pyxel.cls(0)
        
        # The __sequences variable its used for the animation of the objects
        __sequences = ("A","B","C","D","E")
       
        # Draw the platforms:
        for position in range(len(constants.POSITION_PLATFORM)):
            if position == 0:
                __length = 60
            elif position == 5:
                __length = 224
            else:
                __length = 184
            pyxel.blt(self.__platforms[position].x,self.__platforms[position].y,1,0,48,__length,8,colkey = 0)
        
        # Draw the ladders:
        for position in range(len(constants.POSITION_LADDER)):
            if position == 0 or position == 1:
                height = 64
            else:
                height = 32
            pyxel.blt(self.__ladders[position].x,self.__ladders[position].y,1,0,66,8,height,colkey = 0)
            
        # Draw the static barrels:
        pyxel.blt(constants.STATIC_BARRELS[0],constants.STATIC_BARRELS[1],1,
                  0,0,21,30,colkey = 0)
        
        # Draw Donkey Kong
        if pyxel.frame_count % 25 == 0:
            self.__sequence_DK += 1
        if __sequences[self.__sequence_DK] == "C":
            self.__position_DK = 0
        if __sequences[self.__sequence_DK] == "A":
            self.__position_DK = 24
        if __sequences[self.__sequence_DK] == "B":
            self.__position_DK = 56
        if self.__sequence_DK == 3:
            self.__sequence_DK = 0
        pyxel.blt(constants.DONKEY_KONG[0],constants.DONKEY_KONG[1],0,
        self.__position_DK,16,24,32,colkey = 0)
        
        # Draw the barrels
        if pyxel.frame_count % 4 == 0:
            self.__sequence_barrels += 1
        for barrel in range(len(self.__barrels)):
            if __sequences[self.__sequence_barrels] == "A":
                self.__rotation_degree = 41
            if __sequences[self.__sequence_barrels] == "B":
                self.__rotation_degree = 25
            if __sequences[self.__sequence_barrels] == "C":
                self.__rotation_degree = 57
            if __sequences[self.__sequence_barrels] == "D":
                self.__rotation_degree = 73
            if self.__sequence_barrels == 4:
                self.__sequence_barrels = 0
            pyxel.blt(self.__barrels[barrel].x,self.__barrels[barrel].y,1,
                      self.__rotation_degree,1,14,14,colkey = 0)
        
        # Draw Mario
        if pyxel.btn(pyxel.KEY_RIGHT):
            pyxel.blt(self.mario.x,self.mario.y,0,0,0,12,16,colkey = 0) 
        else:
            pyxel.blt(self.mario.x,self.mario.y,0,16,0,12,16,colkey = 0)
        
        # Draw the score text and remaining lives
        pyxel.text(30, 5, "Score: %i "%self.mario.score, 9)
        pyxel.text(170, 5, "Lives: %i "%self.mario.lives, 9)
       
        # Draw Pauline:
        if pyxel.frame_count % 30 == 0:
            self.__sequence_Pauline += 1
        if __sequences[self.__sequence_Pauline] != "D":
            __length = 16
        if __sequences[self.__sequence_Pauline] == "D":
            __length = 40
        if self.__sequence_Pauline == 4:
            self.__sequence_Pauline = 0
        pyxel.blt(constants.X_PAULINE,constants.Y_PAULINE,0,16,48,__length,20,colkey = 0)
        
        # Screen when Mario dies
        if self.mario.game_over:
            pyxel.cls(0)
            pyxel.text(92,128,"GAME  OVER",8)
            
        # Screen when Mario wins
        if self.mario.win_game:
            pyxel.cls(7)
            pyxel.text(92,128,"YOU  WON !",pyxel.frame_count % 16)
    

if __name__ == "__main__":
    Board()