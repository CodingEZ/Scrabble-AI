class player():

    def __init__(self):
        self.points = 0
        self.letterHand = ''

    def addPoints(self, addedPoints):
        self.points += addedPoints

    def addToHand(self, letters):
        self.letterHand += letters

    def playFromHand(self, letters):
        for letter in letters:
            index = self.letterHand.find(letter)
            self.letterHand = self.letterHand[:index] + self.letterHand[index+1:]
