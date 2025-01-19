import altair as alt, polars as pl
alt.renderers.enable('browser') # disable to show elsewhere

def scatter_sqm_price(df: pl.DataFrame): 
	df = pl.DataFrame([
		[ 575, 59, 2 ], [ 600, 54, 2 ], [ 585, 55, 1 ], [ 375, 36, 1 ], 
		[ 550, 45, 1 ], [ 350, 33, 1 ], [ 550, 63, 2 ], [ 575, 72, 2 ], 
		[ 395, 47, 1 ], [ 599, 79, 1 ], [ 375, 37, 1 ], [ 550, 63, 1 ], 
		[ 343, 34, 1 ], [ 565, 50, 2 ], [ 500, 47, 1 ], [ 399, 40, 1 ], 
		[ 450, 55, 1 ], [ 365, 38, 1 ], [ 600, 76, 1 ], [ 500, 57, 2 ], 
		[ 450, 54, 1 ], [ 335, 32, 0 ], [ 400, 38, 0 ], [ 495, 51, 2 ], 
		[ 550, 66, 3 ], [ 350, 36, 1 ], 
	]).transpose(column_names = ['price', 'sqm', 'beds'])

	df.plot.scatter(
		x = 'sqm:Q', 
		y = 'price:Q', 
		color = 'beds:N'
	).show()


