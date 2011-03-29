# vector calculation functions
from math import sin, cos, asin, atan, pi, sqrt, pow

# compute resultant vector from components
def resultant(pos):
    pass

# compute component vectors from resultant. rotation is in degrees, counter-clockwise,
# starting from the positive x axis
def component(len, rot, rnd = True):
    # IF PYTHON'S TRIG FUNCTIONS DIDN'T BLOW NONE OF THIS WOULD BE NECESSARY
    # just round it...
#    if rot is 0:
#        x = len
#        y = 0
#    elif rot is pi/2:
#        x = 0
#        y = len
#    elif rot is pi:
#        x = -len
#        y = 0
#    elif rot is 3 * (pi/2):
#        x = 0
#        y = -len
#    else:
    x = len * cos(rot)
    y = len * sin(rot)
        
    return (round(x, 4), round(y, 4))

# angle a vector makes with the x axis
def anglex(u):
    if u[0]:
        return(round(atan(float(u[1]) / float(u[0])), 4))
    elif u[1]:
        return(round(pi * (float(u[1]) / float(-u[1])), 4))
    else:
        return(0)

# length of a line
def length(p1, p2 = (0, 0)):
	return (sqrt(pow((p2[0] - p1[0]), 2) + pow((p2[1] - p1[1]), 2)))

# dot product
def dot(u, v):
    return(u[0] * v[0] + u[1] * v[1])

# projection of v onto u
def projection(u, v):
    p = dot(u, v) / pow(length(u), 2)
    return(u[0] * p, u[1] * p)

# unit vector of u
def normalize(u):
    l = length(u)
    if l:
        return(u[0] / l, u[1] / l)
    else:
        return(0, 0)
