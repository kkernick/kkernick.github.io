#
# Heatmapper
# Geomap
#
# This file contains the ShinyLive application for Geomap Heatmapper.
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
from folium import Map as FoliumMap, Choropleth
from folium.plugins import HeatMap
from pandas import DataFrame, read_csv, read_excel, read_table
from pathlib import Path
from io import BytesIO
from sys import modules


# Interoperability between ShinyLive and PyShiny
if "pyodide" in modules:
	from pyodide.http import pyfetch
	Source = "https://raw.githubusercontent.com/kkernick/kkernick.github.io/main/geomap/example_input/"
	async def download(url): r = await pyfetch(url); return await r.bytes() if r.ok else None
else:
	from os.path import exists
	Source = "../example_input/"
	async def download(url): return open(url, "rb").read() if exists(url) else None


# Generated from dictionary.sh
Mappings = { "africa.geojson": "Africa", "akron.geojson": "Akron", "alameda.geojson": "Alameda", "albany.geojson": "Albany", "albuquerque.geojson": "Albuquerque", "amsterdam.geojson": "Amsterdam", "amusement-parks.geojson": "Amusement Parks", "anchorage.geojson": "Anchorage", "angers.geojson": "Angers", "angers-loire-metropole.geojson": "Angers Loire Metropole", "antwerp.geojson": "Antwerp", "apulia.geojson": "Apulia", "arlingtonva.geojson": "Arlingtonva", "asia.geojson": "Asia", "athens.geojson": "Athens", "atlanta.geojson": "Atlanta", "augsburg.geojson": "Augsburg", "austin.geojson": "Austin", "australia.geojson": "Australia", "austria-oberoesterreich.geojson": "Austria Oberoesterreich", "austria-states.geojson": "Austria States", "austria-steiermark.geojson": "Austria Steiermark", "bad-belzig.geojson": "Bad Belzig", "badenwuerttemberg-kreise.geojson": "Badenwuerttemberg Kreise", "baltimore.geojson": "Baltimore", "bari.geojson": "Bari", "basel.geojson": "Basel", "bayern.geojson": "Bayern", "belgium-arrondissements.geojson": "Belgium Arrondissements", "berlin.geojson": "Berlin", "bern-districts.geojson": "Bern Districts", "bern-quarters.geojson": "Bern Quarters", "birmingham.geojson": "Birmingham", "blacksburg.geojson": "Blacksburg", "blumenau.geojson": "Blumenau", "bogota.geojson": "Bogota", "boston.geojson": "Boston", "brandenburg.geojson": "Brandenburg", "brandenburg-municipalities.geojson": "Brandenburg Municipalities", "braunschweig.geojson": "Braunschweig", "brazil-states.geojson": "Brazil States", "bremen.geojson": "Bremen", "bronx.geojson": "Bronx", "brooklyn.geojson": "Brooklyn", "buenos-aires.geojson": "Buenos Aires", "calgary.geojson": "Calgary", "california-counties.geojson": "California Counties", "california-vista-points.geojson": "California Vista Points", "caltrain-stations.geojson": "Caltrain Stations", "canada.geojson": "Canada", "canberra.geojson": "Canberra", "caribbean-islands.geojson": "Caribbean Islands", "chapel-hill.geojson": "Chapel Hill", "charlotte.geojson": "Charlotte", "charlottesville.geojson": "Charlottesville", "chemnitz.geojson": "Chemnitz", "chesapeake.geojson": "Chesapeake", "chicago.geojson": "Chicago", "china.geojson": "China", "cincinnati.geojson": "Cincinnati", "cleveland.geojson": "Cleveland", "cologne.geojson": "Cologne", "colorado-counties.geojson": "Colorado Counties", "columbus.geojson": "Columbus", "copenhagen.geojson": "Copenhagen", "cuba.geojson": "Cuba", "dallas.geojson": "Dallas", "dane-county-municipalities.geojson": "Dane County Municipalities", "denmark-municipalities.geojson": "Denmark Municipalities", "denver.geojson": "Denver", "des-moines.geojson": "Des Moines", "detroit.geojson": "Detroit", "dresden.geojson": "Dresden", "dublin.geojson": "Dublin", "duesseldorf.geojson": "Duesseldorf", "durham.geojson": "Durham", "edmonton.geojson": "Edmonton", "eindhoven.geojson": "Eindhoven", "enschede.geojson": "Enschede", "esztergom.geojson": "Esztergom", "europe-1914.geojson": "Europe 1914", "europe-1938.geojson": "Europe 1938", "europe-capitals.geojson": "Europe Capitals", "europe.geojson": "Europe", "fairbanks.geojson": "Fairbanks", "fargo.geojson": "Fargo", "fort-lauderdale.geojson": "Fort Lauderdale", "france-departments.geojson": "France Departments", "france-regions.geojson": "France Regions", "frankfurt-main.geojson": "Frankfurt Main", "freiburg.geojson": "Freiburg", "geneva.geojson": "Geneva", "germany-capitals.geojson": "Germany Capitals", "germany.geojson": "Germany", "ghent.geojson": "Ghent", "gisborne.geojson": "Gisborne", "grand-rapids.geojson": "Grand Rapids", "greece-prefectures.geojson": "Greece Prefectures", "greece-regions.geojson": "Greece Regions", "hamburg.geojson": "Hamburg", "hampton.geojson": "Hampton", "hartford.geojson": "Hartford", "henderson.geojson": "Henderson", "honolulu.geojson": "Honolulu", "houston.geojson": "Houston", "hungary.geojson": "Hungary", "illinois-counties.geojson": "Illinois Counties", "india.geojson": "India", "indianapolis.geojson": "Indianapolis", "iran-provinces.geojson": "Iran Provinces", "ireland-counties.geojson": "Ireland Counties", "isle-of-man.geojson": "Isle Of Man", "italy-provinces.geojson": "Italy Provinces", "italy-regions.geojson": "Italy Regions", "james-city-county.geojson": "James City County", "japan.geojson": "Japan", "kaiserslautern.geojson": "Kaiserslautern", "kansas-city.geojson": "Kansas City", "korea.geojson": "Korea", "las-vegas.geojson": "Las Vegas", "leipzig.geojson": "Leipzig", "le-mans-cantons.geojson": "Le Mans Cantons", "lexington.geojson": "Lexington", "liberia-central.geojson": "Liberia Central", "liberia-east.geojson": "Liberia East", "liberia.geojson": "Liberia", "liberia-west.geojson": "Liberia West", "lombardy.geojson": "Lombardy", "london.geojson": "London", "london-underground.geojson": "London Underground", "long-beach.geojson": "Long Beach", "los-angeles-county.geojson": "Los Angeles County", "los-angeles.geojson": "Los Angeles", "louisville.geojson": "Louisville", "luxembourg-cantons.geojson": "Luxembourg Cantons", "luxembourg-communes.geojson": "Luxembourg Communes", "luzern.geojson": "Luzern", "macon.geojson": "Macon", "madrid-districts.geojson": "Madrid Districts", "madrid.geojson": "Madrid", "malaysia.geojson": "Malaysia", "manhattan-bridges.geojson": "Manhattan Bridges", "manhattan.geojson": "Manhattan", "melbourne.geojson": "Melbourne", "mexico.geojson": "Mexico", "miami.geojson": "Miami", "middle_east_countries.geojson": "Middle_east_countries", "milan.geojson": "Milan", "milwaukee.geojson": "Milwaukee", "minneapolis-cities.geojson": "Minneapolis Cities", "minneapolis.geojson": "Minneapolis", "mississauga.geojson": "Mississauga", "montreal.geojson": "Montreal", "moscow.geojson": "Moscow", "muenster.geojson": "Muenster", "new-haven.geojson": "New Haven", "new-orleans.geojson": "New Orleans", "new-york-areas-of-interest.geojson": "New York Areas Of Interest", "new-york-city-boroughs.geojson": "New York City Boroughs", "new-york-counties.geojson": "New York Counties", "nordrhein-westfalen.geojson": "Nordrhein Westfalen", "norfolk.geojson": "Norfolk", "north-america.geojson": "North America", "north-carolina-cities.geojson": "North Carolina Cities", "oakland.geojson": "Oakland", "oceania.geojson": "Oceania", "oklahoma-cities.geojson": "Oklahoma Cities", "oklahoma-counties.geojson": "Oklahoma Counties", "olympia.geojson": "Olympia", "oman.geojson": "Oman", "oman-provinces.geojson": "Oman Provinces", "orlando.geojson": "Orlando", "pakistan.geojson": "Pakistan", "paris.geojson": "Paris", "peaks.geojson": "Peaks", "philadelphia.geojson": "Philadelphia", "phoenix.geojson": "Phoenix", "pittsburgh.geojson": "Pittsburgh", "poland.geojson": "Poland", "poland-parks.geojson": "Poland Parks", "porirua.geojson": "Porirua", "portland.geojson": "Portland", "portugal.geojson": "Portugal", "potsdam.geojson": "Potsdam", "prague.geojson": "Prague", "providence.geojson": "Providence", "quebec.geojson": "Quebec", "queens.geojson": "Queens", "raleigh.geojson": "Raleigh", "red-deer.geojson": "Red Deer", "richmond.geojson": "Richmond", "riga.geojson": "Riga", "rio-de-janeiro.geojson": "Rio De Janeiro", "rochester.geojson": "Rochester", "rockville.geojson": "Rockville", "roller-coasters-fastest-steel.geojson": "Roller Coasters Fastest Steel", "romania.geojson": "Romania", "rome-rioni.geojson": "Rome Rioni", "rotterdam.geojson": "Rotterdam", "russia.geojson": "Russia", "sacramento.geojson": "Sacramento", "salt-lake-city.geojson": "Salt Lake City", "san-antonio.geojson": "San Antonio", "san-diego.geojson": "San Diego", "san-francisco.geojson": "San Francisco", "san-jose.geojson": "San Jose", "saskatoon.geojson": "Saskatoon", "savannah.geojson": "Savannah", "seattle.geojson": "Seattle", "seoul.geojson": "Seoul", "serbia.geojson": "Serbia", "silicon-valley.geojson": "Silicon Valley", "south-africa.geojson": "South Africa", "south-america.geojson": "South America", "southeast-asia.geojson": "Southeast Asia", "spain-communities.geojson": "Spain Communities", "spain-provinces.geojson": "Spain Provinces", "springfield.geojson": "Springfield", "stamford.geojson": "Stamford", "staten-island.geojson": "Staten Island", "st-louis.geojson": "St Louis", "st-petersburg.geojson": "St Petersburg", "surrey.geojson": "Surrey", "sweden-counties.geojson": "Sweden Counties", "switzerland.geojson": "Switzerland", "sydney.geojson": "Sydney", "szczecin.geojson": "Szczecin", "taiwan.geojson": "Taiwan", "tampa.geojson": "Tampa", "the-hague.geojson": "The Hague", "the-netherlands.geojson": "The Netherlands", "thessaloniki.geojson": "Thessaloniki", "toronto.geojson": "Toronto", "tucson.geojson": "Tucson", "turkey.geojson": "Turkey", "turku.geojson": "Turku", "ulm.geojson": "Ulm", "united-kingdom.geojson": "United Kingdom", "united-kingdom-regions.geojson": "United Kingdom Regions", "united-states-1810.geojson": "United States 1810", "united-states-big-cities.geojson": "United States Big Cities", "united-states.geojson": "United States", "united-states-international-airports.geojson": "United States International Airports", "united-states-mlb-stadiums.geojson": "United States Mlb Stadiums", "unna.geojson": "Unna", "utrecht.geojson": "Utrecht", "vancouver.geojson": "Vancouver", "venice.geojson": "Venice", "venlo.geojson": "Venlo", "vermont-counties.geojson": "Vermont Counties", "vienna.geojson": "Vienna", "villetta.geojson": "Villetta", "washington.geojson": "Washington", "wellington.geojson": "Wellington", "west-linn.geojson": "West Linn", "west-palm-beach.geojson": "West Palm Beach", "wiesenburg.geojson": "Wiesenburg", "williamsburg.geojson": "Williamsburg", "windsor.geojson": "Windsor", "winterthur.geojson": "Winterthur", "zurich-city.geojson": "Zurich City", "zurich.geojson": "Zurich" }

def server(input: Inputs, output: Outputs, session: Session):

	Cache = {}
	Info = {
		"example1.txt": "This example file is from the Open Data Portal. The data is from a carbon monoxide emissions study conducted by Environment Canada. The three columns represent results from 1990, 2000, and 2013.",
		"example2.txt": "This example file is from Statistics Canada. The data is adapted from New cases and age-standardized rate for primary cancer (based on the February 2014 CCR tabulation file), by cancer type and sex, Canada, provinces and territories. The columns represent new cancer cases (age-standardized rate per 100,000 population) from 2006 to 2010.",
		"example3.txt": "This example file is from the U.S. Centers for Disease Control and Prevention. The data is from Diagnosed Diabetes, Age Adjusted Rate (per 100), Adults - Total, 2013."
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


	def LoadJSON():
		"""
		@brief Returns the GeoJSON depending on whether the user wants to use a provided one, or their own.
		@returns Either the path to the uploaded file, or the URL to the one provided by us (Folium supports both)
		"""

		URL = "https://raw.githubusercontent.com/kkernick/kkernick.github.io/main/geomap/data/"

		if input.JSONFile() == "Upload":
			file: list[FileInfo] | None = input.JSONUpload()
			if file is None:
				return URL + "canada.geojson"
			return file[0]["datapath"]
		else:
			return URL + input.JSONSelection()


	async def LoadMap():
		"""
		@brief Generates a map with the provided information
		@returns the Folium.Map
		"""

		df = await LoadData()

		# Give a placeholder map if nothing is selected, which should never really be the case.
		if df.empty: return FoliumMap((53.5213, -113.5213), tiles=input.MapType(), zoom_start=15)

		# Create map
		map = FoliumMap(tiles=input.MapType())

		key = df.columns[0] if input.KeyColumn() is None else input.KeyColumn()
		value = df.columns[1] if input.ValueColumn() is None else input.ValueColumn()

		# Add the heatmap and return.
		Choropleth(
				geo_data=LoadJSON(),
				name='choropleth',
				data=df,
				columns=[key, value],
				key_on='feature.properties.name',
				fill_color=input.ColorMap(),
				fill_opacity=input.Opacity(),
				line_opacity=input.Opacity(),
				legend_name='Legend',
				bins=input.Bins()
		).add_to(map)

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


	@reactive.Effect
	async def _():

		# Give options for the key and value columns
		df = await LoadData()
		choices = df.columns.tolist()
		if choices:
			default_key = input.KeyColumn() if input.KeyColumn() is not None else df.columns[0]
			default_value = input.ValueColumn() if input.ValueColumn() is not None else df.columns[1]

			ui.update_select(id="KeyColumn", choices=choices, selected=default_key)
			ui.update_select(id="ValueColumn", choices=choices, selected=default_value)


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
			selected="Geomap",
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

			ui.input_radio_buttons(id="JSONFile", label="Specify a GeoJSON File", choices=["Provided", "Upload"], selected="Provided", inline=True),

			ui.panel_conditional(
				"input.JSONFile === 'Upload'",
				ui.input_file("JSONUpload", "Choose a File", accept=[".geojson"], multiple=False),
			),

			ui.panel_conditional(
				"input.JSONFile === 'Provided'",
				ui.input_select(id="JSONSelection", label=None, choices=Mappings, multiple=False, selected="canada.geojson"),
			),

			"Table Customization",

			ui.input_select(id="KeyColumn", label="Key", choices=[], multiple=False),
			ui.input_select(id="ValueColumn", label="Value", choices=[], multiple=False),


			# All the features related to map customization are here.
			"Map Customization",

			# Only OpenStreatMap and CartoDB Positron seem to work.
			ui.input_radio_buttons(id="MapType", label="Map Type", choices=["OpenStreetMap", "CartoDB Positron"], selected="CartoDB Positron"),

			ui.input_select(id="ColorMap", label="Color Map", choices={
				"BuGn": "Blue-Green",
				"BuPu": "Blue-Purple",
				"GnBu": "Green-Blue",
				"OrRd": "Orange-Red",
				"PuBu": "Purple-Blue",
				"PuBuGn": "Purple-Blue-Green",
				"PuRd": "Purple-Red",
				"RdPu": "Red-Purple",
				"YlGn": "Yellow-Green",
				"YlGnBu": "Yellow-Green-Blue",
				"YlOrBr": "Yellow-Orange-Brown",
				"YlOrRd": "Yellow-Orange-Red",
				"BrBG": "Brown-Blue-Green",
				"PRGn": "Purple-Red-Green",
				"PiYG": "Pink-Yellow-Green",
				"PuOr": "Purple-Orange",
				"RdBu": "Red-Blue",
				"RdGy": "Red-Grey",
				"RdYlBu": "Red-Yellow-Blue",
				"RdYlGn": "Red-Yellow-Green",
				"Spectral": "Spectral",
				"Accent": "Accent",
				"Dark2": "Dark",
				"Paired": "Paired",
				"Pastel1": "Pastel 1",
				"Pastel2": "Pastel 2",
				"Set1": "Set 1",
				"Set2": "Set 2",
				"Set3": "Set 3"
			}, selected="Viridis"),

			ui.input_slider(id="Opacity", label="Heatmap Opacity", value=0.5, min=0.0, max=1.0, step=0.1),
			ui.input_slider(id="Bins", label="Number of Colors", value=8, min=3, max=12, step=1),

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