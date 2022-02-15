#MenuTitle: Create empty missing SC
# -*- coding: utf-8 -*-

l = []
font = Glyphs.font

f.disableUpdateInterface()

sourceGlyphNames = []
for glyph in font.glyphs:
	if glyph.category == 'Letter' and glyph.subCategory == 'Lowercase':
		sourceGlyphNames.append(glyph.name)

# Create SC paths
for glyphName in sourceGlyphNames:

	scGlyphName = glyphName + '.sc'

	# Create glyph if not existent
	if not font.glyphs.has_key(scGlyphName):
		font.glyphs.append(GSGlyph(scGlyphName))

font.updateFeatures()
f.enableUpdateInterface()
