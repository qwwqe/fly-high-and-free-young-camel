# control functions
import definitions
import entity
import math
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
            # will have to adapt this to teammates / opponents, not just players
            if not entity.Entity.players:
                return
                
            # calculate closest player    
            nearplayer = entity.Entity.players[0]
            neardist = math.fabs(self.ent.pos[0] - nearplayer.pos[0])
            for p in entity.Entity.players:
                if math.fabs(self.ent.pos[0] - p.pos[0]) < neardist:
                    nearplayer = p
            
            # set course
            angle = vec.anglex((nearplayer.pos[0] - self.ent.pos[0], nearplayer.pos[1] - self.ent.pos[1]))
            relrot = self.ent.rot % (2 * math.pi)
            xdist = math.fabs(nearplayer.pos[0] - self.ent.pos[0])
            pys = [y for _, y in nearplayer.vertices()]
            ptop = max(pys)
            pbottom = min(pys)
            
            if nearplayer.pos[0] > self.ent.pos[0]: # player to the right of ai
                if self.ent.vel[0] >= 0: # moving in the right direction, fly a straight path
                    if relrot != 0:
                        if relrot <= math.pi / 2:
                            actions.append("ROT_COUNTER")
                        else:
                            actions.append("ROT_CLOCK")
                    else:
                        if xdist > AI_PLANE_SLOW_DIST:
                            actions.append("ACCEL")
                        elif xdist < AI_PLANE_SLOW_DIST:
                            actions.append("DECEL")
                            
                    if self.ent.pos[1] > pbottom and self.ent.pos[1] < ptop and xdist <= AI_PLANE_ACT_DIST:
                        actions.append("SHOOT_BULLET")
                elif self.ent.vel[0] <= 0: # moving in the wrong direction, turn around
                    actions.append("DECEL")
                    if nearplayer.vel[0] <= 0 or xdist < AI_PLANE_REV_DIST: # fly right by that bitch, just slow down 
                        pass
                    elif relrot <= math.pi:
                        actions.append("ROT_COUNTER")
                    elif relrot != 0: # should always be true, but in case something fucks with the vel and not the rotation
                        actions.append("ROT_CLOCK")
            elif nearplayer.pos[0] < self.ent.pos[0]: # player to the left of ai
                if self.ent.vel[0] <= 0: # right direction
                    if relrot != math.pi:
                        if relrot < math.pi:
                            actions.append("ROT_CLOCK")
                        else:
                            actions.append("ROT_COUNTER")
                    else:
                        if xdist > AI_PLANE_SLOW_DIST:
                            actions.append("ACCEL")
                        elif xdist < AI_PLANE_SLOW_DIST:
                            actions.append("DECEL")
                            
                        if self.ent.pos[1] > pbottom and self.ent.pos[1] < ptop and xdist <= AI_PLANE_ACT_DIST:
                            actions.append("SHOOT_BULLET")
                elif self.ent.vel[0] >= 0: # wrong direction
                    actions.append("DECEL")
                    if nearplayer.vel[0] >= 0 or xdist < AI_PLANE_REV_DIST: # flew right by him
                        pass
                    elif relrot < math.pi:
                        actions.append("ROT_CLOCK")
                    elif relrot != math.pi: # should always be true, but in case something fucks with the vel and not the rotation
                        actions.append("ROT_COUNTER")
            
            # if self.ent.rot / (2 * math.pi) > angle: 
                # actions.append("ROT_COUNTER")
            # elif self.ent.rot / (2 * math.pi) < angle:
                # actions.append("ROT_CLOCK")
                
            # top / bottom stuff
                    
            # speed the fuck up       
            #velmag = vec.length(self.ent.vel)
            #if velmag < SPD_PLANE_MAX and :
            #    actions.append("ACCEL")
        
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
            elif a == "ACCEL" and not self.inter["ACCEL"] and vec.length(self.ent.vel) < SPD_PLANE_MAX:
                self.ent.vel = vec.component(vec.length(self.ent.vel) + 1, self.ent.rot)
                self.inter["ACCEL"] = INT_ACCEL_PLANE
            elif a == "DECEL" and not self.inter["DECEL"] and vec.length(self.ent.vel) > SPD_PLANE_MIN:
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
