import pygame


class Blue:

    def __init__(self, screen, sqrsize, y0, x0):
        self.y0 = y0
        self.x0 = x0
        self.sqrsize = sqrsize
        self.x = (self.x0*self.sqrsize)
        self.y = (self.y0*self.sqrsize)
        self.screen = screen
        self.size = round(0.4*sqrsize)//1

    def drawblue(self):
        pygame.draw.circle(self.screen, (0, 0, 255), (self.x,self.y), self.size, self.size)
