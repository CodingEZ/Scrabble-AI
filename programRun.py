import dataStorage as DS
import computerWordChecker as CWC
import humanChecker as HC
import player
import extraValue as EV
import boardKeeper as BK
import letterBag as LB
import helper
from tkinter import *

# all of the big classes
boardKeeper = BK.boardKeeper()
humanPlayer = player.player()
computerPlayer = player.player()
humanCheck = HC.humanChecker()
computerCheck = CWC.computerWordChecker()
letterBag = LB.letterBag()

# make the dictionary
doc = open('scrabbleDictionary.txt', 'r')
document = doc.read().lower()
dictionary = set(document.split('\n'))
doc.close()

def run(width=1000, height=600):
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height, fill='white', width=0)
        x.redrawAll(canvas)
        canvas.update()    

    def mousePressedWrapper(event, canvas, data):
        if x.data.endOfGame:
            # end of game scenario
            x.data.message1 = "Game Over!!!"
            if humanPlayer.points > computerPlayer.points:
                x.data.message2 = 'Human player wins!'
            elif humanPlayer.points < computerPlayer.points:
                x.data.message2 = 'Computer player wins ...'
            else:
                x.data.message2 = "It's a tie"
        
        elif x.data.computerTurn:
            # case of computer turn
            x.data.message1 = "It's the computer's turn"
            x.data.message2 = 'Waiting for the computer...'
            x.data.message3 = ''
            redrawAllWrapper(canvas, data)

            occupied = set(boardKeeper.refreshOccupied())
            attachments = set(boardKeeper.refreshAttachments())

            computerCheck.changeLetterHand(computerPlayer.letterHand)
            computerCheck.getLetterCombos()
            workingCombos = computerCheck.getDirectedCombos(boardKeeper.board, occupied, attachments, dictionary)
            maxCombo = EV.maxComboValue(workingCombos, boardKeeper.board)
            if maxCombo[0] != -1:
                x.refreshSpecialTiles(EV.tripleWord, EV.doubleWord, EV.doubleLetter, EV.tripleLetter)
                boardKeeper.changeBoard(maxCombo[1], maxCombo[2])
                x.computerChangeBoard(boardKeeper.board, maxCombo[1], maxCombo[2])
                computerPlayer.addPoints(maxCombo[0])
                x.changeScore(computerPlayer.points, False)
                computerPlayer.playFromHand(maxCombo[1])
                removedLetters = letterBag.removeLetters(len(maxCombo[1]))
                x.changeLetterBagSize(len(letterBag.letterBag))
                computerPlayer.addToHand(removedLetters)
                data.message1 = "Score: " + str(maxCombo[0]) + ", Letters used: " + str(maxCombo[1])
            else:
                x.data.message1 = 'The computer was forced to pass.'
            x.data.message2 = "Click to make it the human player's turn."
            x.data.computerTurn = False
            x.data.humanTurn = False

            if len(computerPlayer.letterHand) == 0:
                x.data.endOfGame == True    # reached end of game

        elif x.data.humanTurn:
            # case of human turn

            occupied = set(boardKeeper.refreshOccupied())
            attachments = set(boardKeeper.refreshAttachments())
            
            x.mousePressed(event)

            if x.data.searchOn:
                x.data.searchOn = False
                e = Entry()
                e.pack()
                e.delete(0, END)
                e.insert(0, "a default value")

            elif x.data.switchTurn:
                x.data.switchTurn = False
                x.returnTemporaryLetters()
                #print(Something that produces an error)
                
            elif x.data.passTurn:
                x.data.passTurn = False
                x.returnTemporaryLetters()
                x.data.humanTurn = False
                x.data.computerTurn = True
                
            elif x.data.playTurn:
                x.data.playTurn = False
                humanCheck.changeLetterHand(humanPlayer.letterHand)
                # make the spaces and letters
                spaces = sorted(x.data.temporaryBoardLocations)
                letters = []
                newDict = {}
                for (location, character) in zip(x.data.temporaryBoardLocations, x.data.temporaryBoardLetters):
                    newDict[location] = character
                for space in spaces:
                    letters.append(newDict[space])
                    
                # human check, starts with a space and letter check
                if len(letters) != len(spaces):
                    x.data.message1 = 'Number of letters and number of locations should be equal.'
                    spaces = []
                    letters = []
                elif not helper.areValidLetters(letters):
                    x.data.message1 = 'Some letters were not valid. They should be alphabet characters.'
                    letters = ['$']
                elif not helper.areValidLocations(spaces):
                    x.data.message1 = 'Some locations were not valid. They should be integers.'
                    spaces = []
                else:
                    locations = []
                    for space in spaces:
                        locations.append(int(space))
                    spaces = locations
                    x.data.message1 = 'Locations and letters are valid. '
                    
                # human check, enters word check
                returnedCombos = humanCheck.comboWorks(letters, spaces, boardKeeper.board, occupied, attachments, dictionary)
                x.data.message1 += returnedCombos[2]
                if returnedCombos[0]:
                    # check
                    workingCombos = [[letters, spaces, returnedCombos[1]]]
                    maxCombo = EV.maxComboValue(workingCombos, boardKeeper.board)
                    x.refreshSpecialTiles(EV.tripleWord, EV.doubleWord, EV.doubleLetter, EV.tripleLetter)
                    score = maxCombo[0]
                    lettersPlayed = maxCombo[1]
                    combos = maxCombo[2]
                    x.data.message2 = 'Combo score: ' + str(score) + ', Letters played: ' + str(lettersPlayed)
                    x.data.message3 = 'Click anywhere to start computer turn.'
                    boardKeeper.changeBoard(lettersPlayed, combos)
                    humanPlayer.addPoints(score)
                    x.changeScore(humanPlayer.points, True)
                    humanPlayer.playFromHand(lettersPlayed)
                    removedLetters = letterBag.removeLetters(len(lettersPlayed))
                    humanPlayer.addToHand(removedLetters)
                    x.changeLetterHand(humanPlayer.letterHand)
                    x.changeLetterBagSize(len(letterBag.letterBag))
                    x.resetHand(humanPlayer.letterHand)
                    x.humanChangeBoard(boardKeeper.board)
                    x.resetData()
                    x.data.humanTurn = False
                    x.data.computerTurn = True
                    
                    if len(humanPlayer.letterHand) == 0:
                        x.data.endOfGame == True    # reached end of game
                else:
                    x.data.message2 = "Invalid human turn. Click on a blue box or a button."

        else:
            x.data.message1 = "It's the human's turn"
            x.data.message2 = 'Click on a blue box.'
            x.data.humanTurn = True
            x.data.computerTurn = False

        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        x.keyPressed(event)
        redrawAllWrapper(canvas, data)
    
    # Initialize data
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.endOfGame = False
    x = DS.dataStorage(data)
    x.refreshSpecialTiles(EV.tripleWord, EV.doubleWord, EV.doubleLetter, EV.tripleLetter) # initialize special tiles in dataStorage
    # creates hands for both players
    removedLetters = letterBag.removeLetters(7)
    humanPlayer.addToHand(removedLetters)
    x.data.letterHand = humanPlayer.letterHand
    removedLetters = letterBag.removeLetters(7)
    computerPlayer.addToHand(removedLetters)
    # initialize size of letterbag in datastorage
    x.changeLetterBagSize(len(letterBag.letterBag))
    # create the root and the canvas
    root = Tk()
    frame = Frame(root)
    canvas = Canvas(root, width=x.data.width, height=x.data.height)
    canvas.pack()
    # set up events
    redrawAllWrapper(canvas, x.data)    # this is to show the interface
    root.bind("<Button-1>", lambda event: mousePressedWrapper(event, canvas, x.data))
    root.bind("<Key>", lambda event: keyPressedWrapper(event, canvas, x.data))
    # and launch the app
    while not x.data.endOfGame:
        root.mainloop()  # blocks until window is closed
    print("bye!")

run(1000, 600)
