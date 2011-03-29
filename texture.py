import pygame
import OpenGL
import definitions
import sys

class Texture:
	textures = {}

	def __init__(self, ident, filename, texlist = None):
		if not texlist:
			texlist = Texture.textures

		surface = pygame.image.load(filename)
		(width, height) = surface.get_size()
		data = pygame.image.tostring(pygame.image.load(filename), "RGBA", True) # SDL surfaces position (0, 0) at the top left. OpenGl data position (0, 0) at the bottom left. 'True' here flips the data across a horizontal axis

		t = OpenGL.glGenTextures(1)
		OpenGL.glBindTexture(GL_TEXTURE_2D, t)
		OpenGL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
		OpenGL.glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_FILTER, GL_LINEAR)
		OpenGL.glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_UNSIGNED_BYTE, data)
		texlist[ident] = t

	def delete(self, ident, texlist = None):
		if not texlist:
			texlist = texture.Texture.textures

		OpenGL.glDeleteTextures(texlist[ident])
		texlist.pop(ident)
