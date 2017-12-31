class dataStorage():

    def __init__(self, data):
        self.data = data
        self.data.dataCenter = 750
        self.data.squareLeft = 20
        self.data.squareTop = 70
        self.data.backgroundFill = "#F5CDCD"
        self.data.instructionFill = "#F5FDFD"
        self.data.emptySquareFill = "#E5FDFD"
        self.data.tripleWordFill = "red"
        self.data.doubleWordFill = "orange"
        self.data.doubleLetterFill = "yellow"
        self.data.tripleLetterFill = "green"
        self.data.occupiedSquareFill = "magenta"
        self.data.handSquareFill = "#66DDDD"
        self.data.squareSize = 32

        # for the scrabble board
        self.data.emptyBoardLocations = []
        self.data.board = ''
        for i in range(225):
            self.data.emptyBoardLocations.append(i)  # fills this with every location
            self.data.board += '-'      # would normally be taken from boardMaker
        self.data.occupiedBoardLocations = []
        self.data.occupiedBoardLetters = []
        self.data.temporaryBoardLocations = []
        self.data.temporaryBoardLetters = []

        # letters in hand
        self.data.letterHand = 'abcdefg'
        self.data.emptyHandLocations = []
        self.data.occupiedHandLocations = [0, 1, 2, 3, 4, 5, 6]
        self.data.canSwitchFromHand = False
        self.data.canSwitchFromBoard = False
        self.data.firstClickLocation = -1
        self.data.firstClickLetter = '_'

        self.data.letterBagSize = 0
        self.data.humanScore = 0
        self.data.computerScore = 0

        self.data.tripleWord = []
        self.data.doubleWord = []
        self.data.doubleLetter = []
        self.data.tripleLetter = []

        self.data.humanTurn = False
        self.data.computerTurn = False
        self.data.passTurn = False
        self.data.playTurn = False
        self.data.switchTurn = False
        self.data.invalidTurn = True
        self.data.searchOn = False

        self.data.isPaused = False
        self.data.timerDelay = 50
        self.data.message1 = 'Welcome to Scrabble!'
        self.data.message2 = 'Click anywhere to start.'
        self.data.message3 = ''

    def changeScore(self, score, forHuman):
        if forHuman:
            self.data.humanScore = score
        else:
            self.data.computerScore = score

    def changeLetterBagSize(self, letterBagSize):
        self.data.letterBagSize = letterBagSize

    def changeLetterHand(self, letterHand):
        self.data.letterHand = letterHand

    def humanChangeBoard(self, board):
        for i in range(len(self.data.temporaryBoardLocations)):
            self.data.occupiedBoardLocations.append(self.data.temporaryBoardLocations[i])
            self.data.occupiedBoardLetters.append(self.data.temporaryBoardLetters[i])
        self.data.temporaryBoardLocations = []
        self.data.temporaryBoardLetters = []

    def computerChangeBoard(self, board, letters, spaces):
        self.data.board = board
        for (letter, space) in zip(letters, spaces):
            self.data.emptyBoardLocations.remove(space)
            self.data.occupiedBoardLocations.append(space)
            self.data.occupiedBoardLetters.append(letter)

    def returnTemporaryLetters(self):
        for letter in self.data.temporaryBoardLetters:
            self.data.letterHand += letter
        for i in range(len(self.data.letterHand)-1, 0, -1):
            if self.data.letterHand[i] == '-':
                self.data.letterHand = self.data.letterHand[:i] + self.data.letterHand[i+1:]
        self.data.emptyBoardLocations += self.data.temporaryBoardLocations
        for location in self.data.temporaryBoardLocations:
            self.data.board = self.data.board[:location] + '-' + self.data.board[location+1:]
        handSize = len(self.data.temporaryBoardLocations)+len(self.data.occupiedHandLocations)
        self.data.occupiedHandLocations = []
        for i in range(handSize):
            self.data.occupiedHandLocations.append(i)
        self.data.temporaryBoardLocations = []
        self.data.temporaryBoardLetters = []

    def resetHand(self, letterHand):
        self.data.occupiedHandLocations = []
        for i in range(len(letterHand)):
            self.data.occupiedHandLocations.append(i)
        self.data.emptyHandLocations = []

    def refreshSpecialTiles(self, tw, dw, dl, tl):
        self.data.tripleWord = tw
        self.data.doubleWord = dw
        self.data.doubleLetter = dl
        self.data.tripleLetter = tl

    def resetData(self):
        self.data.canSwitchFromHand = False
        self.data.canSwitchFromBoard = False
        self.data.firstClickLocation = -1
        self.data.firstClickLetter = '_'
        self.data.invalidTurn = True

    def firstClickHand(self, handColumn):
        self.data.message1 = "Clicked letter in hand. Click a non-magent spot on the board."
        self.data.message2 = "Waiting for second click..."
        self.data.canSwitchFromHand = True
        self.data.firstClickLocation = handColumn

    def firstClickBoard(self, spot):
        self.data.message1 = "Clicked blue spot on board. Click a letter in the hand."
        self.data.message2 = "Waiting for second click..."
        self.data.canSwitchFromBoard = True
        self.data.firstClickLocation = spot

    def emptyHandBoardSwitch(self, spot):
        ''' Occupied hand and empty board '''       # firstClickLocation is the handColumn
        handColumn = self.data.firstClickLocation
        # switch the letters
        letterCopy = self.data.letterHand[handColumn]
        self.data.letterHand = self.data.letterHand[:handColumn] + self.data.board[spot] + self.data.letterHand[handColumn+1:]
        self.data.board = self.data.board[:spot] + letterCopy + self.data.board[spot+1:]
        # update the data
        self.data.emptyBoardLocations.remove(spot)      # empty board location becomes temporary
        self.data.temporaryBoardLocations.append(spot)
        self.data.temporaryBoardLetters.append(self.data.board[spot])
        self.data.occupiedHandLocations.remove(handColumn)      # remove the letter
        self.data.emptyHandLocations.append(handColumn)         # add to empty hand locations
        self.data.message1 = "Hand to board letter switch successful!"
        self.data.message2 = "Click something else now."

    def temporaryHandBoardSwitch(self, spot):
        ''' Occupied hand and temporary board '''       # firstClickLocation is the handColumn
        handColumn = self.data.firstClickLocation
        index = self.data.temporaryBoardLocations.index(spot)
        letterCopy = self.data.letterHand[handColumn]
        self.data.temporaryBoardLetters = self.data.temporaryBoardLetters[:index] + [letterCopy] + self.data.temporaryBoardLetters[index+1:]
        self.data.letterHand = self.data.letterHand[:handColumn] + self.data.board[spot] + self.data.letterHand[handColumn+1:]
        self.data.board = self.data.board[:spot] + letterCopy + self.data.board[spot+1:]
        self.data.message1 = "Hand to board letter switch successful!"
        self.data.message2 = "Click something else now."

    def occupiedHandHandSwitch(self, handColumn):
        ''' Occupied hand and occupied hand '''         # this just switches the letter order in letterHand
        handColumn1 = self.data.firstClickLocation
        handColumn2 = handColumn
        letter1 = self.data.letterHand[handColumn1]
        letter2 = self.data.letterHand[handColumn2]
        self.data.letterHand = self.data.letterHand[:handColumn1] + letter2 + self.data.letterHand[handColumn1+1:]
        self.data.letterHand = self.data.letterHand[:handColumn2] + letter1 + self.data.letterHand[handColumn2+1:]
        self.data.message1 = "Hand to hand letter switch successful!"
        self.data.message2 = "Click something else now."
        
    def emptyHandHandSwitch(self, handColumn):
        ''' Occupied hand and empty hand '''            # firstClickLocation is the handColumn
        handColumn1 = self.data.firstClickLocation
        handColumn2 = handColumn
        letter1 = self.data.letterHand[handColumn1]
        letter2 = self.data.letterHand[handColumn2]
        self.data.letterHand = self.data.letterHand[:handColumn1] + letter2 + self.data.letterHand[handColumn1+1:]
        self.data.letterHand = self.data.letterHand[:handColumn2] + letter1 + self.data.letterHand[handColumn2+1:]
        self.data.occupiedHandLocations.remove(handColumn1)
        self.data.emptyHandLocations.remove(handColumn2)
        self.data.occupiedHandLocations.append(handColumn2)
        self.data.emptyHandLocations.append(handColumn1)
        self.data.message1 = "Hand to hand letter switch successful!"
        self.data.message2 = "Click something else now."

    def occupiedBoardHandSwitch(self, handColumn):
        ''' Temporary board and occupied hand '''       # firstClickLocation is the spot
        spot = self.data.firstClickLocation
        index = self.data.temporaryBoardLocations.index(spot)
        letterCopy = self.data.letterHand[handColumn]
        self.data.temporaryBoardLetters = self.data.temporaryBoardLetters[:index] + [letterCopy] + self.data.temporaryBoardLetters[index+1:]
        self.data.letterHand = self.data.letterHand[:handColumn] + self.data.board[spot] + self.data.letterHand[handColumn+1:]
        self.data.board = self.data.board[:spot] + letterCopy + self.data.board[spot+1:]
        self.data.message1 = "Hand to board letter switch successful!"
        self.data.message2 = "Click something else now."

    def emptyBoardHandSwitch(self, handColumn):
        ''' Temporary board and empty hand '''       # firstClickLocation is the spot
        spot = self.data.firstClickLocation
        index = self.data.temporaryBoardLocations.index(spot)   # index maps to both location and letter
        self.data.temporaryBoardLocations.pop(index)        # temporary board location becomes empty
        self.data.temporaryBoardLetters.pop(index)
        self.data.emptyBoardLocations.append(spot)
        self.data.occupiedHandLocations.append(handColumn)      # remove the letter
        self.data.emptyHandLocations.remove(handColumn)         # add to empty hand locations
        # switch the letters
        letterCopy = self.data.letterHand[handColumn]
        self.data.letterHand = self.data.letterHand[:handColumn] + self.data.board[spot] + self.data.letterHand[handColumn+1:]
        self.data.board = self.data.board[:spot] + letterCopy + self.data.board[spot+1:]
        self.data.message1 = "Board to hand letter switch successful!"
        self.data.message2 = "Click something else now."

    def emptyBoardBoardSwitch(self, spot):
        ''' Occupied hand and empty hand '''         # firstClickLocation is the spot
        spot1 = self.data.firstClickLocation
        spot2 = spot
        letter1 = self.data.board[spot1]
        letter2 = self.data.board[spot2]
        self.data.board = self.data.board[:spot1] + letter2 + self.data.board[spot1+1:]
        self.data.board = self.data.board[:spot2] + letter1 + self.data.board[spot2+1:]
        index1 = self.data.temporaryBoardLocations.index(spot1)
        index2 = self.data.emptyBoardLocations.index(spot2)
        self.data.temporaryBoardLocations[index1] = spot2
        self.data.emptyBoardLocations[index2] = spot1
        self.data.message1 = "Board to board letter switch successful!"
        self.data.message2 = "Click something else now."

    def temporaryBoardBoardSwitch(self, spot):
        ''' Occupied hand and occupied hand '''         # this just switches the letter order in letterHand
        spot1 = self.data.firstClickLocation
        spot2 = spot
        letter1 = self.data.board[spot1]
        letter2 = self.data.board[spot2]
        self.data.board = self.data.board[:spot1] + letter2 + self.data.board[spot1+1:]
        self.data.board = self.data.board[:spot2] + letter1 + self.data.board[spot2+1:]
        index1 = self.data.temporaryBoardLocations.index(spot1)
        index2 = self.data.temporaryBoardLocations.index(spot2)
        self.data.temporaryBoardLocations[index1] = spot2
        self.data.temporaryBoardLocations[index2] = spot1
        self.data.message1 = "Board to board letter switch successful!"
        self.data.message2 = "Click something else now."

    def mousePressed(self, event):
        column = ((event.x - self.data.squareLeft) // self.data.squareSize)
        if (column > 14 or column < 0):
            column = 225        # if outside of board, column is only used for the board
        row = ((event.y - self.data.squareTop) // self.data.squareSize)
        spot = row*15 + column          # spot in grid
        onTemporarySpot = spot in self.data.temporaryBoardLocations
        onEmptySpot = spot in self.data.emptyBoardLocations

        handRow = (event.y - 360)//self.data.squareSize
        handColumn = ((event.x - (self.data.dataCenter-115))//self.data.squareSize)        # column in the hand
        occupiedInHand = ((handRow == 0) and (handColumn in self.data.occupiedHandLocations))
        emptyInHand = ((handRow == 0) and (handColumn in self.data.emptyHandLocations))

        onPassButton = (event.y >= 400 and event.y < 430) and (event.x >= 650 and event.x < 700)
        onPlayButton = (event.y >= 400 and event.y < 430) and (event.x >= 700 and event.x < 750)
        onSwitchButton = (event.y >= 400 and event.y < 430) and (event.x >= 750 and event.x < 800)
        onSearchButton = (event.y >= 400 and event.y < 430) and (event.x >= 800 and event.x < 850)
        
        if self.data.canSwitchFromHand:
            if onEmptySpot: self.emptyHandBoardSwitch(spot)     # firstClick was on the hand
            elif onTemporarySpot: self.temporaryHandBoardSwitch(spot)
            elif occupiedInHand: self.occupiedHandHandSwitch(handColumn)
            elif emptyInHand: self.emptyHandHandSwitch(handColumn)
            else:
                self.data.message1 = "Error, second click must be on the board or the hand."
                self.data.message2 = "Click a blue box or one of the buttons."
            self.data.firstClickLocation = -1       # if can switch, reset first click no matter what
            self.data.canSwitchFromHand = False     # if can switch, reset boolean no matter what
        elif self.data.canSwitchFromBoard:
            if occupiedInHand: self.occupiedBoardHandSwitch(handColumn)    # firstClick was on the board
            elif emptyInHand: self.emptyBoardHandSwitch(handColumn)
            elif onEmptySpot: self.emptyBoardBoardSwitch(spot)
            elif onTemporarySpot: self.temporaryBoardBoardSwitch(spot)
            else:
                self.data.message1 = "Error, second click must be on the board or the hand."
                self.data.message2 = "Click a blue box or one of the buttons."
            self.data.firstClickLocation = -1       # if can switch, reset first click no matter what
            self.data.canSwitchFromBoard = False    # if can switch, reset boolean no matter what
        else:
            if occupiedInHand: self.firstClickHand(handColumn)
            elif onTemporarySpot: self.firstClickBoard(spot)
            elif onEmptySpot:
                self.data.message1 = "That spot is unoccupied."
                self.data.message2 = "Try to click a blue box."
            elif onPassButton:
                self.data.passTurn = True
                self.data.message1 = "Clicked to pass turn."
                self.data.message2 = "Click again to let the computer play."
            elif onPlayButton:
                self.data.playTurn = True
                self.data.message1 = "Clicked to play turn."
                self.data.message2 = "Waiting..."
            elif onSwitchButton:
                self.data.switchTurn = True
                self.data.message1 = "Clicked to switch pieces."
                self.data.message2 = "Select your pieces and exchange them."
            elif onSearchButton:
                self.data.searchOn = True
            else:
                self.data.message1 = "Please click a blue letter or orange button."
                self.data.message2 = "Please!!!"

    def keyPressed(self, event):
        if (event.char == "p"):
            self.data.isPaused = not self.data.isPaused

    def drawBoardSquare(self, canvas, row, column, letter, fillColor):
        data = self.data
        canvas.create_rectangle(data.squareLeft + column*data.squareSize,
                    data.squareTop + row*data.squareSize,
                    data.squareLeft + column*data.squareSize + data.squareSize,
                    data.squareTop + row*data.squareSize + data.squareSize,
                    fill=fillColor)
        canvas.create_text(data.squareLeft + (column+0.5)*data.squareSize,
                    data.squareTop + (row+0.5)*data.squareSize,
                    text=letter, font="Arial 10")

    def redrawAll(self, canvas):
        data = self.data
        
        spotList = []           # used to make a list of spots for the board
        for i in range(225):
            spotList.append(i)

        # instruction background
        canvas.create_rectangle(0, 0, 1000, 600, fill=data.backgroundFill)
        canvas.create_rectangle(data.dataCenter-190, 35, data.dataCenter+190, 460, fill=data.instructionFill)
            
        for (letter, spot) in zip(data.board, spotList):
            row = spot//15
            column = spot%15
            letter = data.board[spot]
            if spot in data.emptyBoardLocations:
                if spot in data.tripleWord:
                    self.drawBoardSquare(canvas, row, column, letter, data.tripleWordFill)
                elif spot in data.doubleWord:
                    self.drawBoardSquare(canvas, row, column, letter, data.doubleWordFill)
                elif spot in data.doubleLetter:
                    self.drawBoardSquare(canvas, row, column, letter, data.doubleLetterFill)
                elif spot in data.tripleLetter:
                    self.drawBoardSquare(canvas, row, column, letter, data.tripleLetterFill)
                else:
                    self.drawBoardSquare(canvas, row, column, letter, data.emptySquareFill)
            elif spot in data.temporaryBoardLocations:
                self.drawBoardSquare(canvas, row, column, letter, data.handSquareFill)
            else:
                # for occupied squares
                self.drawBoardSquare(canvas, row, column, letter, data.occupiedSquareFill)

        # draw the letter hand
        canvas.create_text(data.dataCenter+2, 345, text="Scrabble Hand", font="Arial 10")

        indexList = []          # used to make a list of columns for the hand of letters
        for i in range(len(data.letterHand)):
            indexList.append(i)
        
        for (letter, column) in zip(data.letterHand, indexList):
            if letter == '-':
                canvas.create_rectangle(data.dataCenter-115 + data.squareSize*column,
                                360,
                                data.dataCenter-115 + data.squareSize*column + data.squareSize,
                                360 + data.squareSize,
                                fill=data.emptySquareFill)
            else:
                canvas.create_rectangle(data.dataCenter-115 + data.squareSize*column,
                                360,
                                data.dataCenter-115 + data.squareSize*column + data.squareSize,
                                360 + data.squareSize,
                                fill=data.handSquareFill)
            canvas.create_text(data.dataCenter-115 + data.squareSize*(column+0.5),
                               360 + data.squareSize/2,
                               text=letter,
                               font="Arial 10")

        # draw the buttons
        canvas.create_rectangle(650, 400, 700, 430, fill="orange")
        canvas.create_rectangle(700, 400, 750, 430, fill="orange")
        canvas.create_rectangle(750, 400, 800, 430, fill="orange")
        canvas.create_rectangle(800, 400, 850, 430, fill="orange")
        canvas.create_text(675, 415, text="Pass", font="Arial 10")
        canvas.create_text(725, 415, text="Play", font="Arial 10")
        canvas.create_text(775, 415, text="Switch", font="Arial 10")
        canvas.create_text(825, 415, text="Search", font="Arial 10")

        # draw the score
        canvas.create_rectangle(data.dataCenter-140, 250, data.dataCenter+140, 290, fill="#66FF66")

        # draw the text
        canvas.create_text(265, 50, text="Scrabble Board", font="Arial 20")
        canvas.create_text(data.dataCenter, 60, text="Instructions", font="Arial 15")
        canvas.create_text(data.dataCenter, 100, text="Pressing 'p' pauses/unpauses timer")
        canvas.create_text(data.dataCenter, 120, text="Red = 3x word, orange = 2x word, green = 3x letter, yellow = 2x letter")

        canvas.create_text(data.dataCenter, 160, text=("Messages: "), font="Arial 15")
        canvas.create_text(data.dataCenter, 190, text=(data.message1), font="Arial 10")
        canvas.create_text(data.dataCenter, 210, text=(data.message2), font="Arial 10")
        canvas.create_text(data.dataCenter, 230, text=(data.message3), font="Arial 10")

        canvas.create_text(data.dataCenter, 260, text=("Scores:"), font="Arial 10")
        canvas.create_text(data.dataCenter, 280, text=("Human score: " + str(data.humanScore) + "      Computer score: " + str(data.computerScore)), font="Arial 10")
        canvas.create_text(data.dataCenter, 300, text=("Number of letters left in bag: " + str(data.letterBagSize)), font="Arial 10")
