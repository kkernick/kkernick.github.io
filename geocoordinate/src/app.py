from shiny import App, Inputs, Outputs, Session, reactive, render, ui

# We need to import here so ShinyLive doesn't get upset.
import numpy, certifi, branca, xyzservices

import folium

def server(input: Inputs, output: Outputs, session: Session):
	pass


app_ui = ui.page_fluid(
	ui.panel_title(ui.HTML('<a href="https://kkernick.github.io">Heatmapper</a>')),
	ui.layout_sidebar(
		ui.sidebar(
			ui.HTML("<a href=../../about/site/index.html>Data Format</a>"),
			id="SidebarPanel",
			width=200
		),

		ui.navset_tab(
				ui.nav_panel(
					"Interactive",
					folium.Map((45.5236, -122.6750), tiles="cartodb positron")
				),
				ui.nav_panel(
					"Table",
				),
		),
	)
)	

app = App(app_ui, server)