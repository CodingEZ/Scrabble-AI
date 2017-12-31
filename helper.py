def areValidLetters(letters):
    for letter in letters:
        if len(letter) != 1 and (letter not in 'qwertyuiopasdfghjklzxcvbnm'):
            return False
    return True

def areValidLocations(spaces):
    for space in spaces:
        try:
            location = int(space)
        except ValueError:
            return False
    return True

def binarySearch(target, elements):
    left = 0
    right = len(elements)

    if right == 0:
        return False

    middle = 1
    while (left + 1 != right):
        middle = (left + right + 1) // 2
        if target < elements[middle]:
            right = middle
        elif target > elements[middle]:
            left = middle
        else:
            return True

    if target == elements[left]:
        return True
    else:
        return False

    print(low, middle, high)
