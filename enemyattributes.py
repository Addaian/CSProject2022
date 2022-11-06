import pygame
import random
import worldcreate as wc
import main as mn
import playerattributes as pa
import os
import math as m


class BasicEnemy(pygame.sprite.Sprite):
    def __init__(self, worldnum, occupied_list, player_location):
        super().__init__()
        # this inherits __init__ (from pygame)'s pre-programmed functions
        self.locationarray = [0, 0]
        self.name = "Red Blit"
        # declare image and get the rect associated with it. Fill with colour gray.
        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()
        self.image.fill(mn.RED)
        # spawn the enemy in the world, at a random location on the map.
        self.spawn(worldnum, occupied_list, player_location)
        # all attributes associated with the player character
        self.movementspeed = 2
        self.health = random.randint(3, 5)
        self.attack = random.randint(1, 2)
        self.awareness_radius = 4  # determines the distance at which the enemy will become aware of the player.
        self.attack_timer = 1

    def updatelocation(self, locx, locy):
        self.locationarray[0] = locx
        self.locationarray[1] = locy

    def findbestpath(self, worldnum, movementdist, location, finallocation, prevnode, occ_list):
        # using same algorithm as in playerattributes.py.
        listofcoords = []
        if movementdist != -1:
            movementdist -= 1
            worldarray = wc.read(worldnum)  # [y] [x]
            if 0 <= location[0] <= 8 and 0 <= location[1] <= 8:
                listofcoords.append(location)
                if abs(location[0] - finallocation[0]) == 1 and location[1] == finallocation[1]:
                    listofcoords.append(finallocation)
                    return listofcoords
                if abs(location[1] - finallocation[1]) == 1 and location[0] == finallocation[0]:
                    listofcoords.append(finallocation)
                    return listofcoords
                if location == finallocation:  # saying, if the location is found, just return the location
                    return [location]
                if 0 <= location[1] + 1 <= 8 and [location[0], location[1] + 1] not in prevnode:
                    if [location[0], location[1] + 1] not in occ_list:  # if the next part is not in the occupied list:
                        if worldarray[location[1] + 1][location[0]] == "^":
                            None
                        elif worldarray[location[1] + 1][location[0]] == "#":
                            listofcoords.extend(
                                self.findbestpath(worldnum, movementdist, [location[0], location[1] + 1], finallocation,
                                                  listofcoords, occ_list))
                            if listofcoords[-1] == finallocation:
                                # saying, if the last element is the final loc, keep returning it.
                                listofcoords = [x for x in listofcoords if x]
                                return listofcoords
                        elif [location[0], location[1] + 1] == finallocation:
                            listofcoords.append(finallocation)
                            return listofcoords

                if 0 <= location[1] - 1 <= 8 and [location[0], location[1] - 1] not in prevnode:
                    if [location[0], location[1] - 1] not in occ_list:
                        if worldarray[location[1] - 1][location[0]] == "^":
                            None
                        elif worldarray[location[1] - 1][location[0]] != "_":
                            listofcoords.extend(
                                self.findbestpath(worldnum, movementdist, [location[0], location[1] - 1], finallocation,
                                                  listofcoords, occ_list))
                            if listofcoords[-1] == finallocation:
                                listofcoords = [x for x in listofcoords if x]
                                return listofcoords
                        elif [location[0], location[1] - 1] == finallocation:
                            listofcoords.append(finallocation)
                            return listofcoords

                if 0 <= location[0] + 1 <= 8 and [location[0] + 1, location[1]] not in prevnode:
                    if [location[0] + 1, location[1]] not in occ_list:
                        if worldarray[location[1]][location[0] + 1] == "^":
                            None
                        elif worldarray[location[1]][location[0] + 1] != "_":
                            listofcoords.extend(
                                self.findbestpath(worldnum, movementdist, [location[0] + 1, location[1]], finallocation,
                                                  listofcoords, occ_list))
                            if listofcoords[-1] == finallocation:
                                listofcoords = [x for x in listofcoords if x]
                                return listofcoords
                        elif [location[0] + 1, location[1]] == finallocation:
                            listofcoords.append(finallocation)
                            return listofcoords

                if 0 <= location[0] - 1 <= 8 and [location[0] - 1, location[1]] not in prevnode:
                    if [location[0] - 1, location[1]] not in occ_list:
                        if worldarray[location[1]][location[0] - 1] == "^":
                            None
                        elif worldarray[location[1]][location[0] - 1] != "_":
                            listofcoords.extend(
                                self.findbestpath(worldnum, movementdist, [location[0] - 1, location[1]], finallocation,
                                                  listofcoords, occ_list))
                            if listofcoords[-1] == finallocation:
                                listofcoords = [x for x in listofcoords if x]
                                return listofcoords
                        elif [location[0] - 1, location[1]] == finallocation:
                            listofcoords.append(finallocation)
                            return listofcoords
            else:
                return []  # returns blanks if not between 0 and 8
        return []  # returns blanks if no more movement distance.

    # this function will pick a random location that is a land tile, and spawn the enemy on it.
    def spawn(self, worldnum, occupied_list, player_location):
        worldarray = wc.read(worldnum)
        x_length = len(worldarray[0]) - 2  # need to subtract 2 because of the \n at the end of each list
        y_length = len(worldarray) - 1  # number of lists, -1. 9 lists, need 9 - 1 = 8 to iterate.
        done = False
        while not done:
            final_x = random.randint(0, x_length)
            final_y = random.randint(0, y_length)
            if worldarray[final_y][final_x] == "#":
                if [final_x, final_y] not in occupied_list:
                    if abs(final_x - player_location[0]) + abs(final_y - player_location[1]) > 3:
                        done = True
        self.updatelocation(final_x, final_y)


class RookEnemy(BasicEnemy):
    def __init__(self, worldnum, occupied_list, player_location):
        super().__init__(worldnum, occupied_list, player_location)
        self.awareness_radius = 100
        self.name = "Orange Blit"
        self.attack = random.randint(2, 3)
        self.health = random.randint(2, 3)
        self.image.fill(mn.LIGHT_ORANGE)



def drawhealth(screen, font, health_value):
    screen.blit(font.render("Health: ", False, mn.WHITE), [920, 145])
    for i in range(health_value):
        pygame.draw.rect(screen, mn.WHITE, [1010 + i * 15, 150, 10, 22])


def drawattack(screen, font, attack_value):
    screen.blit(font.render("Attack: ", False, mn.WHITE), [920, 175])
    for i in range(attack_value):
        pygame.draw.rect(screen, mn.RED, [1010 + i * 15, 180, 10, 22])
