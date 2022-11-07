
def turnend(boolean):
    global turnnumber
    if boolean:
        turnnumber += 1

def skipturn():
    global turnnumber
    turnnumber += 1


turnnumber = 1
turntitle = ["Player Movement", "Player Attack", "Enemy Movement", "Enemy Attack"]
