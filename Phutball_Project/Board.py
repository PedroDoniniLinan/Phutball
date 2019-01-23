import pygame
import csv

class Board:
    def __init__(self, screen, sqrsize, newgame):
        self.screen = screen
        self.sqrsize = sqrsize
        self.mouseposition = (1, 1)
        self.size = round(0.4*sqrsize)
        if newgame: #create a new Board if newgame was chosen
            self.places = [[0 for i in range(0, 15)] for j in range(0, 20)] #internal matrix to determine pieces deployed and their positions
            self.places[9][7] = 1
        else: #load the old board matrix from the saved_game file
            with open('saved_game.csv', 'r') as saved_game:
                reader = csv.reader(saved_game)
                self.places = [[int(e) for e in r] for r in reader]
                i = 0
                for r in self.places:
                    if r == []:
                        del self.places[i]
                    i += 1

    def drawboard(self):
        gray = (250, 250, 250)
        black = (0, 0, 0)
        self.screen.fill(gray)
        for i in range(1, 19):
            for j in range(1, 15):
                pygame.draw.rect(self.screen, black, (j * self.sqrsize, i * self.sqrsize, self.sqrsize, self.sqrsize), 1)

    def mousehover(self):
        (xm, ym) = pygame.mouse.get_pos()
        if xm <= 15 * self.sqrsize and ym <= 19 * self.sqrsize and xm >= self.sqrsize and ym >= self.sqrsize:
            (xm, ym) = (round(xm / self.sqrsize), round(ym / self.sqrsize))
        self.mouseposition = (xm, ym)

    def highlight(self):
        x = self.mouseposition[0] * self.sqrsize
        y = self.mouseposition[1] * self.sqrsize
        pygame.draw.circle(self.screen, (0, 0, 255), (x, y), self.size, 2)

    def highlightBall(self):
        x = self.mouseposition[0] * self.sqrsize
        y = self.mouseposition[1] * self.sqrsize
        pygame.draw.circle(self.screen, (255, 0, 0), (x, y), self.size + 1, 2)

    def blueDeploy(self, y, x):
        self.places[y-1][x-1] = -1

    def ballMove(self, y1, x1, y2, x2):
        self.places[y1 - 1][x1 - 1] = 0
        self.places[y2 - 1][x2 - 1] = 1

    def clearboard(self):
        self.places = [[0 for i in range(0, 15)] for j in range(0, 20)]
        self.places[9][7] = 1








