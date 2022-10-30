import pygame
import random
import math as m
import main as mn
import worldcreate as wc
import itertools


# using the same logic as the function in playermovement.py , we can calculate the movable spots of an enemy.
def calculatelandmovable(worldnum, movementdist, location, oclist):
    listofcoords = []
    worldarray = wc.read(worldnum)  # [y] [x]
    if movementdist != -1:
        movementdist -= 1
        if 0 <= location[0] <= 8 and 0 <= location[1] <= 8:
            if location not in oclist:
                if worldarray[location[1]][location[0]] == "#":
                    listofcoords.extend([location])
                if 0 <= location[1] + 1 <= 8:
                    if worldarray[location[1] + 1][location[0]] == "#":
                        listofcoords.extend(
                            calculatelandmovable(worldnum, movementdist, [location[0], location[1] + 1], oclist))
                if 0 <= location[1] - 1 <= 8:
                    if worldarray[location[1] - 1][location[0]] == "#":
                        listofcoords.extend(
                            calculatelandmovable(worldnum, movementdist, [location[0], location[1] - 1], oclist))
                if 0 <= location[0] + 1 <= 8:
                    if worldarray[location[1]][location[0] + 1] == "#":
                        listofcoords.extend(
                            calculatelandmovable(worldnum, movementdist, [location[0] + 1, location[1]], oclist))
                if 0 <= location[0] - 1 <= 8:
                    if worldarray[location[1]][location[0] - 1] == "#":
                        listofcoords.extend(
                            calculatelandmovable(worldnum, movementdist, [location[0] - 1, location[1]], oclist))
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


# now, we can implement a basic AI system to find the shortest path to the player.
# this system will only activate if the enemy is within a certain distance of the player.
# else, it will move around randomly.

def findbestmove(awareness_radius, player_location, self_location, movable_list, occ_list):
    bestmove = self_location
    total_dist = abs(player_location[0] - self_location[0]) + abs(player_location[1] - self_location[1])
    if total_dist <= awareness_radius:
        shortest_path = total_dist
        # the following for loop will try to make the enemy move towards the player when in
        # a certain radius.
        for i in movable_list:
            if shortest_path > (abs(player_location[0] - i[0]) + abs(player_location[1] - i[1])):
                if i != player_location:
                    shortest_path = (abs(player_location[0] - i[0]) + abs(player_location[1] - i[1]))
                    bestmove = i
        # we can make this action a little less predictable and mundane by making it do so only 80% of the time.
        rand = random.randint(1, 10)
        if rand <= 2:
            bestmove = random.choice(movable_list)
            if bestmove in occ_list:
                while bestmove in occ_list:
                    bestmove = random.choice(movable_list)
        if rand == 3:  # for fun - might just stay still.
            bestmove = self_location
        return bestmove
    elif total_dist > awareness_radius:
        # just returns any value in movable list.
        bestmove = random.choice(movable_list)
        if bestmove in occ_list:
            while bestmove in occ_list:
                bestmove = random.choice(movable_list)
            if random.randint(1, 10) <= 2:
                bestmove = self_location  # again - for fun - just make the enemy stay still 20% of the time.
        return bestmove
