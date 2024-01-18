from shiny import App, Inputs, Outputs, Session, reactive, render, ui

# This is a temporary fix. I don't like putting HTML in python files, 
# and the far better solution is to simply create a GitHub wiki or something
# Similar. However, for testing purposes, this will remain, as it does
# Technically work, until I get around to replacing it.
from features import features
from information import information
from gallery import gallery


def server(input: Inputs, output: Outputs, session: Session):

	def fetch_page(www_page):
		return ui.HTML("""
			<!DOCTYPE html>
			<html>
				<head>	
					<script>
						$(function(){ 
							$("#panel").load("../../www/""" + www_page + """.html");
						}); 
					</script>
				</head>  
				
				<div id="panel"></div>
			</html>
		""")

	@output
	@render.ui
	@reactive.event(input.NavigationPanel)
	def Tab():
		return ui.TagList(
			ui.navset_tab(
					ui.nav_panel(
						"File Input",
						fetch_page("input/" + input.NavigationPanel())
					),
					ui.nav_panel(
						"Features",
						fetch_page("features/" + input.NavigationPanel())
					),
					ui.nav_panel(
						"Gallery / Links",
						fetch_page("gallery/" + input.NavigationPanel())
					),
					id="Tab"
			),
		)


app_ui = ui.page_fluid(
	ui.panel_title(ui.HTML('<a href="https://kkernick.github.io">Heatmapper v2.8</a>')),
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