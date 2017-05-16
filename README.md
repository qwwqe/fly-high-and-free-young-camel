# Fly High and Free Young Camel

**FHFYC** is an SDL/OpenGL clone of the “Sopwith” sidescroller written in Python. I loved this game as a child and wanted better multiplayer support and custom maps. So I wrote this.

Below is a basic description of the components.

**cell.py** - Defines the collision grid which the map is divided into, as well as
	a few functions for adding and deleting cells, and finding objects in cells.
	Before any entities are instantiated, the Grid class should be instantiated
	once. They will automatically be placed in the appropriate cells based on their
	position and size. Don't spawn Grid objects twice, or the existing grid will be 
	overwritten.

**collision.py** - Defines the generic polygon-polygon collision detection routine (_collide), 
	which with a little teaking should work independently of this project, as well as 
	the collision handling loop used specifically for the game.

**control.py** - Defines modes of behaviour for various entities, including human input.
	For AI, this will eventually contain long term behaviour and its short term
	implementation.

**definitions.py** - Global definitions.

**entity.py** - Defines entities and their default values.

**ground.py** - Height map array.

**sprite.py** - Arrays for simulated pixel sprites.

**testgl.py** - Sandboxing stuff.

**texture.py** - Texture loading for entities. Unused.

**vectors.py** - Functions related to vector manipulation.
