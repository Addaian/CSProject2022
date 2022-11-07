import glob
import os
import random as rd


def create():
    f = open("levels/level" + str(len(glob.glob('levels/*')) + 1), 'w')  # here I am creating a new file
    '''this can be automated to create a new level per function, using glob as an import
       in this case, glob is used to count the number of files in the levels subdirectory.'''

    # after creating a new file, I need to create a way to generate random levels
    '''
       Glossary:
       # == land
       _ == water
       ^ == obstacle
    '''
    landlevel = {1: "#", 2: "#", 3: "#", 4: "#", 5: "#", 6: "_", 7: "_", 8: "_", 9: "^"}
    for i in range(9):
        nlist = []
        rd.random()
        for x in range(9):
            nlist.append(landlevel[rd.randint(1, 9)])
        f.write("".join(nlist))
        f.write("\n")
    f.close()

    # so each floor will have a separate 2D array, and there would be an infinitely many set of floors for each run


def remove(level):
    if os.path.exists("levels/level" + str(level)):  # using the OS module we can check first if the level we want to
        # delete exists first, then delete
        os.remove("levels/level" + str(level))
    else:
        print("nope, world does not exist")


def read(levelnum):
    if os.path.exists("levels/level" + str(levelnum)):  # using the OS module we can check first if the level we want to
        # delete exists first, then delete
        with open("levels/level" + str(levelnum), 'r') as f:
            returnedval = f.readlines()  # returnedval is a list variable (2D)
        return returnedval  # already in a nested list / 2d list
    else:
        print("nope, world does not exist")

