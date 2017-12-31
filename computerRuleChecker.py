''' One-letter-placements are counted as rows '''

def conformsBetterRules(situation, attachments):
    for spot in situation:
        if spot in attachments:
            return True     # checks if any of the spots is an attachment location
    return False

def getMainCombo(isRowCombo, spot, occupied, situation):
    ''' Get the spots that correspond to the main combo in order '''
    locations = [spot]
    locator = spot
    if isRowCombo:
        while (((locator + 1) in occupied) or ((locator + 1) in situation)) and (locator%15 != 14):
            locator += 1
            locations.append(locator)
        locator = spot      # resets the locator to the original position
        while ((locator - 1) in occupied) and (locator%15 != 0):
            locator -= 1
            locations.insert(0, locator)
    else:
        while ((locator + 15) in occupied) or ((locator + 15) in situation):
            locator += 15
            locations.append(locator)
        locator = spot      # resets the locator to the original position
        while (locator - 15) in occupied:
            locator -= 15
            locations.insert(0, locator)
    return locations

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
            locations.insert(0, locator)
    else:
        while ((locator + 1) in occupied) and (locator%15 != 14):
            locator += 1
            locations.append(locator)
        locator = spot
        while ((locator - 1) in occupied) and (locator%15 != 0):
            locator -= 1
            locations.insert(0, locator)

    if locations == [spot]:
        return []
    return locations

def getAllCombos(situation, occupied, isRowCombo):
    ''' Gets combos of letters made by a valid placement for a computer '''
    combosMade = []
    mainCombo = getMainCombo(isRowCombo, situation[0], occupied, situation)
    if len(mainCombo) != 1:
        combosMade.append(mainCombo)
    # take note, the main combo comes first
    for spot in situation:
        sideCombo = getSideCombo(isRowCombo, spot, occupied)
        if sideCombo != []:
            combosMade.append(sideCombo)
    if len(combosMade) == 0:
        combosMade.append(mainCombo)    # for situations where a single letter is played by itself (for avoiding errors)
    return combosMade   # now all of these combos must be checked in the dictionary
