import sys, pygame
import cell, entity, vectors, collision
import math
import random
import ground
import control

import sprite as sprclass

from definitions import *

from OpenGL.GL import *
from OpenGL.GLU import *

FDELAY = (1.0/float(FPS)) * 1000 # FPS in definitions

width, height = 700, 500

pygame.init()
screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.OPENGL)

glClearColor(0.0, 0.0, 0.0, 0.0)    
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

glMatrixMode(GL_PROJECTION)
glLoadIdentity()
gluOrtho2D(0, width, 0, height)
glMatrixMode(GL_MODELVIEW)

#glEnable(GL_TEXTURE_2D)
#glEnable(GL_BLEND)
#glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

grid = cell.Grid((14, 10), (50, 50))
b1 = entity.Entity(size = (40, 30), pos = (300, 100), vel = (random.uniform(-5, 5), random.uniform(-5, 5)), colour = (255, 0, 0))
b2 = entity.Entity(size = (70, 40), pos = (500, 300), vel = (random.uniform(-5, 5), random.uniform(-5, 5)), colour = (0, 0, 255))
player = entity.entPlane(pos = (ground.groundlen / 2, 300), vel = (4, 2), player = True)
#player = entity.Entity(pos = (ground.groundlen / 2, 300), vel = (4, 2), sprite = sprclass.pilot, player = True)

groundoffset = player.pos[0]

col = collision._collide(b1, b2)
move = True

bulletcount = 0

pygame.key.set_repeat(0, 0)

running = 1
while running:
    startticks = pygame.time.get_ticks()
    control.Control.keyevents = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYDOWN:
            control.Control.keyevents.append(event.key)
            if event.key == pygame.K_c:
                print "collision anticipated in", col[2], "frames. (", col[1], ")"                
            elif event.key == pygame.K_p:
                move = not move
#            elif event.key == pygame.K_COMMA or event.key == pygame.K_SLASH:
#                if event.key == pygame.K_COMMA:
#                    player.rot += ROT_PLANE_INT
#                else:
#                    player.rot -= ROT_PLANE_INT
#                player.vel = vectors.component(vectors.length(player.vel), player.rot)
#            elif event.key == pygame.K_d:
#                if vectors.length(player.vel) > 1:
#                    player.vel = vectors.component(vectors.length(player.vel) - 1, player.rot)                
#            elif event.key == pygame.K_f:
#                player.vel = vectors.component(vectors.length(player.vel) + 1, player.rot)
#            elif event.key == pygame.K_SPACE:
#                player.ctlfunc.shoot("WEAP_BULLET")
#                bulletcount += 1
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
    elif groundoffset + math.fabs(player.vel[0]) >= ground.groundlen - width / 2:
        groundoffset = ground.groundlen - width / 2
#    print "gro: {}" .format(groundoffset)	

    # environment collisions, control functions
    if(move):
        for e in entity.Entity.entities:
            e.age += 1
            if e.age >= e.expiry and e.expiry > 0:
                print "dead: {}" .format(e)
                e.delete()
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
            elif right >= ground.groundlen:
#                e._move((width - (e.size[0] / 2), e.pos[1]))
                e._move((ground.groundlen - (e.size[0] / 2) - 1, e.pos[1]))
                e.vel = (-e.vel[0], e.vel[1])
    
            if top >= height:
                e._move((e.pos[0], height - (e.size[1] / 2)))
                e.vel = (e.vel[0], -e.vel[1])
            elif bottom < 0:
                e._move((e.pos[0], e.size[1] / 2))
                e.vel = (e.vel[0], -e.vel[1])

	    # ground collision
            if e.size[0] > 1:
                peak = max(ground.ground[int(e.pos[0] - (e.size[0] / 2)):int(e.pos[0] + (e.size[0] / 2))])
            else:
#		print e.pos[0]
                peak = ground.ground[int(e.pos[0])] # peak = ground.ground[int(e.pos[0])], IndexError: list index out of range

            if bottom < peak:
                e._move((e.pos[0], peak + (e.size[1] / 2) + 1))
                e.vel = (e.vel[0], -e.vel[1])

    
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
    i = groundoffset - width / 2
    glBegin(GL_LINE_STRIP)
    glColor3fv([255, 255, 255])
#    glVertex2f(0, 0)
    while i < groundoffset + width / 2:
#        glVertex2f(i, ground.ground[int(groundoffset - width / 2) + int(i - (groundoffset - width / 2))])
	if i >= ground.groundlen:
		print "i: {}, groundoffset: {}, groundoffset + w / 2: {}" .format(i, groundoffset, groundoffset + width / 2)
	glVertex2f(i, ground.ground[int(i)])
        i += 1
#    glVertex2f(width, 0)
    glEnd()
    
    pygame.display.flip()    

    endticks = pygame.time.get_ticks()
    delay = (FDELAY - (endticks - startticks))
#    print "processing time: {}, delay: {}, bulletcount: {}" .format((endticks - startticks), delay, bulletcount)
    if delay < 0:
        delay = 0
    pygame.time.delay(int(round(delay))) # make variable based on processing time
