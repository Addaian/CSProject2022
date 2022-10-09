import pygame
import random
import worldcreate as wc
import main as mn
import playerattributes as pa
import os
import math as m
class EnemyClass(pygame.sprite.Sprite):
    def __init__(self, worldnum, occupied_list):
        super().__init__()
        # this inherits __init__ (from pygame)'s pre-programmed functions
        self.locationarray = [0, 0]
        # declare image and get the rect associated with it. Fill with colour gray.
        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()
        self.image.fill(mn.RED)
        # spawn the enemy in the world, at a random location on the map.
        self.spawn(worldnum, occupied_list)
        # all attributes associated with the player character
        self.movementspeed = 2
        self.health = 3
        self.attack = 2

    def updatelocation(self, locx, locy):
        self.locationarray[0] = locx
        self.locationarray[1] = locy

    # this function will pick a random location that is a land tile, and spawn the enemy on it.
    def spawn(self, worldnum, occupied_list):
        worldarray = wc.read(worldnum)
        x_length = len(worldarray[0]) - 2  # need to subtract 2 because of the \n at the end of each list
        y_length = len(worldarray) - 1  # number of lists, -1. 9 lists, need 9 - 1 = 8 to iterate.
        done = False
        while not done:
            final_x = random.randint(0, x_length)
            final_y = random.randint(0, y_length)
            if worldarray[final_y][final_x] == "#":
                if [final_x, final_y] not in occupied_list:
                    done = True
        self.updatelocation(final_x, final_y)
