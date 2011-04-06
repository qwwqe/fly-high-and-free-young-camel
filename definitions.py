# definitions
##WEAP_BULLET
##WEAP_MISSILE
##WEAP_BOMB
##WEAP_FLARE
##
##OBJ_PLANE
##OBJ_TANK

from math import pi

FPS = 30

MAX_ENT_BULLET = 50

INT_BULLET_PLANE = int(float(200) / float(FPS)) # fire a bullet every 200 milliseconds
INT_ROT_PLANE = int(float(100) / float(FPS)) # maybe make this a function of the speed?
INT_ACCEL_PLANE  = int(float(500) / float(FPS))
INT_DECEL_PLANE  = int(float(200) / float(FPS))

SPD_BULLET = 8
SPD_PLANE_MAX = 14
SPD_PLANE_MIN = 4

AI_PLANE_ACT_DIST = 400 # distance within which ai planes let loose
AI_PLANE_SLOW_DIST = 50 # distance within which ai planes will slow down. i guess also this is the "distance they keep" from opponents
AI_PLANE_REV_DIST = 50 # turn around distance if passed an opponent
#AI_PLANE_SPD_AVG = 10 # normal flight speed

HEALTH_PLANE = 100

DMG_BULLET = 50

ROT_PLANE_INT = pi / 4

EXPIRY_BULLET = 150 # life of a bullet, in frames

SCROLL_MARGIN_LEFT = 40
SCROLL_MARGIN_RIGHT = 40

IMGDIR = "data"
IMGEXT = "png"
