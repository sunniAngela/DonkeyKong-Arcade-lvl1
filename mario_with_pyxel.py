import pyxel
import constants

class Mario:
    def __init__(self,x,y):
        
        self.is_alive = True
        self.lives = 3
        self.score = 0
        self.jumping = False
        self.descend = False
        self.climbing = False
        self.win_game = False
        self.x = constants.INITIAL_X_MARIO
        self.y = constants.INITIAL_Y_MARIO
        self.jy = 0
        self.cy = 0
        
    def update(self):
        
        ############ right-left movement ############
    
        # Mario cannot move left and right while jumping or climbing
        if pyxel.btn(pyxel.KEY_RIGHT):
            if not (self.x==constants.WIDTH-16 or self.climbing or self.jumping) :
                self.x = self.x + constants.VEL
        elif pyxel.btn(pyxel.KEY_LEFT):
            if not (self.x==0 or self.climbing or self.jumping):
                self.x = self.x - constants.VEL
                
                
        ############ jumping  ############
        
        # if and not elif to improve game experience otherwise
        # we would need to stop pressing left or right in order to jump
        if pyxel.btn(pyxel.KEY_SPACE) and not self.climbing:
            self.jumping = True
        
        elif self.jumping and self.jy < constants.JUMP_HEIGHT:
            self.y -= constants.JUMP_VEL
            self.jy += constants.JUMP_VEL
        elif self.jy == constants.JUMP_HEIGHT and self.jumping:
            self.descend = True
            self.jumping = False
        elif self.descend and self.jy > 0:
            self.y += constants.JUMP_VEL
            self.jy -= constants.JUMP_VEL
        elif self.descend and self.jy == 0:
            self.descend = False


        ############ climbing ############
        
        # While climbing it must be able to move up or down
        # Mario can only move up and down on ladders, no need to restrict
        # movement inside height and width of the screen
        if pyxel.btn(pyxel.KEY_UP):
            if ((self.x==46 or self.x==86) and self.y>192) or ((self.x==126 or self.x==168) and 152<self.y<=192) or \
            ((self.x==46 or self.x==86) and 112<self.y<=152) or ((self.x==126 or self.x==168) and 72<self.y<=112) or \
            ((self.x==46 or self.x==70 or self.x==136) and 32<self.y<=72):
                self.climbing = True
                self.y -= constants.CLIMB_VEL
            else:
                self.climbing = False
                
        if pyxel.btn(pyxel.KEY_DOWN):
            if ((self.x==46 or self.x==86) and 192<=self.y<232) or ((self.x==126 or self.x==168) and 152<=self.y<192) or \
            ((self.x==46 or self.x==86) and 112<=self.y<152) or ((self.x==126 or self.x==168) and 72<=self.y<112) or \
            ((self.x==46 or self.x==70 or self.x==136) and 32<=self.y<72):
                self.climbing = True
                self.y += constants.CLIMB_VEL
            else:
                self.climbing = False
        
            
        ############ falling when platforms ends ############
        #184 and 26 are x coordinates of platforms endings
        elif self.x >= 184 and (152<=self.y<192 or 72<=self.y<112) and not self.jumping and not self.descend:
            self.y += 2
        elif self.x <= 26 and (192<=self.y<232 or 112<=self.y<152 or 32<=self.y<72) and not self.jumping and not self.descend:
            self.y += 2
            
        ############ losing lives ############
        
        
"""self.climbing = True
                if self.climbing and self.cy < constants.CLIMB_HEIGHT:
                    self.y -= constants.CLIMB_VEL
                    self.cy += constants.CLIMB_VEL
                elif self.cy == constants.CLIMB_HEIGHT:
                    self.climbing = False
                    if pyxel.btn(pyxel.KEY_RIGHT) or pyxel.btn(pyxel.KEY_LEFT):
                        self.cy = 0"""
"""if self.x in constants.position_ladder:
                self.climbing = True
                if self.climbing and self.cy > 0:
                    self.y += constants.CLIMB_VEL
                    self.cy -= constants.CLIMB_VEL
                elif self.cy == 0:
                    self.climbing = False"""
