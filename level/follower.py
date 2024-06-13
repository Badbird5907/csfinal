from Processing3 import *

from util.debugger import *

from level.pathfinder import *
from util.random import *
from renderer.human import *

def initFollower():
    global human_turn_debounce
    human_turn_debounce = {}

def getRandomTileAround(pos):
    global tile_size
    x = int(pos[0] // tile_size)
    y = int(pos[1] // tile_size)
    #print("Getting random tile around " + str(x) + ", " + str(y))

    # get a single tile from the 4 surrounding tiles
    global grid
    tiles = []
    if x > 0 and grid[x - 1][y] == 0: # check bounds
        tiles.append((x - 1, y))
    if x < len(grid) - 1 and grid[x + 1][y] == 0:
        tiles.append((x + 1, y))
    if y > 0 and grid[x][y - 1] == 0:
        tiles.append((x, y - 1))
    if y < len(grid[x]) - 1 and grid[x][y + 1] == 0:
        tiles.append((x, y + 1))
    if len(tiles) == 0:
        return None
    return tiles[randInt(0, len(tiles))]

def wander(human):
    global calc_paths, humans, pX, pY, tile_size, difficulty
    #print("Check Wandering: ", str(human))
    if human["state"] == "idle" and not human["follow"]:
        if millis() - human["last_follow_ms"] > 5000 and millis() - human["last_wander_ms"] > human["next_wander_ms"]:
            #print("Wandering")
            randTile = getRandomTileAround(human["pos"])
            posTile = (human["pos"][0] // tile_size, human["pos"][1] // tile_size)
            human["path"] = [randTile]

            human["last_wander_ms"] = millis()
            human["next_wander_ms"] = randInt(3500, 7000) if difficulty == "hard" else randInt(7000, 14000)
            x = human["pos"][0] // tile_size
            y = human["pos"][1] // tile_size
            data = createPathData(human, human["path"], x, y)
            calc_paths[human["id"]] = data
            #print("Wandered to " + str(human["path"]))

def tickFollower():
    tickDebuggerOverlay()
    drawAllHumans()
    global calc_paths, humans, pX, pY, tile_size
    move_speed = 1 # base move speed
    for id in humans:
        human = humans[id]
        if human["hidden"]:
            continue
        wander(human)
        if (id not in calc_paths) or (
            id in calc_paths and len(calc_paths[id]["path"]) <= 1 and human["follow"]): # random bs indentation lol
            human["state"] = "idle"
            continue

        path_data = calc_paths[id]
        if len(path_data["path"]) == 0:
            continue

        if human["follow"]:
            human["last_follow_ms"] = millis()
            human["state"] = "run"
            human["speed"] = 1
            # set the move speed to be faster if they are far away from the player
            dist = len(path_data["path"])
            if dist > 10:
                move_speed = 2
            elif dist > 5:
                move_speed = 1.5
            else:
                move_speed = 1
        human["speed"] = move_speed


        next_tile_idx = 0 if len(path_data["path"]) == 1 else 1
        next_tile = path_data["path"][next_tile_idx]
        curr_pos_tile = (int(human["pos"][0] // tile_size), int(human["pos"][1] // tile_size))

        # calc next pos
        next_pos = (next_tile[0] * tile_size + tile_size / 2, next_tile[1] * tile_size + tile_size / 2)
        next_pos_tile = (int(next_pos[0] // tile_size), int(next_pos[1] // tile_size))
        if (next_pos_tile == curr_pos_tile):
            # fix it bugging out when wandering cause the pathfinding algo is never actually run
            continue
        
        if (isDebuggerEnabled()):
            fill(255, 0, 0)
            ellipse(next_pos[0], next_pos[1], 10, 10)

        # calculate the direction to move
        dx = next_pos[0] - human["pos"][0]
        dy = next_pos[1] - human["pos"][1]

        # only change the direction if the movement is big enough
        if abs(dx) > move_speed or abs(dy) > move_speed:
            if abs(dx) > abs(dy):
                if dx > 0:
                    human["facing"] = "right"
                else:
                    human["facing"] = "left"
            else:
                if dy > 0:
                    human["facing"] = "front"
                else:
                    human["facing"] = "back"

        # FIXING ANOTHER STUPID EDGE CASE:
        # NORMALIZE THE MOVEMENT VECTOR 
        distance = (dx**2 + dy**2)**0.5
        if distance != 0:
            move_x = (dx / distance) * move_speed
            move_y = (dy / distance) * move_speed
        else:
            move_x = 0
            move_y = 0

        human["pos"] = (human["pos"][0] + move_x, human["pos"][1] + move_y)

