import pygame
import OpenGL
import definitions
import sys

from OpenGL.GL import *

def gen_tex((width, height), data):
    t = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, t)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
    return t

class Texture:
    textures = {}
        
    def __init__(self, ident, filename, texlist = None):
        if not texlist:
            texlist = Texture.textures

        surface = pygame.image.load(filename)
        width, height = surface.get_size()
        
        # SDL surfaces position (0, 0) at the top left. OpenGl data position (0, 0) at the bottom left.
        # 'True' here flips the data across a horizontal axis
        data = pygame.image.tostring(surface, "RGBA", True) 

        texlist[ident] = gen_tex((width, height), data)

    def delete(self, ident, texlist = None):
        if not texlist:
            texlist = Texture.textures

        OpenGL.glDeleteTextures(texlist[ident])
        texlist.pop(ident)
        
class mapTexture(Texture):
    textures = []
    call_lists = []
    
    def __init__(self, filename, texsize):
        surface = pygame.image.load(filename)
        width, height = surface.get_size()
        
        rows = height / texsize
        cols = width / texsize
        
        mapTexture.rows, mapTexture.cols, mapTexture.texsize = rows, cols, texsize
        
        # can be optimized... just call glGenTextures with more arguments
        i = 0
        while i < rows:
            mapTexture.textures.append(glGenTextures(cols))
            j = 0
            while j < cols:
                temp_surface = surface.subsurface((j * texsize, i * texsize, texsize, texsize))
                data = pygame.image.tostring(temp_surface, "RGBA", True)
                
                glBindTexture(GL_TEXTURE_2D, mapTexture.textures[i][j])
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, texsize, texsize, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)
                j += 1
            i += 1
    
    def gen_lists(self):
        i = 0
        while i < mapTexture.rows:
            # beginning of range allocated by glGenLists
            toff = glGenLists(mapTexture.cols)
            mapTexture.call_lists.append(range(toff, toff + mapTexture.cols))
            
            j = toff
            while j < toff + mapTexture.cols:
                glNewList(mapTexture.call_lists[i][j - toff], GL_COMPILE)
                
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, mapTexture.textures[i][j - toff])
                
                glColor4f(1.0, 1.0, 1.0, 1.0)
                glBegin(GL_QUADS)
                glTexCoord2f(0.0, 0.0); glVertex2f(0.0, 0.0)
                glTexCoord2f(1.0, 0.0); glVertex2f(mapTexture.texsize, 0.0)
                glTexCoord2f(1.0, 1.0); glVertex2f(mapTexture.texsize, mapTexture.texsize)
                glTexCoord2f(0.0, 1.0); glVertex2f(0.0, mapTexture.texsize)
                glEnd()
                glDisable(GL_TEXTURE_2D)
                
                glEndList()
                j += 1
            i += 1

    def delete(self):
        i = 0
        print len(mapTexture.call_lists)
        while i < mapTexture.rows:
            glDeleteTextures(mapTexture.textures[i])
            glDeleteLists(mapTexture.call_lists[i][0], mapTexture.cols)
            i += 1
