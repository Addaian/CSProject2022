import pygame
import random
import worldcreate as wc
import main as mn
import os
import math as m
class EnemyClass(pygame.sprite.Sprite):
    def __init__(self, worldnum):
        super().__init__()
        # this inherits __init__ (from pygame)'s pre-programmed functions
        self.locationarray = [0, 0]
        # declare image and get the rect associated with it. Fill with colour gray.
        self.image = pygame.Surface([20, 20])
        self.rect = self.image.get_rect()
        self.image.fill(mn.RED)
        # spawn the enemy in the world, at a random location on the map.
        self.spawn(worldnum)

        # all attributes associated with the player character
        self.movementspeed = 2
        self.health = 3
        self.attack = 2

    def updatelocation(self, locx, locy):
        self.locationarray[0] = locx
        self.locationarray[1] = locy
