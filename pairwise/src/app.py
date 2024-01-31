from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg


from scipy.spatial.distance import pdist, squareform

from Bio.PDB import PDBParser

from io import StringIO, BytesIO

Cached = None
Filename = None

def server(input: Inputs, output: Outputs, session: Session):

	# Returns the data of whatever we should generate our map off of.
	def LoadData():
		global Cached, Filename

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

		if Filename == f and Cached is not None:
			return Cached
		else:
			Filename = f

			# Handle extensions.
			if ext.endswith(".csv"):
				Cached = ChartMatrix(pd.read_csv(f))
			elif ext.endswith(".xlsx"):
				Cached = ChartMatrix(pd.read_xlsx(f))
			elif ext.endswith(".pdb"):
				Cached = PDBMatrix(f)
			else:
				Cached = ChartMatrix(pd.read_table(f))
			return Cached


	def PDBMatrix(file):
		parser = PDBParser()
		structure = parser.get_structure('protein', file)

		# Extract atomic coordinates
		coordinates = []
		for model in structure:
			for chain in model:
					if chain.id == input.Chain():
							for residue in chain:
									for atom in residue:
											coordinates.append(atom.coord)

		# Calculate pairwise Euclidean distances
		distances = pdist(coordinates, metric=input.DistanceMethod().lower())
		distance_matrix = squareform(distances)

		return pd.DataFrame(distance_matrix)


	def ChartMatrix(df):
		if "Name" in df:
			distance_matrix = df.iloc[:, 1:].values
			point_names = df["Name"]

		else:
			if 'x' in df.columns and 'y' in df.columns and 'z' in df.columns:
				coordinates = df[['x', 'y', 'z']].values
				point_names = df[list(set(df.columns) - set(['x', 'y', 'z']))[0]].values
			else:
				# This will either handle a 
				coordinates = df.iloc[:, 1:].values
				point_names = None

		distances = pdist(coordinates, metric=input.DistanceMethod().lower())
		distance_matrix = squareform(distances)

		return pd.DataFrame(distance_matrix, index=point_names, columns=point_names)


	def GenerateHeatmap():
		df = LoadData()

		fig, ax = plt.subplots()

		im = ax.imshow(df, cmap=input.ColorMap().lower(), interpolation=input.Interpolation().lower())
		plt.colorbar(im, label="Distance")

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
				ui.input_file("File", "Choose a File", accept=[".csv", ".txt", "xlsx", ".pdb"], multiple=False),
			),

			ui.br(),

			# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html
			ui.input_select(id="DistanceMethod", label="Distance Method", choices=[
				"Braycurtis", "Canberra", "Chebyshev", "Cityblock", "Correlation", "Cosine", "Dice", "Euclidean", "Hamming", "Jaccard", "Jensenshannon", "Kulczynski1", "Mahalanobis", "Matching", "Minkowski", "Rogerstanimoto", "Russellrao", "Seuclidean", "Sokalmichener", "Sokalsneath", "Sqeuclidean", "Yule"], selected="Euclidean"),

			# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
			ui.input_select(id="Interpolation", label="Interpolation", choices=[
				"None", "Antialiased", "Nearest", "Bilinear", "Bicubic", "Spline16", "Spline36", "Hanning", "Hamming", "Hermite", "Kaiser", "Quadric", "Catrom", "Gaussian", "Bessel", "Mitchell", "Sinc", "Lanczos", "Blackman"], selected="Nearest"),

			ui.input_select(id="ColorMap", label="Color Map", choices=["Viridis", "Plasma", "Inferno", "Magma", "Cividis"], selected="Viridis"),

			ui.input_text("Chain", "PDB Chain", "A"),

			ui.br(),

			# Add the download buttons.
			ui.layout_columns(
				ui.download_button("DownloadTable", "Download Table"),
				ui.download_button("DownloadHeatmap", "Download Heatmap")
			),

			id="SidebarPanel",
			width=350,
		),

		# Add the main interface tabs.
		ui.navset_tab(

				# The map
				ui.nav_panel("Interactive", ui.output_plot("Heatmap", height="90vh")),

				# The table
				ui.nav_panel("Table", ui.output_table("LoadedTable"),),
		),

		height="100vh"
	)
)	

app = App(app_ui, server)