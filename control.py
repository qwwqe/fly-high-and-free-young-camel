# control functions
import definitions
import entity
import vectors as vec

from definitions import *
#from vectors import *
#from entities import *

import pygame

# actions:
# ROT_CLOCK
# ROT_COUNTERCLOCK
# ACCEL
# DECEL
# SHOOT_BULLET
# SPINOUT
# CRASH


k_clockwise = pygame.K_COMMA
k_counterclockwise = pygame.K_SLASH
k_gun = pygame.K_SPACE
k_accel = pygame.K_f
k_decel = pygame.K_d
k_flip = pygame.K_PERIOD

# how about one control function for each type of vehicle / object, with the control queue (rotate, jump, move, etc) updated based on
# separate code blocks for player / ai, but a single block of code to translate these control events into velocity and rotation changes

class Control:
    keys = []
    keyevents = []
    
    def __init__(self, ent):
        self.ent = ent
        self.queue = [] # long term stuff
        
        # intervals
        self.inter = {"SHOOT_BULLET" : 0, "ROT" : 0, "ACCEL" : 0, "DECEL" : 0}

    ## main processing function. objects with simple mechanics (mostly bullets) can
    ## instantiate the Control superclass and use the empty process function, so
    ## collision and movement handling will simply update location based on static velocity
    def process(self):
        pass

    ## ancillary functions for processing
    # bam bam
    #def __
    def shoot(self, weapon):
        if weapon is "WEAP_BULLET":
            entity.entBullet(self.ent.projloc("WEAP_BULLET"), vec.component(SPD_BULLET + vec.length(self.ent.vel), self.ent.rot), owner = self.ent)
            print "bullet shot. travelling at %s units per frame %s, at an angle of %s radians" % (SPD_BULLET, vec.component(SPD_BULLET, self.ent.rot), self.ent.rot)
        pass

# take a guess fuck face
class ctlPlane(Control):
#    def __init__(self, ent):
#        self.ent = ent
#        self.queue = []
    
    #
    def process(self):
        actions = [] # immediate actions
        
        # increase 
        for k in self.inter:
            if self.inter[k] > 0:
                self.inter[k] -= 1
        
        if self.ent.player: # human input
            # rotate. all this shit is so you can go like tapTAP to go up or down a slight level. roll on the arrows right?
            if k_clockwise in Control.keyevents:
                actions.append("ROT_CLOCK")
            elif k_counterclockwise in Control.keyevents:
                actions.append("ROT_COUNTER")
            elif Control.keys[k_clockwise] and Control.keys[k_counterclockwise]: # if both are pressed, going by key events will be unsynched
                pass
            elif Control.keys[k_clockwise]: #or k_clockwise in Control.keyevents:
#               self.ent.rot += ROT_PLANE_INT
                actions.append("ROT_CLOCK")
            elif Control.keys[k_counterclockwise]: #or k_counterclockwise in Control.keyevents:
#               self.ent.rot -= ROT_PLANE_INT
                actions.append("ROT_COUNTER")
                
            # accelerate
            if Control.keys[k_accel] and Control.keys[k_decel]:
                pass
            elif Control.keys[k_accel] or k_accel in Control.keyevents:
#               self.ent.vel = vectors.component(vectors.length(self.ent.vel) + 1, self.ent.rot)
                actions.append("ACCEL")
            elif Control.keys[k_decel] or k_decel in Control.keyevents:
#               self.ent.vel = vectors.component(vectors.length(self.ent.vel) - 1, self.ent.rot)
                actions.append("DECEL")
                
            # shoot
            if Control.keys[k_gun] or k_gun in Control.keyevents:
#               self.shoot()
                actions.append("SHOOT_BULLET")
                
        else: # AI
            pass
        
        # perform actions
        for a in actions:
            if a == "ROT_CLOCK" and not self.inter["ROT"]:
                self.ent.rot += ROT_PLANE_INT
                self.ent.vel = vec.component(vec.length(self.ent.vel), self.ent.rot)
                self.inter["ROT"] = INT_ROT_PLANE
            elif a == "ROT_COUNTER" and not self.inter["ROT"]:
                self.ent.rot -= ROT_PLANE_INT
                self.ent.vel = vec.component(vec.length(self.ent.vel), self.ent.rot)
                self.inter["ROT"] = INT_ROT_PLANE
            elif a == "ACCEL" and not self.inter["ACCEL"]:
                self.ent.vel = vec.component(vec.length(self.ent.vel) + 1, self.ent.rot)
                self.inter["ACCEL"] = INT_ACCEL_PLANE
            elif a == "DECEL" and not self.inter["DECEL"]:
                self.ent.vel = vec.component(vec.length(self.ent.vel) - 1, self.ent.rot)
                self.inter["DECEL"] = INT_DECEL_PLANE
            elif a == "SHOOT_BULLET" and not self.inter["SHOOT_BULLET"]:
                self.shoot("WEAP_BULLET")
                self.inter["SHOOT_BULLET"] = INT_BULLET_PLANE
        # sum demo code
#        self.shoot("WEAP_BULLET")
#        self.
        

# ancillary
##    def shoot(self, weapon):
##        if weapon is "WEAP_BULLET":
##            print "pow pow, bullets"
##        elif weapon is "WEAP_MISSLE":
##            pass
##        elif weapon is "WEAP_BOMB":
##            pass
##        elif weapon is "WEAP_FLARE":
##            pass


# we need sub control functions for player input or comp ai
