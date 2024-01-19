from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo

# We need to import here so ShinyLive doesn't get upset.
import certifi, branca, xyzservices
import folium
from folium.plugins import HeatMap

import pandas as pd

from pathlib import Path
from io import StringIO


from examples import examples


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

		# Otherwise, fetch the example file selected.
		else:
			f = StringIO(examples[input.ExampleFile()]["data"])

		# Handle extensions.
		if ext.endswith(".csv"):
			return pd.read_csv(f)
		elif ext.endswith(".xlsx"):
			return pd.read_xlsx(f)
		else:
			return pd.read_table(f)


	# Generates the Map given the current options selected by the user.
	def LoadMap():
		df = LoadData()

		# Give a placeholder map if nothing is selected, which should never really be the case.
		if df.empty:
			return folium.Map((53.5213, -113.5213), tiles=input.MapType(), zoom_start=15)

		# Get the long and lat.
		longitudes = df["Longitude"].tolist()
		latitudes = df["Latitude"].tolist()

		# Guess the associated value for plotting.
		values = []
		for option in ["Value", "Year"]:
			if option in df:
				values = df[option].tolist()
				break
		if not values:
			values = [1] * len(longitudes)
		

		#  Get the data ready.
		data = list(zip(latitudes, longitudes, values))

		# Find a decent initial zoom.
		sw = [min(latitudes), min(longitudes)]
		ne = [max(latitudes), max(longitudes)]
		map = folium.Map((latitudes[0], longitudes[0]), tiles=input.MapType())
		map.fit_bounds([sw, ne])

		# Add the heatmap and return.
		HeatMap(data, min_opacity=input.Opacity(), radius=input.Radius(), blur=input.Blur()).add_to(map)
		return map


	@output
	@render.table
	def LoadedTable():
		return LoadData()


	@output
	@render.ui
	def Map():
		return LoadMap()
		

	# Update the Popup depending on what example the user has selected.
	@reactive.Effect
	def _():
		ui.update_popover("InfoPopup", ui.HTML(examples[input.ExampleFile()]["info"]))


	@session.download(filename="table.csv")
	def DownloadTable():
		yield LoadData().to_string()


	@session.download(filename="heatmap.html")
	def DownloadHeatmap():
		yield LoadMap().get_root().render()



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

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),
			ui.input_slider(id="Radius", label="Size of Points", value=25, min=5, max=50, step=5),
			ui.input_slider(id="Blur", label="Blurring", value=15, min=1, max=30, step=1),

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