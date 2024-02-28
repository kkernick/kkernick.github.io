#
# Heatmapper
# Image
#
# This file contains the ShinyLive application for Image Heatmapper.
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
from matplotlib.pyplot import subplots, colorbar
from pandas import DataFrame, read_csv, read_excel, read_table
from PIL import Image
from io import BytesIO
from sys import modules
from pathlib import Path
from copy import deepcopy


# Interoperability between ShinyLive and PyShiny
if "pyodide" in modules:
	from pyodide.http import pyfetch
	Source = "https://raw.githubusercontent.com/kkernick/kkernick.github.io/main/image/example_input/"
	async def download(url): r = await pyfetch(url); return await r.bytes() if r.ok else None
else:
	from os.path import exists
	Source = "../example_input/"
	async def download(url): return open(url, "rb").read() if exists(url) else None


def server(input: Inputs, output: Outputs, session: Session):

	# Cache the example to prevent multiple fetches.
	Base = {}
	Cache = {}

	# Information regarding example files.
	Info = {
		"Example 1": {
			"Table": "example1.txt",
			"Image": "example1.jpg",
			"Description": "Hypothetical example illustrating data overlaid on a satellite image. Input data are count or magnitude values within the overlaid grid sections."
		}
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
			n = Info[input.Example()]["Table"]
			if n not in Base: Base[n] = HandleData(n, BytesIO(await download(Source + n)))

		if n not in Cache: Cache[n] = deepcopy(Base[n])
		return n


	async def LoadData(): n = await RawData(); return DataFrame() if n is None else Cache[n]


	async def LoadImage():
		"""
		@brief Loads the image to render behind the heatmap.
		@returns an Image object, if an image is specified, otherwise None.
		"""

		# Grab an uploaded file, if its done, or grab an example (Using a cache to prevent redownload)
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.Image()
			return None if file is None else Image.open(file[0]["datapath"])
		else:
			n = Info[input.Example()]["Image"]
			return Cache[n] if n in Cache else Image.open(BytesIO(await download(Source + n)))


	async def GenerateHeatmap():
		"""
		@brief Generates the heatmap, overlaying the Image with the DataFrame
		@returns The Plot's axis, for downloading purposes.
		"""

		df = await LoadData()
		img = await LoadImage()

		if df.empty: return None

		# Wrangle into an acceptable format.
		if {"x", "y", "value"}.issubset(df.columns):
			df = df.pivot(index="y", columns="x", values="value")

		fig, ax = subplots()

		# Add the image as an overlay, if we have one.
		if img is not None: ax.imshow(img, extent=[0, 1, 0, 1], aspect="auto",zorder=0)
		im = ax.imshow(df, cmap=input.ColorMap().lower(), interpolation=input.Interpolation().lower(), aspect="auto", extent=[0, 1, 0, 1], zorder=1, alpha=input.Opacity())

		# Visibility of features
		if "legend" in input.Features(): colorbar(im, ax=ax, label="Value")

		if "y" in input.Features():
			ax.tick_params(axis="y", labelsize=input.TextSize())
		else:
			ax.set_yticklabels([])

		if "x" in input.Features():
			ax.tick_params(axis="x", labelsize=input.TextSize())
		else:
			ax.set_xticklabels([])

		return ax


	@output
	@render.data_frame
	@reactive.event(input.Update, input.Reset, input.Example, input.File, ignore_none=False, ignore_init=False)
	async def LoadedTable(): return await LoadData()


	@output
	@render.plot
	@reactive.event(input.Update, input.Reset, input.Example, input.File, input.UpdateMap, ignore_none=False, ignore_init=False)
	async def Heatmap(): return await GenerateHeatmap()


	@output
	@render.text
	def ExampleInfo(): return Info[input.Example()]["Description"]


	@render.download(filename="table.csv")
	async def DownloadTable(): df = await LoadData(); yield df.to_string()


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
		selected="Image",
	),

	ui.layout_sidebar(
		ui.sidebar(

			# If the user needs help with the formatting.
			ui.HTML('<a href=https://kkernick.github.io/about/site/index.html target="_blank" rel="noopener noreferrer">Data Format</a>'),

			# Specify whether to use example files, or upload one.
			ui.input_radio_buttons(id="SourceFile", label="Specify a Source File", choices=["Example", "Upload"], selected="Example", inline=True),

			# Only display an input dialog if the user is one Upload
			ui.panel_conditional(
				"input.SourceFile === 'Upload'",
				ui.input_file("Image", "Choose your Image File", accept=[".png", ".jpg"], multiple=False),
				ui.input_file("File", "Choose your Grid File", accept=[".csv", ".txt", "xlsx"], multiple=False),
			),

			# Otherwise, add the example selection and an info button.
			ui.panel_conditional(
				"input.SourceFile === 'Example'",
				"Choose an Example File",
				ui.layout_columns(
					ui.input_select(id="Example", label=None, choices=["Example 1"]),
					ui.popover(ui.input_action_link(id="ExampleInfoButton", label="Info"), ui.output_text("ExampleInfo")),
					col_widths=[10,2],
				)
			),

			ui.input_action_button("UpdateMap", "Update Heatmap"),

			ui.br(),

			# Customize the text size of the axes.
			ui.input_numeric(id="TextSize", label="Text Size", value=8, min=1, max=50, step=1),

			# Customize the opacity of the heatmap, making the background image more visible.
			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),

			# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
			ui.input_select(id="Interpolation", label="Interpolation", choices=["None", "Antialiased", "Nearest", "Bilinear", "Bicubic", "Spline16", "Spline36", "Hanning", "Hamming", "Hermite", "Kaiser", "Quadric", "Catrom", "Gaussian", "Bessel", "Mitchell", "Sinc", "Lanczos", "Blackman"], selected="Bilinear"),

			# Set the ColorMap used.
			ui.input_select(id="ColorMap", label="Color Map", choices=["Viridis", "Plasma", "Inferno", "Magma", "Cividis"], selected="Viridis"),

			# Customize what aspects of the heatmap are visible
			ui.input_checkbox_group(id="Features", label="Heatmap Features",
					choices={"x": "X Labels", "y": "Y Labels", "legend": "Legend"},
					selected=["legend"]),

			# Add the download buttons.
			ui.download_button("DownloadTable", "Download Table"),

			id="SidebarPanel",
		),

		# Add the main interface tabs.
		ui.navset_tab(
				ui.nav_panel("Interactive", ui.output_plot("Heatmap", height="90vh")),
				ui.nav_panel("Table",
					ui.layout_columns(
						ui.input_numeric("TableRow", "Row", 0),
						ui.input_numeric("TableCol", "Column", 0),
						ui.input_text("TableVal", "Value", 0),
						ui.input_select(id="Type", label="Datatype", choices=["Integer", "Float", "String"]),
						col_widths=[2,2,6,2],
					),
					ui.layout_columns(
						ui.input_action_button("Update", "Update"),
						ui.input_action_button("Reset", "Reset Values"),
					),
					ui.output_data_frame("LoadedTable"),
				),
		),
	)
)

app = App(app_ui, server)