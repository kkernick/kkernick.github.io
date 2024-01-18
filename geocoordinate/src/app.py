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
		if input.SourceFile() == "Upload File":
			file: list[FileInfo] | None = input.File()
			if file is None:
					return pd.DataFrame()
			f = file[0]["datapath"]
		else:
			if not Path(input.ExampleFile()).is_file():
				file = open(input.ExampleFile() , 'w')
				file.write(examples[input.ExampleFile()])
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



app_ui = ui.page_fluid(
	ui.panel_title(ui.HTML('<a href="https://kkernick.github.io">Heatmapper</a>')),
	ui.layout_sidebar(
		ui.sidebar(
			ui.HTML("<a href=https://kkernick.github.io/about/site/index.html>Data Format</a>"),

			ui.input_radio_buttons(id="SourceFile", label="Specify a Source File", choices=["Example File", "Upload File"], selected="Example File"),

			ui.panel_conditional(
				"input.SourceFile === 'Upload File'",
				ui.input_file("File", "Choose a File", accept=[".csv", ".txt", "xlsx"], multiple=False),

			),

			ui.panel_conditional(
				"input.SourceFile === 'Example File'",
				ui.input_select(id="ExampleFile", label="Choose an Example File", choices=["Example 1", "Example 2", "Example 3"], multiple=False),

			),

			ui.HTML("Map Customization"),
			ui.input_radio_buttons(id="MapType", label="Map Type", choices=["OpenStreetMap", "CartoDB Positron"], selected="CartoDB Positron"),

			id="SidebarPanel",
			width=300
		),

		ui.navset_tab(
				ui.nav_panel(
					"Interactive",
					ui.output_ui("Map") 
				),
				ui.nav_panel(
					"Table",
					ui.output_table("LoadedTable"),
				),
		),
	)
)	

app = App(app_ui, server)