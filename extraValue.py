tripleWord = [0, 7, 14, 105, 119, 210, 217, 224]
doubleWord = [16, 28, 32, 42, 48, 56, 64, 70, 154, 160, 168, 176, 182, 192, 196, 208]
doubleLetter = [3, 11, 36, 38, 45, 52, 59, 92, 96, 98, 102, 108, 116, 122, 126, 128, 132, 165, 172, 179, 186, 188, 213, 221]
tripleLetter = [20, 24, 76, 80, 84, 88, 136, 140, 144, 148, 200, 204]

dictionary = {'A': 1, 'B': 3, 'C': 3, 'D': 2, 'E': 1, 'F': 4, 'G': 2,
                  'H': 4, 'I': 1, 'J': 8, 'K': 5, 'L': 1, 'M': 3, 'N': 1,
                  'O': 1, 'P': 3, 'Q': 10, 'R': 1, 'S': 1, 'T': 1, 'U': 1,
                  'V': 4, 'W': 4, 'X': 8, 'Y': 4, 'Z': 10}

def calcWordValue(combo, letterDict, board):
    wordValue = 0
    timesDouble = 0
    timesTriple = 0
    
    for spot in combo:
        if spot in doubleWord:
            timesDouble += 1
        elif spot in tripleWord:
            timesTriple += 1
        if spot in doubleLetter:
            if spot in letterDict.keys():
                wordValue += 2 * dictionary[letterDict[spot]]
            else:
                wordValue += 2 * dictionary[board[spot]]
        elif spot in tripleLetter:
            if spot in letterDict.keys():
                wordValue += 3 * dictionary[letterDict[spot]]
            else:
                wordValue += 3 * dictionary[board[spot]]
        else:
            if spot in letterDict.keys():
                wordValue += dictionary[letterDict[spot]]
            else:
                wordValue += dictionary[board[spot]]
                
    return wordValue * (2**timesDouble) * (3**timesTriple)

def maxComboValue(workingCombos, board):
    maxCombo = [-1, [], []]
    maxLocations = []
    for workingCombo in workingCombos:
        letterDict = {}
        for (letter, space) in zip(workingCombo[0], workingCombo[1]):
            letterDict[space] = letter
        comboValue = 0
        for combo in workingCombo[2]:
            # add value of every combo to the total comboValue
            comboValue += calcWordValue(combo, letterDict, board)
        if len(workingCombo[1]) == 7:
            # add 50 to any combo that uses all seven letters in hand
            comboValue += 50
        if comboValue > maxCombo[0]:
            maxCombo = [comboValue, workingCombo[0], workingCombo[1]]
            maxLocations = workingCombo[1]
    for location in maxLocations:
        if location in tripleWord:
            tripleWord.remove(location)
        elif location in doubleWord:
            doubleWord.remove(location)
        elif location in doubleLetter:
            doubleLetter.remove(location)
        elif location in tripleLetter:
            tripleLetter.remove(location)
    return maxCombo
