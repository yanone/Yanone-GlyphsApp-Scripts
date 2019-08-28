Collection of my Glyphs.app scripts.

If you like, you can clone this repository directly into Glyphs.app’s script folder which is normally located at `~/Application Support/Glyphs/Scripts`.

In Glyphs.app, you will then find the scripts in the Scripts menu under `Yanone-GlyphsApp-Scripts`.

# Contents

## Interpolation

### Create Missing Brace Layers in Components

This script goes through all component glyphs and adds missing intermediate masters (called "Brace Layers" in Glyphs) to the component glyphs where their respective base glyphs have them. For instance, if an `e` has a brace layer, all glyphs based on it such as `é` etc. also need a brace layer at the same value.

This is necessary to create correct Variable Fonts in environments outside Glyphs (such as [googlefonts/fontmake](https://github.com/googlefonts/fontmake), and even in Glyphs itself as of this writing, August 2019).

Otherwise, component glyphs’ metrics get interpolated linearly between the main masters, ignoring the intermediate masters, while the outlines get interpolated correctly. This leads to sidebearing discrepancies of component glyphs with base glyphs referencing intermediate masters between instances of a Variable Font and the same instance when generated statically from within Glyphs, when the metrics are interpolated correctly.

### Expand Intermediate Masters

This script takes all the intermediate masters it can find (called "Brace Layers" in Glyphs) and adds them as fully expanded masters to the font, then removes all brace layers.

This is necessary as a workaround for environments that can’t properly deal with brace layers, such as [googlefonts/fontmake](https://github.com/googlefonts/fontmake) as of this writing, August 2019. Once the brace layers are flattened into the font as fully expanded masters, everything interpolates correctly.

The masters will simply be added to the font’s master list at the end, not their correct positions in the list, which does not affect the interpolation.