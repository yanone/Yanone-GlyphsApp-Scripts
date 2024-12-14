# MenuTitle: Update auto-metrics
# -*- coding: utf-8 -*-

import unicodedata

from GlyphsApp import *

f = Glyphs.font

f.disableUpdateInterface()

for glyph in f.selection:
    for layer in glyph.layers:
        layer.syncMetrics()

f.enableUpdateInterface()
