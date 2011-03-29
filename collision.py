# collision module
# while the control module handles path modification and corresponding velocity changes,
# the collision module decides whether these velocity changes are possible, and if so,
# enacts them

import cell
import entity
import vectors
import math
from definitions import *

# k it goes like this, run through all occupied cells and check for collisions. if 
# the cell's flag is set for revisal, include the corresponding flagged objects in the check.
# in every case, if an object's trajectory brings it to another cell(s) by the next step,
# flag it and the cell. by the end of the first iteration, if there are flagged cells
# whose contents have been entirely checked (i.e. all the objects flagged for that cell
# were flagged before the cell was checked), unflag the cells. repeat once.
# best case scenario, there is one iteration through n cells, checking o objects, and 
# 

# BIG NOTE: i have a hunch that integration would be handy to know if angular collisions come into play

def _collide(e1, e2):
    # orthogonally project the polygons onto the normal of each face. if all intersect,
    # the polygons intersect
    v = [e1.vertices(), e2.vertices()]

    col = True          # currently colliding
    colfuture = False   # will collide within one step
    minstep = 999999    # for a collision this frame, 0 <= step <= 1
    
    # cut some corners if both objects are rectangular and axis-aligned

    aa = False
    if len(v[0]) == 4 and len(v[1]) == 4 and False: # two boxes. remove the False when code is fixed
        a = sorted(v[0])
        b = sorted(v[1])

        for i in [a, b]:
            if i[0][0] != i[1][0] or a[2][0] != a[3][0]: # should be two unique x values (lists sorted by x val)
                break
            elif i[0][1] != i[2][1] or i[1][1] != i[3][1]: # should be two unique y values
                break
        else: # axis aligned
            xs1 = ys1 = xs2 = ys2 = []
            for i in a:
                xs1 += i[0]
                ys1 += i[1]
            for i in b:
                xs2 += i[0]
                ys2 += i[1]

            coords = [(xs1, ys1), (xs2, ys2)]        

            overx = False
            if min(xs1) > max(xs2):
                maxx, minx = xs1, xs2
                maxxe, minxe = e1, e2
            elif min(xs2) > max(xs1):
                maxx, minx = xs2, xs1
                maxxe, minxe = e2, e1
            else:                       # they're overlapping on x. what if the shape moves right past?
                overx = True

            overy = False
            if min(ys1) > max(ys2):
                maxy, miny = ys1, ys2
                maxye, minye = e1, e2
            elif min(ys2) > max(ys1):
                maxy, miny = ys2, ys1
                maxye, minye = e2, e1
            else:                       # they're overlapping on y
                overy = True

            if overx and overy:
                col = True
                colfuture = True
                minstep = 0
                aa = True
            else:
#needs work
                tx = (minxe.pos[0] - maxxe.pos[0]) / (maxxe.vel[0] - minxe.vel[0])
                ty = (minye.pos[1] - maxye.pos[1]) / (maxye.vel[1] - maxye.vel[1])

    j = 0
    while j < 2 and not aa:
        i = 0
        while i < len(v[j]):
            axis = vectors.normalize((-(v[j][i][1] - v[j][i-1][1]), v[j][i][0] - v[j][i-1][0])) # axis of projection / normal
    
            # first poly
            min1 = max1 = vectors.dot(axis, v[0][0]) # the magnitude of a projection onto a unit vector is just their dot product
            #min1p = max1p = v[0][0]
            n = 0
            while n < len(v[0]):
                proj = vectors.dot(axis, v[0][n])
                if proj > max1:
                    max1 = proj
                    #max1p = v[0][n]
                elif proj < min1:
                    min1 = proj
                    #min1p = v[0][n]
                n += 1
    
            #off = vectors.dot(axis, e1.pos)
            #min1 += off
            #max1 += off

            # second poly
            min2 = max2 = vectors.dot(axis, v[1][0])
            #min2p = max2p = v[1][0]
            n = 0
            while n < len(v[1]):
                proj = vectors.dot(axis, v[1][n])
                if proj > max2:
                    max2 = proj
                    #max2p = v[1][n]
                elif proj < min2:
                    min2 = proj
                    #min2p = v[1][n]
                n += 1
            
            #off = vectors.dot(axis, e2.pos)
            #min2 += off
            #max2 += off

            #print "j:", j, "i:", i
            #print "axis:", axis, "normal of:", v[j][i], "and", v[j][i - 1]
            #print "\tmin1:", min1, "max2:", max2, "min2:", min2, "max1:", max1
            #print "\tmin1:", min1p, "max2:", max2p, "min2:", min2p, "max1:", max1p
            if min1 > max2 or min2 > max1: # potential for collision!!
                col = False
                
                # they are not overlapping, so both values of one projection (a) are larger than both values for the other (b)
                if(min1 > max2): # min1 will touch max2 on collision
                    a, b = min1, max2
                    ae, be = e1, e2
                elif(min2 > max1): # min2 will touch max1 on collision
                    a, b = min2, max1
                    ae, be = e2, e1

                # multiply the axis' unit vector by the vector magnitudes to find their coordinates
                maxp, minp = (axis[0] * a, axis[1] * a), (axis[0] * b, axis[1] * b) 

                #print "collision anticipated at step ="
                # prevent division by zero error. they are not moving or are moving at the same speed
                #if be.vel[1] - ae.vel[1]: 
                #    step = (axis[0] - maxp[1] + minp[1]) / (be.vel[1] - ae.vel[1])
                #    print "\t", step
                #    if 0 <= step < minstep:
                #        minstep = step
                #if ae.vel[0] - be.vel[0]:
                #    step = (axis[1] - minp[0] + maxp[0]) / (ae.vel[0] - be.vel[0])
                #    print "\t", step
                #    if 0 <= step < minstep:
                #        minstep = step
                denom = (axis[0] * (ae.vel[0] - be.vel[0])) + (axis[1] * (ae.vel[1] - be.vel[1]))
                if denom:  
                    # "eggs"-planation: the magnitude of the step factor is the parameter value that brings two objects from different points on the
                    # projection axis to the same point. the sign of the step factor is determined by the object whose projection is largest in
                    # magnitude, as this object is always bound to 'a' and 'ae'. if this object lies below the point of intersection,
                    # the step factor will be positive, as its value needs to increase to reach the point. likewise, if it lies below, 
                    # the movement is downwards, and the step factor will be negative. so we take the absolute value of the whole thing if we just
                    # want the step size
                    step = math.fabs((axis[0] * (minp[0] - maxp[0])) + (axis[1] * (minp[1] - maxp[1])) / denom)
                    #print "\t", step
                    if step < minstep:
                        minstep = step

                if minstep <= 1: # who cares if the collision isn't happening this turn
                    colfuture = True
            i += 1
        j += 1
#    if col:
#        print "axis:", axis
#        print "\tmin1:", min1, "max2:", max2, "min2:", min2, "max1:", max1
#        print "\tmin1:", min1p, "max2:", max2p, "min2:", min2p, "max1:", max1p

    return (col, colfuture, minstep)

def checkObjects():
    flagsc = {} # cells flagged for revision
    flagso = [] # objects flagged for revision
    
    for c in cell.Grid.dcells:
        objlist = cell.Grid.dcells[c] #  + flagsc[c]
        if len(objlist) < 2: # skip if single-object cell
            continue
        if not filter(lambda a: not isinstance(a, entity.entBullet), objlist): # skip if entirely bullets
            continue

#        print "cell {}: {}" .format(c, objlist)
                
        i = len(objlist) - 1
        while i > 0:
            # inter-cell movement flag. kind of inefficient
            #pos = objlist[i].pos
            #cells = objlist[i].cells
            #objlist[i]._move((objlist[i].pos[0] + objlist[i].vel[0], objlist[i].pos[1] + objlist[i].vel[1]))
            #if cells != objlist[i]:
            #    if flagsc
            #    flagsc[a] for a in list(set(cells).intersection(objlist[i])))
            #    flagso.append(objlist[i])
            #objlist[i]._move(pos)

            j = i - 1
            while j >= 0:
                if isinstance(objlist[i], entity.entBullet) and isinstance(objlist[j], entity.entBullet): # skip bullet-bullet collision
                    j -= 1 
                    continue
            
                c = _collide(objlist[i], objlist[j])
                
                # resolve collisions
                if c[0] or c[1]:
                    if isinstance(objlist[i], entity.entBullet) or isinstance(objlist[j], entity.entBullet):  # bullets
                        print "i: {}, len(objlist): {}" .format(i, len(objlist))
                        if isinstance(objlist[i], entity.entBullet):
                            objlist[j].health -= DMG_BULLET
                            objlist[i].delete()
                            i -= 2              # iterating down the list, so decrementing i brings us two elements down the old list, but one element down the new one.
                            continue            # in this case the root of the iteration is being deleted, so we need to move two down the new one
                        else:
                            objlist[i].health -= DMG_BULLET
                            objlist[j].delete()
                            i -= 1
                
#                if c[0]:
#                    print "collision: {}({}) {}({})" .format(objlist[i], objlist[i].pos, objlist[j], objlist[j].pos)
#                elif c[1]:
#                    print "collision ({} steps): {} {}" .format(c[2], objlist[i], objlist[j])
#                    
                j -= 1
            #_collide(objlist[i], 
            i -= 1
