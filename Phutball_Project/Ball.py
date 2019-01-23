import pygame



class Ball:

    def __init__(self, screen, sqrsize, y0, x0):
        self.y0 = y0
        self.x0 = x0
        self.sqrsize = sqrsize
        self.x = (self.x0*self.sqrsize)
        self.y = (self.y0*self.sqrsize)
        self.screen = screen
        self.clicked = False
        self.size = round(0.4*sqrsize)
        self.testClick()

    def drawball(self):
        pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), self.size, self.size)

    def testClick(self):
        (xm, ym) = pygame.mouse.get_pos()
        dist = (xm-self.x)**2 + (ym-self.y)**2
        if dist <= self.size**2:
            self.clicked = not self.clicked

    def highlight(self):
         pygame.draw.circle(self.screen, (255, 0, 0), (self.x, self.y), self.size + 3, 2)







