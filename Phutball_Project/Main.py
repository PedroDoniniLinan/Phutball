from Game import*
from pygame_textinput import*
from time import sleep
import pygame
import webbrowser
import threading
from Credits import*

def inside(rectout, i, once, test):
    (xm, ym) = pygame.mouse.get_pos()
    if xm >= rectout[0] and xm <= (rectout[0]+rectout[2]) and ym >= rectout[1] and ym <= (rectout[1]+rectout[3]):
        if once[i] and test:
            select.play()
            once[i] = False
        return True
    else:
        once[i] = True
        return False


def sizeCursor(cursor):
       (xm, ym) = pygame.mouse.get_pos()
       dist = (xm-cursor[0])**2 + (ym-cursor[1])**2
       if dist <= 1.25*cursorSize**2:
           return True


def updatesize(sqrsize):
    (w, h) = (sqrsize*16, sqrsize*20)
    screen = pygame.display.set_mode((w, h))
    bg = pygame.image.load('philo.jpg')
    bg = pygame.transform.scale(bg, (w, h))
    myfont = pygame.font.SysFont("Comic Sans MS", round((w + h)/43.5))
    myfont1 = pygame.font.SysFont("Comic Sans MS", round((w + h)/55))
    word = [myfont.render("New Game", 1, red), myfont.render("Continue", 1, red), myfont.render("UP", 1, red), myfont.render("Down", 1, red), myfont.render("Help", 1, red), myfont.render("Credits", 1, red), myfont1.render("name:", 1, blue), myfont1.render("AI", 1, blue), myfont1.render("HB", 1, blue)]
    rectout = [(round(w*0.36), round(h*0.244), round(w*0.28), round(h*0.06)), (round(w*0.38), round(h*0.327), round(w*0.237), round(h*0.06)), (round(w*0.435), round(h*0.41), round(w*0.1), round(h*0.06)), (round(w*0.42), round(h*0.5), round(w*0.155), round(h*0.06)), (round(w*0.428), round(h*0.58), round(w*0.14), round(h*0.06)), (round(w*0.40), round(h*0.67), round(w*0.219), round(h*0.06)), (round(w*0.6), round(h*0.41), round(w*0.38), round(h*0.155)), (round(w*0.66), round(h*0.47), round(w*0.1), round(h*0.06)), (round(w*0.82), round(h*0.47), round(w*0.1), round(h*0.06))]
    rectin  = [(round(w*0.36)+1, round(h*0.244)+1, round(w*0.28)-2, round(h*0.06)-2), (round(w*0.38)+1, round(h*0.327)+1, round(w*0.237)-2, round(h*0.06)-2), (round(w*0.435)+1, round(h*0.41)+1, round(w*0.1)-2, round(h*0.06)-2), (round(w*0.42)+1, round(h*0.5)+1, round(w*0.155)-2, round(h*0.06)-2), (round(w*0.428)+1, round(h*0.58)+1, round(w*0.14)-2, round(h*0.06)-2), (round(w*0.4)+1, round(h*0.67)+1, round(w*0.219)-2, round(h*0.06)-2), (round(w*0.6)+1, round(h*0.41)+1, round(w*0.38)-2, round(h*0.155)-2), (round(w*0.66)+1, round(h*0.47)+1, round(w*0.1)-2, round(h*0.06)-2), (round(w*0.82)+1, round(h*0.47)+1, round(w*0.1)-2, round(h*0.06)-2)]
    pos = [(round(w*0.37), round(h*0.244)), (round(w*0.392), round(h*0.327)), (round(w*0.452), round(h*0.41)), (round(w*0.431), round(h*0.5)), (round(w*0.44), round(h*0.58)), (round(w*0.422), round(h*0.67)), (round(w*0.62), round(h*0.41)), (round(w*0.675), round(h*0.48)), (round(w*0.835), round(h*0.48))]
    dash = [round(w*0.1), round(h*0.137), round((h+w)/13.92), 1]
    cursorPos = round(h*0.1379)
    return (screen, bg, (w, h), word, rectout, rectin, pos, cursorPos, dash, myfont1)


def checkNamesize(name,up):
    if up:
        if len(name) > 9:
            upName.input_string = name[0:9]
        upName.cursor_position = len(name)
    else:
        if len(name) > 9:
            downName.input_string = name[0.9]
        downName.cursor_position = len(name)

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption("Phutball prototype")

#Sound declaration
select = pygame.mixer.Sound("select.wav")
opensound = pygame.mixer.Sound("opensound.wav")
closesound = pygame.mixer.Sound("closesound.wav")
quit = pygame.mixer.Sound("exit.wav")
select.set_volume(0.05)

#Menu Tabs
black = (0, 0, 0)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (50, 50, 255)
gray = (250, 250, 250)
sqrsize = 29
cursorSize = 10

#Initialization
running = True
buttonRelease = True
mouseclick = False
windowUp = False
windowDown = False
upName = TextInput()
downName = TextInput()
upPlayer = []
downPlayer = []
once = []
(screen, bg, (w, h), word, rectout, rectin, pos, x, dash, upName.font_object) = updatesize(sqrsize)
downName.font_object = upName.font_object
cursorPos = [round(dash[0]+dash[2]/2), round(h*0.1379)]
for i in range(9): once.append(True) #To insure select sound only plays once entered within the label
try:
    with open('upName.txt', 'r') as name:
        upName.input_string = name.read()
except:
    upName.input_string = ""
try:
    with open('downName.txt', 'r') as name:
        downName.input_string = name.read()
except:
    downName.input_string = ""
try:
    with open('upPlayer.csv', 'r') as saved_game:
        reader = csv.reader(saved_game)
        upPlayer = [[int(e) for e in r] for r in reader]
        i = 0
        for r in upPlayer:
            if r == []:
                del upPlayer[i]
            i += 1
        upPlayer = upPlayer[0]

except:
    upPlayer = [0, 1] #Ai then HB
try:
    with open('downPlayer.csv', 'r') as saved_game:
        reader = csv.reader(saved_game)
        downPlayer = [[int(e) for e in r] for r in reader]
        i = 0
        for r in downPlayer:
            if r == []:
                del downPlayer[i]
            i += 1
        downPlayer = downPlayer[0]

except:
    downPlayer = [0, 1] #Ai then HB

#Main Loop
while running:
    clock.tick(60) #frames per second

    #event detection
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            buttonRelease = True
        if buttonRelease: #ensures that one self.mouseclick is computed only once
            if event.type == pygame.QUIT:
                running = False
                quit.play()
                sleep(quit.get_length()*0.55)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouseclick = True
            elif event.type != pygame.MOUSEMOTION:
                mouseclick = False

    #Mouseclick Treatment
    if mouseclick and buttonRelease:
        #Create NewGame
        if inside(rectout[0], 1, once, False):
            buttonRelease = False
            opensound.play()
            game = Game(screen, sqrsize, w, h, True)
            game.p1AI = upPlayer[0]
            game.p2AI = downPlayer[0]
            game.run()
            buttonRelease = True

        #Load saved game
        if inside(rectout[1], 0, once, False):
            buttonRelease = False
            opensound.play()
            game = Game(screen, sqrsize, w, h, False)
            game.p1AI = upPlayer[0]
            game.p2AI = downPlayer[0]
            game.run()
            buttonRelease = True
        #subwindow of choosing up player
        if windowUp:
            if not inside(rectout[6], 0, once, False): #anywhere pressed except subwindow of up
                windowUp = False
                windowDown = False
                with open('upName.txt', 'w') as name: #saving the name to a file
                    name.write(upName.get_text())
                with open('upPlayer.csv', 'w') as player:
                    writer = csv.writer(player)
                    writer.writerow(upPlayer)
                if not windowDown: closesound.play()
            if inside(rectout[7], 0, once, False):
                upPlayer = [1, 0]
            if inside(rectout[8], 0, once, False):
                upPlayer = [0, 1]
        if windowDown:#subwindow of choosing down player
            if not inside(rectout[6], 0, once, False):#anywhere pressed except subwindow of down
                windowDown = False
                windowUp = False
                with open('downName.txt', 'w') as name: # saving the name to a file
                    name.write(downName.get_text())
                with open('downPlayer.csv', 'w') as player:
                    writer = csv.writer(player)
                    writer.writerow(downPlayer)
                if not windowUp: closesound.play()
            if inside(rectout[7], 0, once, False):
                downPlayer = [1, 0]
            if inside(rectout[8], 0, once, False):
                downPlayer = [0, 1]

        #Up label pressed
        if inside(rectout[2], 0, once, False):
            buttonRelease = False
            opensound.play()
            windowUp = True

        #Down label pressed
        if inside(rectout[3], 0, once, False):
            buttonRelease = False
            opensound.play()
            windowDown = True

        #Help label pressed
        if inside(rectout[4], 0, once, False):
            buttonRelease = False
            opensound.play()
            webbrowser.open('https://en.wikipedia.org/wiki/Phutball')  # Go to example.com

        #credits label pressed
        if inside(rectout[5], 0, once, False):
            buttonRelease = False
            opensound.play()
            credits = Credits(screen, sqrsize, w, h)
            credits.run()
            print("!!!!!!!!!!!!!!!!!!!")
            buttonRelease = True

    #zoom activated
    if sizeCursor(cursorPos):
        xm = pygame.mouse.get_pos()[0]
        if dash[0] <= xm <= dash[0]+dash[2]:
            cursorPos[0] = xm
        sqrsize = round(0.14*(cursorPos[0]-dash[0]/dash[2]) + 15)
        (screen, bg, (w, h), word, rectout, rectin, pos, cursorPos[1], dash, upName.font_object) = updatesize(sqrsize)
        downName.font_object = upName.font_object

    #Drawing background and menu Buttons
    screen.fill(blue)
    screen.blit(bg, (0, 0))
    pygame.draw.rect(screen, black, dash, 4)
    pygame.draw.circle(screen, blue if not sizeCursor(cursorPos) else red, cursorPos,cursorSize, cursorSize)
    for i in range(9):
        if i < 6:
            pygame.draw.rect(screen, black, rectout[i], 2)
            pygame.draw.rect(screen, yellow if inside(rectout[i], i, once, True) else gray, rectin[i], 0)
            screen.blit(word[i], pos[i])
        elif windowUp:
            pygame.draw.rect(screen, black, rectout[i], 2)
            if i == 6:
                pygame.draw.rect(screen, gray, rectin[i], 0)
            else:
                pygame.draw.rect(screen, yellow if inside(rectout[i], i, once, True) or upPlayer[i % 7]==1 else gray, rectin[i], 0)
            screen.blit(word[i], pos[i])
        elif windowDown:
            pygame.draw.rect(screen, black, rectout[i], 2)
            if i == 6:
                pygame.draw.rect(screen, gray, rectin[i], 0)
            else:
                pygame.draw.rect(screen, yellow if inside(rectout[i], i, once, True) or downPlayer[i % 7]==1 else gray, rectin[i], 0)
            screen.blit(word[i], pos[i])

    #Up Text Input activated
    if windowUp:
        upName.update(events)
        checkNamesize(upName.get_text(), True)
        aux = rectout[6][0:2]
        screen.blit(upName.get_surface(), (round(aux[0]*1.23),aux[1]))

    #DownText Input activated
    if windowDown:
        downName.update(events)
        checkNamesize(downName.get_text(), False)
        aux = rectout[6][0:2]
        screen.blit(downName.get_surface(), (round(aux[0]*1.23),aux[1]))

    pygame.display.update()

