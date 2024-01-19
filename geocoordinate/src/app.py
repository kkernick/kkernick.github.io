from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo

# We need to import here so ShinyLive doesn't get upset.
import certifi, branca, xyzservices
import folium
from folium.plugins import HeatMap

import numpy as np
import pandas as pd

from pathlib import Path

from examples import examples


def server(input: Inputs, output: Outputs, session: Session):

	def LoadData():
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.File()
			if file is None:
					return pd.DataFrame()
			f = file[0]["datapath"]
		else:
			if not Path(input.ExampleFile()).is_file():
				file = open(input.ExampleFile() , 'w')
				file.write(examples[input.ExampleFile()]["data"])
				file.close()
			f = input.ExampleFile()
		if f.endswith(".csv"):
			return pd.read_csv(f)
		elif f.endswith(".xlsx"):
			return pd.read_xlsx(f)
		else:
			return pd.read_table(f)

	@output
	@render.table
	def LoadedTable():
		return LoadData()

	@output
	@render.ui
	def Map():	
		df = LoadData()
		if df.empty:
			return folium.Map((53.5213, -113.5213), tiles=input.MapType(), zoom_start=15)


		longitudes = df["Longitude"].tolist()
		latitudes = df["Latitude"].tolist()
		values = []
		
		for option in ["Value", "Year"]:
			if option in df:
				values = df[option].tolist()
				break
		if not values:
			values = [1] * len(longitudes)
		

		data = list(zip(latitudes, longitudes, values))

		sw = [min(latitudes), min(longitudes)]
		ne = [max(latitudes), max(longitudes)]

		map = folium.Map((latitudes[0], longitudes[0]), tiles=input.MapType())
		map.fit_bounds([sw, ne])

		HeatMap(data).add_to(map)

		return map

	# Update the Popup depending on what example the user has selected.
	@reactive.Effect
	def _():
		ui.update_popover("InfoPopup", ui.HTML(examples[input.ExampleFile()]["info"]))


	@session.download()
	def DownloadTable():
		df = LoadData()
		path = os.path.join(os.path.dirname(__file__), "table.txt")

		np.savetext(path, df.values, fmt='%d')
		return path


	@session.download()
	def DownloadHeatmap():
		path = os.path.join(os.path.dirname(__file__), "map.html")

		Map().save(path)
		return path



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
				ui.input_file("File", "Choose a File", accept=[".csv", ".txt", "xlsx"], multiple=False),
			),

			# Otherwise, add the example selection and an info button.
			ui.panel_conditional(
				"input.SourceFile === 'Example'",

				# Put them side-by-side.
				ui.layout_columns(

					ui.input_select(id="ExampleFile", label=None, choices=["Example 1", "Example 2", "Example 3"], multiple=False),

					# This message never appears, the server updates it depending
					# on the selection from the above input selection.					
					ui.popover(
						ui.input_action_button(id="InfoButton", label="Info"),
						"Please choose an example!",
						id="InfoPopup"
					),
				)
			),

			ui.br(),

			# All the features related to map customization are here.
			ui.HTML("Map Customization"),

			# Only OpenStreatMap and CartoDB Positron seem to work.
			ui.input_radio_buttons(id="MapType", label="Map Type", choices=["OpenStreetMap", "CartoDB Positron"], selected="CartoDB Positron"),


			ui.br(),

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

				# The map
				ui.nav_panel("Interactive", ui.output_ui("Map")),

				# The table
				ui.nav_panel("Table", ui.output_table("LoadedTable"),),
		),
	)
)	

app = App(app_ui, server)