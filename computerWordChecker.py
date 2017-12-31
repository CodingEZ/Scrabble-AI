import itertools
import computerRuleChecker as CRC
import helper

class computerWordChecker():

    def changeLetterHand(self, letters):
        self.letters = letters
    
    def getLetterCombos(self):
        ''' Find all permutations of a string of any possible length and returns a set '''
        letters = self.letters
        letterCombos = []
        for length in range(1, len(letters)+1):
            listTuples = list( itertools.permutations(list(letters), length) )
            letterCombos.append( set(listTuples) )
        return letterCombos        # this is a list of sets

    def getSpaceCombos(self, board, occupied, attachments):
        ''' Get all of the spatial combinations relatively efficiently '''
        letters = self.letters

        spaceCombos = []
        
        for length in range(1, len(letters)+1):
            rows = []
            columns = []
            
            for spot in range(len(board)):
                if spot not in occupied:
                    # if spot is occupied, go to next spot
                    row = spot//15
                    column = spot%15 + 1    # first spot is already considered
                    spaceCount = 1
                    spaceCombo = [spot]     # first spot is already considered
                    while spaceCount != length:
                        # while the specified number of letters have not been played
                        if column != 15:
                            # when the column is not outside of the board
                            if (row*15 + column) not in occupied:
                                # if spot is occupied, move to next column
                                spaceCount += 1
                                spaceCombo.append(row*15 + column)
                            column += 1     # move to next column no matter if column is or is not occupied
                        else:
                            spaceCount = length     # makes escape when number of letters is NOT satisfied
                    if len(spaceCombo) == length and CRC.conformsBetterRules(spaceCombo, attachments):
                                # second part of if statement checks if the combo attaches to the current board
                        rows.append(spaceCombo)     # does not append in the escape case

            if length != 1:
                # combinations of length one should only be considered as rows
                for spot in range(len(board)):
                    if spot not in occupied:
                        row = spot//15 + 1
                        column = spot%15
                        spaceCount = 1
                        spaceCombo = [spot]
                        while spaceCount != length:
                            if row != 15:
                                if (row*15 + column) not in occupied:
                                    spaceCount += 1
                                    spaceCombo.append(row*15 + column)
                                row += 1
                            else:
                                spaceCount = length
                        if len(spaceCombo) == length and CRC.conformsBetterRules(spaceCombo, attachments):
                            columns.append(spaceCombo)

            spaceCombos.append([rows, columns])      # row words first, column words second

        return spaceCombos

    def comboWorks(self, letterCombo, spaceCombo, board, occupied, dictionary, isRowCombo):
        self.allCombos = CRC.getAllCombos(spaceCombo, occupied, isRowCombo)
        for combo in self.allCombos:
            possibleWord = ''   # this is where the check really starts!
            for spot in combo:
                if spot in spaceCombo:
                    possibleWord += letterCombo[spaceCombo.index(spot)]
                else:
                    possibleWord += board[spot]
            if possibleWord.lower() not in dictionary:
                return False
        return True
        
    def getDirectedCombos(self, board, occupied, attachments, dictionary):
        allLetterCombos = self.getLetterCombos()
        allSpaceCombos = self.getSpaceCombos(board, occupied, attachments)

        workingCombos = []
        for (letterCombos, spaceCombos) in zip(allLetterCombos, allSpaceCombos):
            for letterCombo in letterCombos:
                for spaceCombo in spaceCombos[0]:
                    # row combos dealt with first
                    if self.comboWorks(letterCombo, spaceCombo, board, occupied, dictionary, True):
                        workingCombos.append([letterCombo, spaceCombo, self.allCombos])
                for spaceCombo in spaceCombos[1]:
                    # column combos dealt with second
                    if self.comboWorks(letterCombo, spaceCombo, board, occupied, dictionary, False):
                        workingCombos.append([letterCombo, spaceCombo, self.allCombos])

        return workingCombos
