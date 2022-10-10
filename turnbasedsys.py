import pygame
import random
import math as m


def turnend(bool):
    global turnnumber
    if bool:
        turnnumber += 1

def skipturn():
    global turnnumber
    turnnumber += 1

turnnumber = 1
turntitle = ["Player Movement", "Player Attack", "Enemy Movement", "Enemy Attack"]
