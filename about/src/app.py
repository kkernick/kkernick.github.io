from shiny import App, Inputs, Outputs, Session, reactive, render, ui

# This is a temporary fix. I don't like putting HTML in python files, 
# and the far better solution is to simply create a GitHub wiki or something
# Similar. However, for testing purposes, this will remain, as it does
# Technically work, until I get around to replacing it.
from features import features
from information import information
from gallery import gallery

def server(input: Inputs, output: Outputs, session: Session):

	@output
	@render.ui
	@reactive.event(input.NavigationPanel)
	def Tab():
		return ui.TagList(
			ui.navset_tab(
					ui.nav_panel(
						"File Input",
						ui.HTML("../www/input/" + input.NavigationPanel() + ".html")
					),
					ui.nav_panel(
						"Features",
						ui.HTML("../www/features/" + input.NavigationPanel() + ".html")
					),
					ui.nav_panel(
						"Gallery / Links",
						ui.HTML("../www/gallery/" + input.NavigationPanel() + ".html")
					)
			),
		)


app_ui = ui.page_fluid(
	ui.panel_title(ui.HTML('<a href="https://kkernick.github.io">Heatmapper</a>')),
	ui.layout_sidebar(
		ui.sidebar(

			# This is out main tab of choices the user can select.
			ui.navset_tab(
				ui.nav_panel(title="Introduction", value="introduction"), 
				ui.nav_panel(title="Expression", value="expression"), 
				ui.nav_panel("Pairwise", value="pairwise"), 
				ui.nav_panel("Image Overlay", value="image"),
				ui.nav_panel("Geomap", value="geomap"),
				ui.nav_panel("Geocoordinate", value="geocoordinate"),
				id="NavigationPanel",
			),
			id="SidebarPanel",
			width=200
		),

		# This is the content regarding the choice, rendering in server()
		ui.output_ui("Tab"),
	)
)	

app = App(app_ui, server)