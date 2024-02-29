#
# Heatmapper
# Geocoordinate
#
# This file contains the ShinyLive application for Geocoordinate Heatmapper.
# It can be run with the following command within this directory:
#		shinylive export . [site]
# Where [site] is the destination of the site folder.
#
# If you would rather deploy the application as a PyShiny application,
# run the following command within this directory:
#		shiny run
#
#


from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from folium import Map as FoliumMap
from folium.plugins import HeatMap
from pandas import DataFrame

from shared import Table, Cache, NavBar, FileSelection

# Fine, Shiny
import branca, certifi, xyzservices


def server(input: Inputs, output: Outputs, session: Session):

	Info = {
		"example1.txt": "This example dataset shows deaths from a cholera outbreak in 1854. John Snow used this data in conjunction with local pump locations as evidence that cholera is spread by contaminated water. A digitised version of the data is available online, courtesy of Robin Wilson (robin@rtwilson.com).",
		"example2.txt": "This example data set shows bike thefts in Vancouver in 2011. The data was obtained from a 2013 Vancouver Sun blog post by Chad Skelton.",
		"example3.txt": "This example data set shows the location of traffic signals in Toronto. The data was obtained from Toronto Open Data. The idea to use this data set comes from this R-bloggers post by Myles Harrison."
	}

	DataCache = Cache("geocoordinate")

	async def LoadMap():
		"""
		@brief Generates a map with the provided information
		@returns the Folium.Map
		"""

		df = await DataCache.Load(input)

		# Give a placeholder map if nothing is selected, which should never really be the case.
		if df.empty: return FoliumMap((53.5213, -113.5213), tiles=input.MapType(), zoom_start=15)

		# Get the long and lat.
		longitudes = df["Longitude"].tolist()
		latitudes = df["Latitude"].tolist()

		# Guess the associated value for plotting.
		values = []
		for option in ["Value", "Year"]:
			if option in df:
				values = df[option].tolist()
				break
		if not values: values = [1] * len(longitudes)


		#  Get the data ready.
		data = list(zip(latitudes, longitudes, values))

		# Find a decent initial zoom.
		map = FoliumMap((latitudes[0], longitudes[0]), tiles=input.MapType())
		HeatMap(data, min_opacity=input.Opacity(), radius=input.Radius(), blur=input.Blur()).add_to(map)
		map.fit_bounds(map.get_bounds())

		return map


	@output
	@render.data_frame
	@reactive.event(input.Update, input.Reset, input.Example, input.File, ignore_none=False, ignore_init=False)
	async def LoadedTable(): return await DataCache.Load(input)


	@output
	@render.ui
	@reactive.event(input.Update, input.Reset, input.Example, input.File, input.UpdateMap, ignore_none=False, ignore_init=False)
	async def Map(): return await LoadMap()


	@output
	@render.text
	def ExampleInfo(): return Info[input.Example()]


	@render.download(filename="table.csv")
	async def DownloadTable(): df = await DataCache.Load(input); yield df.to_string()


	@render.download(filename="heatmap.html")
	async def DownloadHeatmap(): m = await LoadMap(); yield m.get_root().render()


	@reactive.Effect
	@reactive.event(input.Update)
	async def Update(): await DataCache.Update(input)


	@reactive.Effect
	@reactive.event(input.Reset)
	async def Reset(): await DataCache.Purge(input)


	@reactive.Effect
	@reactive.event(input.TableRow, input.TableCol, input.Example, input.File, input.Reset, input.Update)
	async def UpdateTableValue():
		"""
		@brief Updates the label for the Value input to display the current value.
		"""
		df = await DataCache.Load(input)

		rows, columns = df.shape
		row, column = int(input.TableRow()), int(input.TableCol())

		if 0 <= row <= rows and 0 <= column <= columns:
			ui.update_text(id="TableVal", label="Value (" + str(df.iloc[row, column]) + ")"),


app_ui = ui.page_fluid(

	NavBar("Geocoordinate"),

	ui.layout_sidebar(
		ui.sidebar(

			FileSelection(
				examples={"example1.txt": "Example 1", "example2.txt": "Example 2","example3.txt": "Example 3"},
				types=[".csv", ".txt", ".xlsx"]
			),

			ui.input_action_button("UpdateMap", "Update Heatmap"),

			ui.br(),

			# Only OpenStreatMap and CartoDB Positron seem to work.
			ui.input_radio_buttons(id="MapType", label="Map Type", choices=["OpenStreetMap", "CartoDB Positron"], selected="CartoDB Positron"),

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),
			ui.input_slider(id="Radius", label="Size of Points", value=25, min=5, max=50, step=5),
			ui.input_slider(id="Blur", label="Blurring", value=15, min=1, max=30, step=1),

			# Add the download buttons.
			ui.download_button("DownloadHeatmap", "Heatmap"),
			ui.download_button("DownloadTable", "Table"),
		),

		# Add the main interface tabs.
		ui.navset_tab(
				ui.nav_panel("Interactive", ui.output_ui("Map")),
				Table,
		),
	)
)

app = App(app_ui, server)