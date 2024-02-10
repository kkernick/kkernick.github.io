#
# Heatmapper
# Pairwise
#
# This file contains the ShinyLive application for Pairwise Heatmapper.
# It can be run with the following command within this directory:
#		shinylive export . [site]
# Where [site] is the destination of the site folder.
#
# If you would rather deploy the application as a PyShiny application,
# run the following command within this directory:
#		shiny run
#
# Last Modified: 2024/02/03
#


from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo
from matplotlib.pyplot import subplots, colorbar
from scipy.spatial.distance import pdist, squareform
from Bio.PDB import PDBParser
from io import BytesIO
from sys import modules
from pathlib import Path
from pandas import DataFrame, read_csv, read_excel, read_table


# Interoperability between ShinyLive and PyShiny
if "pyodide" in modules:
	from pyodide.http import pyfetch
	Source = "https://raw.githubusercontent.com/kkernick/kkernick.github.io/main/pairwise/example_input/"
	async def download(url): r = await pyfetch(url); return await r.bytes() if r.ok else None
else:
	from os.path import exists
	Source = "../example_input/"
	async def download(url): return open(url, "rb").read() if exists(url) else None


def server(input: Inputs, output: Outputs, session: Session):
	# Cache for examples. We can't assume users will have unique file names, so we cannot use the cache for
	# Uploaded files. Regardless, this prevents the application from fetching the example every time its needed.
	Cache = {}

	# Information about the Examples
	Info = {
		"example1.txt": "This example dataset represents pairwise distances between C-alpha atoms in ubiquitin (1ubq).",
		"example2.txt": "This example dataset was generated randomly.",
		"example3.txt": "This example dataset was generated randomly."
	}


	async def LoadData():
		"""
		@brief Returns a table containing the pairwise matrix.
		@returns	A DataFrame containing the data requested, formatted as a pairwise matrix, or
							an empty DataFrame if we're on Upload, but the user has not supplied a file.
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
			case ".csv": return ChartMatrix(read_csv(f))
			case ".xlsx": return ChartMatrix(read_excel(f))
			case ".pdb": return PDBMatrix(f)
			case _: return ChartMatrix(read_table(f))


	def PDBMatrix(file):
		"""
		@brief Generates a pairwise matrix from a PDB file
		@param file: The path to a PDB file (Or BytesIO file if applicable)
		@returns The pairwise matrix.
		"""

		parser = PDBParser()
		structure = parser.get_structure("protein", file)

		# Extract atomic coordinates
		coordinates = []
		for model in structure:
			for chain in model:
					if chain.id == input.Chain():
							for residue in chain:
									for atom in residue:
											coordinates.append(atom.coord)

		# Calculate pairwise distances
		distances = pdist(coordinates, metric=input.DistanceMethod().lower())
		distance_matrix = squareform(distances)

		return DataFrame(distance_matrix)


	def ChartMatrix(df):
		"""
		@brief Generates a pairwise matrix from charts
		@param df:	The DataFrame containing the data. This can either be a chart
								containing {x,y,z} columns outlining each point on a row, with
								an optional name column (Any fourth column), a chart to which
								an explicit "Name" column is provided, to which the first row
								and column are assumed variable names for an existing matrix,
								or the default, where it is assumed that the chart is an
								unlabeled collection either of points, or an existing matrix.
		@returns A DataFrame containing the provided data as a pairwise matrix
		"""

		# If "Name" is found, its assumed to be the label for the points.
		if "Name" in df:
			point_names = df["Name"]

		# If explicit coordinates ar eprovided, use them, with the final column used as labels.
		if "x" in df.columns and "y" in df.columns and "z" in df.columns:
			coordinates = df[["x", "y", "z"]].values
			point_names = df[list(set(df.columns) - set(["x", "y", "z"]))[0]].values

		# Magic. How this handles all other cases I don't know, but it somehow works.
		else:
			coordinates = df.iloc[:, 1:].values
			point_names = None

		# Calculate a distant matrix, and return it
		distances = pdist(coordinates, metric=input.DistanceMethod().lower())
		distance_matrix = squareform(distances)
		return DataFrame(distance_matrix, index=point_names, columns=point_names)


	async def GenerateHeatmap():
		"""
		@brief Generates the Heatmap
		@returns The heatmap
		"""

		df = await LoadData()
		fig, ax = subplots()

		im = ax.imshow(df, cmap=input.ColorMap().lower(), interpolation=input.Interpolation().lower())

		# Visibility of features
		if "legend" in input.Features(): plt.colorbar(im, ax=ax, label="Distance")

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
	@render.table
	async def LoadedTable(): return await LoadData()


	@output
	@render.plot
	async def Heatmap(): return await GenerateHeatmap()

	@output
	@render.text
	def ExampleInfo(): return Info[input.Example()]


	@session.download(filename="table.csv")
	async def DownloadTable(): df = await LoadData(); yield df.to_string()


app_ui = ui.page_fluid(

	# Welcome back, NavBar :)
	ui.panel_title(title=None, window_title="Heatmapper"),
	ui.navset_bar(
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/expression/site/index.html target="_blank" rel="noopener noreferrer">Expression</a>'), value="Expression"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/pairwise/site/index.html target="_blank" rel="noopener noreferrer">Pairwise</a>'), value="Pairwise"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/image/site/index.html target="_blank" rel="noopener noreferrer">Image</a>'), value="Image"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/geomap/site/index.html target="_blank" rel="noopener noreferrer">Geomap</a>'), value="Geomap"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/geocoordinate/site/index.html target="_blank" rel="noopener noreferrer">Geocoordinate</a>'), value="Geocoordinate"),
		ui.nav_panel(ui.HTML('<a href=https://kkernick.github.io/about/site/index.html target="_blank" rel="noopener noreferrer">About</a>'), value="About"),
		title="Heatmapper",
		selected="Pairwise",
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
				ui.input_file("File", "Choose a File", accept=[".csv", ".txt", "xlsx", ".pdb", ".dat"], multiple=False),
			),

			# Otherwise, add the example selection and an info button.
			ui.panel_conditional(
				"input.SourceFile === 'Example'",
				"Choose an Example File",
				ui.layout_columns(
					ui.input_select(id="Example", label=None, choices={
											"example1.txt": "Example 1",
											"example2.txt": "Example 2",
											"example3.txt": "Example 3",
					}),
					ui.popover(ui.input_action_link(id="ExampleInfoButton", label="Info"), ui.output_text("ExampleInfo")),
					col_widths=[10,2],
				)
			),

			# Customize the text size of the axes.
			ui.input_numeric(id="TextSize", label="Text Size", value=8, min=1, max=50, step=1),

			# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
			ui.input_select(id="DistanceMethod", label="Distance Method", choices=[
				"Braycurtis", "Canberra", "Chebyshev", "Cityblock", "Correlation", "Cosine", "Dice", "Euclidean", "Hamming", "Jaccard", "Jensenshannon", "Kulczynski1", "Mahalanobis", "Matching", "Minkowski", "Rogerstanimoto", "Russellrao", "Seuclidean", "Sokalmichener", "Sokalsneath", "Sqeuclidean", "Yule"], selected="Euclidean"),

			# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
			ui.input_select(id="Interpolation", label="Interpolation", choices=["None", "Antialiased", "Nearest", "Bilinear", "Bicubic", "Spline16", "Spline36", "Hanning", "Hamming", "Hermite", "Kaiser", "Quadric", "Catrom", "Gaussian", "Bessel", "Mitchell", "Sinc", "Lanczos", "Blackman"], selected="Nearest"),

			# Set the ColorMap used.
			ui.input_select(id="ColorMap", label="Color Map", choices=["Viridis", "Plasma", "Inferno", "Magma", "Cividis"], selected="Viridis"),

			# Customize what aspects of the heatmap are visible
			ui.input_checkbox_group(id="Features", label="Heatmap Features",
					choices={"x": "X Labels", "y": "Y Labels", "legend": "Legend"},
					selected=["legend"]),

			# Specify the PDB Chain
			ui.input_text("Chain", "PDB Chain", "A"),

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