#MenuTitle: Create Missing Brace Layers in Components
# -*- coding: utf-8 -*-

'''
This script goes through all component glyphs and adds missing intermediate masters (called "Brace Layers" in Glyphs)
to the component glyphs where their respective base glyphs have them. For instance, if an `e` has a brace layer, 
all glyphs based on it such as `é` etc. also need a brace layer at the same value.

This is necessary to create correct Variable Fonts in environments outside Glyphs 
(such as [googlefonts/fontmake](https://github.com/googlefonts/fontmake), and even in Glyphs itself 
as of this writing, August 2019).

Otherwise, component glyphs’ metrics get interpolated linearly between the main masters, ignoring the 
intermediate masters, while the outlines get interpolated correctly. This leads to sidebearing discrepancies 
of component glyphs with base glyphs referencing intermediate masters.
'''

from GlyphsApp import *
f = Glyphs.font

def normalizeBraceLayerName(name):
	return name.replace(' ', '').replace(',', ', ')

def glyphHasBraceLayer(g):
	for l in g.layers:
		if '{' in l.name and '}' in l.name:
			return True
	return False

def glyphBraceLayerNames(g):
	'''Return layer names and associatedMasterIds as list'''
	layerNames = []
	for l in g.layers:
		if '{' in l.name and '}' in l.name:
			newLayerName = normalizeBraceLayerName(l.name)
			if not newLayerName in layerNames:
				layerNames.append([newLayerName, l.associatedMasterId])
	return layerNames

# Go through glyphs
for g in f.glyphs:
	for l in g.layers:
		if l.components:
			for c in l.components:
				if glyphHasBraceLayer(c.component):

					# Remove duplicates already present in component glyph
					createBraceLayerNames = glyphBraceLayerNames(c.component)
					for layerName, associatedMasterId in glyphBraceLayerNames(g):
						if [normalizeBraceLayerName(layerName), associatedMasterId] in createBraceLayerNames:
							createBraceLayerNames.remove([normalizeBraceLayerName(layerName), associatedMasterId])

					# Insert new brace layers
					for layerName, associatedMasterId in createBraceLayerNames:
						newLayer = GSLayer()
						newLayer.associatedMasterId = associatedMasterId
						newLayer.name = layerName
						g.layers.append(newLayer)
						newLayer.reinterpolate()
