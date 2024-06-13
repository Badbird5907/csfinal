def sqrt(x): # lmfao processing doesn't have sqrt????
  return x ** 0.5 # hack


def euclidean_dist(p1, p2):
  return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def abs(x):
  if (x < 0):
    return -x
  return x