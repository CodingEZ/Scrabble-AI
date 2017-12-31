import random

class letterBag():

    def __init__(self):
        letterDict = {'A' : 9, 'B' : 2, 'C' : 2, 'D' : 3, 'E' : 12, 'F' : 2, 'G' : 3, 'H' : 2,
                      'I' : 9, 'J' : 1, 'K' : 1, 'L' : 4, 'M' : 2, 'N' : 6, 'O' : 8, 'P' : 2,
                      'Q' : 1, 'R' : 6, 'S' : 4, 'T' : 6, 'U' : 3, 'V' : 2, 'W' : 2, 'X' : 1,
                      'Y' : 2, 'Z' : 1}
        self.letterBag = []
        for key in letterDict.keys():
            for _ in range(letterDict[key]):
                self.letterBag.append(key)

    def removeLetters(self, num):
        removedLetters = ''
        if num < len(self.letterBag):
            for _ in range(num):
                x = random.random()
                index = int(x*len(self.letterBag) // 1)
                removedLetters += self.letterBag[index]
                self.letterBag.pop(index)
        else:
            for letter in self.letterBag:
                removedLetters += letter
            self.letterBag = []
        return removedLetters
            
