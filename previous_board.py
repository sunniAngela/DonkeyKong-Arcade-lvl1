import pyxel
from mario import Mario
from platforms import Platform
from ladder import Ladder
import constants


class Board:
    '''Class that represents the board including score and lives, Mario, 
    barrels, platforms, ladders DK and Pauline's image and barrels next to DK'''
    
    def __init__(self):
        
        pyxel.init(constants.WIDTH,constants.HEIGHT, caption="DONKEY KONG")
        
        # Creates the objects for the platforms
        count = 0
        self.platforms = []
        for number in range(6):
            self.platform = Platform(constants.position_platform[count],
                                     constants.position_platform[count + 1])
            self.platforms.append(self.platform)
            count += 2
            
        # Creates the objects for the ladders
        count = 0
        self.ladders = []
        for number in range(9):
            self.ladder = Ladder(constants.position_ladder[count], 
                                 constants.position_ladder[count + 1])
            self.ladders.append(self.ladder)
            count += 2
            
        # Calling Mario
        self.mario=Mario(constants.INITIAL_X_MARIO,
                         constants.INITIAL_Y_MARIO)
        
        # loading images from pyxres file
        pyxel.load("assets/my_resource.pyxres")

        pyxel.run(self.update, self.draw)
        
    def update(self):
        ''' This function is executed every frame. It checks if the Q key 
        is pressed to finish the program and updates Mario's position'''
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        else:
            # call update() method from mario to update mario position
            self.mario.update()
        
    def draw(self):
        pyxel.cls(0)
        
        # Platforms
        for number in range(6):
            if number == 0:
                length = 60
            elif number == 5:
                length = 224
            else:
                length = 184
            pyxel.blt(self.platforms[number].x,self.platforms[number].y,1,0,48,length,8)
        
        # Ladders
        for position in range(9):
            pyxel.blt(self.ladders[position].x,self.ladders[position].y,1,0,66,8,32)
        
        # Mario (bank 0)
        pyxel.blt(self.mario.x,self.mario.y,0,0,0,12,16)

        
        # Score and lives
        """pyxel.text(80, 0, "SCORE", 8)
        pyxel.text(80,20,"here goes the score",7)
        
        pyxel.text(20,0,"LIVES",8)
        pyxel.text(20,20,"here goes lives left",7)"""
        
    
Board()