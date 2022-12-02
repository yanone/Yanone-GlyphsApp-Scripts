# MenuTitle: Delete Sequence
# -*- coding: utf-8 -*-

from GlyphsApp import Glyphs, GSRTL
import base64

font = Glyphs.font
tab = font.currentTab


def glyph_or_class(i):

    glyph = tab.layers[i].parent
    if i >= tab.textCursor:
        if tab.direction == GSRTL:
            return glyph.rightKerningKey
        else:
            return glyph.leftKerningKey
    else:
        if tab.direction == GSRTL:
            return glyph.leftKerningKey
        else:
            return glyph.rightKerningKey


def contextual_kerning_name():
    return f"kern {'RTL' if tab.direction == GSRTL else 'LTR'}: {substitution}"


traditional_kerning_pair = [
    glyph_or_class(tab.textCursor - 1),
    glyph_or_class(tab.textCursor),
]

if not font.userData["de.yanone.contextualKerning.name"]:
    Glyphs.clearLog()
    print(f"Need to activate a contextual kerning sequence first.")
else:

    # Set stored contextual kerning value
    for master in font.masters:

        # Set all to 0
        # TODO:
        # Actually remove here
        master.setNumberValueValue_forName_(0, font.userData["de.yanone.contextualKerning.name"])

        # Restore traditional kerning value
        if font.userData["de.yanone.contextualKerning.traditionalKerningValue"][master.id]:
            font.setKerningForPair(
                master.id,
                font.userData["de.yanone.contextualKerning.traditionalKerningPair"][0],
                font.userData["de.yanone.contextualKerning.traditionalKerningPair"][1],
                font.userData["de.yanone.contextualKerning.traditionalKerningValue"][master.id],
                tab.direction,
            )
        else:
            font.removeKerningForPair(
                master.id,
                font.userData["de.yanone.contextualKerning.traditionalKerningPair"][0],
                font.userData["de.yanone.contextualKerning.traditionalKerningPair"][1],
                tab.direction,
            )

    # Reset stored userData
    font.userData["de.yanone.contextualKerning.name"] = ""
    font.userData["de.yanone.contextualKerning.traditionalKerningPair"] = ""
    font.userData["de.yanone.contextualKerning.traditionalKerningValue"] = ""

    Glyphs.clearLog()
    print(f"Deleted sequence")
