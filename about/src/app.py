from shiny import App, Inputs, Outputs, Session, reactive, render, ui

# This is a temporary fix. I don't like putting HTML in python files, 
# and the far better solution is to simply create a GitHub wiki or something
# Similar. However, for testing purposes, this will remain, as it does
# Technically work, until I get around to replacing it.
from features import features
from information import information
from gallery import gallery

introduction = """
<!DOCTYPE html>
<html>
		<meta charset="UTF-8">
		
		<title>Contact</title>
        
		<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
		
		<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.8.2/jquery.min.js"></script>
		<script src="http://netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>
		
		<script>
			$(function(){ 
				$("#navbar").load("../../../www/navbar.html", function(){ 
					$('#aboutTab').addClass('active');
					$('#heatmapper-logo').on('click', function(){ window.location.href = '/'; });
				});
			}); 
		</script>
		
		<script type="text/javascript" src="../../../www/js/google-analytics.js"></script>
</html>
"""

def server(input: Inputs, output: Outputs, session: Session):

	@output
	@render.ui
	@reactive.event(input.NavigationPanel)
	def Tab():
		return ui.TagList(
			ui.navset_tab(
					ui.nav_panel(
						"File Input",
						ui.HTML(introduction)
					),
					ui.nav_panel(
						"Features",
						#ui.HTML(open("../../www/features/" + input.NavigationPanel() + ".html").read())
					),
					ui.nav_panel(
						"Gallery / Links",
						#ui.HTML(open("../www/gallery/" + input.NavigationPanel() + ".html").read())
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