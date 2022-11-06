import os

import pygame

import main as mn
import worldcreate as wc


class PlayerClass(pygame.sprite.Sprite):
    def __init__(self, worldnum):
        super().__init__()
        # this inherits __init__ (from pygame)'s pre-programmed functions
        self.locationarray = [0, 0]
        # declare image and get the rect associated with it. Fill with colour light orange (temporary).
        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()
        self.image.fill(mn.BLACK)
        # spawn the player in the world, at the entrance of the room.
        self.spawn(worldnum)

        # all attributes associated with the player character
        self.movementspeed = 2  # the max number of traversable spaces a character may travel at once.
        self.health = 4  # the health value of a character
        self.attack = 2  # the damage a character may deal in one cycle
        self.reach = 2  # the attack reach a character has

    ###
    def updatelocation(self, locx, locy):
        # using this function, we can take the current location of the player and the location of the final location,
        # then we can animate the player to that location.
        self.locationarray[0] = locx
        self.locationarray[1] = locy
        # we must find the optimal path to the location in question. therefore, we must use recursion.

    def findbestpath(self, worldnum, movementdist, location, finallocation, prevnode, occ_list):
        # we can also use this function to draw arrows during player movement.
        listofcoords = []
        # using recursion, we can find a list of coords from the original location to the end
        # point and append all locations between those points
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

    ###

    def updatemovementspeed(self, newspeed):
        self.movementspeed = newspeed

    # This function will spawn the player at the "entrance" of the room, typically towards the bottom of the room.
    # If an obstacle or a water block is encountered on the desired spawn block, replace the block with a land block.
    def spawn(self, worldnum):
        self.locationarray = [int((len(wc.read(worldnum)) - 1) // 2), len(wc.read(worldnum)) - 1]
        if wc.read(worldnum)[len(wc.read(worldnum)) - 1][int((len(wc.read(worldnum)) - 1) // 2)] != "#":
            if os.path.exists("levels/level" + str(worldnum)):
                # using the OS module we can check first if the level we want to delete exists first, then delete
                with open("levels/level" + str(worldnum), 'r') as infile:  # opens a file as "read"
                    oldworldlist = infile.readlines()  # reads the file, stores a 2D list
                with open("levels/level" + str(worldnum),
                          'w+') as outfile:  # opens the same file again as write, in replace mode
                    newworldlist = oldworldlist[len(oldworldlist) - 1]
                    newworldlist = list(newworldlist)
                    newworldlist[
                        (len(newworldlist) - 2) // 2] = "#"  # find the middle element in list, replace with "#"
                    oldworldlist[len(oldworldlist) - 1] = "".join(newworldlist)
                    for i in oldworldlist:  # append back into world array
                        outfile.write(i)


def drawhealth(screen, font, health_value):
    screen.blit(font.render("Health:", False, mn.WHITE), [3, 145])
    for i in range(health_value):
        pygame.draw.rect(screen, mn.WHITE, [93 + i * 15, 150, 10, 22])


def drawattack(screen, font, attack_value):
    screen.blit(font.render("Attack: ", False, mn.WHITE), [3, 175])
    for i in range(attack_value):
        pygame.draw.rect(screen, mn.RED, [93 + i * 15, 180, 10, 22])
