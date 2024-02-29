from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo
from pandas import DataFrame, read_csv, read_excel, read_table
from io import BytesIO
from sys import modules
from copy import deepcopy
from pathlib import Path

if "pyodide" in modules:
	from pyodide.http import pyfetch
	Pyodide = True
else:
	from os.path import exists
	Pyodide = False


class Cache:

	@staticmethod
	def DefaultHandler(n, i):
		match Path(n).suffix:
			case ".csv": df = read_csv(i)
			case ".xlsx": df = read_excel(i)
			case _: df = read_table(i)
		return df.fillna(0)

	@staticmethod
	async def Remote(url): r = await pyfetch(url); return await r.bytes() if r.ok else None

	@staticmethod
	async def Local(url): return open(url, "rb").read() if exists(url) else None


	def __init__(self, project, DataHandler = DefaultHandler):
		self._primary = {}
		self._secondary = {}
		self._handler = DataHandler

		if Pyodide:
			self.Download = lambda url: Cache.Remote(url)
			self.Source = "https://raw.githubusercontent.com/kkernick/kkernick.github.io/main/{}/example_input/".format(project)
		else:
			self.Download = lambda url: Cache.Local(url)
			self.Source = "../example_input/"


	async def Load(self, input): n = await self.N(input); return DataFrame() if n is None else self._secondary[n]


	async def N(self, input):
		# Grab an uploaded file, if its done, or grab an example (Using a cache to prevent redownload)
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.File()
			if file is None: return None
			n = file[0]["name"]

			# Populate the base cache, if we need to
			if n not in self._primary: self._primary[n] = self._handler(n, read(file[0]["datapath"], "wb"))

		else:
			n = input.Example()
			print(self.Source + n)
			if n not in self._primary: self._primary[n] = self._handler(n, BytesIO(await self.Download(self.Source + n)))
		if n not in self._secondary: self._secondary[n] = deepcopy(self._primary[n])
		return n


	def Cache(self): return self._secondary


	async def Update(self, input):
		# Get the data
		df = await self.Load(input)

		row_count, column_count = df.shape
		row, column = input.TableRow(), input.TableCol()

		# So long as row and column are sane, update.
		if row < row_count and column < column_count:
			match input.Type():
				case "Integer": df.iloc[row, column] = int(input.TableVal())
				case "Float": df.iloc[row, column] = float(input.TableVal())
				case "String": df.iloc[row, column] = input.TableVal()


	async def Purge(self, input):
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.File()
			if file is None: return None
			n = file[0]["name"]
		else:
			n = input.Example()
		del self._secondary[n]


def NavBar(current):
	return [
			ui.panel_title(title=None, window_title="Heatmapper"),

		ui.navset_bar(
				ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io//expression/site/index.html target="_blank" rel="noopener noreferrer">Expression</a>'), value="Expression"),
				ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io//pairwise/site/index.html target="_blank" rel="noopener noreferrer">Pairwise</a>'), value="Pairwise"),
				ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io//image/site/index.html target="_blank" rel="noopener noreferrer">Image</a>'), value="Image"),
				ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io//geomap/site/index.html target="_blank" rel="noopener noreferrer">Geomap</a>'), value="Geomap"),
				ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io//geocoordinate/site/index.html target="_blank" rel="noopener noreferrer">Geocoordinate</a>'), value="Geocoordinate"),
				ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io//about/site/index.html target="_blank" rel="noopener noreferrer">About</a>'), value="About"),
				title="Heatmapper",
				selected=current,
		)
	]


def FileSelection(examples, types):
	# If the user needs help with the formatting.
	return [ui.HTML('<a href=https://kkernick.github.io//about/site/index.html target="_blank" rel="noopener noreferrer">Data Format</a>'),

	# Specify whether to use example files, or upload one.
	ui.input_radio_buttons(id="SourceFile", label="Specify a Source File", choices=["Example", "Upload"], selected="Example", inline=True),

	# Only display an input dialog if the user is one Upload
	ui.panel_conditional(
		"input.SourceFile === 'Upload'",
		ui.input_file("File", "Choose a File", accept=types, multiple=False),
	),

	# Otherwise, add the example selection and an info button.
	ui.panel_conditional(
		"input.SourceFile === 'Example'",
		ui.layout_columns(
			ui.input_select(id="Example", label=None, choices=examples, multiple=False),
			ui.popover(ui.input_action_link(id="ExampleInfoButton", label="Info"), ui.output_text("ExampleInfo")),
			col_widths=[10,2],
		)
	)]


Table = ui.nav_panel("Table",
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
)
