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
# Last Modified: 2024/02/06
#

from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo
import matplotlib.pyplot as plt
from pandas import DataFrame, read_csv, read_excel, read_table
from PIL import Image
from io import BytesIO
from sys import modules
from pathlib import Path


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
	Cache = {}

	# Information regarding example files.
	Info = {
		"Example 1": {
			"Table": "example1.txt",
			"Image": "example1.jpg",
			"Description": "Hypothetical example illustrating data overlaid on a satellite image. Input data are count or magnitude values within the overlaid grid sections."
		}
	}


	async def LoadData():
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
			f = file[0]["datapath"]
		else:
			n = input.Example()
			f = Cache[n] if n in Cache else BytesIO(await download(Source + Info[input.Example()]["Table"]))

		match Path(n).suffix:
			case ".csv": return read_csv(f)
			case ".xlsx": return read_excel(f)
			case _: return read_table(f)


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
			n = input.Example()
			return Cache[n] if n in Cache else Image.open(BytesIO(await download(Source + Info[input.Example()]["Image"])))


	async def GenerateHeatmap():
		"""
		@brief Generates the heatmap, overlaying the Image with the DataFrame
		@returns The Plot's axis, for downloading purposes.
		"""

		df = await LoadData()
		img = await LoadImage()

		if df.empty: return None

		# Wrangle into an acceptable format.
		if {'x', 'y', 'value'}.issubset(df.columns):
			df = df.pivot(index='y', columns='x', values='value')

		fig, ax = plt.subplots()

		# Add the image as an overlay, if we have one.
		if img is not None: ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto',zorder=0)
		im = ax.imshow(df, cmap=input.ColorMap().lower(), interpolation=input.Interpolation().lower(), aspect='auto', extent=[0, 1, 0, 1], zorder=1, alpha=input.Opacity())

		# Visibility of features
		if "legend" in input.Features(): plt.colorbar(im, ax=ax, label='Value')

		if "y" in input.Features():
			ax.tick_params(axis="y", labelsize=input.TextSize())
		else:
			ax.set_yticklabels([])

		if "x" in input.Features():
			ax.tick_params(axis="x", labelsize=input.TextSize())
		else:
			ax.set_xticklabels([])

		#plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)

		return ax


	@output
	@render.table
	async def LoadedTable(): return await LoadData()


	@output
	@render.plot
	async def Heatmap(): return await GenerateHeatmap()


	@output
	@render.text
	def ExampleInfo(): return Info[input.Example()]["Description"]


	@session.download(filename="table.csv")
	async def DownloadTable(): df = await LoadData(); yield df.to_string()


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
			ui.HTML("<a href=https://kkernick.github.io/about/site/index.html>Data Format</a>"),

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

			ui.HTML("Heatmap Customization"),

			ui.input_numeric(id="TextSize", label="Text Size", value=8, min=1, max=50, step=1),

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),

			# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
			ui.input_select(id="Interpolation", label="Interpolation", choices=["None", "Antialiased", "Nearest", "Bilinear", "Bicubic", "Spline16", "Spline36", "Hanning", "Hamming", "Hermite", "Kaiser", "Quadric", "Catrom", "Gaussian", "Bessel", "Mitchell", "Sinc", "Lanczos", "Blackman"], selected="Bilinear"),

			# Set the ColorMap used.
			ui.input_select(id="ColorMap", label="Color Map", choices=["Viridis", "Plasma", "Inferno", "Magma", "Cividis"], selected="Viridis"),

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
				ui.nav_panel("Table", ui.output_table("LoadedTable"),),
		),
	)
)

app = App(app_ui, server)