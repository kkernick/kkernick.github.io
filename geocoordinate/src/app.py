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
# Last Modified: 2024/02/07
#


from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo
from folium import Map as FoliumMap
from folium.plugins import HeatMap
from pandas import DataFrame, read_csv, read_excel, read_table
from pathlib import Path
from io import BytesIO
from sys import modules


# Interoperability between ShinyLive and PyShiny
if "pyodide" in modules:
	from pyodide.http import pyfetch
	Source = "https://raw.githubusercontent.com/kkernick/kkernick.github.io/main/geocoordinate/example_input/"
	async def download(url): r = await pyfetch(url); return await r.bytes() if r.ok else None
else:
	from os.path import exists
	Source = "../example_input/"
	async def download(url): return open(url, "rb").read() if exists(url) else None


def server(input: Inputs, output: Outputs, session: Session):

	Cache = {}
	Info = {
		"example1.txt": "This example dataset shows deaths from a cholera outbreak in 1854. John Snow used this data in conjunction with local pump locations as evidence that cholera is spread by contaminated water. A digitised version of the data is available online, courtesy of Robin Wilson (robin@rtwilson.com).",
		"example2.txt": "This example data set shows bike thefts in Vancouver in 2011. The data was obtained from a 2013 Vancouver Sun blog post by Chad Skelton.",
		"example3.txt": "This example data set shows the location of traffic signals in Toronto. The data was obtained from Toronto Open Data. The idea to use this data set comes from this R-bloggers post by Myles Harrison."
	}


	async def LoadData():
		"""
		@brief Returns the DataFrame representation of the data to place on the map
		@returns The DataFrame
		"""

		# Grab an uploaded file, if its done, or grab an example (Using a cache to prevent redownload)
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.File()
			if file is None:
					return DataFrame()
			n = file[0]["name"]
			f = file[0]["datapath"]
		else:
			n = input.Example()
			f = Cache[n] if n in Cache else BytesIO(await download(Source + input.Example()))

		match Path(n).suffix:
			case ".csv": return read_csv(f)
			case ".xlsx": return read_excel(f)
			case _: return read_table(f)


	async def LoadMap():
		"""
		@brief Generates a map with the provided information
		@returns the Folium.Map
		"""

		df = await LoadData()

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
	@render.table
	async def LoadedTable(): return await LoadData()


	@output
	@render.ui
	async def Map(): return await LoadMap()


	@output
	@render.text
	def ExampleInfo(): return Info[input.Example()]


	@session.download(filename="table.csv")
	async def DownloadTable(): yield await LoadData().to_string()


	@session.download(filename="heatmap.html")
	async def DownloadHeatmap(): yield await LoadMap().get_root().render()



app_ui = ui.page_fluid(

	ui.panel_title(title=None, window_title="Heatmapper"),
	ui.navset_bar(
		ui.nav_panel(ui.HTML("<a href=https://kkernick.github.io/expression/site/index.html>Expression</a>"), value="Expression"),
		ui.nav_panel(ui.HTML("<a href=https://kkernick.github.io/pairwise/site/index.html>Pairwise</a>"), value="Pairwise"),
		ui.nav_panel(ui.HTML("<a href=https://kkernick.github.io/image/site/index.html>Image</a>"), value="Image"),
		ui.nav_panel(ui.HTML("<a href=https://kkernick.github.io/geomap/site/index.html>Geomap</a>"), value="Geomap"),
		ui.nav_panel(ui.HTML("<a href=https://kkernick.github.io/geocoordinate/site/index.html>Geocoordinate</a>"), value="Geocoordinate"),
		ui.nav_panel(ui.HTML("<a href=https://kkernick.github.io/about/site/index.html>About</a>"), value="About"),
		title="Heatmapper",
		selected="Geocoordinate",
	),

	ui.layout_sidebar(
		ui.sidebar(

			# If the user needs help with the formatting.
			ui.HTML("<a href=https://kkernick.github.io/about/site/index.html>Data Format</a>"),

			# Specify whether to use example files, or upload one.
			ui.input_radio_buttons(id="SourceFile", label="Specify a Source File", choices=["Example", "Upload"], selected="Example"),

			# Only display an input dialog if the user is one Upload
			ui.panel_conditional(
				"input.SourceFile === 'Upload'",
				ui.input_file("File", "Choose a File", accept=[".csv", ".txt", "xlsx"], multiple=False),
			),

			# Otherwise, add the example selection and an info button.
			ui.panel_conditional(
				"input.SourceFile === 'Example'",

				# Put them side-by-side.
				ui.layout_columns(

					ui.input_select(id="Example", label=None, choices={
						"example1.txt": "Example 1",
						"example2.txt": "Example 2",
						"example3.txt": "Example 3"},
						multiple=False),
					ui.popover(ui.input_action_link(id="ExampleInfoButton", label="Info"), ui.output_text("ExampleInfo")),
					col_widths=[10,2],
				)
			),

			# All the features related to map customization are here.
			ui.HTML("Map Customization"),

			# Only OpenStreatMap and CartoDB Positron seem to work.
			ui.input_radio_buttons(id="MapType", label="Map Type", choices=["OpenStreetMap", "CartoDB Positron"], selected="CartoDB Positron"),

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),
			ui.input_slider(id="Radius", label="Size of Points", value=25, min=5, max=50, step=5),
			ui.input_slider(id="Blur", label="Blurring", value=15, min=1, max=30, step=1),

			# Add the download buttons.
			ui.layout_columns(
				ui.download_button("DownloadHeatmap", "Download Heatmap"),
				ui.download_button("DownloadTable", "Download Table")
			),


			id="SidebarPanel",
			width=350
		),

		# Add the main interface tabs.
		ui.navset_tab(
				ui.nav_panel("Interactive", ui.output_ui("Map")),
				ui.nav_panel("Table", ui.output_table("LoadedTable"),),
		),
	)
)

app = App(app_ui, server)