#MenuTitle: Polytonic Greek UC & SC
# -*- coding: utf-8 -*-

f = Glyphs.font

l = []

f.disableUpdateInterface()

for g in f.glyphs:
	if g.selected:
		

		# Automatic alignment ON
		for l in g.layers:
			for c in l.components:
				c.automaticAlignment = True

		# Automatic alignment ON
		for l in g.layers:
			for c in l.components:
				c.automaticAlignment = False

		g.leftMetricsKey = g.layers[0].components[-1].componentName
		g.rightMetricsKey = g.layers[0].components[0].componentName

		# Kerning Key
		g.leftKerningGroup = ''
		g.rightKerningGroup = g.layers[0].components[0].component.rightKerningGroup

		# Sync Metrics
		for l in g.layers:
			l.syncMetrics()

f.enableUpdateInterface()
