#MenuTitle: Expand Intermediate Masters
# -*- coding: utf-8 -*-

'''
This script takes all the intermediate masters it can find (called "Brace Layers" in Glyphs) and adds them as fully expanded masters to the font, 
then removes all brace layers.

This is necessary as a workaround for environments that can’t properly deal with brace layers, such as [googlefonts/fontmake](https://github.com/googlefonts/fontmake) 
as of this writing, August 2019. Once the brace layers are flattened into the font as fully expanded masters, everything interpolates correctly.

The masters will simply be added to the font’s master list at the end, not their correct positions in the list, which does not affect the interpolation.

Use this script only to generate static instances, not a Variable Font, as otherwise the font file size will increase.
To create Variable Fonts, use the `Create Missing Brace Layers in Components` script.
'''

from GlyphsApp import *
f = Glyphs.font


def braceLayerNameAsList(name):
	return list(map(float, layer.name.replace('{', '').replace('}', '').replace(' ', '').split(',')))

def braceLayerNameAsString(name):
	return str(name).replace('[', '').replace(']', '')


# Go through all glyphs and collect necessary intermediate master values
intermediateMasters = []
for glyph in f.glyphs:
	for layer in glyph.layers:
		
		if '{' in layer.name and '}' in layer.name:
			interpolationValues = braceLayerNameAsList(layer.name)
			if not interpolationValues in intermediateMasters:
				intermediateMasters.append(interpolationValues)

# Compare with present masters to avoid duplicates
for master in f.masters:
	if list(master.axes) in intermediateMasters:
		intermediateMasters.remove(list(master.axes))

# Create a temporary instance that matches a new intermediate master and add it as a master, one by one
for intermediateMaster in intermediateMasters:

	# Create new instance at intermediate master positions
	newInstance = GSInstance()
	f.instances.append(newInstance)
	newInstance.axes = intermediateMaster
	newInstance.name = braceLayerNameAsString(intermediateMaster)

	# Add interpolatedFont of instance as new master	
	interpolatedFont = newInstance.interpolatedFont
	f.addFontAsNewMaster_(interpolatedFont.masters[0])

	# Remove new instance
	f.instances.remove(newInstance)

	# Remove the currently treated brace layer from all glyphs
	# This is done here because if we wait till the very end to remove them, the newly created masters will all be the same somehow
	for glyph in f.glyphs:
		for layer in glyph.layers:
			if '{' in layer.name and '}' in layer.name:
				if braceLayerNameAsList(layer.name) == intermediateMaster:
					glyph.layers.remove(layer)

	print('Expanded %s into new master' % intermediateMaster)