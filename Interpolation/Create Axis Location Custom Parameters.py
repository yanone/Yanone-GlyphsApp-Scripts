#MenuTitle: Create Axis Location Custom Parameters
# -*- coding: utf-8 -*-

'''
In order to properly create instances from a VF using fontmake,
the font needs to carry appropriate Axis Location parameters on the masters.
This script creates them.
'''

from GlyphsApp import *
f = Glyphs.font

fontAxesNames = [f.customParameters['Axes'][x]['Name'] for x in range(len(f.customParameters['Axes']))] 

for m in f.masters:
	masterAxes = []
	for i, axisName in enumerate(fontAxesNames):
		masterAxes.append({'Axis': axisName, 'Location': m.axes[i]})
	m.customParameters['Axis Location'] = masterAxes