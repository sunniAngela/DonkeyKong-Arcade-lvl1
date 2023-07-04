# @author: javie and angy

import pyxel
from platforms import Platform
from ladder import Ladder
import constants
from barrel import Barrel
from mario import Mario

 
class Board:
    '''This class represents our gameboard, which contains everything related
   to our game like Mario, barrels, ladders, etc'''
    
    def __init__(self):
        
        pyxel.init(constants.WIDTH, constants.HEIGHT)
       
        # Loading sprites from pyxres file
        pyxel.load("assets/my_resource.pyxres")
        
        # Creates Mario object
        self.mario = Mario(constants.INITIAL_X_MARIO,
                         constants.INITIAL_Y_MARIO)
       
        # Creates the objects for the platforms
        self.platforms = []
        for number in range(len(constants.POSITION_PLATFORM)):
            self.platform = Platform(constants.POSITION_PLATFORM[number][0],
            constants.POSITION_PLATFORM[number][1])
            self.platforms.append(self.platform)
       
        # Creates the objects for the ladders
        self.ladders = []
        for number in range(len(constants.POSITION_LADDER)):
            self.ladder = Ladder(constants.POSITION_LADDER[number][0],
            constants.POSITION_LADDER[number][1])
            self.ladders.append(self.ladder)
            
        # Creates the variables needed for the animation of the barrels
        self.sequence_barrels = 0
        self.barrels = []
        self.rotation_degree = 0
        
        # Creates the variables needed for the animation of Donkey Kong
        self.sequence_DK = 0
        self.position_DK = 0
        
        # Creates the variables needed for the animation of Pauline
        self.sequence_Pauline = 0
        
        pyxel.run(self.update,self.draw)

    def update(self):
        ''' This function is executed every frame. It checks if the Q key 
        is pressed to finish the program, and updates Mario and the barrels.'''
        
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        else:
            # Allows mario to fall off the platforms
            self.mario.platform_falling()
            
            # Allows mario to jump
            if pyxel.btn(pyxel.KEY_SPACE) and not self.mario.climbing:
                self.mario.jumping = True
            if self.mario.jumping or self.mario.descending:
                self.mario.jump_motion()
        
            # Updates the position of mario
            self.update_mario_direction()
            
            # It checks if a barrel is passing above a ladder and its probability of falling down
            for barrel in self.barrels:
                barrel.go_down_ladders()
            
            # This invokes the move function for each of the barrels
            for barrel in self.barrels:
                barrel.move_barrel()
                
            # It invokes the make_barrel function to create barrels from time to time
            if pyxel.frame_count % 75 == 0:
                self.make_barrel()
            
            # It checks if a barrel has killed Mario
            self.check_death()
            
            # Gains 100 points when Mario jumps over a barrel
            self.gain_score()
            
            # Checks if Mario's at the winning position
            self.mario.check_win()
            
    def update_mario_direction(self):
       """ Determines in which direction Mario it is going to move based on the key pressed"""
       
       if pyxel.btn(pyxel.KEY_RIGHT):
            self.mario.update_position('right')
       elif pyxel.btn(pyxel.KEY_LEFT):
            self.mario.update_position('left')
       elif pyxel.btn(pyxel.KEY_UP):
            self.mario.update_position('up')
       elif pyxel.btn(pyxel.KEY_DOWN):
            self.mario.update_position('down')
    
    def make_barrel(self):
        """ This function creates a new barrel everytime is invoked"""
        
        self.barrel = Barrel(constants.INITIAL_X_BARREL,constants.INITIAL_Y_BARREL)
        self.barrels.append(self.barrel)
    
    def gain_score(self):
        """ This method allows the player to obtain 100 points every time
            Mario jumps over a barrel"""
        
        for barrel in self.barrels:
            if (abs(self.mario.x - barrel.x) <= 8) and \
            (0 <= barrel.y - self.mario.y <= 30) and \
            (self.mario.jumping or self.mario.descending) and not barrel.points_gained:
                self.mario.score += 100
                barrel.points_gained = True
                
    def check_death(self):
        """ Defines when Mario dies (when touched by a barrel) comparing
        his position with the ones of each barrel object"""
        
        # There is certain range for their positions as their hitbox is larger
        # At initial position Mario is invincible to avoid dying immediatly when
        # the character reappears if a barrel is passing by
        for barrel in self.barrels:
            if (abs(self.mario.x - barrel.x) <= 8) \
            and (abs(self.mario.y - barrel.y) <= 8) and not (self.mario.x == constants.INITIAL_X_MARIO and \
            self.mario.y == constants.INITIAL_Y_MARIO) and self.mario.is_alive:
                self.mario.is_alive = False
                self.mario.death_event()      
    
    def draw(self):
        """ Draws all elements of the game on the board"""
        
        # The sequences variable its used for the animation of the objects
        sequences = ("A","B","C","D","E")
        pyxel.cls(0)
       
        # Draw the platforms:
        for position in range(len(constants.POSITION_PLATFORM)):
            if position == 0:
                length = 60
            elif position == 5:
                length = 224
            else:
                length = 184
            pyxel.blt(self.platforms[position].x,self.platforms[position].y,1,0,48,length,8,colkey = 0)
        
        # Draw the ladders:
        for position in range(len(constants.POSITION_LADDER)):
            if position == 0 or position == 1:
                height = 64
            else:
                height = 32
            pyxel.blt(self.ladders[position].x,self.ladders[position].y,1,0,66,8,height,colkey = 0)
            
        # Draw the static barrels:
        pyxel.blt(constants.STATIC_BARRELS[0],constants.STATIC_BARRELS[1],1,0,0,21,30,colkey = 0)
        
        # Draw Donkey Kong
        if pyxel.frame_count % 25 == 0:
            self.sequence_DK += 1
        if sequences[self.sequence_DK] == "C":
            self.position_DK = 0
        if sequences[self.sequence_DK] == "A":
            self.position_DK = 24
        if sequences[self.sequence_DK] == "B":
            self.position_DK = 56
        if self.sequence_DK == 3:
            self.sequence_DK = 0
        pyxel.blt(constants.DONKEY_KONG[0],constants.DONKEY_KONG[1],0,
        self.position_DK,16,24,32,colkey = 0)
        
        # Draw the barrels
        if pyxel.frame_count % 4 == 0:
            self.sequence_barrels += 1
        for barrel in range(len(self.barrels)):
            if sequences[self.sequence_barrels] == "A":
                self.rotation_degree = 41
            if sequences[self.sequence_barrels] == "B":
                self.rotation_degree = 25
            if sequences[self.sequence_barrels] == "C":
                self.rotation_degree = 57
            if sequences[self.sequence_barrels] == "D":
                self.rotation_degree = 73
            if self.sequence_barrels == 4:
                self.sequence_barrels = 0
            pyxel.blt(self.barrels[barrel].x,self.barrels[barrel].y,1,self.rotation_degree,1,14,14,colkey = 0)
                 
        # Draw Pauline:
        if pyxel.frame_count % 30 == 0:
            self.sequence_Pauline += 1
        if sequences[self.sequence_Pauline] != "D":
            lenght = 16
        if sequences[self.sequence_Pauline] == "D":
            lenght = 40
        if self.sequence_Pauline == 4:
            self.sequence_Pauline = 0
        pyxel.blt(constants.X_PAULINE,constants.Y_PAULINE,0,16,48,lenght,20,colkey = 0)
        
        # Draw Mario
        if pyxel.btn(pyxel.KEY_RIGHT):
            pyxel.blt(self.mario.x,self.mario.y,0,0,0,12,16,colkey = 0) 
        else:
            pyxel.blt(self.mario.x,self.mario.y,0,16,0,12,16,colkey = 0)
        
        # Draw the score text and remaining lives
        pyxel.text(30, 5, "Score: %i " %(self.mario.score), 9)
        pyxel.text(170, 5, "Lives: %i " %(self.mario.lives), 9)

        # Screen when Mario dies
        if self.mario.game_over:
            pyxel.cls(0)
            pyxel.text(92,128,"GAME  OVER",8)
            
        # Screen when Mario wins
        if self.mario.win_game:
            pyxel.cls(1)
            pyxel.text(92,128,"YOU  WON !",3)

Board()