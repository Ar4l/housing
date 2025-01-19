# todo: one day add a background from openstreetmap using Altair Tiles
# (would be nice to visualise the canals)

import altair as alt, polars as pl, geopandas as gpd
alt.renderers.enable('browser') # disable to show elsewhere
alt.data_transformers.disable_max_rows()

# Variables 
buurten = [
	'Frans Halsbuurt', 
	'Gerard Doubuurt', 
	'Hercules Seghersbuurt', 
	'Sarphatiparkbuurt', 
	'Hemonybuurt', 
	'Willibrordusbuurt', 
	'Diamantbuurt',
	'Burgemeester Tellegenbuurt-Oost', 
	'BurgemeesterTellegenbuurt-West', 
	'Van der Helstpleinbuurt',
	'Lizzy Ansinghbuurt',
	'Cornelis Troostbuurt', 
]

# Retrieved from https://cartomap.github.io/nl/
buurten_data = ('https://cartomap.github.io/nl/rd/buurt_2024.topojson', 'buurt_2024')
# wijken_data = ('https://cartomap.github.io/nl/rd/wijk_2024.topojson', 'wijk_2024')
geo_data = gpd.read_file(buurten_data[0])

# code for Amsterdam, according to 
# https://download.cbs.nl/regionale-kaarten/kwb-2024.xlsx
geo_data = geo_data[
	geo_data.statcode.str.contains('0363') 
	& ~geo_data.statnaam.str.contains('Buitengebied Achterveld')
] 
# geo_data = geo_data[geo_data.statnaam.isin(buurten)]

# for col in geo_data[geo_data.statnaam.eq('Frans Halsbuurt')]: 
# 	print(f'{col}\n\n{geo_data[col]}\n\n\n')
print(f'{set(buurten) - set(geo_data.statnaam)} missing!')

# Other data scraped from funda 
funda_data = pl.DataFrame()
columns = ['avg sqm price', 'bedrooms']

buurt_filter = alt.selection_point('statnaam', 'Hemonybuurt')
click_state = alt.selection_point('statnaam')# alt.selection_single(fields=['statnaam'])
opacity = alt.when(click_state).then(alt.value(1)).otherwise(alt.value(0.2))

# plot this biatch
cloropleth = (
	alt.Chart(geo_data)
	.mark_geoshape(
		stroke = 'white', strokeWidth = 2.0,
	)
	# .transform_lookup(
	# 	lookup = 'statnaam',
	# 	from_  = alt.LookupData(funda_data, 'statnaam', columns)
	# )
	.encode(
		tooltip = ['statnaam:N', 'statcode:N'],
		opacity = opacity, 
	)
	.project(
		'identity',		# stick with raw coordinates
		reflectY = True,  # necessary for svg
		# scale: [0.001, 0.000999643366619117],
		# translate = [3.363, 50.751],
		# scale = 2,
	)
	.add_params(click_state)
	.transform_filter(dict(field='statnaam', oneOf=buurten))
	.properties(
		width = 800, height = 800,
	)
)
cloropleth.show()

