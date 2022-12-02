# MenuTitle: Show All Defined Sequences
# -*- coding: utf-8 -*-

from GlyphsApp import Glyphs, GSLTR, GSRTL, GSControlLayer
import base64
import re

font = Glyphs.font
tab = font.currentTab

Glyphs.clearLog()

class_match = re.compile(r"(@[a-zA-Z0-9_.-]+)")

NEWLINE = font.glyphs["space"].layers[font.selectedFontMaster.id]


def first_glyph_in_class(class_name, direction):
    if direction == "RTL":
        for glyph in font.glyphs:
            if "MMK_R_" in class_name and glyph.leftKerningKey == class_name:
                return glyph.name
            if "MMK_L_" in class_name and glyph.rightKerningKey == class_name:
                return glyph.name

    if direction == "LTR":
        for glyph in font.glyphs:
            if "MMK_R_" in class_name and glyph.leftKerningKey == class_name:
                return glyph.name
            if "MMK_L_" in class_name and glyph.rightKerningKey == class_name:
                return glyph.name


sequences = {}

for variable in [number.name() for number in font.masters[0].numbers()]:
    try:
        sequence = base64.b32decode(variable.replace("_", "=")).decode()
        direction, code = sequence.split(": ")
        direction = direction.split(" ")[1]

        code = code.replace("'", "")
        for class_name in class_match.findall(code):
            code = code.replace(class_name, f"{first_glyph_in_class(class_name, direction)}")

        if direction not in sequences:
            sequences[direction] = []
        sequences[direction].append(code)
    except:
        pass

for direction in sequences:
    if sequences[direction]:
        lines = []
        for sequence in sequences[direction]:
            glyphs = [font.glyphs[name] for name in sequence.split(" ")]
            lines.extend([glyph.layers[font.selectedFontMaster.id] for glyph in glyphs] + [NEWLINE])

        font.newTab(lines)
        tab = font.tabs[-1]
        if direction == "RTL":
            tab.direction = GSRTL
        else:
            tab.direction = GSLTR
