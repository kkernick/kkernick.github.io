#
# Heatmapper
# Expression
#
# This file contains the ShinyLive application for Expression Heatmapper.
# It can be run with the following command within this directory:
#		shinylive export . [site]
# Where [site] is the destination of the site folder.
#
# If you would rather deploy the application as a PyShiny application,
# run the following command within this directory:
#		shiny run
#
# Last Modified: 2024/02/09
#


from shiny import App, Inputs, Outputs, Session, reactive, render, ui
from shiny.types import FileInfo
from matplotlib.pyplot import figure, subplots, colorbar
from matplotlib.colors import Normalize
from scipy.cluster import hierarchy
from io import BytesIO
from sys import modules
from pathlib import Path
from pandas import DataFrame, read_csv, read_excel, read_table


# Interoperability between ShinyLive and PyShiny
if "pyodide" in modules:
	from pyodide.http import pyfetch
	Source = "https://raw.githubusercontent.com/kkernick/kkernick.github.io/main/expression/example_input/"
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
		"example1.txt": "This example dataset is sample input retrieved from the website for the Ashley Lab Heatmap Builder.",
		"example2.txt": "This example dataset is sample input retrieved from an online tutorial by Yan Cui (ycui2@uthsc.edu).",
		"example3.txt": "This example dataset is retrieved from the online supplement to Eisen et al. (1998), which is a very well known paper about cluster analysis and visualization. The details of how the data was collected are outlined in the paper."
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
			case ".csv": return read_csv(f)
			case ".xlsx": return read_excel(f)
			case _: return read_table(f)


	async def HandleData():
		df = await LoadData()

		index_col = "NAME" if "NAME" in df.columns else "UNIQID"
		index_labels = df[index_col]

		# Drop the naming columns before linkage.
		data = df.drop(columns=[col for col in ["UNIQID", "NAME"] if col in df.columns])
		x_labels = ['X' + name if list(data.columns).count(name) == 1 else 'X' + name + f'.{i+1}' for i, name in enumerate(data.columns)]

		return list(index_labels), x_labels, data


	def GenerateDendrogram(data, ax, orientation, labels = [], invert=False):
		matrix = hierarchy.linkage(data.values.T if invert else data.values, method=input.ClusterMethod().lower(), metric=input.DistanceMethod().lower())
		dendrogram = hierarchy.dendrogram(matrix, ax=ax, orientation=orientation.lower())

		if labels:
			labels = [labels[i] for i in dendrogram['leaves']]

		match orientation:
			case "Left" | "Right":
				ax.set_xticks([])
				ax.set_yticklabels(labels, fontsize=input.TextSize())
			case "Top" | "Bottom":
				ax.set_yticks([])
				ax.set_xticklabels(labels, fontsize=input.TextSize())

		return dendrogram


	async def GenerateHeatmap():
		"""
		@brief Generates the Heatmap
		@returns The heatmap
		"""

		index_labels, x_labels, data = await HandleData()

		# Create a figure with a heatmap and associated dendrograms
		fig = figure(figsize=(12, 10))
		gs = fig.add_gridspec(4, 2, height_ratios=[2, 8, 1, 1], width_ratios=[2, 8], hspace=0, wspace=0)

		# If we render the row dendragram, we change the order of the index labels to match the dendragram.
		# However, if we aren't rendering it, and thus row_dendragram isn't defined, we simply assign df
		# To data, so the order changes when turning the toggle.
		if "row" in input.Features():
			ax_row = fig.add_subplot(gs[1, 0])
			row_dendrogram = GenerateDendrogram(data, ax_row, "Left")
			ax_row.axis("off")
			index_labels = [index_labels[i] for i in row_dendrogram['leaves']]
			df = data.iloc[row_dendrogram['leaves']]
		else:
			df = data

		# If we render the column dendragram.
		if "col" in input.Features():
			ax_col = fig.add_subplot(gs[0, 1])
			col_dendrogram = GenerateDendrogram(data, ax_col, "Top", invert=True)
			ax_col.axis("off")

		# Handle normalization
		match input.ScaleType():
			case "Row": df = df.div(df.max(axis=1), axis=0)
			case "Column": df = df.div(df.max(axis=0), axis=1)

		# Render the heatmap.
		ax_heatmap = fig.add_subplot(gs[1, 1])
		heatmap = ax_heatmap.imshow(
			df,
			cmap=input.ColorMap().lower(),
			interpolation=input.Interpolation().lower(),
			aspect="auto",
		)

		# If we render the Y axis.
		if "y" in input.Features():
			ax_heatmap.set_yticks(range(len(index_labels)))
			ax_heatmap.set_yticklabels(index_labels, fontsize=input.TextSize())
			ax_heatmap.yaxis.tick_right()
		else:
			ax_heatmap.set_yticklabels([])

		# If we render the X axis.
		if "x" in input.Features():
			ax_heatmap.set_xticks(range(len(x_labels)))
			ax_heatmap.set_xticklabels(x_labels, rotation=90, fontsize=input.TextSize())
		else:
			ax_heatmap.set_xticklabels([])

		# If we render the legend.
		if "legend" in input.Features():
			ax_cbar = fig.add_subplot(gs[3, 1])
			cbar = fig.colorbar(heatmap, cax=ax_cbar, orientation='horizontal')

		return fig


	@output
	@render.table
	async def LoadedTable(): return await LoadData()

	@output
	@render.plot
	async def Heatmap(): return await GenerateHeatmap()


	@output
	@render.plot
	async def RowDendrogram():
		index_labels, _, data = await HandleData()

		fig = figure(figsize=(12, 10))
		ax = fig.add_subplot(111)

		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['left'].set_visible(False)

		GenerateDendrogram(data, ax, input.Orientation(), index_labels)
		return fig


	@output
	@render.plot
	async def ColumnDendrogram():
		_, x_labels, data = await HandleData()

		fig = figure(figsize=(12, 10))
		ax = fig.add_subplot(111)

		ax.spines['top'].set_visible(False)
		ax.spines['right'].set_visible(False)
		ax.spines['bottom'].set_visible(False)
		ax.spines['left'].set_visible(False)

		GenerateDendrogram(data, ax, input.Orientation(), x_labels, invert=True)
		return fig


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

			# https://docs.scipy.org/doc/scipy/reference/generated/scipy.cluster.hierarchy.linkage.html
			ui.input_select(id="ClusterMethod", label="Clustering Method", choices=["Single", "Complete", "Average", "Weighted", "Centroid", "Median", "Ward"], selected="Average"),

			# https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.distance.pdist.html#scipy.spatial.distance.pdist
			ui.input_select(id="DistanceMethod", label="Distance Method", choices=["Braycurtis", "Canberra", "Chebyshev", "Cityblock", "Correlation", "Cosine", "Dice", "Euclidean", "Hamming", "Jaccard", "Jensenshannon", "Kulczynski1", "Mahalanobis", "Matching", "Minkowski", "Rogerstanimoto", "Russellrao", "Seuclidean", "Sokalmichener", "Sokalsneath", "Sqeuclidean", "Yule"], selected="Euclidean"),

			ui.input_numeric(id="TextSize", label="Text Size", value=8, min=1, max=50, step=1),

			ui.panel_conditional(
				"input.MainTab === 'Interactive'",
				ui.br(),

				# Define how the colors are scaled.
				ui.input_select(id="ScaleType", label="Scale Type", choices=["Row", "Column", "None"], selected="None"),

				# https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.imshow.html
				ui.input_select(id="Interpolation", label="Interpolation", choices=["None", "Antialiased", "Nearest", "Bilinear", "Bicubic", "Spline16", "Spline36", "Hanning", "Hamming", "Hermite", "Kaiser", "Quadric", "Catrom", "Gaussian", "Bessel", "Mitchell", "Sinc", "Lanczos", "Blackman"], selected="Nearest"),

				# Set the ColorMap used.
				ui.input_select(id="ColorMap", label="Color Map", choices=["Viridis", "Plasma", "Inferno", "Magma", "Cividis"], selected="Viridis"),

				# Toggle rendering features. All are on by default.
				ui.input_checkbox_group(id="Features", label="Heatmap Features",
					choices={"row": "Row Dendrogram", "col": "Column Dendrogram", "x": "X Labels", "y": "Y Labels", "legend": "Legend"},
					selected=["row", "col", "x", "y", "legend"])
			),

			ui.panel_conditional(
				"input.MainTab === 'Row' || input.MainTab === 'Column'",
				ui.br(),

				# Define the Orientation of the Dendrogram in the Tab
				ui.input_select(id="Orientation", label="Dendrogram Orientation", choices=["Top", "Bottom", "Left", "Right"], selected="Left"),
			),


			# Add the download buttons. You can download the heatmap by right clicking it :)
			ui.download_button("DownloadTable", "Download Table"),

			id="SidebarPanel",
		),

		# Add the main interface tabs.
		ui.navset_tab(
				ui.nav_panel("Interactive", ui.output_plot("Heatmap", height="90vh"), value="Interactive"),
				ui.nav_panel("Row Dendrogram", ui.output_plot("RowDendrogram", height="90vh"), value="Row"),
				ui.nav_panel("Column Dendrogram", ui.output_plot("ColumnDendrogram", height="90vh"), value="Column"),
				ui.nav_panel("Table", ui.output_table("LoadedTable"), value="Table"),

				id="MainTab"
		),
	)
)

app = App(app_ui, server)