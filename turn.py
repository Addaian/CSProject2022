import pygame
import random
import worldcreate as wc
import main as mn
import playerattributes as pa
import os
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
