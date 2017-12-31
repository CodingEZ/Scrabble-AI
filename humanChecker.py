import itertools
import helper

def noSpaceAlreadyOccupied(situation, occupied):
    for spot in situation:
        if spot in occupied:
            return False
    return True

def allInRow(situation):
    ''' Checks if the spaces are in one row '''
    row = situation[0]//15
    for spot in range(1, len(situation)):
        if row != situation[spot]//15:
            return (False, 0)
    return (True, row)

def allInColumn(situation):
    ''' Checks if the spaces are in one column '''
    column = situation[0]%15
    for spot in range(1, len(situation)):
        if column != situation[spot]%15:
            return (False, 0)
    return (True, column)

# One-letter-placements are counted as rows
def lineConnected(situation, occupied, attachments):    
    # remove this later
    if len(situation) == 0:
        return (False, 'Please use some letters.')
    
    rowCheck = allInRow(situation)
    columnCheck = allInColumn(situation)
    
    if rowCheck[0]:
        columns = []        # checks in row
        # adds spots from situation
        row = situation[0]//15      ### this can be simplified since we return the row number
        for spot in situation:
            columns.append(spot%15)
        # checks if they are connected in line
        numColumn = 0
        while numColumn != len(columns)-1:
            # once numColumn == len(columns), this loop should end
            if (((row*15 + columns[numColumn] + 1) in occupied) and (numColumn != 14)):
                columns = columns[:numColumn+1] + [columns[numColumn] + 1] + columns[numColumn+1:]
            if columns[numColumn] + 1 != columns[numColumn+1]:
                return (False, 'Columns not consecutive: ' + str(columns[numColumn]) + '/' + str(columns[numColumn+1]))
            numColumn += 1
        return (True, True)
            
    elif columnCheck[0]:
        rows = []       # checks in column
        # adds occupied squares from the correct column
        column = situation[0]%15
        for spot in situation:
            rows.append(spot//15)
        # checks if they are connected in line
        numRow = 0
        while numRow != len(rows)-1:
            # once numRow == len(rows), this loop should end
            if (((rows[numRow]*15 + column + 15) in occupied) and (numRow != 14)):
                rows = rows[:numRow+1] + [rows[numRow] + 1] + rows[numRow+1:]
            if rows[numRow] + 1 != rows[numRow+1]:
                return (False, 'Rows not consecutive: ' + str(rows[numRow]) + '/' + str(rows[numRow+1]))
            numRow += 1
        return (True, False)
        
    else:
        return (False, 'Letters not in one line.')
    
def attached(situation, occupied, attachments):
    ''' Checks if the placement of letters conform to placement rules '''
    isRow = lineConnected(situation, occupied, attachments)[1]
    for spot in situation:
        if spot in attachments:
            return (True, isRow)     # Checks if any of the spots is an attachment location. Returns whether it attaches as a row or column.
    return (False, 'Letters have to connect to the current letters on the board.')

def letterLeftRight(spot, occupied):
    ''' Checks if there is a letter to the left or right '''
    column = spot%15
    if column != 0:
        if (spot-1) in occupied:
            return True
    if column != 14:
        if (spot+1) in occupied:
            return True
    return False

def letterUpDown(spot, occupied):
    ''' Checks if there is a letter up or down '''
    row = spot//15
    if row != 0:
        if (spot-15) in occupied:
            return True
    if row != 14:
        if (spot+15) in occupied:
            return True
    return False

def getMainCombo(isRowCombo, occupied, situation):
    ''' Get the spots that correspond to the main combo in order '''
    spot = situation[0]
    locations = [spot]
    locator = spot
    if isRowCombo:
        while (((locator + 1) in occupied) or ((locator + 1) in situation)) and (locator%15 != 14):
            locator += 1
            locations.append(locator)
        locator = spot      # resets the locator to the original position
        while (((locator - 1) in occupied) or ((locator - 1) in situation)) and (locator%15 != 0):
            locator -= 1
            locations.append(locator)
    else:
        while ((locator + 15) in occupied) or ((locator + 15) in situation):
            locator += 15
            locations.append(locator)
        locator = spot      # resets the locator to the original position
        while ((locator - 15) in occupied) or ((locator - 15) in situation):
            locator -= 15
            locations.append(locator)
    return sorted(locations)

def getSideCombo(isRowCombo, spot, occupied):
    ''' Get the spots that correspond to the side combo in order '''
    locations = [spot]
    locator = spot
    if isRowCombo:
        while (locator + 15) in occupied:
            locator += 15
            locations.append(locator)
        locator = spot
        while (locator - 15) in occupied:
            locator -= 15
            locations.append(locator)
    else:
        while ((locator + 1) in occupied) and (locator%15 != 14):
            locator += 1
            locations.append(locator)
        locator = spot
        while ((locator - 1) in occupied) and (locator%15 != 0):
            locator -= 1
            locations.append(locator)
    return sorted(locations)

def getAllCombos(situation, occupied, isRowCombo):
    ''' Gets combos of letters made by a valid placement for a computer '''
    combosMade = []
    mainCombo = getMainCombo(isRowCombo, occupied, situation)
    if len(mainCombo) != 1:
        combosMade.append(mainCombo)
    # take note, the main combo comes first
    for spot in situation:
        if (isRowCombo) and (letterUpDown(spot, occupied)):
            # checks if it is a row combo and if there exists a side combo
            combosMade.append(getSideCombo(isRowCombo, spot, occupied))
        if (not isRowCombo) and (letterLeftRight(spot, occupied)):
            # checks if it is a row combo and if there exists a side combo
            combosMade.append(getSideCombo(isRowCombo, spot, occupied))
    if len(combosMade) == 0:
        combosMade.append(mainCombo)    # for situations where a single letter is played by itself (for avoiding errors)
    return combosMade   # now all of these combos must be checked in the dictionary

#############################################################################
#############################################################################

class humanChecker():

    def __init__(self):
        # make the dictionary of all possible words
        doc = open('scrabbleDictionary.txt', 'r')
        document = doc.read().lower()
        self.dictionary = set(document.split('\n'))

    def changeLetterHand(self, letters):
        self.letters = letters

    def mkAlphabet(self, letters):
        ''' Helper function that check for illegal characters '''        
        alphabet = {'A' : 0, 'B' : 0, 'C' : 0, 'D' : 0,
                       'E' : 0, 'F' : 0, 'G' : 0, 'H' : 0,
                       'I' : 0, 'J' : 0, 'K' : 0, 'L' : 0,
                       'M' : 0, 'N' : 0, 'O' : 0, 'P' : 0,
                       'Q' : 0, 'R' : 0, 'S' : 0, 'T' : 0,
                       'U' : 0, 'V' : 0, 'W' : 0, 'X' : 0,
                       'Y' : 0, 'Z' : 0, '$' : 0}
        for char in letters:
            if char in """1234567890!@#$%^&*()[]{}:;"'<>,.?/|~`\\ """:
                return 'Error'      # needs more editing
            else:
                alphabet[char] += 1
        return alphabet
    
    def enoughLetters(self, letterCombo):
        ''' Checks if dictionary word can be made by the give hand '''
        if '$' in letterCombo:
            return False
        letterHandAlphabet = self.mkAlphabet(self.letters)
        letterComboAlphabet = self.mkAlphabet(letterCombo)
        for letter in letterHandAlphabet.keys():
            if letterComboAlphabet[letter] > letterHandAlphabet[letter]:
                return False
        return True

    def comboValid(self, letters, spaces, board, occupied, dictionary, combos):
        for combo in combos:
            possibleWord = ''   # this is where the check really starts!
            for spot in combo:
                if spot in spaces:
                    possibleWord += letters[spaces.index(spot)]
                else:
                    possibleWord += board[spot]
            if possibleWord.lower() not in dictionary:
                message = 'This combo is not a word: ' + possibleWord
                return (False, message)
        return (True, '')

    def comboWorks(self, letters, spaces, board, occupied, attachments, dictionary):
        if self.enoughLetters(letters):
            message = 'Your hand supports the letters you chose.'
            if noSpaceAlreadyOccupied(spaces, occupied):
                message = 'The spaces you chose were not occupied.'
                lineCheck = lineConnected(spaces, occupied, attachments)
                if lineCheck[0]:
                    message = 'The letters are connected.'
                    if attached(spaces, occupied, attachments)[0]:
                        message = 'Letters are attached to the current situation.'
                        combos = getAllCombos(spaces, occupied, lineCheck[1])
                        validCombo = self.comboValid(letters, spaces, board, occupied, dictionary, combos)
                        if validCombo[0]:
                            message = 'The combo follows all of the rules.'
                            return (True, combos, message)
                        else:
                            message = validCombo[1]
                    else:
                        message = 'Letters are not attached to the current situation.'
                else:
                    message = lineCheck[1]
            else:
                message = 'At least one of the spaces you chose was occupied. Try again.'
        else:
            message = 'Your hand does not support the letters you chose. Try again.'

        return (False, [], message)
