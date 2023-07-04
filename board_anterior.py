import pyxel
from mario import Mario
from platforms import Platform
from ladder import Ladder
from barrel import Barrel
import constants


class Board:
    '''Class that represents the board including score and lives, Mario, 
    barrels, platforms, ladders DK and Pauline's image and barrels next to DK'''
    
    def __init__(self):
        
        pyxel.init(constants.WIDTH,constants.HEIGHT, caption="DONKEY KONG")
        # Loading sprites from pyxres file
        pyxel.load("assets/my_resource.pyxres")
        
        # Creates the objects for the platforms
        self.platforms = []
        for number in range(6):
            self.platform = Platform(constants.POSITION_PLATFORM_X[number],
            constants.POSITION_PLATFORM_Y[number])
            self.platforms.append(self.platform)
       
        # Creates the objects for the ladders
        self.ladders = []
        for number in range(11):
            self.ladder = Ladder(constants.POSITION_LADDER_X[number],
            constants.POSITION_LADDER_Y[number])
            self.ladders.append(self.ladder)
            
        # Creates Mario object
        self.mario=Mario(constants.INITIAL_X_MARIO,
                         constants.INITIAL_Y_MARIO)
        
        # Creates the objects for the barrels
        self.sequence_barrels = 0
        self.barrels = []
        self.rotation_degree = 0
        
        # Creates the variables for Donkey Kong
        self.sequence_DK = 0
        self.position_DK = 0
        
        # Creates the variables for Pauline
        self.sequence_Pauline = 0

        pyxel.run(self.update, self.draw)
        
    def update(self):
        ''' This function is executed every frame. It checks if the Q key 
        is pressed to finish the program and updates Mario's position'''
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        else:
            # Calls update() method from mario to be able to update mario's position
            self.mario.update()
            
            # It checks if the barrel is passing above a ladder and its 
            # probability of falling down
            for barrel in self.barrels:
                barrel.go_down_ladders()
            
            # This invokes the move function for each of the barrels
            for barrel in self.barrels:
                barrel.move_barrel()
                
            # It invokes the make_barrel function to create barrels from time to time
            if pyxel.frame_count % 75 == 0:
                self.make_barrel()
            
            # Mario touches a barrel and loses a life
            for barrel in self.barrels:
                if (self.mario.x % barrel.x <= 4 or barrel.x % self.mario.x <= 4) \
                and (self.mario.y % barrel.y <= 4 or self.mario.y - barrel.y <= 4) and self.mario.is_alive:
                    self.mario.is_alive = False
                    self.mario.lives -= 1
                    self.death_event()
                
    def make_barrel(self):
        # This function creates the barrels
        self.barrel = Barrel(constants.INITIAL_X_BARREL,constants.INITIAL_Y_BARREL)
        self.barrels.append(self.barrel)
        
    def death_event(self):
        self.score = 0
        
        if self.mario.lives > 0:
            # Respawns at initial point
            self.mario.x = constants.INITIAL_X_MARIO
            self.mario.y = constants.INITIAL_Y_MARIO
            self.mario.is_alive = True
        if self.mario.lives == 0:
            self.mario.x = 300
            self.mario.y = 300
        
    def draw(self):
        pyxel.cls(0)
        
        
        # The sequences variable its used for the animation of the objects
        sequences = ("A","B","C","D","E")
       
        # Draw the platforms:
        for position in range(6):
            if position == 0:
                length = 60
            elif position == 5:
                length = 224
            else:
                length = 184
            pyxel.blt(self.platforms[position].x,self.platforms[position].y,1,
                      0,48,length,8,colkey = 0)
        
        # Draw the ladders:
        for position in range(11):
            if position == 0 or position == 1:
                height = 64
            else:
                height = 32
            pyxel.blt(self.ladders[position].x,self.ladders[position].y,1,
                      0,66,8,height,colkey = 0)
            
        # Draw the static barrels:
        pyxel.blt(constants.STATIC_BARRELS[0],constants.STATIC_BARRELS[1],1,
                  0,0,21,30,colkey = 0)
        
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
            pyxel.blt(self.barrels[barrel].x,self.barrels[barrel].y,1,
                      self.rotation_degree,1,14,14,colkey = 0)
        
        # Draw Mario
        pyxel.blt(self.mario.x,self.mario.y,0,0,0,12,16,colkey = 0)  
        
        # Text when Mario dies
        
        # Draw the score text and remaining lives
        pyxel.text(30, 5, "Score: ", 9)
        pyxel.text(170, 5, "Lives: %i "%self.mario.lives, 9)
       
        # Draw Pauline:
        if pyxel.frame_count % 30 == 0:
            self.sequence_Pauline += 1
        if sequences[self.sequence_Pauline] != "D":
            length = 16
        if sequences[self.sequence_Pauline] == "D":
            length = 40
        if self.sequence_Pauline == 4:
            self.sequence_Pauline = 0
        pyxel.blt(constants.X_PAULINE,constants.Y_PAULINE,0,16,48,length,20,colkey = 0)
        
        
        
        
    
Board()