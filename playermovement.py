import pygame
import random
import math as m
import main as mn
import worldcreate as wc
import itertools


# this function pops out all coordinates on the map, that the player can possibly move to, in a list datatype
def calculatelandmovable(worldnum, movementdist, location, oclist):  # takes in movement speed of the enemy / player object, and takes the
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
    worldarray = wc.read(worldnum)  # [y] [x]
    if movementdist != -1:
        movementdist -= 1
        if 0 <= location[0] <= 8 and 0 <= location[1] <= 8:
            if location not in oclist:
                if worldarray[location[1]][location[0]] == "#":
                    listofcoords.extend([location])
                if 0 <= location[1] + 1 <= 8:
                    if worldarray[location[1] + 1][location[0]] == "#":
                        listofcoords.extend(calculatelandmovable(worldnum, movementdist, [location[0], location[1] + 1], oclist))
                if 0 <= location[1] - 1 <= 8:
                    if worldarray[location[1] - 1][location[0]] == "#":
                        listofcoords.extend(calculatelandmovable(worldnum, movementdist, [location[0], location[1] - 1], oclist))
                if 0 <= location[0] + 1 <= 8:
                    if worldarray[location[1]][location[0] + 1] == "#":
                        listofcoords.extend(calculatelandmovable(worldnum, movementdist, [location[0] + 1, location[1]], oclist))
                if 0 <= location[0] - 1 <= 8:
                    if worldarray[location[1]][location[0] - 1] == "#":
                        listofcoords.extend(calculatelandmovable(worldnum, movementdist, [location[0] - 1, location[1]], oclist))
    if not listofcoords:
        return []
    listofcoords = [x for x in listofcoords if x]
    new_list = []

    for l in listofcoords:
        if l not in new_list:
            new_list.append(l)
    return new_list


def calculatewatermovable(worldnum, movementdist, location, oclist):
    listofcoords = []
    worldarray = wc.read(worldnum)  # [y] [x]
    if movementdist != -1:
        movementdist -= 1
        if 0 <= location[0] <= 8 and 0 <= location[1] <= 8:
            if location not in oclist:
                if 0 <= location[1] + 1 <= 8:
                    if worldarray[location[1] + 1][location[0]] == "#":
                        listofcoords.extend(calculatewatermovable(worldnum, movementdist, [location[0], location[1] + 1], oclist))
                    elif worldarray[location[1] + 1][location[0]] == "_" and movementdist != -1:
                        if [location[0], location[1] + 1] not in oclist:
                            listofcoords.append([location[0], location[1] + 1])

                if 0 <= location[1] - 1 <= 8:
                    if worldarray[location[1] - 1][location[0]] == "#":
                        listofcoords.extend(calculatewatermovable(worldnum, movementdist, [location[0], location[1] - 1], oclist))
                    elif worldarray[location[1] - 1][location[0]] == "_" and movementdist != -1:
                        if [location[0], location[1] - 1] not in oclist:
                            listofcoords.append([location[0], location[1] - 1])

                if 0 <= location[0] + 1 <= 8:
                    if worldarray[location[1]][location[0] + 1] == "#":
                        listofcoords.extend(calculatewatermovable(worldnum, movementdist, [location[0] + 1, location[1]], oclist))
                    elif worldarray[location[1]][location[0] + 1] == "_" and movementdist != -1:
                        if [location[0] + 1, location[1]] not in oclist:
                            listofcoords.append([location[0] + 1, location[1]])

                if 0 <= location[0] - 1 <= 8:
                    if worldarray[location[1]][location[0] - 1] == "#":
                        listofcoords.extend(calculatewatermovable(worldnum, movementdist, [location[0] - 1, location[1]], oclist))
                    elif worldarray[location[1]][location[0] - 1] == "_" and movementdist != -1:
                        if [location[0] - 1, location[1]] not in oclist:
                            listofcoords.append([location[0] - 1, location[1]])

                if worldarray[location[1]][location[0]] == "_":
                    listofcoords.append(location)
    if not listofcoords:
        return []

    listofcoords = [x for x in listofcoords if x]
    new_list = []

    for l in listofcoords:
        if l not in new_list:
            new_list.append(l)
    return new_list


def drawlandmove(screen, color, locx, locy, listoflandcoords):
    for x in listoflandcoords:
        pygame.Surface.blit(screen, color, [locx(x[0]) + 1, locy(x[1]) + 1])


def drawwatermove(screen, color, locx, locy, listofwatercoords):
    for x in listofwatercoords:
        pygame.Surface.blit(screen, color, [locx(x[0]) + 1, locy(x[1]) + 1])
