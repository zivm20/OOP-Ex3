import pygame as pg
from pygame.locals import *
class Game():
    def __init__(self,width:int=900, height:int=900,setupArgs=None):
        pg.init()
        self.clock = pg.time.Clock()
        self.size = self.width, self.height = width,height
        self.screen = pg.display.set_mode(self.size)
        self.setup(setupArgs)
        self.update()
        self.play()
    
    #run game
    def play(self):
        while self.isAlive():
            
            
            #only update canvas when needed
            if self.eventHandler():
                self.update()
                


    #make sure game is alive
    def isAlive(self) -> bool:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
        return True



    
    def setup(self,setupArgs=None):
        """
        runs once after init
        """
        
    def eventHandler(self) -> bool:
        """
        pygames event handler
        @returns True if an event was triggered, false o.w
        """
        return False

    def update(self):
        """
        updates the game every time event handler returns true
        """













