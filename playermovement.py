import pygame
import random
import math as m
import main as mn
import worldcreate as wc
import itertools


# this function pops out all coordinates on the map, that the player can possibly move to, in a list datatype
def calculatelandmoveable(worldnum, movementdist,
                          location):  # takes in movement speed of the enemy / player object, and takes the
    # location of the enemy / player object.
    listofcoords = []
    '''
    This algorithm uses the movement speed to generate a circle around the player equivalent to the movementdist / speed.
    it also checks for possible paths to potential destinations through recursion. 
    This algorithm can be subject to room size (purely by changing the number 9 in the if statements). 
    
    To simulate obstacles, the algorithm can plug in worldcreate's read function to check if the coordinate is an
    obstacle tile. If it is, the coordinate in question will be removed. 
    
    The beautiful thing about perfect borderless circles is that every space is reachable irregardless of 1 obstacle in
    the context of a traversal path; however, when encountering more than 1, we have to employ recursion. We can check, 
    from the players' location, 1 square each iteration away, until we reach max movement distance. 
    
    The same can be said about water tiles; however, it is much simpler to program. When you reach a water tile, the 
    player can no longer move further. This means when a water tile is reached, recursion stops, and the coordinate is 
    inputted into a separate list.
    
    To expand on this algorithm, see drawmove() below. 
    '''

    '''
    PREVIOUS CODE
    for i in range(-movementdist, movementdist + 1):
        if 0 <= location[0] + i <= 8:
            for x in range(movementdist - abs(i) + 1):
                if 0 <= location[1] - x <= 8:
                    if wc.read(worldnum)[location[1] - x][location[0] + i] == "#":
                        listofcoords.append([location[0] + i, location[1] - x])

                if 0 < location[1] + x <= 8:
                    if wc.read(worldnum)[location[1] + x][location[0] + i] == "#":
                        listofcoords.append([location[0] + i, location[1] + x])
    # after finding all coordinates that the player can possibly land on that is land, we can find all inaccessible
    # tiles from our tile.'''

    if movementdist != -1:
        movementdist -= 1
        worldarray = wc.read(worldnum)  # [y] [x]
        if 0 <= location[0] <= 8 and 0 <= location[1] <= 8:
            if worldarray[location[1]][location[0]] == "#":
                listofcoords.extend([location])
            if 0 <= location[1] + 1 <= 8:
                if worldarray[location[1] + 1][location[0]] == "#":
                    listofcoords.extend(calculatelandmoveable(worldnum, movementdist, [location[0], location[1] + 1]))
            if 0 <= location[1] - 1 <= 8:
                if worldarray[location[1] - 1][location[0]] == "#":
                    listofcoords.extend(calculatelandmoveable(worldnum, movementdist, [location[0], location[1] - 1]))
            if 0 <= location[0] + 1 <= 8:
                if worldarray[location[1]][location[0] + 1] == "#":
                    listofcoords.extend(calculatelandmoveable(worldnum, movementdist, [location[0] + 1, location[1]]))
            if 0 <= location[0] - 1 <= 8:
                if worldarray[location[1]][location[0] - 1] == "#":
                    listofcoords.extend(calculatelandmoveable(worldnum, movementdist, [location[0] - 1, location[1]]))
    if listofcoords == []:
        return []
    listofcoords = [x for x in listofcoords if x]
    new_list = []

    for l in listofcoords:
        if l not in new_list:
            new_list.append(l)
    return new_list


def calculatewatermoveable(worldnum, movementdist, location):
    listofcoords = []
    if movementdist != -1:
        movementdist -= 1
        worldarray = wc.read(worldnum)  # [y] [x]
        if 0 <= location[0] <= 8 and 0 <= location[1] <= 8:
            if 0 <= location[1] + 1 <= 8:
                if worldarray[location[1] + 1][location[0]] == "#":
                    listofcoords.extend(calculatewatermoveable(worldnum, movementdist, [location[0], location[1] + 1]))
                elif worldarray[location[1] + 1][location[0]] == "_" and movementdist != -1:
                    listofcoords.append([location[0], location[1] + 1])

            if 0 <= location[1] - 1 <= 8:
                if worldarray[location[1] - 1][location[0]] == "#":
                    listofcoords.extend(calculatewatermoveable(worldnum, movementdist, [location[0], location[1] - 1]))
                elif worldarray[location[1] - 1][location[0]] == "_" and movementdist != -1:
                    listofcoords.append([location[0], location[1] - 1])

            if 0 <= location[0] + 1 <= 8:
                if worldarray[location[1]][location[0] + 1] == "#":
                    listofcoords.extend(calculatewatermoveable(worldnum, movementdist, [location[0] + 1, location[1]]))
                elif worldarray[location[1]][location[0] + 1] == "_" and movementdist != -1:
                    listofcoords.append([location[0] + 1, location[1]])

            if 0 <= location[0] - 1 <= 8:
                if worldarray[location[1]][location[0] - 1] == "#":
                    listofcoords.extend(calculatewatermoveable(worldnum, movementdist, [location[0] - 1, location[1]]))
                elif worldarray[location[1]][location[0] - 1] == "_" and movementdist != -1:
                    listofcoords.append([location[0] - 1, location[1]])

            if worldarray[location[1]][location[0]] == "_":
                listofcoords.append(location)
    if listofcoords == []:
        return []

    listofcoords = [x for x in listofcoords if x]
    new_list = []

    for l in listofcoords:
        if l not in new_list:
            new_list.append(l)
    return new_list


def drawlandmove(screen, currentcolor, locx, locy, levelblocksize, listoflandcoords):
    for x in listoflandcoords:
        pygame.draw.rect(screen, currentcolor, [locx(x[0]), locy(x[1]), levelblocksize, levelblocksize])
        pygame.draw.rect(screen, mn.BLACK, [locx(x[0]), locy(x[1]), levelblocksize, levelblocksize], 1, 1)


def drawwatermove(screen, currentcolor, locx, locy, levelblocksize, listofwatercoords):
    for x in listofwatercoords:
        pygame.draw.rect(screen, currentcolor, [locx(x[0]), locy(x[1]), levelblocksize, levelblocksize])
        pygame.draw.rect(screen, mn.BLACK, [locx(x[0]), locy(x[1]), levelblocksize, levelblocksize], 1, 1)
