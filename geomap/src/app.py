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


	def LoadJSON():
		file: list[FileInfo] | None = input.JSON()
		if file is None:
				return None
		return file[0]["datapath"]


	# Generates the Map given the current options selected by the user.
	def LoadMap():
		df = LoadData()

		# Give a placeholder map if nothing is selected, which should never really be the case.
		if df.empty:
			return folium.Map((53.5213, -113.5213), tiles=input.MapType(), zoom_start=15)

		# Create map		
		map = folium.Map(tiles=input.MapType())

		json = LoadJSON()
		if json is not None:
			key = df.columns[0] if input.KeyColumn() is None else input.KeyColumn()
			value = df.columns[1] if input.ValueColumn() is None else input.ValueColumn()

			# Add the heatmap and return.
			folium.Choropleth(
					geo_data=json,
					name='choropleth',
					data=df,
					columns=[key, value],
					key_on='feature.properties.name',
					fill_color='YlGn',
					fill_opacity=input.Opacity(),
					line_opacity=input.Opacity(),
					legend_name='Legend'
			).add_to(map)
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

		df = LoadData()
		choices = df.columns.tolist()
		if choices:
			default_key = input.KeyColumn() if input.KeyColumn() is not None else df.columns[0] 
			default_value = input.ValueColumn() if input.ValueColumn() is not None else df.columns[1] 

			ui.update_select(id="KeyColumn", choices=choices, selected=default_key)
			ui.update_select(id="ValueColumn", choices=choices, selected=default_value)


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
					col_widths=[8,4]
				)
			),

			ui.layout_columns(
				ui.HTML("Choose a GeoJSON file"),
				ui.popover(
					ui.input_action_button(id="GeoButton", label="Info"),
					ui.HTML("Heatmapper uses GeoJSON files to create country/territory boundaries. A good source is from <a href=https://github.com/codeforgermany/click_that_hood/tree/main/public/data>here</a>."),
					id="JSONPopup"
				),
				col_widths=[8,4]
			),

			ui.input_file(id="JSON", label=None, accept=[".geojson"], multiple=False),


			ui.input_select(id="KeyColumn", label="Key", choices=[], multiple=False),
			ui.input_select(id="ValueColumn", label="Value", choices=[], multiple=False),


			ui.br(),

			# All the features related to map customization are here.
			ui.HTML("Map Customization"),

			# Only OpenStreatMap and CartoDB Positron seem to work.
			ui.input_radio_buttons(id="MapType", label="Map Type", choices=["OpenStreetMap", "CartoDB Positron"], selected="CartoDB Positron"),

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),

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