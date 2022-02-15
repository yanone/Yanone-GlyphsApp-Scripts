#MenuTitle: Open kerning pair in overview
# -*- coding: utf-8 -*-

import unicodedata

from GlyphsApp import *
f = Glyphs.font


texts = {
	'LlLl': 'mmmmmaaaammmmm',
	'LuLu': 'HHHHHaaaaHHHHH',
	'LuLl': 'mmmmmammmmm',
	'sc': '/h.sc/h.sc/h.sc/h.sc/h.sc/a/a/a/a/h.sc/h.sc/h.sc/h.sc/h.sc',
	'c2sc': '/h.sc/h.sc/h.sc/h.sc/h.sc',
}


layers = []

if f.currentTab:

	t = f.currentTab

	if t.textCursor >= 1 and len(t.text) >= 2:
	
		a = t.text[t.textCursor-1]
		b = t.text[t.textCursor]

		if a != '\n' and b != '\n':

			print(a, b)

			cat = None

			cat = unicodedata.category(a) + unicodedata.category(b)

			if cat in texts:

				for master in f.masters:

					text = texts[cat]
					if '/' in text:
						text = text.split('/')

					lineHasLetters = False

					for letter in text:
						if letter:
							if letter == 'a':
								layers.append(f.glyphs[a].layers[master.id])
								layers.append(f.glyphs[b].layers[master.id])
							else:
								layers.append(f.glyphs[letter].layers[master.id])
							lineHasLetters = True

					if lineHasLetters:
						layers.append(GSControlLayer(10))









if layers:


	# Tab
	if f.tabs:
		t = f.tabs[-1]
	else:
		t = f.newTab()
	f.currentTab = t
	t.layers = layers
