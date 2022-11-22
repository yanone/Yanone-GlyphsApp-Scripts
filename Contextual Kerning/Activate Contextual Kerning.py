# MenuTitle: Activate Contextual Kerning
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

Glyphs.showMacroWindow()
Glyphs.clearLog()

if font.userData["de.yanone.contextualKerning.name"]:
    print(f"Contextual kerning already active for {font.userData['de.yanone.contextualKerning.name']}. Save first.")
else:

    substitution = f"{glyph_or_class(tab.textCursor - 1)}' {glyph_or_class(tab.textCursor)} {glyph_or_class(tab.textCursor + 1)}"
    sequence = contextual_kerning_name()
    name = base64.b32encode(sequence.encode()).decode().replace("=", "_")

    # Read kerning from font
    kerning_at_traditional_kerning_pair = {}
    for master in font.masters:
        kerning_at_traditional_kerning_pair[master.id] = font.kerningForPair(
            master.id,
            traditional_kerning_pair[0],
            traditional_kerning_pair[1],
            tab.direction,
        )

    # Read store contextual kerning value
    stored_contextual_kerning_values = {}
    for master in font.masters:
        stored_contextual_kerning_values[master.id] = master.numberValueValueForName_(name)

    print(f'Contextual kerning activated for "{sequence}"')

    # Get stored kerning value from number values
    for master in font.masters:
        # Apply stored value to "traditional" kerning
        font.setKerningForPair(
            master.id,
            traditional_kerning_pair[0],
            traditional_kerning_pair[1],
            (stored_contextual_kerning_values[master.id] or 0) + (kerning_at_traditional_kerning_pair[master.id] or 0),
            tab.direction,
        )

    font.userData["de.yanone.contextualKerning.name"] = name
    font.userData["de.yanone.contextualKerning.traditionalKerningPair"] = traditional_kerning_pair
    font.userData["de.yanone.contextualKerning.traditionalKerningValue"] = kerning_at_traditional_kerning_pair
