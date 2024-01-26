from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo

import numpy as np
import pandas as pd

import jinja2

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


from PIL import Image

from io import StringIO, BytesIO

def server(input: Inputs, output: Outputs, session: Session):

	# Returns the data of whatever we should generate our map off of.
	def LoadData():

		# To work well with StringIO
		ext = ""

		# If we have an upload file, try and open it.
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.File()
			if file is None:
					return pd.DataFrame()
			f = file[0]["datapath"]
			ext = f
		else:
			# TODO: Actually implement the example
			return pd.DataFrame()

		# Handle extensions.
		if ext.endswith(".csv"):
			return pd.read_csv(f)
		elif ext.endswith(".xlsx"):
			return pd.read_xlsx(f)
		else:
			return pd.read_table(f)


	def LoadImage():
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.Image()
			if file is None:
					return None
			return Image.open(file[0]["datapath"])

	def GenerateHeatmap():
		df = LoadData()
		img = LoadImage()

		if df.empty:
			return None

		# Wrangle into an acceptable format.
		if {'x', 'y', 'value'}.issubset(df.columns):
			df = df.pivot(index='y', columns='x', values='value')
				
		fig, ax = plt.subplots()

		# Add the image as an overlay
		if img is not None:
			ax.imshow(img, extent=[0, 1, 0, 1], aspect='auto',zorder=0)

		im = ax.imshow(df, cmap='viridis', interpolation=input.Interpolation(), aspect='auto', extent=[0, 1, 0, 1], zorder=1, alpha=input.Opacity())

		cbar = plt.colorbar(im, ax=ax, label='Value')

		plt.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labelleft=False)

		return ax


	@output
	@render.table
	def LoadedTable():
		return LoadData()

	@output
	@render.plot
	def Heatmap():
		return GenerateHeatmap()

	@session.download(filename="table.csv")
	def DownloadTable():
		yield LoadData().to_string()

	@session.download(filename="heatmap.png")
	def DownloadHeatmap():
		ax = GenerateHeatmap()

		output = BytesIO()
		FigureCanvasAgg(ax.figure).print_png(output)

		output.seek(0)
		yield output.read()

		

app_ui = ui.page_fluid(
	# Place the Heatmapper Home on the top.
	ui.panel_title(ui.HTML('<a href="https://kkernick.github.io">Heatmapper</a>')),
	ui.layout_sidebar(
		ui.sidebar(

			# If the user needs help with the formatting.
			ui.HTML("<a href=https://kkernick.github.io/about/site/index.html>Data Format</a>"),

			# Specify whether to use example files, or upload one.
			ui.input_radio_buttons(id="SourceFile", label="Specify a Source File", choices=["Example", "Upload"], selected="Example"),

			# Only display an input dialog if the user is one Upload
			ui.panel_conditional(
				"input.SourceFile === 'Upload'",
				ui.input_file("Image", "Choose your Image File", accept=[".png", ".jpg"], multiple=False),
				ui.input_file("File", "Choose your Grid File", accept=[".csv", ".txt", "xlsx"], multiple=False),
			),

			ui.br(),

			ui.HTML("Heatmap Customization"),

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),
			
			ui.input_select(id="Interpolation", label="Interpolation", choices={
					"antialiased": "Antialiased", 
					"bilinear": "Bilinear",
					"bicubic": "Bicubic",
					"quadric": "Quadric",
					"gaussian": "Gaussian"
				}, 
				multiple=False, selected="bilinear"),

			ui.br(),

			# Add the download buttons.
			ui.layout_columns(
				ui.download_button("DownloadTable", "Download Table"),
				ui.download_button("DownloadHeatmap", "Download Heatmap")
			),

			id="SidebarPanel",
			width=350
		),

		# Add the main interface tabs.
		ui.navset_tab(

				# The map
				ui.nav_panel("Interactive", ui.output_plot("Heatmap")),

				# The table
				ui.nav_panel("Table", ui.output_table("LoadedTable"),),
		),
	)
)	

app = App(app_ui, server)