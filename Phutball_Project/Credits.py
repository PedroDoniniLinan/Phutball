import pygame


class Credits:
    def __init__(self, screen, sqrsize, w, h):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.quit = pygame.mixer.Sound("closesound.wav")

        #screen declaration
        (self.screen, self.sqrsize, self.w, self.h) = (screen, sqrsize, w, h)

        #fonts and colors
        self.black = (0, 0, 0)
        self.red = (255, 0, 0)
        self.gray = (250, 250, 250)
        self.myfont = pygame.font.SysFont("Comic Sans MS", round(sqrsize*0.8))
        self.running = True
        self.i=0

        #text definitions
        self.text1 = "Programmers:"
        self.text2 = "Wassim KABBARA"
        self.text3 =  "Pedro DONINI LINAN"
        self.text4 = "Instructor:"
        self.text5 = "prof. Marc-Antoine WEISSER"
        self.text6 = "Testers:"
        self.text7 = "©Copyrights 2018"


    def event_detector(self):
        for event in pygame.event.get():
            if  event.type == pygame.QUIT or self.h / 0.43 - self.i<-5:
                self.running = False
                self.quit.play() #playing quit sound


    def run(self):
        while self.running:
            self.clock.tick(60)
            #event detection
            self.event_detector()
            #define phrases phrases
            label1 = self.myfont.render(self.text1, 1, self.gray)
            label2 = self.myfont.render(self.text2, 1, self.gray)
            label3 = self.myfont.render(self.text3, 1, self.gray)
            label4 = self.myfont.render(self.text4, 1, self.gray)
            label5 = self.myfont.render(self.text5, 1, self.gray)
            label6 = self.myfont.render(self.text6, 1, self.gray)
            label7 = self.myfont.render(self.text7, 1, self.gray)
            #fill screen
            self.screen.fill(self.black)
            #draw and move phrases
            self.screen.blit(label1, (self.w / 3.9, self.h / 0.95 - self.i))
            self.screen.blit(label2, (self.w / 3.9, self.h / 0.90 - self.i))
            self.screen.blit(label3, (self.w / 3.9, self.h / 0.85 - self.i))
            self.screen.blit(label4, (self.w / 3.9, self.h / 0.65 - self.i))
            self.screen.blit(label5, (self.w / 3.9, self.h / 0.63 - self.i))
            self.screen.blit(label6, (self.w / 3.9, self.h / 0.53 - self.i))
            self.screen.blit(label2, (self.w / 3.9, self.h / 0.515 - self.i))
            self.screen.blit(label3, (self.w / 3.9, self.h / 0.5 - self.i))
            self.screen.blit(label7, (self.w / 3.9, self.h / 0.43 - self.i))
            self.i+=1
            #self.screen update
            pygame.display.update()
