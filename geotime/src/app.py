#
# Heatmapper
# Geotime
#
# This file contains the ShinyLive application for Geotime Heatmapper.
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
from folium.plugins import HeatMapWithTime
from pandas import DataFrame

from shared import Table, Cache, NavBar, FileSelection

# Fine, Shiny
import branca, certifi, xyzservices


def server(input: Inputs, output: Outputs, session: Session):

	Info = {
		"example1.csv": "Random data",
		"example21.csv": "A parsed version of the Northeast and North Central Pacific hurricane database (HURDAT2) 2000-2022, available at https://www.nhc.noaa.gov/data/",
		"example32.csv": "A parsed subset of Seoul's air quality in the year 2021, month of January, available at https://www.kaggle.com/datasets/williamhyun/seoulairqualityhistoricdata",

	}

	DataCache = Cache("geotime")

	async def LoadMap():
		"""
		@brief Generates a map with the provided information
		@returns the Folium.Map
		"""

		df = await DataCache.Load(input)

		# Give a placeholder map if nothing is selected, which should never really be the case.
		if df.empty: return FoliumMap((53.5213, -113.5213), tiles=input.MapType(), zoom_start=15)

		# Don't do anything until the application has had time to choose columns
		default_time = input.TimeColumn()
		if default_time is None or default_time not in df: return
		default_value = input.ValueColumn()
		if default_value is None or default_value not in df: return

		df = df.sort_values(by=default_time)

		# Normalize
		values = df[default_value]
		df[default_value] = (values - values.min()) / (values.max() - values.min())

		# Group data by time
		data = []
		for time, group_df in df.groupby(default_time):
			time_slice = []
			for _, row in group_df.iterrows():
				lat = row["Latitude"]
				lon = row["Longitude"]
				value = row[default_value]
				time_slice.append([lat, lon, value])
			data.append(time_slice)

		# Find a decent initial zoom.
		map = FoliumMap((df["Latitude"][0], df["Longitude"][0]), tiles=input.MapType())
		HeatMapWithTime(
			data,
			index=df[default_time].drop_duplicates().to_list(),
			radius=input.Radius(),
			min_opacity=input.Opacity(),
			blur=input.Blur(),
			max_speed=60,
		).add_to(map)
		#map.fit_bounds(map.get_bounds())

		return map


	@output
	@render.data_frame
	@reactive.event(input.Update, input.Reset, input.Example, input.File, ignore_none=False, ignore_init=False)
	async def LoadedTable(): return await DataCache.Load(input)


	@output
	@render.ui
	@reactive.event(input.Update, input.Reset, input.Example, input.File, input.UpdateMap, input.TimeColumn, input.ValueColumn, ignore_none=False, ignore_init=False)
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


	@reactive.Effect
	async def UpdateColumns():

		# Give options for the key and value columns
		df = await DataCache.Load(input)
		choices = df.columns.tolist()
		if choices:

			default_time = None
			for time in ["Time", "Date"]:
				if time in df: default_time = time; break
			if not default_time:
				columns = df.columns.tolist()
				for n in ["Longitude", "Latitude", "Weight", "Intensity"]:
					if n in columns:
						columns.remove(n)
				print(columns)
				default_time = columns[0]

			default_value = None
			for value in ["Weight", "Intensity"]:
				if value in df: default_value = value; break
			if not default_value:
				columns = df.columns.tolist()
				for n in ["Longitude", "Latitude", "Time", "Date"]:
					if n in columns:
						columns.remove(n)
				print(columns)
				default_value = columns[0]

			ui.update_select(id="TimeColumn", choices=choices, selected=default_time)
			ui.update_select(id="ValueColumn", choices=choices, selected=default_value)


app_ui = ui.page_fluid(

	NavBar("Geotime"),

	ui.layout_sidebar(
		ui.sidebar(

			FileSelection(
				examples={"example1.csv": "Example 1", "example21.csv": "Example 2", "example32.csv": "Example 3"},
				types=[".csv", ".txt", ".xlsx"]
			),

			ui.input_action_button("UpdateMap", "Update Heatmap"),

			ui.input_select(id="TimeColumn", label="Time Column", choices=[], multiple=False),
			ui.input_select(id="ValueColumn", label="Value Column", choices=[], multiple=False),

			# Only OpenStreatMap and CartoDB Positron seem to work.
			ui.input_radio_buttons(id="MapType", label="Map Type", choices=["OpenStreetMap", "CartoDB Positron"], selected="CartoDB Positron"),

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.6, min=0.0, max=1.0, step=0.1),
			ui.input_slider(id="Radius", label="Size of Points", value=15, min=1, max=50, step=1),
			ui.input_slider(id="Blur", label="Blurring", value=0.8, min=0.0, max=1.0, step=0.1),

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