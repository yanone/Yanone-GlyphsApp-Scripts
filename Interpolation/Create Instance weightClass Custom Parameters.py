#MenuTitle: Create Instance weightClass Custom Parameters
# -*- coding: utf-8 -*-

'''
In order to properly create instances from a VF using fontmake,
the font needs to carry appropriate weightClass parameters on the instances.
This script creates them.
'''

from GlyphsApp import *
f = Glyphs.font

weights = {
'Thin': 100,
'ExtraLight': 200,
'UltraLight': 100,
'Light': 300,
'Normal': 400,
'Regular': 400,
'Medium': 500,
'DemiBold': 600,
'SemiBold': 600,
'Bold': 700,
'UltraBold': 800,
'ExtraBold': 800,
'Black': 900,
'Heavy': 900,
}

for i in f.instances:
	i.customParameters['weightClass'] = weights[i.weight]
