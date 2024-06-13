from Processing3 import *
from util.math import *

def rayIntersectsRay(ray1, ray2): # (x, y), [(x1, y1), (x2, y2)]
  # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection

  # x1 = pos[0]
  # y1 = pos[1]
  # # extrapolate out the line to "infinity" lol
  # x2 = pos[0] + 1000
  # y2 = pos[1]
  x1 = ray1[0][0]
  y1 = ray1[0][1]
  x2 = ray1[1][0]
  y2 = ray1[1][1]

  l0 = ray2[0]
  l1 = ray2[1]
  x3 = l0[0]
  y3 = l0[1]
  x4 = l1[0]
  y4 = l1[1]

  denom = ((x1-x2)*(y3-y4)-(y1-y2)*(x3-x4))
  if denom == 0: # if denominator is 0, the lines are parallel or coincident
    return None
  a = (x1 * y2 - y1 * x2)
  b = (x3*y4 - y3 * x4)
  x = (a * (x3-x4) - (x1-x2) * b) / denom
  y = (a * (y3-y4) - (y1-y2) * b) / denom
  return [(x, y), x1, y1, x, y]

def normalizeSegment(seg):
  if True:
    return seg
  return [(min(seg[0][0], seg[1][0]), min(seg[0][1], seg[1][1])), (max(seg[0][0], seg[1][0]), max(seg[0][1], seg[1][1]))]
def lineSegIntersectsLineSeg(_seg1, _seg2): # [(x1, y1), (x2, y2)], [(x3, y3), (x4, y4)]
  seg1 = normalizeSegment(_seg1)
  seg2 = normalizeSegment(_seg2)
  # https://en.wikipedia.org/wiki/Intersection_(geometry)#Two_line_segments
  # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
  x0 = seg1[0][0]
  y0 = seg1[0][1]
  x1 = seg1[1][0]
  y1 = seg1[1][1]
  x2 = seg2[0][0]
  y2 = seg2[0][1]
  x3 = seg2[1][0]
  y3 = seg2[1][1]
  # https://www.desmos.com/calculator/0wr2rfkjbk
  p0 = ((y3 - y2) * (x3 - x0)) - ((x3 - x2) * (y3 - y0))
  p1 = ((y3 - y2) * (x3 - x1)) - ((x3 - x2) * (y3 - y1))
  p2 = ((y1 - y0) * (x1 - x2)) - ((x1 - x0) * (y1 - y2))
  p3 = ((y1 - y0) * (x1 - x3)) - ((x1 - x0) * (y1 - y3))
  # {{p0 * p1 <= 0:1, 0} + {p2 * p3 <= 0:1, 0} = 2:1, 0}
  # this returns 1 when the lines are intersect and 0 when they don't
  if (p0 * p1 <= 0 and p2 * p3 <= 0):
    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
    denom = ((x0-x1)*(y2-y3)-(y0-y1)*(x2-x3))
    if denom == 0: # if denominator is 0, the lines are parallel or coincident
      return None
    a = (x0 * y1 - y0 * x1)
    b = (x2*y3 - y2 * x3)
    x = (a * (x2-x3) - (x0-x1) * b) / denom
    y = (a * (y2-y3) - (y0-y1) * b) / denom
    return [(x, y), x0, y0, x, y]
  return None

def extrapolateRay(ray, length):
  new_ray = [(ray[0][0], ray[0][1]), (ray[0][0] + length, ray[0][1])]
  return new_ray

def posToExtrapolated(pos): # (x, y)
  return [(pos[0], pos[1]), (pos[0] + 2000, pos[1])]