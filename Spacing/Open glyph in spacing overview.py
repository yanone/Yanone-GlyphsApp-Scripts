#MenuTitle: Open glyph in spacing overview
# -*- coding: utf-8 -*-

import unicodedata

from GlyphsApp import *
f = Glyphs.font

texts = {
	'Ll': 'mmmmammmmaaammmm',
	'Lu': 'HHHHaHHHHaaaHHHH',
	'Nd': 'HHHHaHHHHaaaHHHH',
	'sc': '/h.sc/h.sc/h.sc/h.sc/a/h.sc/h.sc/h.sc/h.sc/a/a/a/h.sc/h.sc/h.sc/h.sc',
	'c2sc': '/h.sc/h.sc/h.sc/h.sc/a/h.sc/h.sc/h.sc/h.sc/a/a/a/h.sc/h.sc/h.sc/h.sc',
}

layers = []
newCursorPosition = 0

g = None

if f.currentTab:

	t = f.currentTab

	if t.layers:
		g = t.layers[t.textCursor].parent


if not g and f.selection:
	# Set Tab

	# Glyph
	g = f.selection[0]

if g:

	cat = None

	if g.string:
		cat = unicodedata.category(g.string)

	else:
		l = list(set(g.name.split('.')) & set(texts.keys()))
		if l:
			cat = l[0]

	if cat in texts:

		for master in f.masters:

			text = texts[cat]
			if '/' in text:
				text = text.split('/')

			lineHasLetters = False
			i = 0
			for letter in text:
				if letter:
					if letter == 'a':
						layers.append(g.layers[master.id])
						if newCursorPosition == 0:
							newCursorPosition = i
					else:
						layers.append(f.glyphs[letter].layers[master.id])
					lineHasLetters = True
				i += 1

			if lineHasLetters:
				layers.append(GSControlLayer(10))

	else:
		print('%s not defined' % cat)

if layers:


	# Tab
	if f.tabs:
		t = f.tabs[-1]
	else:
		t = f.newTab()
	f.currentTab = t
	t.layers = layers
	t.textCursor = newCursorPosition
