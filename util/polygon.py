
from Processing3 import *
from util.raycast import *

def isValidPolygon(polygon): # check if the last point is the same as the first point
  if len(polygon) < 2:
    return False
  return polygon[0] == polygon[-1]

def drawPolygon(polygon, color = None, allowInvalid = False): # draw the polygon from point to point, with the last point connecting to the first point
  if (not color == None):
    stroke(color[0], color[1], color[2])
  for i in range(len(polygon) - 1):
    line(polygon[i][0], polygon[i][1], polygon[i + 1][0], polygon[i + 1][1])
  return

def isInsidePolygon(pos, polygon):
  intersections = 0
  ray = posToExtrapolated(pos)
  #stroke(255,0,0)
  #line(ray[0][0], ray[0][1], ray[1][0], ray[1][1])
  for i in range(len(polygon) - 1):
    #line(polygon[i][0], polygon[i][1], polygon[i + 1][0], polygon[i + 1][1])
    inter = lineSegIntersectsLineSeg(ray, [polygon[i], polygon[i + 1]])
    if (not inter == None):
      intersections += 1
  #print(intersections)
  return intersections % 2 != 0