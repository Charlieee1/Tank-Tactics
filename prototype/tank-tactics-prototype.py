from time import sleep, time
import threading
import random

random.seed(time())

try:
    with open("Pygame 2d Renderer.py") as f:
        exec(f.read())
    renderThings = True
except:
    print("No rendering engine available! Proceeding without it.")
    renderThings = False

playerCount = int(input("Players? "))
playersLeft = playerCount
actions = [5 for i in range(playerCount)]
health = [3 for i in range(playerCount)]
ranges = [2 for i in range(playerCount)]
names = [input("Player name {}? ".format(str(i+1))) for i in range(playerCount)]
mapWidth = int(input("Map Width? "))
mapHeight = int(input("Map Height? "))
positions = [(random.randint(1, mapWidth), random.randint(1, mapHeight)) for i in range(playerCount)]
for i in range(playerCount):
    print("Position of {}: {}".format(names[i], str(positions[i])))
status = ["ALIVE" for i in range(playerCount)]
endOfGame = False


class threadClass(threading.Thread):
    def __init__(self, threadID):
        threading.Thread.__init__(self)
        self.threadID = threadID
    def run(self):
        updatePoints()

# Used to be give one random player an action point every 10 seconds
# Now it's give every player an action point every minute
def updatePoints():
    global actions
    global endOfGame
    while not endOfGame:
        for i in range(playerCount):
            update = i
            #update = random.randint(0, playerCount - 1)
            if status[update] == "ALIVE":
                actions[update] = actions[update] + 1
                #print("Gifted 1 action point to {}.".format(names[update]))
        sleep(30)

def printInfoForPlayer(playerName):
    player = names.index(playerName)
    print("Player info for {}:".format(playerName))
    print("Status: {}".format(status[player]))
    print("HP: {}".format(str(health[player])))
    print("Action points left: {}".format(str(actions[player])))
    print("Range: {}".format(str(ranges[player])))
    print("Position: {}".format(str(positions[player])))

def distance(pos1, pos2):
    return max(abs(pos1[0]-pos2[0]),abs(pos1[1]-pos2[1]))

def getRecForPlayer(player):
    pos=fromNormalizedCoords(((positions[player][0]-1)/mapWidth,(positions[player][1]-1)/mapHeight))
    return objectClass(type="Rec",pos=(pos[0]+2,pos[1]+2),width=screen_width/mapWidth-2,height=screen_height/mapHeight-2,colour=(255,255,0))if status[player]=="ALIVE"else objectClass(type="None")

def updateRenderedPlayerPosition(player):
    renderedObjects[-1][player] = getRecForPlayer(player)

thread = threadClass(0)
thread.start()

if renderThings:
    # Add vertical lines for the grid
    for i in range(-1, mapWidth):
        renderedObjects.append(objectClass(type="Line",pos1=fromNormalizedCoords(((i+1)/mapWidth,0)),pos2=fromNormalizedCoords(((i+1)/mapWidth,1)),thickness=2,colour=(50,50,50)))

    # Add horizontal lines for the grid
    for i in range(-1, mapHeight):
        renderedObjects.append(objectClass(type="Line",pos1=fromNormalizedCoords((0,(i+1)/mapHeight)),pos2=fromNormalizedCoords((1,(i+1)/mapHeight)),thickness=2,colour=(50,50,50)))
    renderedObjects.append([])
    for i in range(playerCount):
        renderedObjects[-1].append(getRecForPlayer(i))

print("Valid commands:")
print("exit: stop the game")
print("view <player name>: view a player's stats")
print("move <player name> <posX> <posY>: move a player")
print("donate <player name> <player name> <amount>: donate some action points to another player")
print("upgrade <player name> <amount>: upgrade your range")
print("attack <player name> <player name> <damage>: attack another player")

while playersLeft > 0:
    command = input("> ").split()
    if command[0] == "exit":
        break
    if command[0] == "view":
        try:
            if command[1] == "all":
                print("Printing all player's info.")
                print("There are {} players left".format(str(playersLeft)))
                for name in names:
                    printInfoForPlayer(name)
                continue
            printInfoForPlayer(command[1])
        except:
            print("view <player name>: view a player's stats")
    elif command[0] == "move":
        try:
            player = names.index(command[1])
            if actions[player] == 0:
                print("Unable to move {}! The player has no action points left!".format(command[1]))
                continue
            coords = (int(command[2]), int(command[3]))
            if coords[0] < 1 or coords[0] > mapWidth or coords[1] < 1 or coords[1] > mapHeight:
                print("Invalid coordinates! Please input coordinates within the map.")
                continue
            if distance(coords, positions[player]) > 1:
                print("You cannot move that far! You are currently at {}".format(str(positions[player])))
                continue
            positions[player] = coords
            actions[player] = actions[player] - 1
            updateRenderedPlayerPosition(player)
            print("You have moved to {}".format(str(coords)))
        except:
            print("move <player name> <posX> <posY>: move a player")
    elif command[0] == "donate":
        try:
            player1 = names.index(command[1])
            player2 = names.index(command[2])
            amount = int(command[3])
            if distance(positions[player1], positions[player2]) > ranges[player1]:
                print("You are too far to donate! Come within {} square{} of each other to donate action points.".format(str(ranges[player]), "s"if ranges[player] > 1 else ""))
                continue
            if actions[player1] < amount:
                print("You don't have that many actions!")
                continue
            actions[player1] = actions[player1] - amount
            actions[player2] = actions[player2] + amount
            print("You have donated {} action point{} to {}".format(command[3], "s"if amount>1 else"", command[2]))
        except:
            print("donate <player name> <player name> <amount>: donate some action points to another player")
    elif command[0] == "upgrade":
        try:
            player = names.index(command[1])
            amount = int(command[2])
            if amount > actions[player]:
                print("You don't have enough action points! You need {} action points.".format(str(amount)))
                continue
            ranges[player] = ranges[player] + amount
            actions[player] = actions[player] - amount
        except:
            print("upgrade <player name> <amount>: upgrade your range")
    elif command[0] == "attack":
        try:
            player1 = names.index(command[1])
            player2 = names.index(command[2])
            if distance(positions[player1], positions[player2]) > ranges[player1]:
                print("You are too far to attack! Come within {} square{} of someone else to attack them.".format(str(ranges[player]), "s"if ranges[player] > 1 else ""))
                continue
            cost = int(command[3])# * distance(positions[player1], positions[player2])
            if cost > actions[player1]:
                print("You do not have enough action points to attack! You need {} action points.".format(str(cost)))
                continue
            health[player2] = max(health[player2] - int(command[3]), 0)
            actions[player1] = actions[player1] - cost
            if health[player2] == 0:
                print("You killed {}!".format(command[2]))
                status[player2] = "DEAD"
                updateRenderedPlayerPosition(player2)
                playersLeft = playersLeft - 1
                if playersLeft == 1:
                    break
        except:
            print("attack <player name> <player name> <damage>: attack another player")

endOfGame = True
print("Game ended!")
if playersLeft == 1:
    print("{} Won!".format(names[health.index(max(health))]))
