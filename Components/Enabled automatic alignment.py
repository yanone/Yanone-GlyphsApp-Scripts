#MenuTitle: Enabled automatic alignment
# -*- coding: utf-8 -*-

from GlyphsApp import *
f = Glyphs.font

f.disableUpdateInterface()

for glyph in f.glyphs:
	if glyph.selected:
		for layer in glyph.layers:
			for component in layer.components:
				component.automaticAlignment = True

f.enableUpdateInterface()