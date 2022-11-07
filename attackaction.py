import pygame
import random
import worldcreate as wc


# this function will find the enemies that is in range of the player.
def calculate_melee(location, attackrange, occupiedlist):
    attackable_list = []
    for i in occupiedlist:
        if abs(i[0] - location[0]) + abs(i[1] - location[1]) <= attackrange:
            if i != location:
                attackable_list.append(i)
    return attackable_list


def drawattack(screen, worldnum, landcol, watercol, locx, locy, attack_list):
    worldarray = wc.read(worldnum)
    for x in attack_list:
        if worldarray[x[1]][x[0]] == "#":
            pygame.Surface.blit(screen, landcol, [locx(x[0])+1, locy(x[1])+1])
        elif worldarray[x[1]][x[0]] == "_":
            pygame.Surface.blit(screen, watercol, [locx(x[0])+1, locy(x[1])+1])


# needed to define certain information about an attack. Is not pygame sprite as no need to draw this class.
class Attack:
    def __init__(self, location, timer, damage, enemy_location):
        self.timer = timer  # this will determine when the attack will finish
        self.damage = damage  # determines the damage
        self.location = location  # the location of the attack on a tile.
        self.range = 1  # the range of which the attack will reach (eg: 1 square to 1 direction)
        self.origin = enemy_location  # this is to tie the attack to an enemy


def enemy_attack(worldnum, enemy_class, enemy_location, player_location, attack_timer, damage):
    worldarray = wc.read(worldnum)
    distance = abs(player_location[0] - enemy_location[0]) + abs(player_location[1] - enemy_location[1])
    y_direct = player_location[1] - enemy_location[1]
    x_direct = player_location[0] - enemy_location[0]
    if enemy_class == "BasicEnemy":
        if distance == 1:
            new_attack = Attack([player_location[0], player_location[1]], attack_timer, damage, enemy_location)
            return new_attack
        elif distance == 2:
            temporary_list = []
            final_list = []
            if 0 <= enemy_location[0] + 1 <= 8:
                temporary_list.append([enemy_location[0] + 1, enemy_location[1]])
            if 0 <= enemy_location[0] - 1 <= 8:
                temporary_list.append([enemy_location[0] - 1, enemy_location[1]])
            if 0 <= enemy_location[1] + 1 <= 8:
                temporary_list.append([enemy_location[0], enemy_location[1] + 1])
            if 0 <= enemy_location[1] - 1 <= 8:
                temporary_list.append([enemy_location[0], enemy_location[1] - 1])
            for element in temporary_list:
                if worldarray[element[1]][element[0]] != "^":
                    final_list.append(element)
            new_attack = Attack(random.choice(final_list), attack_timer, damage, enemy_location)
            return new_attack
    elif enemy_class == "RookEnemy":
        if distance == 1:
            attack_list = []
            not_hit_obstacle = True
            new_attack = Attack([player_location[0], player_location[1]], attack_timer, damage, enemy_location)
            attack_list.append(new_attack)
            if abs(x_direct) == 1:
                while not_hit_obstacle:
                    if 0 <= player_location[0] + x_direct <= 8:
                        if worldarray[player_location[1]][player_location[0] + x_direct] != "^":
                            new_attack = Attack([player_location[0] + x_direct, player_location[1]], attack_timer, damage, enemy_location)
                            attack_list.append(new_attack)
                            if x_direct < 0:
                                x_direct -= 1
                            else:
                                x_direct += 1
                        else:
                            not_hit_obstacle = False
                    else:
                        not_hit_obstacle = False
                return attack_list
            else:
                while not_hit_obstacle:
                    if 0 <= player_location[1] + y_direct <= 8:
                        if worldarray[player_location[1] + y_direct][player_location[0]] != "^":
                            new_attack = Attack([player_location[0], player_location[1] + y_direct], attack_timer, damage, enemy_location)
                            attack_list.append(new_attack)
                            if y_direct < 0:
                                y_direct -= 1
                            else:
                                y_direct += 1
                        else:
                            not_hit_obstacle = False
                    else:
                        not_hit_obstacle = False
                return attack_list
        else:
            direction = random.choice([-1, 1])
            axis = random.choice([0, 1])
            if player_location[0] - enemy_location[0] == 0:
                dist = enemy_location[1] - player_location[1]
                if dist < 0:
                    for i in range(abs(dist)):
                        if worldarray[player_location[1] - i][player_location[0]] == "^":
                            direction = random.choice([-1, 1])
                            axis = random.choice([0, 1])
                            break
                        else:
                            direction = 1
                            axis = 1
                else:
                    for i in range(dist):
                        if worldarray[player_location[1] + i][player_location[0]] == "^":
                            direction = random.choice([-1, 1])
                            axis = random.choice([0, 1])
                            break
                        else:
                            direction = -1
                            axis = 1
            if player_location[1] - enemy_location[1] == 0:
                dist = enemy_location[0] - player_location[0]
                if dist < 0:
                    for i in range(abs(dist)):
                        if worldarray[player_location[1]][player_location[0] - i] == "^":
                            direction = random.choice([-1, 1])
                            axis = random.choice([0, 1])
                            break
                        else:
                            direction = 1
                            axis = 0
                else:
                    for i in range(dist):
                        if worldarray[player_location[1]][player_location[0] + i] == "^":
                            direction = random.choice([-1, 1])
                            axis = random.choice([0, 1])
                            break
                        else:
                            direction = -1
                            axis = 0

            attack_list = []
            not_hit_obstacle = True
            x_direct = enemy_location[0]
            y_direct = enemy_location[1]
            if axis == 0:
                while not_hit_obstacle:
                    x_direct += direction
                    if 0 <= x_direct <= 8:
                        if worldarray[y_direct][x_direct] != "^":
                            new_attack = Attack([x_direct, y_direct], attack_timer, damage, enemy_location)
                            attack_list.append(new_attack)
                        else:
                            not_hit_obstacle = False
                    else:
                        not_hit_obstacle = False
                return attack_list
            else:
                while not_hit_obstacle:
                    y_direct += direction
                    if 0 <= y_direct <= 8:
                        if worldarray[y_direct][x_direct] != "^":
                            new_attack = Attack([x_direct, y_direct], attack_timer, damage, enemy_location)
                            attack_list.append(new_attack)
                        else:
                            not_hit_obstacle = False
                    else:
                        not_hit_obstacle = False
                return attack_list


