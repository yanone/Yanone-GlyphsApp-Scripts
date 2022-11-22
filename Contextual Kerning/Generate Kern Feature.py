# MenuTitle: Generate Kern Feature
# -*- coding: utf-8 -*-

from GlyphsApp import Glyphs, GSFeature
import base64
import re

font = Glyphs.font
tab = font.currentTab

Glyphs.clearLog()

###

class_match = re.compile(r"(@[a-zA-Z0-9_.-]+)")


def glyphs_in_class(class_name, direction):
    if direction == "RTL":
        for glyph in font.glyphs:
            if "MMK_R_" in class_name and glyph.leftKerningKey == class_name:
                yield glyph.name
            if "MMK_L_" in class_name and glyph.rightKerningKey == class_name:
                yield glyph.name

    if direction == "LTR":
        for glyph in font.glyphs:
            if "MMK_R_" in class_name and glyph.leftKerningKey == class_name:
                yield glyph.name
            if "MMK_L_" in class_name and glyph.rightKerningKey == class_name:
                yield glyph.name


###

kerning_per_direction = {}

# Read store contextual kerning value
for variable in [number.name() for number in font.masters[0].numbers()]:
    sequence = base64.b32decode(variable.replace("_", "=")).decode()
    direction, code = sequence.split(": ")
    direction = direction.split(" ")[1]
    if direction == "RTL":
        line = f"pos {code} <${variable} 0 ${variable} 0>;"
    else:
        line = f"pos {code} ${variable};"

    if direction not in kerning_per_direction:
        kerning_per_direction[direction] = []
    kerning_per_direction[direction].append(line)

feature_code = """# Automatic Code End

"""

for direction in kerning_per_direction:
    feature_code += f"""
lookup contextual_kerning_{direction} {{"""

    if direction == "RTL":
        feature_code += """
    lookupflag RightToLeft IgnoreMarks;
"""
    for line in kerning_per_direction[direction]:

        for class_name in class_match.findall(line):
            line = line.replace(class_name, f"[{' '.join(list(glyphs_in_class(class_name, direction)))}]")

        feature_code += f"""
    {line}"""
    feature_code += f"""
}} contextual_kerning_{direction};
"""

if font.features["kern"]:
    font.features["kern"].code = feature_code
else:
    font.features.append(GSFeature("kern", feature_code))

print("Generated kern feature")
