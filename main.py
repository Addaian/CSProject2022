import pygame
import random
import glob
import itertools
import worldcreate as wc
import turnbasedsys as tb
import playermovement as pm
import math as m
import playerattributes as pa

pygame.init()
pygame.font.init()

# colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 69, 0)
LIME = (0, 255, 0)
BLUE = (65, 105, 225)
LIGHTORANGE = (253, 173, 92)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)

clock = pygame.time.Clock()

# used for color wheel cycles
landmovecolors = itertools.cycle([GRAY, YELLOW])
watermovecolors = itertools.cycle([BLUE, YELLOW])

land_base_color = next(landmovecolors)
land_next_color = next(landmovecolors)
current_land_color = land_base_color

water_base_color = next(watermovecolors)
water_next_color = next(watermovecolors)
current_water_color = water_base_color

FPS = 60
change_every_x_seconds = 0.7
number_of_steps = change_every_x_seconds * FPS
step = 1

# global variables
worldnum = 0  # world number - the unique identifier of a world in a floor.
difficulty = 2  # difficulty - 1 - easy, 2 - medium, 3 - hard, 4 - ironmode (1 health cap)
draw_move_speed = 10  # drawn 2 px at a time. This is for objects that are animated through the tiles.

# fonts
detsans = pygame.font.Font("fonts/detsans.ttf", 30)

if __name__ == '__main__':
    # globals
    # deploy random seed, and create first world
    random.seed()
    wc.create()
    worldnum += 1

    # level block size, and calculating the block locations on the screen per stage
    levelblocksize = 60
    # temporary level block list (will increase automatically later)
    levelblocklist = wc.read(worldnum)


    def levelblockloc_x(x):
        return (x * levelblocksize) + (screen.get_width() - levelblocksize * 9) / 2


    def levelblockloc_y(y):
        return (y * levelblocksize) + (screen.get_height() - levelblocksize * 9) / 2


    # display
    # Set the height and width of the screen
    screen = pygame.display.set_mode([1280, 720], pygame.RESIZABLE)

    # set the window title and the icon of the screen
    pygame.display.set_caption('Unnamed Dungeon Crawler')

    # sprites groups
    all_sprites_list = pygame.sprite.Group()

    # declare and add player to the sprites list
    player = pa.PlayerClass(worldnum)
    all_sprites_list.add(player)

    # movement variables
    completedmovement = True
    tempaddx = 0
    tempaddy = 0
    current_land_movable = pm.calculatelandmoveable(worldnum, player.movementspeed, player.locationarray)
    current_water_movable = pm.calculatewatermoveable(worldnum, player.movementspeed, player.locationarray)

    done = False

    while not done:

        screen.fill(BLACK)

        '''INPUTS THAT ARE ACHIEVED'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # had an issue with running the game before implementing this
                for i in range(1, len(glob.glob('levels/*')) + 1):
                    wc.remove(i)
                done = True
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and tb.turntitle[(tb.turnnumber - 1) % 4] == "Player Movement" and completedmovement:
                    pos_x = int(
                        (pygame.mouse.get_pos()[0] - (screen.get_width() - levelblocksize * 9) / 2) // levelblocksize)
                    pos_y = int(
                        (pygame.mouse.get_pos()[1] - (screen.get_height() - levelblocksize * 9) / 2) // levelblocksize)
                    if (0 <= pos_x <= 8 and 0 <= pos_y <= 8) and [pos_x, pos_y] in current_land_movable or [pos_x,
                                                                                                          pos_y] in current_water_movable:
                        completedmovement = False
                        player_move_draw_list = player.findbestpath(worldnum, player.movementspeed,
                                                                    player.locationarray, [pos_x, pos_y], [])
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    tb.turnend(True)

        # blit all the squares on the level
        for y in range(len(levelblocklist)):
            for x in range(len(levelblocklist)):
                if levelblocklist[y][x] == "#":
                    pygame.draw.rect(screen, GRAY,
                                     [levelblockloc_x(x), levelblockloc_y(y), levelblocksize, levelblocksize])
                    pygame.draw.rect(screen, BLACK,
                                     [levelblockloc_x(x), levelblockloc_y(y), levelblocksize, levelblocksize], 1, 1)
                elif levelblocklist[y][x] == "_":
                    pygame.draw.rect(screen, BLUE,
                                     [levelblockloc_x(x), levelblockloc_y(y), levelblocksize, levelblocksize])
                    pygame.draw.rect(screen, BLACK,
                                     [levelblockloc_x(x), levelblockloc_y(y), levelblocksize, levelblocksize], 1, 1)
                else:
                    pygame.draw.rect(screen, BLACK,
                                     [levelblockloc_x(x), levelblockloc_y(y), levelblocksize, levelblocksize])

        # update the colours of highlighted moves
        step += 1
        if step < number_of_steps:
            # (y-x)/number_of_steps calculates the amount of change per step required to
            # fade one channel of the old color to the new color
            # We multiply it with the current step counter
            current_land_color = [x + (((y - x) / number_of_steps) * step) for x, y in
                                  zip(pygame.color.Color(land_base_color), pygame.color.Color(land_next_color))]
            current_water_color = [x + (((y - x) / number_of_steps) * step) for x, y in
                                   zip(pygame.color.Color(water_base_color), pygame.color.Color(water_next_color))]
        else:
            step = 0.5
            land_base_color = land_next_color
            land_next_color = next(landmovecolors)
            water_base_color = water_next_color
            water_next_color = next(watermovecolors)

        # update all sprites on the list
        player.rect.x = player.locationarray[0] * levelblocksize + (screen.get_width() - levelblocksize * 9) / 2 + (
                (levelblocksize - 20) / 2) + tempaddx
        player.rect.y = player.locationarray[1] * levelblocksize + (screen.get_height() - levelblocksize * 9) / 2 + (
                (levelblocksize - 20) / 2) + tempaddy

        # this if statement will animate the player from one location to another.
        if completedmovement == False:
            if player_move_draw_list[0] == player.locationarray:
                player_move_draw_list.pop(0)
                if len(player_move_draw_list) == 0:
                    completedmovement = True
                    tb.turnend(True)
                    current_land_movable = pm.calculatelandmoveable(worldnum, player.movementspeed, player.locationarray)
                    current_water_movable = pm.calculatewatermoveable(worldnum, player.movementspeed, player.locationarray)
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

        # print all sprites on the list
        screen.blit(detsans.render("Turn Number: " + str(m.ceil(tb.turnnumber / 4)), False, WHITE), [10, 10])

        screen.blit(detsans.render(str(tb.turntitle[(tb.turnnumber - 1) % 4]), False, WHITE), [10, 40])

        if tb.turntitle[(tb.turnnumber - 1) % 4] == "Player Movement" and completedmovement:
            pm.drawlandmove(screen, current_land_color, levelblockloc_x, levelblockloc_y, levelblocksize,
                            current_land_movable)
            pm.drawwatermove(screen, current_water_color, levelblockloc_x, levelblockloc_y, levelblocksize,
                             current_water_movable)
        pa.drawhealth(screen, detsans, player.health)

        all_sprites_list.draw(screen)

        # update the screen.
        pygame.display.flip()
        # Limit to 60 frames per second
        clock.tick(60)

pygame.quit()
