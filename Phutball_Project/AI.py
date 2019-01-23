
class AI:
    def __init__(self, board, side):
        self.stopDep = 0
        self.moveDep = 0
        self.blueDep = 0
        self.side = side
        self.ballClicked = False
        self.board = [row[:] for row in board]

    def avJumpList(self, x0, y0):
        avPlace = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                y = y0-1+i
                x = x0-1+j
                outBoard = x > 14 or x < 0 or y > 18 or y < 0
                if self.board[y][x] == -1:
                    while not outBoard:
                        if self.board[y][x] == 0 or (self.board[y][x] == -1 and (y == 0 or y == 18)):
                           avPlace.append((x+1, y+1))
                           break
                        y += i
                        x += j
                        outBoard = x > 14 or x < 0 or y > 18 or y < 0
        return avPlace

    def availablePlay(self, x0, y0):
        for i in range(-1, 2):
            for j in range(-1, 2):
                y = y0-1+i
                x = x0-1+j
                outBoard = x > 14 or x < 0 or y > 18 or y < 0
                if self.board[y][x] == -1:
                    while not outBoard:
                        if self.board[y][x] == 0 or (self.board[y][x] == -1 and (y == 0 or y == 18)):
                            return True
                        y += i
                        x += j
                        outBoard = x > 14 or x < 0 or y > 18 or y < 0
        return False

    def jumpExecute(self, x, y, x0, y0):
        if x == x0:
            if y > y0 + 1:
                for i in range(y0, y-1):
                    self.board[i][x-1] = 0
            elif y < y0 - 1:
                for i in range(y, y0-1):
                    self.board[i][x-1] = 0
        elif y == y0:
            if x > x0 + 1:
                for j in range(x0, x-1):
                    self.board[y-1][j] = 0
            elif x < x0 - 1:
                for j in range(x, x0-1):
                    self.board[y-1][j] = 0
        elif x-y == x0-y0:
            if x > x0 + 1:
                for k in range(0, x-x0-1):
                    self.board[y0+k][x0+k] = 0
            elif x < x0 - 1:
                for k in range(0, x0-x-1):
                    self.board[y0-k-2][x0-k-2] = 0
        elif x+y == x0+y0:
            if x > x0 + 1:
                for k in range(0, x-x0-1):
                    self.board[y0-k-2][x0+k] = 0
            elif x < x0 - 1:
                for k in range(0, x0-x-1):
                    self.board[y0+k][x0-k-2] = 0

    def dumbMove(self, x0, y0):
        if self.board[y0-2][x0-1] != -1:
            type = 0
            x = x0
            y = y0-1
        else:
            type = 1
            x = x0
            y = y0-2
        return (type,x,y)

    def printBoard(self, x):
        print()
        for i in range(0, 19):
            print()
            for j in range(0, 15):
                print('{0:2d}'.format(x[i][j]), end=" ")

    def frontZone(self, x0, y0, list, direction):
        for i in range(-1, 2):
            if (x0-i, y0-direction) not in list:
                list.append((x0-i, y0-direction))

    def interestZone(self, x0, y0, direction):
        avPlaces = self.avJumpList(x0, y0)
        interestList = []
        self.frontZone(x0, y0, interestList, direction)
        for p in avPlaces:
            self.frontZone(p[0], p[1], interestList, direction)
        return interestList

    def minmax(self, x0, y0, board, minmax):
        self.board = [row[:] for row in board]
        scores = []
        moves = []
        bestMove = (1, x0, y0)
        bestScore = minmax*(-150)
        interestZone = self.interestZone(x0, y0, minmax*self.side)
        if not self.ballClicked:
            minmaxNext = -minmax
            for i in range(0, 19):
                for j in range(1, 14):
                    if self.board[i][j] == 0 and ((j+1), (i+1)) in interestZone:
                        if self.blueDep < 3:#############3
                            self.blueDep += 1
                            clickAux = self.ballClicked
                            self.ballClicked = False
                            scoreAux = self.minmax(x0, y0, [row[:] for row in self.board], minmaxNext)
                            self.ballClicked = clickAux
                            self.blueDep -= 1
                            scores.append(scoreAux[1])
                        else:
                            scores.append(0)
                        moves.append((0, j+1, i+1))
                    self.board = [row[:] for row in board]
        if self.availablePlay(x0, y0):
            minmaxNext = minmax
            avPlaces = self.avJumpList(x0, y0)
            for n in avPlaces:
                self.jumpExecute(n[0], n[1], x0, y0)
                self.board[y0 - 1][x0 - 1] = 0
                self.board[n[1] - 1][n[0] - 1] = 1
                if self.moveDep < 25:##############15
                    self.moveDep += 1
                    clickAux = self.ballClicked
                    self.ballClicked = True
                    scoreAux = self.minmax(n[0], n[1], [row[:] for row in self.board], minmaxNext)
                    self.ballClicked = clickAux
                    self.moveDep -= 1
                    scores.append((y0-n[1])*self.side + scoreAux[1])
                else:
                    scores.append((y0 - n[1])*self.side)
                moves.append((1, n[0], n[1]))
                self.board = [row[:] for row in board]
        elif self.ballClicked:
            minmaxNext = -minmax
            if self.stopDep < 25:###########7
                self.stopDep += 1
                clickAux = self.ballClicked
                self.ballClicked = False
                scoreAux = self.minmax(x0, y0, [row[:] for row in self.board], minmaxNext)
                self.ballClicked = clickAux
                self.stopDep -= 1
                scores.append(scoreAux[1])
            else:
                scores.append(0)
            moves.append((2, 0, 0))
        k = 0
        for s in scores:
            if minmax == 1 and s > bestScore:
                bestMove = moves[k]
                bestScore = s
            elif minmax == -1 and s < bestScore:
                bestMove = moves[k]
                bestScore = s
            k += 1
        if self.side == 1 and y0 == 19 or self.side == -1 and y0 == 1:
            bestScore = -100
            #print("WAT")
        elif self.side == -1 and y0 == 19 or self.side == 1 and y0 == 1:
            bestScore = 100
            #print("WAT2", self.side, y0)

        if bestMove[0] == 1:
            self.ballClicked = True

        #self.board = [row[:] for row in boardCpy]
        return (bestMove, bestScore)
        #return self.dumbMove(x0, y0, board)
