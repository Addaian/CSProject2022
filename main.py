import glob
import itertools
import math as m
import time as t
import random

import pygame

import attackaction as aa
import enemyattributes as ea
import enemymovement as em
import playerattributes as pa
import playermovement as pm
import turn as tb
import worldcreate as wc

pygame.init()
pygame.font.init()

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 69, 0)
LIME = (0, 255, 0)
BLUE = (65, 105, 225)
LIGHT_ORANGE = (253, 173, 92)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

clock = pygame.time.Clock()

FPS = 60  # used for color wheel cycles and generally determines the FPS of the screen.
step = 0
switch_color_direction = False

# level block size, and calculating the block locations on the screen per stage
levelblocksize = 60

# we need both land and water as we need to cycle through the colors in the game loop.

attack_land_color = pygame.Surface([levelblocksize - 1, levelblocksize - 1])
attack_land_color.fill(RED)

attack_water_color = pygame.Surface([levelblocksize - 1, levelblocksize - 1])
attack_water_color.fill(RED)

current_land_color = pygame.Surface([levelblocksize - 1, levelblocksize - 1])
current_land_color.fill(YELLOW)

current_water_color = pygame.Surface([levelblocksize - 1, levelblocksize - 1])
current_water_color.fill(YELLOW)


def blockloc_x(var_x):
    return (var_x * levelblocksize) + (screen.get_width() - levelblocksize * 9) / 2


def blockloc_y(var_y):
    return (var_y * levelblocksize) + (screen.get_height() - levelblocksize * 9) / 2


# global variables
worldnum = 0  # world number - the unique identifier of a world in a floor.
difficulty = 2  # difficulty - 1 - easy, 2 - medium, 3 - hard, 4 - ironmode (1 health cap)
draw_move_speed = 10  # drawn 2 px at a time. This is for objects that are animated through the tiles.
occ_list = []  # this list is used to notate all tiles that are currently occupied or cannot be moved to.
attack_list = []  # this list is used to notate a tile that is about to be attacked.

has_drawn_splash = False  # this bool will ask every start of turn if the splash indicator has been drawn.
draw_splash_alpha = 256

# additional info: the tile will finish being attacked before the next enemy movement. Other attacks will have a longer time to finish.


# global functions
#  duplicate code functions

def remove_redundancy(listofcoords):
    temporaryvar = -1  # -1, as we want the while loop to loop at least once.
    temporarystart = 0
    while temporarystart < len(
            listofcoords) - 2:  # this while loop will loop the array and find out if there are redundant paths.
        if len(listofcoords) != 0:
            for z1 in range(temporarystart + 2, len(listofcoords)):  # finds out the next redundant
                if abs(listofcoords[temporarystart][0] - listofcoords[z1][0]) == 1 and listofcoords[temporarystart][
                    1] == listofcoords[z1][1]:
                    temporaryvar = z1
                elif abs(listofcoords[temporarystart][1] - listofcoords[z1][1]) == 1 and listofcoords[temporarystart][
                    0] == listofcoords[z1][0]:
                    temporaryvar = z1
            if temporaryvar > 0:
                listofcoords = listofcoords[:temporarystart + 1] + listofcoords[temporaryvar:]
                temporaryvar = -1
            temporarystart += 1
    return listofcoords


def find_mouse_location(dimension):
    if dimension == "x":
        return int((pygame.mouse.get_pos()[0] - (screen.get_width() - levelblocksize * 9) / 2) // levelblocksize)
    elif dimension == "y":
        return int((pygame.mouse.get_pos()[1] - (screen.get_height() - levelblocksize * 9) / 2) // levelblocksize)
    else:
        return 0


def draw_rect_alpha(surface, color, rect):  # this function will draw a transparent rectangle.
    shape_surf = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(shape_surf, color, shape_surf.get_rect())
    surface.blit(shape_surf, rect)


# fonts
detsans_normal = pygame.font.Font("fonts/detsans.ttf", 30)
detsans_large = pygame.font.Font("fonts/detsans.ttf", 60)
detsans_super_large = pygame.font.Font("fonts/detsans.ttf", 120)

if __name__ == '__main__':
    # globals
    # deploy random seed, and create first world
    random.seed()
    wc.create()
    worldnum += 1

    # display
    # Set the height and width of the screen
    screen = pygame.display.set_mode([1280, 720], pygame.RESIZABLE)

    # set the window title and the icon of the screen
    pygame.display.set_caption('Unnamed Dungeon Crawler')

    # sprites groups
    all_sprites_list = pygame.sprite.Group()
    enemylist = []
    # declare and add player to the sprites list
    player = pa.PlayerClass(worldnum)

    occ_list.append(player.locationarray)  # the space the player is on is now unavailable for future spawns and moves.

    # using this for loop, spawn an initial 5 enemies into first world.
    for i in range(int(m.ceil(difficulty * 3.5))):
        enemy_instance = ea.BasicEnemy(worldnum, occ_list)
        occ_list.append(enemy_instance.locationarray)  # this space is now unavailable for future moves.
        enemylist.append(enemy_instance)  # used to update all enemies
        all_sprites_list.add(enemy_instance)

    all_sprites_list.add(player)  # used to draw both player and enemy at the end of the loop.

    skip_button = pygame.image.load("images/skip_button.png")
    skip_button.convert()  # button sprite.

    land_tile = pygame.image.load("images/land_tile.jpg")

    water_tile = pygame.image.load("images/water_tile.jpg")

    wall_tile = pygame.image.load("images/wall_tile.jpg")

    # movement variables
    player_completedmove = True
    player_move_draw_list = []
    tempaddx = 0
    tempaddy = 0

    enemy_completedmove = True
    enemy_event_list = []
    enemy_tempaddx = 0
    enemy_tempaddy = 0

    # declaring the first instance of current land and water movables. updates throughout the loop.
    occ_list.remove(player.locationarray)
    current_land_movable = pm.calculatelandmovable(worldnum, player.movementspeed, player.locationarray, occ_list)
    current_water_movable = pm.calculatewatermovable(worldnum, player.movementspeed, player.locationarray, occ_list)
    occ_list.append(player.locationarray)
    current_in_range = aa.calculate_melee(player.locationarray, player.reach, occ_list)

    done = False

    while not done:

        screen.fill(BLACK)

        # temporary level block list (will increase automatically later)
        levelblocklist = wc.read(worldnum)

        '''INPUTS THAT ARE ACHIEVED'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # had an issue with running the game before implementing this
                for i in range(1, len(glob.glob('levels/*')) + 1):
                    wc.remove(i)
                done = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and tb.turntitle[
                    (tb.turnnumber - 1) % 4] == "Player Movement" and player_completedmove:
                    if pygame.Rect.collidepoint(skip_button.get_rect(topleft=[790, 635]), pygame.mouse.get_pos()):
                        tb.skipturn()
                        has_drawn_splash = False
                        break
                    pos_x = find_mouse_location("x")
                    pos_y = find_mouse_location("y")
                    if 0 <= pos_x <= 8 and 0 <= pos_y <= 8:
                        if [pos_x, pos_y] in current_land_movable or [pos_x, pos_y] in current_water_movable:
                            player_completedmove = False
                            occ_list.remove(player.locationarray)
                            player_move_draw_list = player.findbestpath(worldnum, player.movementspeed,
                                                                        player.locationarray, [pos_x, pos_y], [],
                                                                        occ_list)
                            occ_list.append(player.locationarray)
                            # extra - first updates the draw_list for redundant moves
                            player_move_draw_list = remove_redundancy(player_move_draw_list)
                            occ_list[occ_list.index(player.locationarray)] = [pos_x, pos_y]
                            # then hops over to move animation if statement.

                if event.button == 1 and tb.turntitle[
                    (tb.turnnumber - 1) % 4] == "Player Attack" and player_completedmove:
                    if pygame.Rect.collidepoint(skip_button.get_rect(topleft=[790, 635]), pygame.mouse.get_pos()):
                        tb.skipturn()
                        has_drawn_splash = False
                        break
                    pos_x = find_mouse_location("x")
                    pos_y = find_mouse_location("y")
                    if [pos_x, pos_y] in current_in_range:
                        for enemy in enemylist:
                            if enemy.locationarray == [pos_x, pos_y]:
                                enemy.health -= player.attack
                            if enemy.health < 1:
                                enemylist.remove(enemy)
                                all_sprites_list.remove(enemy)
                                occ_list.remove(enemy.locationarray)
                                del enemy
                        tb.turnend(True)
                        has_drawn_splash = False
                        aa.calculate_melee(player.locationarray, player.reach, occ_list)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    tb.turnend(True)
                    has_drawn_splash = False

        # blit all the squares on the level
        for y in range(len(levelblocklist)):
            for x in range(len(levelblocklist)):
                if levelblocklist[y][x] == "#":
                    pygame.Surface.blit(screen, land_tile, [blockloc_x(x), blockloc_y(y)])
                elif levelblocklist[y][x] == "_":
                    pygame.Surface.blit(screen, water_tile, [blockloc_x(x), blockloc_y(y)])
                else:
                    pygame.Surface.blit(screen, wall_tile, [blockloc_x(x), blockloc_y(y)])

        # enemy movement for loop
        if tb.turntitle[(tb.turnnumber - 1) % 4] == "Enemy Movement" and enemy_completedmove:
            while len(attack_list) != 0:
                if attack_list[0].location == player.locationarray:
                    player.health -= attack_list[0].damage
                attack_list.pop()
            enemy_event_list = []  # this list will be iterated and animated.
            for enemy in enemylist:
                enemy_movable_list = []  # this list will have all possible moves for the enemy to choose from.
                occ_list.remove(enemy.locationarray)
                enemy_movable_list.extend(
                    em.calculatelandmovable(worldnum, enemy.movementspeed, enemy.locationarray, occ_list))
                enemy_movable_list.extend(
                    em.calculatewatermovable(worldnum, enemy.movementspeed, enemy.locationarray, occ_list))
                occ_list.append(enemy.locationarray)
                best_move = em.findbestmove(enemy.awareness_radius, player.locationarray, enemy.locationarray,
                                            enemy_movable_list, occ_list)
                # after finding all final locations of all enemies on screen, we can find the best path of all moves.

                occ_list.remove(enemy.locationarray)
                best_path = enemy.findbestpath(worldnum, enemy.movementspeed, enemy.locationarray, best_move, [],
                                               occ_list)
                occ_list.append(enemy.locationarray)

                enemy_event_list.append(best_path)
                occ_list[occ_list.index(enemy.locationarray)] = best_move
            enemy_completedmove = False

        if tb.turntitle[(tb.turnnumber - 1) % 4] == "Enemy Attack" and enemy_completedmove:
            if len(enemylist) > 0:
                for enemy in enemylist:
                    attack_instance = aa.enemy_attack(worldnum, attack_list, enemy.locationarray, player.locationarray,
                                                      enemy.attack_timer, enemy.attack)
                    if attack_instance is not None:
                        attack_list.append(attack_instance)
            tb.turnend(True)

        # update the colours of highlighted moves
        if not switch_color_direction:
            step += 4
        else:
            step -= 4
        if 256 > step > 0:
            # (y-x)/number_of_steps calculates the amount of change per step required to
            # fade one channel of the old color to the new color
            # We multiply it with the current step counter
            current_land_color.set_alpha(256 - step)
            current_water_color.set_alpha(256 - step)
            attack_land_color.set_alpha(256 - step)
            attack_water_color.set_alpha(256 - step)
        else:
            if switch_color_direction:
                switch_color_direction = False
            else:
                switch_color_direction = True

        # update player sprite
        player.rect.x = player.locationarray[0] * levelblocksize + (screen.get_width() - levelblocksize * 9) / 2 + (
                (levelblocksize - 20) / 2) + tempaddx
        player.rect.y = player.locationarray[1] * levelblocksize + (screen.get_height() - levelblocksize * 9) / 2 + (
                (levelblocksize - 20) / 2) + tempaddy

        # update enemy sprites
        for i in range(len(enemylist)):
            enemylist[i].rect.x = enemylist[i].locationarray[0] * levelblocksize + (
                        screen.get_width() - levelblocksize * 9) / 2 + (
                                          (levelblocksize - 20) / 2)
            if i == len(enemylist) - len(enemy_event_list):
                enemylist[i].rect.x += enemy_tempaddx
            enemylist[i].rect.y = enemylist[i].locationarray[1] * levelblocksize + (
                        screen.get_height() - levelblocksize * 9) / 2 + (
                                          (levelblocksize - 20) / 2)
            if i == len(enemylist) - len(enemy_event_list):
                enemylist[i].rect.y += enemy_tempaddy

        # this if statement will animate the player from one location to another.
        if not player_completedmove:
            if player_move_draw_list[0] == player.locationarray:
                player_move_draw_list.pop(0)
                if len(player_move_draw_list) == 0:
                    player_completedmove = True  # tell the program the animation is completed.

                    # here, the new attacks are calculated for player.
                    current_in_range = aa.calculate_melee(player.locationarray, player.reach, occ_list)

                    # end the turn.
                    tb.turnend(True)
                    has_drawn_splash = False
            else:
                pos_x = player_move_draw_list[0][0]
                pos_y = player_move_draw_list[0][1]
                if player.locationarray[0] != pos_x:
                    if player.locationarray[0] - pos_x > 0:
                        tempaddx -= draw_move_speed
                    else:
                        tempaddx += draw_move_speed
                    if player.rect.x == pos_x * levelblocksize + (screen.get_width() - levelblocksize * 9) / 2 + (
                            (levelblocksize - 20) / 2):
                        player.locationarray[0] = pos_x
                        tempaddx = 0
                if player.locationarray[1] != pos_y:
                    if player.locationarray[1] - pos_y > 0:
                        tempaddy -= draw_move_speed
                    else:
                        tempaddy += draw_move_speed
                    if player.rect.y == pos_y * levelblocksize + (screen.get_height() - levelblocksize * 9) / 2 + (
                            (levelblocksize - 20) / 2):
                        player.locationarray[1] = pos_y
                        tempaddy = 0

        # this if statement will animate all enemies from one location to another.
        if not enemy_completedmove:
            if len(enemylist) != 0:
                enemy_move_draw_list = enemy_event_list[0]
                current_enemy = enemylist[len(enemylist) - len(enemy_event_list)]
                if enemy_move_draw_list[0] == current_enemy.locationarray:
                    enemy_move_draw_list.pop(0)
                    if len(enemy_move_draw_list) == 0:
                        enemy_event_list.pop(0)
                        if len(enemy_event_list) == 0:
                            enemy_completedmove = True  # tell the program the animation is completed.

                            # here, the new attacks are calculated for player.
                            current_in_range = aa.calculate_melee(player.locationarray, player.reach, occ_list)

                            # new movables are calculated for player.
                            occ_list.remove(player.locationarray)
                            current_land_movable = pm.calculatelandmovable(worldnum, player.movementspeed,
                                                                           player.locationarray, occ_list)
                            current_water_movable = pm.calculatewatermovable(worldnum, player.movementspeed,
                                                                             player.locationarray, occ_list)
                            occ_list.append(player.locationarray)

                            # finally, end the turn.
                            tb.turnend(True)
                            has_drawn_splash = False
                else:
                    pos_x = enemy_move_draw_list[0][0]
                    pos_y = enemy_move_draw_list[0][1]
                    if current_enemy.locationarray[0] != pos_x:
                        if current_enemy.locationarray[0] - pos_x > 0:
                            enemy_tempaddx -= draw_move_speed
                        else:
                            enemy_tempaddx += draw_move_speed
                        if current_enemy.rect.x == pos_x * levelblocksize + (
                                screen.get_width() - levelblocksize * 9) / 2 + (
                                (levelblocksize - 20) / 2):
                            current_enemy.locationarray[0] = pos_x
                            enemy_tempaddx = 0
                    if current_enemy.locationarray[1] != pos_y:
                        if current_enemy.locationarray[1] - pos_y > 0:
                            enemy_tempaddy -= draw_move_speed
                        else:
                            enemy_tempaddy += draw_move_speed
                        if current_enemy.rect.y == pos_y * levelblocksize + (
                                screen.get_height() - levelblocksize * 9) / 2 + (
                                (levelblocksize - 20) / 2):
                            current_enemy.locationarray[1] = pos_y
                            enemy_tempaddy = 0
            else:
                enemy_completedmove = True  # tell the program the animation is completed.

                # here, the new attacks are calculated for player.
                current_in_range = aa.calculate_melee(player.locationarray, player.reach, occ_list)

                # new movables are calculated for player.
                occ_list.remove(player.locationarray)
                current_land_movable = pm.calculatelandmovable(worldnum, player.movementspeed,
                                                               player.locationarray, occ_list)
                current_water_movable = pm.calculatewatermovable(worldnum, player.movementspeed,
                                                                 player.locationarray, occ_list)
                occ_list.append(player.locationarray)

                # finally, end the turn.
                tb.turnend(True)
                has_drawn_splash = False

        # print all sprites on the list
        screen.blit(detsans_normal.render("Turn Number: " + str(m.ceil(tb.turnnumber / 4)), False, WHITE), [10, 10])

        screen.blit(detsans_normal.render(str(tb.turntitle[(tb.turnnumber - 1) % 4]), False, WHITE), [10, 40])

        if tb.turntitle[(tb.turnnumber - 1) % 4] == "Player Movement":
            screen.blit(skip_button, [790, 635])
            if player_completedmove:
                pm.drawlandmove(screen, current_land_color, blockloc_x, blockloc_y, current_land_movable)
                pm.drawwatermove(screen, current_water_color, blockloc_x, blockloc_y, current_water_movable)

        if tb.turntitle[(tb.turnnumber - 1) % 4] == "Player Attack":
            screen.blit(skip_button, [790, 635])
            aa.drawattack(screen, worldnum, attack_land_color, attack_water_color, blockloc_x, blockloc_y, current_in_range)

        all_sprites_list.draw(screen)

        # a loop that detects if the mouse is hovering on an enemy instance.
        # if yes, then draw the attributes of enemy on right side of screen
        for enemy in enemylist:
            if enemy.rect.collidepoint(pygame.mouse.get_pos()):
                screen.blit(detsans_large.render("Red Blit", False, WHITE), [920, 80])
                for attack in attack_list:
                    if attack.origin == enemy.locationarray:
                        screen.blit(detsans_normal.render("Attacking: " + str(attack.location), False, WHITE),
                                    [920, 210])
                ea.drawhealth(screen, detsans_normal, enemy.health)
                ea.drawattack(screen, detsans_normal, enemy.attack)

        # a loop that detects if the mouse is hovering on the player.
        # if yes, then draw the attributes of player on left side of screen
        if player.rect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(detsans_large.render("Player", False, WHITE), [180, 80])
            pa.drawhealth(screen, detsans_normal, player.health)
            pa.drawattack(screen, detsans_normal, player.attack)

        # a loop that detects if there are any impending enemy attacks.
        # if yes, then draw the attack transparently.
        if len(attack_list) > 0:
            for attack in attack_list:
                draw_rect_alpha(screen, (255, 69, 0, 127), (
                blockloc_x(attack.location[0]) + 1, blockloc_y(attack.location[1]) + 1, levelblocksize - 1, levelblocksize - 1))

        # a loop that detects if the mouse is hovering over the map.
        # if yes, then draw the type on bottom of screen
        for y in range(len(levelblocklist)):
            for x in range(len(levelblocklist)):
                block_surface = pygame.Surface([levelblocksize, levelblocksize])
                if pygame.Rect.collidepoint(block_surface.get_rect(topleft=[blockloc_x(x), blockloc_y(y)]),
                                            pygame.mouse.get_pos()):
                    if levelblocklist[y][x] == "#":
                        screen.blit(detsans_normal.render("Land", False, WHITE), [372, 630])
                    elif levelblocklist[y][x] == "_":
                        screen.blit(detsans_normal.render("Water", False, WHITE), [372, 630])
                    else:
                        screen.blit(detsans_normal.render("Wall", False, WHITE), [372, 630])

        # this block of code will make the splash text at the start of every turn fade out.
        turn_change_splash_text = detsans_super_large.render(str(tb.turntitle[(tb.turnnumber - 1) % 4]), False, WHITE)
        surf_splash_screen = pygame.Surface(turn_change_splash_text.get_rect().size)
        surf_splash_screen.set_colorkey((1, 1, 1))
        surf_splash_screen.fill((1, 1, 1))
        surf_splash_screen.blit(turn_change_splash_text, (0, 0))

        # blit at the end so that it will supercede all other surfaces
        if not has_drawn_splash:
            draw_splash_alpha = (draw_splash_alpha - 4)
            surf_splash_screen.set_alpha(draw_splash_alpha)
            screen.blit(surf_splash_screen, ((screen.get_width() - surf_splash_screen.get_width()) / 2, (screen.get_height() - surf_splash_screen.get_height()) / 2))
            if draw_splash_alpha == 0:
                draw_splash_alpha = 256
                has_drawn_splash = True

        # DEBUG DEBUG DEBUG
        screen.blit(detsans_normal.render("Player coord: " + str(player.locationarray), False, WHITE), [20, 620])
        screen.blit(detsans_normal.render("X coord: " + str(pygame.mouse.get_pos()[0]), False, WHITE), [20, 650])
        screen.blit(detsans_normal.render("Y coord: " + str(pygame.mouse.get_pos()[1]), False, WHITE), [20, 680])
        # update the screen.
        pygame.display.flip()
        # Limit to 60 frames per second
        clock.tick(60)

pygame.quit()
