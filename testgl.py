import sys, pygame
import cell, entity, vectors, collision
import math
import random
import ground
import control
import texture

import sprite as sprclass

from definitions import *

from OpenGL.GL import *
from OpenGL.GLU import *

FDELAY = (1.0/float(FPS)) * 1000 # FPS in definitions

groundmap = ground.load_xpm("maps/map1collision.xpm")

width, height = 700, groundmap[0][1]

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

glClearColor(0.0, 0.0, 0.0, 1.0)    
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, width, 0, height)
glMatrixMode(GL_MODELVIEW)

#glEnable(GL_TEXTURE_2D)
#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

maptex = texture.mapTexture("maps/map1texture.bmp", 256)
maptex.gen_lists()

grid = cell.Grid((14, 10), (50, 50))
b1 = entity.Entity(size = (40, 30), pos = (300, 100), vel = (random.uniform(-5, 5), random.uniform(-5, 5)), colour = (255, 0, 0))
b2 = entity.Entity(size = (70, 40), pos = (500, 300), vel = (random.uniform(-5, 5), random.uniform(-5, 5)), colour = (0, 0, 255))
#player = entity.entPlane(pos = (ground.groundlen / 2, 300), vel = (4, 2), player = True)
player = entity.entPlane(pos = (groundmap[0][0] / 2, groundmap[0][1] / 2), vel = (4, 2), player = True)
#player = entity.Entity(pos = (ground.groundlen / 2, 300), vel = (4, 2), sprite = sprclass.pilot, player = True)

groundoffset = player.pos[0]

col = collision._collide(b1, b2)
move = True

bulletcount = 0

pygame.key.set_repeat(0, 0)

dibs = texture.mapTexture.call_lists[1]

running = 1
while running:
    startticks = pygame.time.get_ticks()
    control.Control.keyevents = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            maptex.delete()
            # if texture.Texture.textures.values():
                # glDeleteTextures(texture.Texture.textures.values())
            # for i in texture.mapTexture.textures:
                # glDeleteTextures(i)
            sys.exit()
        if event.type == pygame.KEYDOWN:
            control.Control.keyevents.append(event.key)
            if event.key == pygame.K_c:
                print "collision anticipated in", col[2], "frames. (", col[1], ")"                
            elif event.key == pygame.K_p:
                move = not move
            elif event.key == pygame.K_e:
                if player.sprite == sprclass.plane:
                    entity.entPlane(pos = player.pos, vel = (0,0))
                    player.sprite = sprclass.pilot
                    player.size = len(player.sprite[0]), len(player.sprite)
                    #player.ctlfunc = control.player_pilot
        if event.type == pygame.MOUSEMOTION:
            #mouse._move(event.pos)
            if event.buttons[0]:
                if pygame.key.get_pressed()[pygame.K_LCTRL]:
                    b1._move((b1.pos[0] + event.rel[0], b1.pos[1] - event.rel[1]))
                else:
                    b2._move((b2.pos[0] + event.rel[0], b2.pos[1] - event.rel[1]))    

    control.Control.keys = pygame.key.get_pressed()

    groundoffset = player.pos[0]
    if groundoffset + math.fabs(player.vel[0]) < width / 2:
        groundoffset = width / 2
    elif groundoffset + math.fabs(player.vel[0]) >= groundmap[0][0] - width / 2:
        groundoffset = groundmap[0][0] - width / 2	

    # environment collisions, control functions
    if(move):
        for e in entity.Entity.entities:
            e.age += 1
            if e.age >= e.expiry and e.expiry > 0:
                print "dead: {}" .format(e)
                e.delete()
                continue
            if not e.interact:
                continue
            
            e.ctlfunc.process()

            # shouldn't be here
            if e.vel[0] or e.vel[1]:
                e._move((e.pos[0] + e.vel[0], e.pos[1] + e.vel[1]))
            xs = list(map((lambda (x,_): x), e.vertices()))
            left = min(xs)
            right = max(xs)
            ys = list(map((lambda (_, y): y), e.vertices()))
            top = max(ys)
            bottom = min(ys)
            if left < 0:
                e._move((e.size[0] / 2, e.pos[1]))
                e.vel = (-e.vel[0], e.vel[1])
#            elif right > width:
            elif right >= groundmap[0][0]: # ... >= ground.groundlen:
#                e._move((width - (e.size[0] / 2), e.pos[1]))
                e._move((groundmap[0][0] - (e.size[0] / 2) - 1, e.pos[1])) # e._move((ground.groundlen - (e.size[0] / 2) - 1, e.pos[1]))
                e.vel = (-e.vel[0], e.vel[1])
    
            if top >= height:
                e._move((e.pos[0], height - (e.size[1] / 2)))
                e.vel = (e.vel[0], -e.vel[1])
            elif bottom < 0:
                e._move((e.pos[0], e.size[1] / 2))
                e.vel = (e.vel[0], -e.vel[1])

	    # ground collision
            base = height
            peak = 0
            isbase = False
            ispeak = False
            for vs in groundmap[1][int(left) : int(right)]:
                i = 0
                if len(vs) == 2:
                    print "wtf?"
                while i < len(vs):
                    if i == 0: # lowest ground (0 <= y <= vs[0])
                        if bottom < vs[0]:   # sinking below... ;_;
                            ispeak = True
                            if vs[0] > peak:
                                peak = vs[0]
                            break
                        i += 1
                    else:
                        if top > vs[i] and bottom < vs[i]: # bottom of a segment / ceiling above the sprite
                            isbase = True
                            if vs[i] < base:
                                base = vs[i]
                            break
                        if bottom < vs[i + 1] and top > vs[i + 1]: # top of a segment / floor below the sprite
                            ispeak = True
                            if vs[i + 1] > peak:
                                peak = vs[i + 1]
                            break
                        i += 2

            if isbase:
                e._move((e.pos[0], base - ((top - bottom) / 2)))
                e.vel = (e.vel[0], -e.vel[1])
            elif ispeak:
                e._move((e.pos[0], peak + ((top - bottom) / 2)))
                e.vel = (e.vel[0], -e.vel[1])

            #if bottom < peak:
            #    e._move((e.pos[0], peak + (e.size[1] / 2) + 1))
            #    e.vel = (e.vel[0], -e.vel[1])

    
    # check and resolve collisions
    collision.checkObjects()

    collision.sorttime()

    # draw shit
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(groundoffset - width / 2, groundoffset + width / 2, 0, height)
    glMatrixMode(GL_MODELVIEW)

    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    
    # draw ground. l/r boundaries are inclusive
    if groundoffset >= groundmap[0][0] - width / 2: # far right
        left = int((groundmap[0][0] - width) / texture.mapTexture.texsize)
        right = int(groundmap[0][0] / texture.mapTexture.texsize) - 1
    elif groundoffset <= width / 2: # far left
        left = 0
        right = int(width / texture.mapTexture.texsize)
    else: # a o k
        left = int((groundoffset - width / 2) / texture.mapTexture.texsize)
        right = left + int(width / texture.mapTexture.texsize) + 1
    #print left, right, "(", texture.mapTexture.cols, ")"
    
    glPushMatrix()
    glLoadIdentity()
    glEnable(GL_TEXTURE_2D)
    xoff = (left * texture.mapTexture.texsize)
    yoff = (texture.mapTexture.rows - 1) * texture.mapTexture.texsize
    #print xoff, yoff, left, right
    
    # columns, then rows. inconsistent, maybe fix it up later...
    i = left
    while i <= right and i < texture.mapTexture.cols:
        j = 0
        while j < texture.mapTexture.rows:
            glPushMatrix()
            glTranslatef(xoff + (i - left) * texture.mapTexture.texsize, yoff - (j * texture.mapTexture.texsize), 1.0)
            glCallList(texture.mapTexture.call_lists[j][i])
            glPopMatrix()
            j += 1
        i += 1
    
    glDisable(GL_TEXTURE_2D)
    glPopMatrix()
        
    for e in entity.Entity.entities:
#        xs = list(map((lambda (x,_): x), e.vertices()))
#        if max(xs) < groundoffset - width / 2:
#            continue
#        if min(xs) > groundoffset + width / 2:
#            continue
#        if e.player: # account for texture-based player too
#            sprclass.draw(e, pos = (width / 2, height / 2))
        if e.sprite:
            sprclass.draw(e)
        else:
            glBegin(GL_POLYGON)
            glColor3fv(e.colour)
            for x,y in e.vertices(): glVertex2f(x, y)
            glEnd()
        
    pygame.display.flip()    

    endticks = pygame.time.get_ticks()
    delay = (FDELAY - (endticks - startticks))
#    print "processing time: {}, delay: {}, bulletcount: {}" .format((endticks - startticks), delay, bulletcount)
    if delay < 0:
        delay = 0
    pygame.time.delay(int(round(delay))) # make variable based on processing time
