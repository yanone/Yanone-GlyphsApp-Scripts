# MenuTitle: Mark Inaccessible Glyphs
# -*- coding: utf-8 -*-

"""
Large fonts bear the potential to contain inaccessible glyphs.
Those are glyphs that are neither encoded (have a Unicode value), nor are accessible
through one of the OpenType features. 

This script marks glyphs as white that are either
encoded OR reachable through an OpenType substitution feature OR are 
contained in other glyphs as components. It marks glyphs red that are
not encoded AND not reachable through OpenType AND not used as components.

Depending on the setup of your font, you may want to either delete
the inaccessible glyphs from your font or make them accessible.

Tested only in Glyphs 3.
This requires fontTools. Install it on the command line with `pip install fontTools`.
"""

import os
import tempfile
import subprocess
import traceback

try:
    from fontTools.ttLib import TTFont
    from fontTools.subset import main as pyftsubset

except:
    Message("This script requires fontTools. Please install it in the command line using 'pip install fontTools'")

font = Glyphs.font
font.disableUpdateInterface()

# Append instance
instance = GSInstance()
instance.name = "inaccessibleglyphstest"
font.instances.append(instance)

try:
    # Paths
    tempDir = tempfile.gettempdir()
    filename = font.familyName.replace(" ", "") + "-" + instance.name.replace(" ", "") + ".otf"
    path = os.path.join(tempDir, filename)
    outPath = os.path.join(tempDir, filename.replace(".otf", ".subset.otf"))
    if os.path.exists(path):
        os.remove(path)
    if os.path.exists(outPath):
        os.remove(outPath)

    # Create temporary instance
    instance.generate(
        Format="OTF",
        FontPath=path,
        AutoHint=False,
        RemoveOverlap=False,
        UseSubroutines=False,
        UseProductionNames=False,
        DecomposeSmartStuff=False,
    )

    # Run pyftsubset (throws out the inaccessible glyphs)
    pyftsubset([path, "--unicodes=*", "--layout-features=*"])

    # Read results
    if os.path.exists(outPath):

        tt = TTFont(outPath)
        glyphsInFont = tt.getGlyphOrder()

        # Mark glyphs
        for glyph in font.glyphs:
            if glyph.name in glyphsInFont:
                glyph.color = None
            else:
                glyph.color = 0

        # Mark all components or non-exporting glyphs white
        for glyph in font.glyphs:
            if glyph.export is False:
                glyph.color = None
            elif glyph.color is None:
                for layer in glyph.layers:
                    if layer.components:
                        for component in layer.components:
                            component.component.color = None

        font.enableUpdateInterface()

        print("done")

    else:
        Message("Subset font wasn't created. Check the Macro panel for details.")

    if os.path.exists(path):
        os.remove(path)
    if os.path.exists(outPath):
        os.remove(outPath)

    # Remove temp instance
    if font.instances[-1].name == "inaccessibleglyphstest":
        del font.instances[-1]
except:
    print(traceback.format_exc())
    Message("Subset font wasn't created. Check the Macro panel for details.")

    # Remove temp instance
    if font.instances[-1].name == "inaccessibleglyphstest":
        del font.instances[-1]
