# game entities
import texture
import control
import vectors
import cell
import math
import sprite as sprclass

from texture import Texture
#from control import *
from definitions import *

# the position of all entities is defined as their centre.
# rotation is stored separately, also defined about their centre.
# so collision detection will have to calculate the position
# of an entity's vertices

# superclass
class Entity:
    entities = []

    # we need cells, collision stuff, etc
    def __init__(self, pos = (0, 0), rot = 0, vel = (0, 0), size = None, \
                ctlfunc = None, interact = True, player = False, sprite = None, colour = (255, 255, 255), health = 100, owner = None):
        self.age = 0
        self.expiry = -1
        self.health = health
        
        self.owner = owner
    
        self.pos = pos # centre
        self.rot = rot
        self.vel = vel

        self.sprite = sprite

        if not size:
            if sprite:
                self.size = len(self.sprite[0]), len(self.sprite)
            else:
                self.size = (0, 0)
        else:
            self.size = size

        if not ctlfunc:
            self.ctlfunc = control.Control(self)
        else:
            self.ctlfunc = ctlfunc
            
        self.interact = interact # check collisions
        self.player = player
        self.colour = colour

        self.cells = []
        cell.add(self)
        Entity.entities.append(self)

    def delete(self):
        cell.delete(self)
        Entity.entities.remove(self)

    # return the local vertices, described counterclockwise, of the sprite
    # rectangle rotated about its centre and the origin
    def _localVertices(self):
        w, h = self.size[0], self.size[1]
        rot = self.rot
        radius = vectors.length((0, 0), (w, h)) / 2

        # top right corner
        #  ______
        # |     /|
        # |    / | 
        # |   /__|    
        # |a     |
        # |      |
        # |______|

        a = math.asin(h/(2 * radius))
        #c = (radius * round(cos(rot + a), 2), radius * round(sin(rot + a), 2)) 
        c = vectors.component(radius, rot + a)
        v = [(c[0], c[1])]

        # top left corner
        #c = (radius * round(cos(rot + pi - a), 2), radius * round(sin(rot + pi - a), 2)) 
        c = vectors.component(radius, rot + (math.pi - a))
        v.append((c[0], c[1]))

        # bottom left corner
        #c = (radius * round(cos(rot + pi + a), 2), radius * round(sin(rot + pi + a), 2)) 
        c = vectors.component(radius, rot + (math.pi + a))
        v.append((c[0], c[1]))
    
        # bottom right corner
        #c = (radius * round(cos(rot - a), 2), radius * round(sin(rot - a), 2)) 
        c = vectors.component(radius, rot - a)
        v.append((c[0], c[1]))

        return (list(map(lambda t: (round(t[0], 2), round(t[1], 2)), v)))

    # orient the above in the scene
    def vertices(self):
        if(self.size[0] == 1 and self.size[1] == 1): # a bullet or something
            v = [(0, 0)]
        else:
            v = self._localVertices()
        return (list(map(lambda a: (a[0] + self.pos[0], a[1] + self.pos[1]), v)))

    # projectile locations
    def projloc(self, weapon):
        right_mid = vectors.component(self.size[0] / 2, self.rot) # front middle.. tat tat tat
        if weapon == "WEAP_BULLET":
            return(self.pos[0] + right_mid[0], self.pos[1] + right_mid[1])
        else:
            return(self.pos)

    # naughty ones, don't use this function. only the collision detector needs to
    def _move(self, pos):
        self.pos = pos
        cell.delete(self)
        cell.add(self)


# primary objects
class entPlane(Entity):
    def __init__(self, pos, rot = 0, vel = (0, 0), player = False, sprite = None, size = None, expiry = -1, interact = True, health = HEALTH_PLANE, owner = None):
        self.age = 0
        self.expiry = expiry
        self.health = health

        self.owner = owner

        self.pos = pos

        # if rotation and velocity is given, use only the magnitude of the velocity
        if rot:
            self.rot = ROT_PLANE_INT * round(rot / ROT_PLANE_INT)
        else:
            self.rot = ROT_PLANE_INT * round(vectors.anglex(vel) / ROT_PLANE_INT)
        self.vel = vectors.component(vectors.length(vel), self.rot)

        self.ctlfunc = control.ctlPlane(self)
        self.player = player
        self.interact = interact
        
        #if not Texture.textures.has_key("OBJ_PLANE"):
        #    Texture("OBJ_PLANE", IMGDIR + "OBJ_PLANE" + IMGEXT)
        #self.texture = Texture.textures["OBJ_PLANE"]
        #self.size = (40, 40)#(self.image.w, self.image.h)
        if not sprite:
            self.sprite = sprclass.plane
        else:
            self.sprite = sprite

        if not size:
            self.size = len(self.sprite[0]), len(self.sprite)
        else:
            self.size = size

        self.cells = []
        cell.add(self)
        Entity.entities.append(self)

class entTank(Entity):
    pass
        
# projectiles
class entBullet(Entity):
    def __init__(self, pos, vel = None, rot = 0, owner = None, sprite = None, size = None, expiry = EXPIRY_BULLET, health = 100, interact = True):
        self.age = 0
        self.expiry = expiry
        self.health = health
        
        self.pos = pos
        self.rot = rot
        self.player = False
        self.interact = interact
        
        if not vel:
            if owner: self.vel = vector.component(SPD_BULLET, owner.rot)
            else: self.vel = (SPD_BULLET, 0)
        else:
            self.vel = vel

        self.owner = owner

        self.ctlfunc = control.Control(self)

        #if not Image.images.has_key("OBJ_BULLET"):
        #    Image("OBJ_BULLET", IMGDIR + "OBJ_BULLET" + IMGEXT)
        #self.image = Image.images["OBJ_BULLET"]
        #self.size  = (self.image.w, self.image.h)
        if not sprite:
            self.sprite = sprclass.bullet
        else:
            self.sprite = sprite

        if not size:
            self.size = len(self.sprite[0]), len(self.sprite)
        else:
            self.size = size

        self.cells = []
        cell.add(self)
        Entity.entities.append(self)
