Collection of my Glyphs.app scripts.

If you like, you can clone this repository directly into Glyphs.app’s script folder which is normally located at `~/Application Support/Glyphs/Scripts`.

In Glyphs.app, you will then find the scripts in the Scripts menu under `Yanone-GlyphsApp-Scripts`.

# Contents

## Interpolation

### Expand Intermediate Masters

This script takes all the intermediate masters it can find (called "Brace Layers" in Glyphs) and adds them as fully expanded masters to the font, then removes all brace layers.

This is necessary as a workaround for environments that can’t properly deal with brace layers, such as [googlefonts/fontmake](https://github.com/googlefonts/fontmake) as of this writing. Once the brace layers are flattened into the font as fully expanded masters, everything interpolates correctly.

The masters will simply be added to the font’s master list at the end, not their correct positions in the list, which does not affect the interpolation.