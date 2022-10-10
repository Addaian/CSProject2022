import pygame
import random
import worldcreate as wc
import main as mn
import os
import math as m


# this function will find the enemies that is in range of the player.
def calculate_melee(location, moverange, occupiedlist):
    attackable_list = []
    for i in occupiedlist:
        if abs(i[0] - location[0]) + abs(i[1] - location[1]) <= moverange:
            if i != location:
                attackable_list.append(i)
    print(attackable_list, "a_list")
    return attackable_list


def drawattack(screen, worldnum, landcol, watercol, locx, locy, attack_list):
    worldarray = wc.read(worldnum)
    for x in attack_list:
        if worldarray[x[1]][x[0]] == "#":
            pygame.draw.rect(screen, landcol, [locx(x[0]), locy(x[1]), mn.levelblocksize, mn.levelblocksize])
            pygame.draw.rect(screen, mn.BLACK, [locx(x[0]), locy(x[1]), mn.levelblocksize, mn.levelblocksize], 1, 1)
        elif worldarray[x[1]][x[0]] == "_":
            pygame.draw.rect(screen, watercol, [locx(x[0]), locy(x[1]), mn.levelblocksize, mn.levelblocksize])
            pygame.draw.rect(screen, mn.BLACK, [locx(x[0]), locy(x[1]), mn.levelblocksize, mn.levelblocksize], 1, 1)
