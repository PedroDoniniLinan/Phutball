from Board import*
from Ball import*
from Blue import*
from AI import*
import threading
import time
import pygame


class Game:
    def __init__(self, screen, sqrsize, w, h, newgame):
        pygame.init()
        self.clock = pygame.time.Clock()

        #Sound declaration
        pygame.display.set_caption("Phutball prototype")
        self.quit = pygame.mixer.Sound("closesound.wav")

        #screen declaration
        (self.screen, self.sqrsize, self.w, self.h) = (screen, sqrsize, w, h)

        #fonts and colors
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.gray = (250, 250, 250)
        self.myfont = pygame.font.SysFont("Comic Sans MS", 12)

        #Initialization
        self.buttonRelease = True
        self.mouseclick = False
        self.gameOver = False
        self.running = True
        self.board = Board(self.screen, self.sqrsize, newgame)
        (i,j) = self.ballocation(self.board.places)
        self.ball = Ball(self.screen, self.sqrsize, i, j)
        self.AI1 = AI(self.board.places, -1)
        self.AI2 = AI(self.board.places, 1)
        self.p1AI = False
        self.p2AI = False
        try:
            with open('upName.txt', 'r') as name:
               self.upName= name.read()
        except:
               self.upName = "Player1"
        try:
            with open('downName.txt', 'r') as name:
               self.downName = name.read()
        except:
               self.downName = "Player2"
        if newgame:
            self.player1 = True
        else:
            with open('saved_turn.csv', 'r') as saved_game:
                reader = csv.reader(saved_game)
                aux = [[int(e) for e in r] for r in reader]
                self.player1 = True if int(aux[0][0]) == 1 else False
        (x, y) = (self.board.mouseposition[0], self.board.mouseposition[1])
        self.avJump(0,0)
        self.availablePlay()
        self.jumpExecute(x, y)
        self.color_decision()
        self.event_detector()

    def ballocation(self,matrix):
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                if (matrix[i][j] == 1): return(i+1,j+1)

    def avJump(self, xx, yy):
        avPlace = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                y = self.ball.y0-1+i
                x = self.ball.x0-1+j
                outBoard = x > 14 or x < 0 or y > 18 or y < 0
                if self.board.places[y][x] == -1:
                    while not outBoard:
                        if self.board.places[y][x] == 0 or (self.board.places[y][x] == -1 and (y == 0 or y == 18)):
                           avPlace.append((x+1, y+1))
                           break
                        y += i
                        x += j
                        outBoard = x > 14 or x < 0 or y > 18 or y < 0
        for n in avPlace:
            if n == (xx, yy):
                return True
        return False

    def jumpExecute(self, x, y):
        if x == self.ball.x0:
            if y > self.ball.y0 + 1:
                for i in range(self.ball.y0, y-1):
                    self.board.places[i][x-1] = 0
            elif y < self.ball.y0 - 1:
                for i in range(y, self.ball.y0-1):
                    self.board.places[i][x-1] = 0
        elif y == self.ball.y0:
            if x > self.ball.x0 + 1:
                for j in range(self.ball.x0, x-1):
                    self.board.places[y-1][j] = 0
            elif x < self.ball.x0 - 1:
                for j in range(x, self.ball.x0-1):
                    self.board.places[y-1][j] = 0
        elif x-y == self.ball.x0-self.ball.y0:
            if x > self.ball.x0 + 1:
                for k in range(0, x-self.ball.x0-1):
                    self.board.places[self.ball.y0+k][self.ball.x0+k] = 0
            elif x < self.ball.x0 - 1:
                for k in range(0, self.ball.x0-x-1):
                    self.board.places[self.ball.y0-k-2][self.ball.x0-k-2] = 0
        elif x+y == self.ball.x0+self.ball.y0:
            if x > self.ball.x0 + 1:
                for k in range(0, x-self.ball.x0-1):
                    self.board.places[self.ball.y0-k-2][self.ball.x0+k] = 0
            elif x < self.ball.x0 - 1:
                for k in range(0, self.ball.x0-x-1):
                    self.board.places[self.ball.y0+k][self.ball.x0-k-2] = 0

    def availablePlay(self):
        for i in range(-1, 2):
            for j in range(-1, 2):
                y = self.ball.y0-1+i
                x = self.ball.x0-1+j
                outBoard = x > 14 or x < 0 or y > 18 or y < 0
                if self.board.places[y][x] == -1:
                    while not outBoard:
                        if self.board.places[y][x] == 0 or (self.board.places[y][x] == -1 and (y == 0 or y == 18)):
                            return True
                        y += i
                        x += j
                        outBoard = x > 14 or x < 0 or y > 18 or y < 0
        return False

    def color_decision(self):
       #color decision for the label of the player whose turn is now (Currant Player is the Red Player)
       if self.player1:
           label1 = self.myfont.render(self.upName, 1, self.red)
           label2 = self.myfont.render(self.downName, 1, self.black)
       else:
           label1 = self.myfont.render(self.upName, 1, self.black)
           label2 = self.myfont.render(self.downName, 1, self.red)
       self.screen.blit(label1, (15*self.sqrsize/2 - 5,  0))
       self.screen.blit(label2, (15*self.sqrsize/2 - 5, self.h - 20))

    def event_detector(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.buttonRelease = True
            if self.buttonRelease: #ensures that one self.mouseclick is computed only once
                if event.type == pygame.QUIT:
                    self.running = False
                    with open('saved_game.csv', 'w') as saved_game: # saving the currant Board matrix to saved_game file
                        writer = csv.writer(saved_game)
                        [writer.writerow(r) for r in self.board.places]
                    with open('saved_turn.csv', 'w') as saved_game: # saving the currant Board matrix to saved_game file
                        writer = csv.writer(saved_game)
                        if self.player1:
                            writer.writerow("1")
                        else:
                            writer.writerow("2")

                    self.quit.play() #playing quit sound
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mouseclick = True
                else:
                    self.mouseclick = False

    def drawElements(self):
        for i in range(0, 19):
            for j in range(0, 15):
                if self.board.places[i][j] == -1:
                    blue = Blue(self.screen, self.sqrsize, i + 1, j + 1)
                    blue.drawblue()
                elif self.board.places[i][j] == 1:
                    self.ball.drawball()

    def run(self):
        #board GUI preparation
        self.board.drawboard()
        self.color_decision()
        #blues and self.ball GUI preparation
        self.drawElements()
        #self.screen update
        pygame.display.update()
        while self.running:
            #event detection
            self.event_detector()
            if not self.gameOver:
               #checking if it is the turn of a humain
               human = (not self.p1AI and self.player1) or (not self.p2AI and not self.player1)
               #frames per second
               if human: self.clock.tick(60)

               #board GUI preparation
               self.board.drawboard()
               self.color_decision()

               #coordinates of mouse position
               self.board.mousehover()
               (xm,ym)=(self.board.mouseposition[0],self.board.mouseposition[1])

               #important conditions tests
               hoverBall = (xm == self.ball.x0) and (ym == self.ball.y0)
               mouseInBoard = ym >= 1 and ym <= 19 and xm >= 1 and xm <= 15

               #turn treatment (blue deploy or self.ball move)
               if human:
                   if not self.ball.clicked: #blue deploy
                       if self.mouseclick and self.buttonRelease and mouseInBoard:
                           self.ball.testClick()
                           if not hoverBall and self.board.places[ym-1][xm-1] != -1:
                               self.board.blueDeploy(ym, xm)
                               self.player1 = not self.player1 #player deployed a blue (change of player)
                           else:
                               self.buttonRelease = False
                       elif not hoverBall and mouseInBoard:
                           self.board.highlight()
                   elif self.availablePlay(): #self.ball move by a player
                       if mouseInBoard:
                           if self.avJump(xm, ym):
                               self.board.highlightBall()
                           if self.mouseclick and self.buttonRelease:
                               self.ball.testClick()
                               if hoverBall:
                                   self.ball.clicked = False
                                   self.player1 = not self.player1
                               elif self.avJump(xm, ym):
                                   (x, y) = (xm, ym)
                                   self.jumpExecute(x, y)
                                   self.board.ballMove(self.ball.y0, self.ball.x0, ym, xm)
                                   self.ball = Ball(self.screen, self.sqrsize, ym, xm)
                                   if self.availablePlay():
                                       self.ball.clicked = True
                                   else:
                                       self.ball.clicked = False
                                       self.player1 = not self.player1 #no more available self.ball moves (change of player)
                               self.buttonRelease = False
                       self.ball.highlight()
                   else: #no available self.ball moves
                       self.ball.clicked = False
                       self.player1 = not self.player1
                   self.color_decision()
               else:
                   #self.ball.clicked = False
                   #if self.p1AI and self.p2AI:
                       #time.sleep(0.02)
                   if self.p1AI and self.player1:
                       print("-------------------AI1------------------------")
                       m = self.AI1.minmax(self.ball.x0,self.ball.y0,self.board.places, 1)
                       (type, xai, yai) = m[0]
                       if type == 0 and self.board.places[yai-1][xai-1] != -1:
                           self.board.blueDeploy(yai, xai)
                           self.player1 = not self.player1 #AI deployed a blue (change of player)
                       elif self.avJump(xai, yai):
                           self.jumpExecute(xai, yai)
                           self.board.ballMove(self.ball.y0, self.ball.x0, yai, xai)
                           self.ball = Ball(self.screen, self.sqrsize, yai, xai)
                           if not self.availablePlay():
                               self.AI1.ballClicked = False
                               self.player1 = not self.player1  # no more available self.ball moves (change of player)
                       else:
                           self.AI1.ballClicked = False
                           self.player1 = not self.player1
                       self.color_decision()
                   elif self.p2AI and not self.player1:
                       print("-------------------AI2------------------------")
                       m = self.AI2.minmax(self.ball.x0,self.ball.y0,self.board.places, 1)
                       (type, xai, yai) = m[0]
                       if type == 0 and self.board.places[yai-1][xai-1] != -1:
                           self.board.blueDeploy(yai, xai)
                           self.player1 = not self.player1 #player deployed a blue (change of player)
                       elif self.avJump(xai, yai):
                           self.jumpExecute(xai, yai)
                           self.board.ballMove(self.ball.y0, self.ball.x0, yai, xai)
                           self.ball = Ball(self.screen, self.sqrsize, yai, xai)
                           if not self.availablePlay():
                               self.AI2.ballClicked = False
                               self.player1 = not self.player1  # no more available self.ball moves (change of player)
                       else:
                           self.AI2.ballClicked = False
                           self.player1 = not self.player1
                       self.color_decision()

               #blues and self.ball GUI preparation
               self.drawElements()

               #Test whether Someone has WON
               if self.ball.y0 == 1:
                   self.myfont2 = pygame.font.SysFont("Comic Sans MS", 24)
                   label3 = self.myfont2.render(self.downName+" wins!", 1, self.red)
                   pygame.draw.rect(self.screen, self.black, (self.w/2-80, self.h/2-30, 160, 35), 2)
                   pygame.draw.rect(self.screen, self.gray, (self.w/2-79, self.h/2-29, 158, 33), 0)
                   self.screen.blit(label3, (self.w / 2 - 75, self.h / 2 - 30))
                   self.board.clearboard()
                   self.gameOver = True
               elif self.ball.y0 == 19:
                   self.myfont2 = pygame.font.SysFont("Comic Sans MS", 24)
                   label3 = self.myfont2.render(self.upName+" wins!", 1, self.red)
                   pygame.draw.rect(self.screen, self.black, (self.w/2-80, self.h/2-30, 160, 35), 2)
                   pygame.draw.rect(self.screen, self.gray, (self.w/2-79, self.h/2-29, 158, 33), 0)
                   self.screen.blit(label3, (self.w / 2 - 75, self.h / 2 - 30))
                   self.board.clearboard()
                   self.gameOver = True

               #self.screen update
               pygame.display.update()

