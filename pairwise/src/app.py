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
# Last Modified: 2024/02/10
#


from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo
from matplotlib.pyplot import subplots, colorbar
from scipy.spatial.distance import pdist, squareform
from Bio.PDB import PDBParser
from Bio import SeqIO
from io import BytesIO
from sys import modules
from pathlib import Path
from pandas import DataFrame, Series, read_csv, read_excel, read_table
from copy import deepcopy


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

	# We use a two-tiered cache system to allow the user to modify files without requiring
	# re-fetching to restore the original values.
	#
	# Base is the immutable, primary cache, that contains the contents of files (example or uploaded)
	# in their original form. Nothing is allowed to modify the contents of values in Base, nor are they
	# allowed to be exposed to the user in any capacity. If Base is not populated, content will be fetched
	# Externally (Either by opening a user-supplied file, or fetching the content online)
	#
	# Cache is the modifiable, secondary cache, that contains the content of Base. The user is only provided
	# Data via Cache, as an abstraction of Base. If Cache is not populated, content will be fetched by making
	# A copy of the value within Base.
	Base = {}
	Cache = {}



	# Information about the Examples
	Info = {
		"example1.txt": "This example dataset represents pairwise distances between C-alpha atoms in ubiquitin (1ubq).",
		"example2.txt": "This example dataset was generated randomly.",
		"example3.txt": "This example dataset was generated randomly."
	}


	def HandleData(n, i):
		"""
		@brief Given the file name n, handle the file at i
		@param n The name of the file, extension is used to differentiate
		@param i The path to the file.
		"""
		match Path(n).suffix:
			case ".csv": return read_csv(i)
			case ".xlsx": return read_excel(i)
			case ".pdb": return PDBMatrix(i)
			case ".fasta": return FASTAMatrix(i)
			case _: return read_table(i)


	async def RawData():
		"""
		@brief Returns the raw data that has been supplied, before modifying it into a matrix.
		@returns the name associated with the values stored in the Cache.
		"""

		# Grab an uploaded file, if its done, or grab an example (Using a cache to prevent redownload)
		if input.SourceFile() == "Upload":
			file: list[FileInfo] | None = input.File()
			if file is None: return None
			n = file[0]["name"]

			# Populate the base cache, if we need to
			if n not in Base: Base[n] = HandleData(n, read(file[0]["datapath"], "wb"))

		else:
			n = input.Example()

			# Populate the base cache, if we need to
			if n not in Base: Base[n] = HandleData(n, BytesIO(await download(Source + input.Example())))

		# Populate the secondary cache if we need to, and return the name for lookup.
		if n not in Cache: Cache[n] = deepcopy(Base[n])
		return n


	async def LoadData():
		"""
		@brief Returns a table containing the pairwise matrix.
		@returns	A DataFrame containing the data requested, formatted as a pairwise matrix, or
							an empty DataFrame if we're on Upload, but the user has not supplied a file.
		"""

		n = await RawData()
		df = DataFrame() if n is None else Cache[n]
		if n is None: return DataFrame()

		match Path(n).suffix:
			case ".csv": df = ChartMatrix(df)
			case ".xlsx": df = ChartMatrix(df)
			case ".pdb": pass
			case ".fasta": pass
			case _: df = ChartMatrix(df)

		# Fix garbage data and return the resultant DataFrame.
		return df.fillna(0)


	def FASTAMatrix(file):
		"""
		@brief Computes the pairwise matrix from a FASTA file.
		@param file: The path to the FASTA File
		@returns a pairwise matrix.
		"""

		# Get information from the file
		records = list(SeqIO.parse(open(file), "fasta"))
		sequences = [str(record.seq) for record in records]
		column_names = [record.id for record in records]

		# Get our K-Mer value
		k = input.K()

		# Generate the value
		dictionary = {}
		for x, seq in enumerate(sequences):
			kmers = [seq[i:i+k] for i in range(len(seq) - k + 1)]
			increment = 1 / len(kmers)
			for kmer in kmers:
					if kmer not in dictionary:
							dictionary[kmer] = [0.0] * len(sequences)
					dictionary[kmer][x] += increment
		frequencies = DataFrame.from_dict(dictionary, orient='index')

		# Calculate matrix
		if input.MatrixType() == "Distance":
			distances = pdist(frequencies.T, metric=input.DistanceMethod().lower())
			return DataFrame(squareform(distances), index=column_names, columns=column_names)
		else:
			return frequencies.corr(method=input.CorrelationMethod().lower())


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

		# Calculate matrix
		if input.MatrixType() == "Distance":
			distances = pdist(coordinates, metric=input.DistanceMethod().lower())
			return DataFrame(squareform(distances))
		else:
			return DataFrame(coordinates).corr(method=input.CorrelationMethod().lower())


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
		if input.MatrixType() == "Distance":
			distances = pdist(coordinates, metric=input.DistanceMethod().lower())
			return DataFrame(squareform(distances), index=point_names, columns=point_names)
		else:
			return DataFrame(coordinates, index=point_names, columns=point_names).corr(method=input.CorrelationMethod().lower())


	async def GenerateHeatmap():
		"""
		@brief Generates the Heatmap
		@returns The heatmap
		"""

		df = await LoadData()
		fig, ax = subplots()

		im = ax.imshow(df, cmap=input.ColorMap().lower(), interpolation=input.Interpolation().lower())

		# Visibility of features
		if "legend" in input.Features(): colorbar(im, ax=ax, label="Distance")

		if "y" in input.Features():
			ax.tick_params(axis="y", labelsize=input.TextSize())
			ax.set_yticks(range(len(df.columns)))
			ax.set_yticklabels(df.columns)
		else:
			ax.set_yticklabels([])

		if "x" in input.Features():
			ax.tick_params(axis="x", labelsize=input.TextSize())
			ax.set_xticks(range(len(df.columns)))
			ax.set_xticklabels(df.columns, rotation=90)
		else:
			ax.set_xticklabels([])

		# Annotate each cell with its value
		if "label" in input.Features():
			for i in range(df.shape[0]):
					for j in range(df.shape[1]):
							ax.text(j, i, '{:.2f}'.format(df.iloc[i, j]), ha='center', va='center', color='white')

		return ax


	@output
	@render.data_frame
	@reactive.event(input.Update, input.Reset, input.Example, input.File, ignore_none=False, ignore_init=False)
	async def LoadedTable(): n = await RawData(); return DataFrame() if n is None else Cache[n]


	@output
	@render.plot
	@reactive.event(input.Update, input.Reset, input.Example, input.File, ignore_none=False, ignore_init=False)
	async def Heatmap(): return await GenerateHeatmap()

	@output
	@render.text
	def ExampleInfo(): return Info[input.Example()]


	@render.download(filename="table.csv")
	async def DownloadTable(): df = await LoadData(); yield df.to_string()


	@reactive.Effect
	@reactive.event(input.Update)
	async def Update():
		"""
		@brief Updates the value in the table with the one the user typed in upon updating
		"""

		# Get the data
		n = await RawData()
		df = DataFrame() if n is None else Cache[n]

		row_count, column_count = df.shape
		row, column = input.TableRow(), input.TableCol()

		# So long as row and column are sane, update.
		if row < row_count and column < column_count:
			match input.Type():
				case "Integer": df.iloc[row, column] = int(input.TableVal())
				case "Float": df.iloc[row, column] = float(input.TableVal())
				case "String": df.iloc[row, column] = input.TableVal()


	@reactive.Effect
	@reactive.event(input.Reset)
	async def Reset(): del Cache[await RawData()]


	@reactive.Effect
	@reactive.event(input.TableRow, input.TableCol, input.Example, input.File, input.Reset, input.Update)
	async def UpdateTableValue():
		"""
		@brief Updates the label for the Value input to display the current value.
		"""
		df = await LoadData()

		rows, columns = df.shape
		row, column = int(input.TableRow()), int(input.TableCol())

		if 0 <= row <= rows and 0 <= column <= columns:
			ui.update_text(id="TableVal", label="Value (" + str(df.iloc[row, column]) + ")", value=0),


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
			ui.HTML('<a href=https://kkernick.github.io/about/site/index.html target="_blank" rel="noopener noreferrer">Data Format</a>'),

			# Specify whether to use example files, or upload one.
			ui.input_radio_buttons(id="SourceFile", label="Specify a Source File", choices=["Example", "Upload"], selected="Example", inline=True),

			# Only display an input dialog if the user is one Upload
			ui.panel_conditional(
				"input.SourceFile === 'Upload'",
				ui.input_file("File", "Choose a File", accept=[".csv", ".txt", "xlsx", ".pdb", ".dat", ".fasta"], multiple=False),
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

			ui.layout_columns(
				ui.input_action_button("Update", "Update"),
				ui.popover(ui.input_action_link(id="UpdateInfo", label="?"),
					"Heatmapper will automatically update the heatmap when you change the file source. However, when modifying the table or changing feature visibility, you'll need to update the view manually."
				),
				col_widths=[11,1],
			),

			ui.layout_columns(
				ui.input_action_button("Reset", "Reset Values"),
				ui.popover(ui.input_action_link(id="ResetInfo", label="?"),
					"If you modify the values displayed in the Table Tab, you can reset the values back to their original state with this button."
				),
				col_widths=[11,1],
			),

			ui.br(),

			# Specify Matrix Type
			ui.input_radio_buttons(id="MatrixType", label="Matrix Type", choices=["Distance", "Correlation"], selected="Distance", inline=True),

			# Customize the text size of the axes.
			ui.input_numeric(id="TextSize", label="Text Size", value=8, min=1, max=50, step=1),

			# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
			ui.panel_conditional(
				"input.MatrixType === 'Distance'",
				ui.input_select(id="DistanceMethod", label="Distance Method", choices=[
					"Braycurtis", "Canberra", "Chebyshev", "Cityblock", "Correlation", "Cosine", "Dice", "Euclidean", "Hamming", "Jaccard", "Jensenshannon", "Kulczynski1", "Mahalanobis", "Matching", "Minkowski", "Rogerstanimoto", "Russellrao", "Seuclidean", "Sokalmichener", "Sokalsneath", "Sqeuclidean", "Yule"], selected="Euclidean"),
			),

			# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.corr.html
			ui.panel_conditional(
				"input.MatrixType === 'Correlation'",
				ui.input_select(id="CorrelationMethod", label="Correlation Method", choices=["Pearson", "Kendall", "Spearman"], selected="Pearson"),
			),

			# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
			ui.input_select(id="Interpolation", label="Interpolation", choices=["None", "Antialiased", "Nearest", "Bilinear", "Bicubic", "Spline16", "Spline36", "Hanning", "Hamming", "Hermite", "Kaiser", "Quadric", "Catrom", "Gaussian", "Bessel", "Mitchell", "Sinc", "Lanczos", "Blackman"], selected="Nearest"),

			# Set the ColorMap used.
			ui.input_select(id="ColorMap", label="Color Map", choices=["Viridis", "Plasma", "Inferno", "Magma", "Cividis"], selected="Viridis"),

			# Customize what aspects of the heatmap are visible
			ui.input_checkbox_group(id="Features", label="Heatmap Features",
					choices={"x": "X Labels", "y": "Y Labels", "label": "Data Labels", "legend": "Legend"},
					selected=["legend"]),

			# Specify the PDB Chain
			ui.input_text("Chain", "PDB Chain", "A"),

			# Customize the K-mer to compute for FASTA sequences
			ui.input_numeric(id="K", label="K-Mer Length", value=3, min=3, max=5, step=1),

			# Add the download buttons.
			ui.download_button("DownloadTable", "Download Table"),

			id="SidebarPanel",
		),

		# Add the main interface tabs.
		ui.navset_tab(
				ui.nav_panel("Interactive", ui.output_plot("Heatmap", height="90vh")),
				ui.nav_panel("Table",
					ui.layout_columns(
						ui.input_numeric("TableRow", "Row", 0),
						ui.input_numeric("TableCol", "Column", 0),
						ui.input_text("TableVal", "Value", 0),
						ui.input_select(id="Type", label="Datatype", choices=["Integer", "Float", "String"]),
						col_widths=[2,2,6,2],
					),

					ui.output_data_frame("LoadedTable"),
				),
		),
	)
)

app = App(app_ui, server)
