class boardKeeper():

    def __init__(self):
        row1  = "---------------"
        row2  = "---------------"
        row3  = "---------------"
        row4  = "---------------"
        row5  = "---------------"
        row6  = "---------------"
        row7  = "---------------"
        row8  = "---------------"
        row9  = "---------------"
        row10 = "---------------"
        row11 = "---------------"
        row12 = "---------------"
        row13 = "---------------"
        row14 = "---------------"
        row15 = "---------------"
        self.board = row1 + row2 + row3 + row4 + row5 + row6 + row7 + row8 + row9 + row10 + row11 + row12 + row13 + row14 + row15

    def changeBoard(self, letterCombo, spaceCombo):
        for (letter, space) in zip(letterCombo, spaceCombo):
            self.board = self.board[:space] + letter + self.board[space+1:]

    def printBoard(self):
        ''' Prints the board with either an error or a passing statement '''
        board = self.board
        print('Here is the current board situation.')
        for row in range( int(len(board)//15) ):
            # print(row, end = ' ')  ## for future extension
            for column in range(15):
                print(board[15*row + column], end = ' ')
            print('')

    def refreshOccupied(self):
        ''' Get locations occupied by a letter '''
        board = self.board
        occupied = []
        for spot in range(len(board)):
            if board[spot] not in '-23@#':
                occupied.append(spot)
        return occupied

    def refreshAttachments(self):
        ''' Finds every place where a word could start (called attachments) given a board '''
        board = self.board
        attachments = set([])

        for i in range(len(board)):
            if board[i] not in '-23@#':
                row = i//15
                column = i%15
                # space directions
                down = (row-1)*15 + column
                up = (row+1)*15 + column
                left = row*15 + column-1
                right = row*15 + column+1
                
                # attachments are added
                if (row != 0) and (board[down] in '-23@#') and (down not in attachments):
                    attachments.add(down)
                if (row != 14) and (board[up] in '-23@#') and (up not in attachments):
                    attachments.add(up)
                if (column != 0) and (board[left] in '-23@#') and (left not in attachments):
                    attachments.add(left)
                if (column != 14) and (board[right] in '-23@#') and (right not in attachments):
                    attachments.add(right)

        if len(attachments) == 0:
            attachments.add(112)
        
        return attachments
