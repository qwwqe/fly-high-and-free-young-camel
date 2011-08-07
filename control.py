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
    actions_camp = []
    
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
            realangle = vec.anglex((nearplayer.pos[0] - self.ent.pos[0], nearplayer.pos[1] - self.ent.pos[1]))
            if realangle < 0:
                realangle = 2 * math.pi + realangle
            rotangle = ROT_PLANE_INT * int(realangle / ROT_PLANE_INT)
            
            xdist = math.fabs(nearplayer.pos[0] - self.ent.pos[0])
            ydist = math.fabs(nearplayer.pos[1] - self.ent.pos[1])
            #pys = [y for _, y in nearplayer.vertices()]
            #ptop = max(pys)
            #pbottom = min(pys)
            pvs = nearplayer.vertices()
            pxs = [x for x, _ in pvs]
            pys = [y for _, y in pvs]
            left, right = min(pxs), max(pxs)
            bottom, top = min(pys), max(pys) 
            
            #print self.ent, self.ent.rot, rotangle
            
            # set course. if far away, take your turns easy, otherwise, sharp is ok
            #if xdist > AI_PLANE_ACT_DIST: # far, easy
            cmpangle = rotangle
            #else: # close, hard
            #    cmpangle = realangle
                
            # latter conditions checks for alignment     
            if self.ent.rot < cmpangle:
                if cmpangle - self.ent.rot > math.pi:
                    actions.append("ROT_COUNTER")
                else:
                    actions.append("ROT_CLOCK")
            elif self.ent.rot > cmpangle:
                if self.ent.rot - cmpangle > math.pi:
                    actions.append("ROT_CLOCK")
                else:
                    actions.append("ROT_COUNTER")
                    
                    
            # speed up
            if xdist <= AI_PLANE_SLOW_DIST:
                actions.append("DECEL")
            else:
                actions.append("ACCEL")
                
            # woah, cool
            def supercmp(f):
                if not f and f == self.ent.vel[0]:
                    return cmp(nearplayer.pos[0] - self.ent.pos[0], 0)
                elif not f and f == self.ent.vel[1]:
                    return cmp(nearplayer.pos[1] - self.ent.pos[1], 0)
                return cmp(f, 0)
                    
            # blaze
            if xdist <= AI_PLANE_ACT_DIST:
                # facing the bastard
                if ((supercmp(self.ent.vel[0]) == cmp(nearplayer.pos[0] - self.ent.pos[0], 0)) and \
                    (supercmp(self.ent.vel[1]) == cmp(nearplayer.pos[1] - self.ent.pos[1], 0))):
                # ^ test is failing on vel[0] == 0 or vel[1] == 0
                    
                    # b = y - mx. we take the linear equation of our ai's velocity, 
                    # and compare its offset (b = 0) with the offset computed by
                    # substituting the y and x values of each vertex of the player.
                    # if these vertices lie both above (b > 0) and below (b < 0)
                    # the line of velocity, then a bullet might intersect, so shoot, shoot
                    #if not self.ent.vel[0]:
                    
                    if not self.ent.vel[0]: # up/down
                        if self.ent.pos[0] > left and self.ent.pos[0] < right:
                            actions.append("SHOOT_BULLET")
                    else:
                        slope = self.ent.vel[1] / self.ent.vel[0]
                        b = self.ent.pos[1] - slope * self.ent.pos[0]
                        above = below = False
                        for v in pvs:
                            if (v[1] - slope * v[0]) > b:
                                above = True
                            else:
                                below = True
                                
                            if above and below:
                                break
                                    
                        if above and below:
                            actions.append("SHOOT_BULLET")
        
        # perform actions
        for a in actions:
            if a == "ROT_CLOCK" and not self.inter["ROT"]:
                self.ent.rot += ROT_PLANE_INT
                if self.ent.rot >= 2 * math.pi:
                    self.ent.rot = 0
                
                self.ent.vel = vec.component(vec.length(self.ent.vel), self.ent.rot)
                self.inter["ROT"] = INT_ROT_PLANE
            elif a == "ROT_COUNTER" and not self.inter["ROT"]:
                self.ent.rot -= ROT_PLANE_INT
                if self.ent.rot < 0:
                    self.ent.rot = 2 * math.pi - ROT_PLANE_INT 
                
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
