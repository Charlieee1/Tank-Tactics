#print("exit")

from time import sleep, time
import random
from filelock import FileLock
import sys
from hashlib import sha256

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

#sys.exit()

command = sys.argv[1].split(" ")
#print(command)

# If we don't do this, then there is no randomness involved
random.seed(time())

# Define helper functions for getting and setting little bits of data from files, among other things
# WARNING: Do not touch doFileModifs and setData ever again
# "If it works, don't fix it"
def doFileModifs(file_name, edits, data):
    with open("python server/" + file_name, 'r') as f:
        curr = f.readlines()
    lock = FileLock("python server/" + file_name+".lock")
    with lock:
        with open("python server/" + file_name, 'w') as f:
            edits(f, curr, data) # `edits` is a lambda function

def setData(file_name, id, data):
    # WARNING: Very Dangerous!
    # We cannot have the program crash while editing a file!
    def changeFileContents(f, arr, data):
        arr[data[0] + 1] = data[1] + "\n"
        f.writelines(arr)
    doFileModifs(file_name, changeFileContents, (id, data))

def addHistory(data):
    lock = FileLock("python server/player_history.lock")
    with lock:
        with open("python server/player_history", 'a') as f:
            f.write(data + "\n")

def getDatas(file_name):
    with open("python server/" + file_name, 'r') as f:
        datas = f.readlines()
    return datas[1:-1] # The last line is always empty, the first is a comment

def getData(file_name, id):
    with open("python server/" + file_name, 'r') as f:
        data = f.readlines()[id + 1] # First line is a comment
    if data == "":
        sys.exit()
    return data.strip()

def setPlayerData(file_name, player, data):
    # Make sure that the player being accessed is always valid
    # Check that the player id is valid
    # Probably redundant, as the player id is determined by the player name
    if player >= int(getData("global_data", 0).split(" ")[1]):
        sys.exit()
    setData(file_name, player, data)

# Useful
def distance(pos1, pos2):
    return max(abs(pos1[0]-pos2[0]),abs(pos1[1]-pos2[1]))

def encrypt(password):
    return sha256(password.encode()).hexdigest()

#move <player id> <player password> <posX> <posY>
if command[0] == "move":
    try:
        player = int(command[1])
        given_pass = command[2]
        if encrypt(given_pass) != getData("player_password_hashes", player).strip():
            print("invalid_input ::: Incorrect password! Someone is trying to move someone else... there will be punishments")
            sys.exit()
        player_name = getData("player_names", player)
        player_actions = int(getData("player_actions", player))
        mapWidth, mapHeight = map(int,getData("global_data", 2).split(" "))
        if player_actions == 0:
            print("invalid_input ::: Unable to move {}! The player has no action points left! They are trying to cheat the system... there will be punishments".format(player_name))
            sys.exit()
        coords = (int(command[3]), int(command[4]))
        if coords[0] < 1 or coords[0] > mapWidth or coords[1] < 1 or coords[1] > mapHeight:
            print("invalid_input ::: There are boundaries to the map, you know! Illegal movement detected! FBI on the way... there will be punishments")
            sys.exit()
        player_position = tuple(map(int,getData("player_positions", player).split(" ")))
        if distance(coords, player_position) > 1:
            print("invalid_input ::: {} cannot move that far! The player is currently at {} Somone is attempting teleportation magic... there will be punishments".format(player_name, ", ".join(map(str,player_position))))
            sys.exit()
        setPlayerData("Player_actions", player, str(player_actions - 1))
        setPlayerData("player_positions", player, " ".join(map(str,coords)))
        addHistory("move {} {}".format(player_name, ", ".join(map(str,coords))))
        print("data_update ::: move {} {} {}".format(str(player), str(coords[0]), str(coords[1])))
        print("data_update ::: actions {} {}".format(str(player), str(player_actions - 1)))
        print("exit")
        sys.exit()
    except:
        print("invalid_input ::: malformed input! Someone does not know how to send correct packets! Someone is attempting hacking... there will be punishments")
        sys.exit()
#donate <player id> <player password> <player2 id> <amount>
elif command[0] == "donate":
    try:
        player1 = int(command[1])
        given_pass = command[2]
        if encrypt(given_pass) != getData("player_password_hashes", player1):
            print("invalid_input ::: Incorrect password! Someone is trying to steal from someone else... there will be punishments")
            sys.exit()
        player2 = int(command[3])
        player1_name = getData("player_names", player1)
        player2_name = getData("player_names", player2)
        amount = int(command[4])
        player1_position = tuple(map(int,getData("player_positions", player1).split(" ")))
        player2_position = tuple(map(int,getData("player_positions", player2).split(" ")))
        player1_range = int(getData("player_ranges", player1))
        if distance(player1_position, player2_position) > player1_range:
            print("invalid_input ::: {} is unable to donate to {}! {}'s range is not large enough! They are trying to use reach hack... there will be punishments".format(player1_name, player2_name, player1_name))
            sys.exit()
        player1_actions = int(getData("player_actions", player1))
        if player1_actions < amount:
            print("invalid_input ::: {} is unable to donate to {}! The player does not have enough action points! They are trying to cheat the system... there will be punishments".format(player1_name, player2_name))
            sys.exit()
        player2_actions = int(getData("player_actions", player2))
        setPlayerData("player_actions", player1, str(player1_actions - amount))
        setPlayerData("player_actions", player2, str(player2_actions + amount))
        addHistory("donate {} {} {}".format(player1_name, player2_name, str(amount)))
        print("data_update ::: actions {} {}".format(str(player1), str(player1_actions - amount)))
        print("data_update ::: actions {} {}".format(str(player2), str(player2_actions + amount)))
        sys.exit()
    except:
        print("invalid_input ::: malformed input! Someone does not know how to send correct packets! Someone is attempting hacking... there will be punishments")
        sys.exit()
#upgrade <player id> <player password> <amount>
elif command[0] == "upgrade":
    try:
        player = int(command[1])
        given_pass = command[2]
        if encrypt(given_pass) != getData("player_password_hashes", player):
            print("invalid_input ::: Incorrect password! Someone is trying to control someone else... there will be punishments")
            sys.exit()
        player_name = getData("player_names", player)
        player_actions = int(getData("player_actions", player))
        amount = int(command[3])
        if amount > player_actions:
            print("invalid_input ::: {} cannot upgrade their range! The player does not have enough action points! They are trying to cheat the system... there will be punishments".format(player_name))
            sys.exit()
        player_range = int(getData("player_ranges", player))
        setPlayerData("player_actions", player, str(player_actions - amount))
        setPlayerData("player_ranges", player, str(player_range + amount))
        addHistory("upgrade {} {}".format(player_name, str(amount)))
        print("data_update ::: actions {} {}".format(str(player), str(player_actions - amount)))
        print("data_update ::: range {} {}".format(str(player), str(player_range + amount)))
        sys.exit()
    except:
        print("invalid_input ::: malformed input! Someone does not know how to send correct packets! Someone is attempting hacking... there will be punishments")
        sys.exit()
# Everything under here is not worked on - it is the original prototype code
#elif command[0] == "attack":
#    try:
#        player1 = names.index(command[1])
#        player2 = names.index(command[2])
#        if distance(positions[player1], positions[player2]) > ranges[player1]:
#            print("You are too far to attack! Come within {} square{} of someone else to attack them.".format(str(ranges[player]), "s"if ranges[player] > 1 else ""))
#            continue
#        cost = int(command[3])# * distance(positions[player1], positions[player2])
#        if cost > actions[player1]:
#            print("You do not have enough action points to attack! You need {} action points.".format(str(cost)))
#            continue
#        health[player2] = max(health[player2] - int(command[3]), 0)
#        actions[player1] = actions[player1] - cost
#        if health[player2] == 0:
#            print("You killed {}!".format(command[2]))
#            status[player2] = "DEAD"
#            updateRenderedPlayerPosition(player2)
#            playersLeft = playersLeft - 1
#            if playersLeft == 1:
#                break
#    except:
#        print("attack <player name> <player name> <damage>: attack another player")
