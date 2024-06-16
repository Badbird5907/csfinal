from Processing3 import *

from util.key import *
from util.ticker import *
from util.threading import *
from util.random import *

import heapq

def construct_grid():
  global tile_size
  grid = []
  for i in range(1920 // tile_size):
    grid.append([])
    for j in range(1080 // tile_size):
      if rd() < 0.1:  # 10% chance to add a random weight
        grid[i].append(1)  # random weight between 1 and 10
      else:
        grid[i].append(0)
  #print(grid)
  return grid
def draw_debugger_grid(grid):
  global pX, pY, humans, tile_size, calc_paths
  human_positions = calc_paths

  pXRounded = pX // tile_size
  pYRounded = pY // tile_size

  for i in range(len(grid)):
    for j in range(len(grid[i])):
      x = i*tile_size
      y = j*tile_size
      
      fill(255)
      for h1 in human_positions:
        human_pos = human_positions[h1]
        human = humans[human_pos["id"]]
        human_tile_pos = (human["pos"][0] // tile_size, human["pos"][1] // tile_size)
        if human_tile_pos == (i, j):
          fill(255, 0, 0)
        elif (i, j) in human_pos["path"]: # path pos
          # get the pf_debug_color from the human dict
          cl = human["pf_debug_color"]
          fill(cl[0], cl[1], cl[2])
      if grid[i][j] == 1:
        fill(0)
      if (i, j) == (pXRounded, pYRounded): # draw player pos
        fill(0, 255, 0)
      rect(x, y, tile_size, tile_size)
      # draw the coordinates if it is close to the player to save performance
      if abs(i - pXRounded) <= 5 and abs(j - pYRounded) <= 5:
        fill(0)
        textSize(10)
        text(str(i) + ", " + str(j), x + 5, y + 20)
  return

# pathfind() will return a list of tuples, where each tuple is a position
# in the grid that the human should move

def createPathData(human, path, x, y):
  global tile_size
  dict = {
    "pos": (x*tile_size, y*tile_size),
    "path": path,
    "id": human["id"],
  }
  return dict
  

def calculatePaths():
  global pX, pY, humans, tile_size, calc_paths, grid
  # check if the variables are defined
  if "pX" not in globals() or "pY" not in globals() or "humans" not in globals() or "tile_size" not in globals() or "calc_paths" not in globals() or "grid" not in globals():
    return
  human_positions = {} # [ (x, y), (x, y), ...]
  for id in humans:
    human = humans[id]
    if human["hidden"] or human["enemy_fade_start"] != -1:
      continue
    if not human["follow"] and not human["enemy"]:
      currPath = []
      if id in calc_paths:
        currPath = calc_paths[id]["path"] # copy over the old path (wander)
      human_positions[id] = createPathData(human, currPath, human["pos"][0] // tile_size, human["pos"][1] // tile_size)
      continue
    x = human["pos"][0] // tile_size
    y = human["pos"][1] // tile_size
    target = ((pX // tile_size) + ((1 * 32) // tile_size), (pY // tile_size) + ((2 * 32) // tile_size)) if human["enemy"] else (pX // tile_size, pY // tile_size)
    path = pathfind(grid, (x, y), target)
    if (isKeyPressed("p")):
      print(path)
    dict = createPathData(human, path, x, y)
    human_positions[id] = dict
  calc_paths = human_positions

def getCost(path, grid):
  cost = 0
  for i in range(len(path) - 1):
    a = path[i][0]
    b = path[i][1]
    cost += grid[a][b]
  return cost

def guessCost(a, b):
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

def pathfind(grid, start, end): # WOOOOOO A* PATHFINDING I ACTUALLY IMPLEMENTED IT LOL
  open_set = []
  heapq.heappush(open_set, (0, start))
  frm = {}
  gs = {start: 0}
  f_score = {start: guessCost(start, end)}

  while open_set:
    current = heapq.heappop(open_set)[1]
    
    if current == end:
      return reconstruct_path(frm, current)
    
    for neighbour in calcNeighours(grid, current):
      ec =  grid[neighbour[0]][neighbour[1]]
      tent_gs = gs[current] + 1 + ec
      # print(tent_gs)

      if neighbour not in gs or tent_gs < gs[neighbour]:
        frm[neighbour] = current
        gs[neighbour] = tent_gs
        f_score[neighbour] = int(tent_gs + guessCost(neighbour, end))
        if neighbour not in [i[1] for i in open_set]:
          heapq.heappush(open_set, (f_score[neighbour], neighbour))
  
  return []  # no path found

def calcNeighours(grid, node):
  neighbours = []
  x, y = node
  directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
  global pX, pY, tile_size
  for dx, dy in directions:
    nx, ny = x + dx, y + dy
    # if nx, ny are a float, we need to round them
    if type(nx) == float:
      nx = int(nx)
    if type(ny) == float:
      ny = int(ny)
    #print(nx, ny, " | ", x, y, " | ", dx, dy)
    if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]): # and grid[nx][ny] == 0:
      if grid[nx][ny] == 0 or (grid[nx][ny] == 1 and (pX // tile_size) == nx and (pY // tile_size) == ny): 
        # we are on a "blacklisted" tile, fix the dumbass edge case
        neighbours.append((nx, ny))
      
  return neighbours

def reconstruct_path(frm, cr):
  total_path = [cr]
  while cr in frm:
    cr = frm[cr]
    total_path.append(cr)
  total_path.reverse()
  return total_path
