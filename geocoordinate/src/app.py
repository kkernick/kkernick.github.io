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
from shiny.types import FileInfo
from folium import Map as FoliumMap
from folium.plugins import HeatMap
from pandas import DataFrame, read_csv, read_excel, read_table
from pathlib import Path
from io import BytesIO
from sys import modules
from copy import deepcopy

from shared import Table

# Fine, Shiny
import branca, certifi, xyzservices


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
	Base = {}

	Info = {
		"example1.txt": "This example dataset shows deaths from a cholera outbreak in 1854. John Snow used this data in conjunction with local pump locations as evidence that cholera is spread by contaminated water. A digitised version of the data is available online, courtesy of Robin Wilson (robin@rtwilson.com).",
		"example2.txt": "This example data set shows bike thefts in Vancouver in 2011. The data was obtained from a 2013 Vancouver Sun blog post by Chad Skelton.",
		"example3.txt": "This example data set shows the location of traffic signals in Toronto. The data was obtained from Toronto Open Data. The idea to use this data set comes from this R-bloggers post by Myles Harrison."
	}


	def HandleData(n, i):
		"""
		@brief Given the file name n, handle the file at i
		@param n The name of the file, extension is used to differentiate
		@param i The path to the file.
		"""
		match Path(n).suffix:
			case ".csv": df = read_csv(i)
			case ".xlsx": df = read_excel(i)
			case _: df = read_table(i)
		return df.fillna(0)


	async def RawData():
		"""
		@brief Returns a DataFrame containing the heatmap table
		@returns 	A DataFrame, who's format can either be a matrix grid, or a chart
							containing x, y, and value columns.
		"""

		# Grab an uploaded file, if its done, or grab an example (Using a cache to prevent redownload)
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.File()
			if file is None:
					return DataFrame()
			n = file[0]["name"]

			if n not in Base: Base[n] = HandleData(n, file[0]["datapath"])
		else:
			n = input.Example()
			if n not in Base: Base[n] = HandleData(n, BytesIO(await download(Source + n)))

		if n not in Cache: Cache[n] = deepcopy(Base[n])
		return n


	async def LoadData(): n = await RawData(); return DataFrame() if n is None else Cache[n]


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
	@render.data_frame
	@reactive.event(input.Update, input.Reset, input.Example, input.File, ignore_none=False, ignore_init=False)
	async def LoadedTable(): return await LoadData()


	@output
	@render.ui
	@reactive.event(input.Update, input.Reset, input.Example, input.File, input.UpdateMap, ignore_none=False, ignore_init=False)
	async def Map(): return await LoadMap()


	@output
	@render.text
	def ExampleInfo(): return Info[input.Example()]


	@render.download(filename="table.csv")
	async def DownloadTable(): df = await LoadData(); yield df.to_string()


	@render.download(filename="heatmap.html")
	async def DownloadHeatmap(): m = await LoadMap(); yield m.get_root().render()


	@reactive.Effect
	@reactive.event(input.Update)
	async def Update():
		"""
		@brief Updates the value in the table with the one the user typed in upon updating
		"""

		# Get the data
		df = await LoadData()

		row_count, column_count = df.shape
		row, column = input.TableRow(), input.TableCol()

		# So long as row and column are sane, update.
		if row < row_count and column < column_count:
			match input.Type():
				case "Integer": df.iloc[row, column] = int(input.TableVal())
				case "Float": df.iloc[row, column] = float(input.TableVal())
				case "String": df.iloc[row, column] = input.TableVal()


	@reactive.Effect
	@reactive.event(input.Reset)
	async def Reset(): del Cache[await RawData()]


	@reactive.Effect
	@reactive.event(input.TableRow, input.TableCol, input.Example, input.File, input.Reset, input.Update)
	async def UpdateTableValue():
		"""
		@brief Updates the label for the Value input to display the current value.
		"""
		df = await LoadData()

		rows, columns = df.shape
		row, column = int(input.TableRow()), int(input.TableCol())

		if 0 <= row <= rows and 0 <= column <= columns:
			ui.update_text(id="TableVal", label="Value (" + str(df.iloc[row, column]) + ")"),


app_ui = ui.page_fluid(

	ui.panel_title(title=None, window_title="Heatmapper"),
	ui.navset_bar(
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/expression/site/index.html target="_blank" rel="noopener noreferrer">Expression</a>'), value="Expression"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/pairwise/site/index.html target="_blank" rel="noopener noreferrer">Pairwise</a>'), value="Pairwise"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/image/site/index.html target="_blank" rel="noopener noreferrer">Image</a>'), value="Image"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/geomap/site/index.html target="_blank" rel="noopener noreferrer">Geomap</a>'), value="Geomap"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/geocoordinate/site/index.html target="_blank" rel="noopener noreferrer">Geocoordinate</a>'), value="Geocoordinate"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/about/site/index.html target="_blank" rel="noopener noreferrer">About</a>'), value="About"),
		title="Heatmapper",
		selected="Geocoordinate",
	),

	ui.layout_sidebar(
		ui.sidebar(

			# If the user needs help with the formatting.
			ui.HTML('<a href=https://kkernick.github.io/about/site/index.html target="_blank" rel="noopener noreferrer">Data Format</a>'),

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

			ui.input_action_button("UpdateMap", "Update Heatmap"),

			ui.br(),

			# All the features related to map customization are here.
			ui.HTML("Map Customization"),

			# Only OpenStreatMap and CartoDB Positron seem to work.
			ui.input_radio_buttons(id="MapType", label="Map Type", choices=["OpenStreetMap", "CartoDB Positron"], selected="CartoDB Positron"),

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),
			ui.input_slider(id="Radius", label="Size of Points", value=25, min=5, max=50, step=5),
			ui.input_slider(id="Blur", label="Blurring", value=15, min=1, max=30, step=1),

			# Add the download buttons.
			"Download",
			ui.download_button("DownloadHeatmap", "Heatmap"),
			ui.download_button("DownloadTable", "Table"),

			id="SidebarPanel",
		),

		# Add the main interface tabs.
		ui.navset_tab(
				ui.nav_panel("Interactive", ui.output_ui("Map")),
				Table,
		),
	)
)

app = App(app_ui, server)