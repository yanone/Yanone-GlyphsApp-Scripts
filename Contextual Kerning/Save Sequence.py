# MenuTitle: Save Sequence
# -*- coding: utf-8 -*-

from GlyphsApp import Glyphs

font = Glyphs.font
tab = font.currentTab


if font.userData["de.yanone.contextualKerning.name"]:

    # Read kerning from font
    kerning_at_traditional_kerning_pair = {}
    for master in font.masters:
        kerning_at_traditional_kerning_pair[master.id] = font.kerningForPair(
            master.id,
            font.userData["de.yanone.contextualKerning.traditionalKerningPair"][0],
            font.userData["de.yanone.contextualKerning.traditionalKerningPair"][1],
            tab.direction,
        )

    # See if we even need to save contextual kerning
    save = False
    for master in font.masters:
        if kerning_at_traditional_kerning_pair[master.id]:
            contextual_kerning_value = (kerning_at_traditional_kerning_pair[master.id] or 0) - (
                font.userData["de.yanone.contextualKerning.traditionalKerningValue"][master.id] or 0
            )
            if contextual_kerning_value:
                save = True

    # Set stored contextual kerning value
    for master in font.masters:

        # Save only if there is a difference
        if save:
            # If user has deleted the kerning pair during the contextual kerning editing
            # we want to set the contextual kerning value to 0 and the traditional kerning
            # value to the stored value.
            if kerning_at_traditional_kerning_pair[master.id]:
                contextual_kerning_value = (kerning_at_traditional_kerning_pair[master.id] or 0) - (
                    font.userData["de.yanone.contextualKerning.traditionalKerningValue"][master.id] or 0
                )
            else:
                contextual_kerning_value = 0
            master.setNumberValueValue_forName_(
                contextual_kerning_value,
                font.userData["de.yanone.contextualKerning.name"],
            )

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

    if save:
        print("Contextual kerning saved and deactivated.")
    else:
        print("Contextual kerning deactivated. Nothing was saved.")
