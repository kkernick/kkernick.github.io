gallery = {
	"introduction": """
<!DOCTYPE html>
<html>
  <head>
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
		
  </head>  
	
  <body>
		<div id="navbar"></div>
		<div class="container-fluid well">
			<h2>Contact</h2>
			Questions or comments? Please use our <a href="http://feedback.wishartlab.com/?site=heatmapper" target="_blank">feedback page</a>.
			<br />
			<br />
			This project was developed in the <a href="http://www.wishartlab.com/" target="_blank">Wishart Research Group</a> at the University of Alberta.<br />
			Financial support was provided by the <a href="http://www.cihr-irsc.gc.ca" target="_blank">Canadian Institutes of Health Research (CIHR)</a><br />
			and by <a href="http://genomealberta.ca" target="_blank">Genome Alberta</a>, a division of Genome Canada.
			<br />
			Information on file format requirements can be found on the <a href="/about/instructions">Instructions Page</a>. 
			<br />
			All source code for this project can be found on <a href="https://github.com/sbabicki/heatmapper" target="_blank">GitHub</a>.
			<br />
			License: <a href="http://creativecommons.org/licenses/by-sa/2.0/" target="_blank">Creative Commons Attribution-ShareAlike 2.0 Generic</a>
		</div>
	</body>
</html>
""",

"expression": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
		<style>
			.border-img {
				border:0.2em solid black;
				width:100%;
				height:15em;
				border-radius:0.4em;
				max-width:20em;
				display: block;
				margin-left: auto;
				margin-right: auto;
			}
			
			
			
			figcaption {
				text-align:center;
				margin-bottom:0.5em;
			}

			.myRow {
				display:table-row;
			}
			.myCol {
				display:table-cell;
				width:33%;
			}
			.myTable {
				border-spacing:1em;
			}

		</style>
    </head>  
    <body>
		<!-- <img src="../../www/images/expression.png" alt="image overlay" class="border-img"> -->

		<div class="myTable">
			
			<div class="myRow">
				
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HME1.png">
							<img src="../../www/gallery/images/HME1_low.png" alt="Example 1" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 1</h5>
							<em>
							Sample input retreived from the website for the Ashley Lab 
							<a href="http://ashleylab.stanford.edu/tools/tools-scripts.html" target="_blank">Heatmap Builder</a>
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
				
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HME2.png">
							<img src="../../www/gallery/images/HME2_low.png" alt="Example 2" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 2</h5>
							<em>
							Example dataset from a tutorial by Yan Cui (ycui2@uthsc.edu).
							</em>
						</figcaption>
						
					 </figure>
				</div>
			</div>
				
			<div class="myRow">	
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HME3.png">
							<img src="../../www/gallery/images/HME3_low.png" alt="Example 3" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 3</h5>
							<em>
							Dataset from the 		
							<a href="http://genome-www.stanford.edu/clustering/" target="_blank">online supplement</a>
							 to Eisen et al. (1998). The details of how the data was collected are outlined in the paper.
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
			</div>
			
			
		
		</div>
    </body>
</html>	
""",

"geocoordinate": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
		<style>
			.border-img {
				border:0.2em solid black;
				width:100%;
				height:15em;
				border-radius:0.4em;
				max-width:20em;
				display: block;
				margin-left: auto;
				margin-right: auto;
			}
			
			
			
			figcaption {
				text-align:center;
				margin-bottom:0.5em;
			}

			.myRow {
				display:table-row;
			}
			.myCol {
				display:table-cell;
				width:33%;
			}
			.myTable {
				border-spacing:1em;
			}

		</style>
    </head>  
    <body>

		<div class="myTable">
			
			<div class="myRow">
				
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMC1.png">
							<img src="../../www/gallery/images/HMC1_low.png" alt="Example 1" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 1</h5>
							<em>
							Deaths from a 
							<a href="https://en.wikipedia.org/wiki/1854_Broad_Street_cholera_outbreak" target="_blank">cholera outbreak</a>
							 in 1854. 
							<a href="https://en.wikipedia.org/wiki/John_Snow_(physician)" target="_blank">John Snow</a>  
							 used this data in conjunction with local pump locations as evidence that cholera is spread by contaminated water. A 
							<a href="https://www.google.com/fusiontables/DataSource?docid=147wlDisDp6NnpNxHQpbnjAQ-iW4dR2MAmFdQxYc#map:id=3" target="_blank">digitised version</a>
							 of the data is available online, courtesy of Robin Wilson.
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
				
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMC2.png">
							<img src="../../www/gallery/images/HMC2_low.png" alt="Example 2" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 2</h5>
							<em>
							Bike thefts in Vancouver in 2011. The data was obtained from a 2013 Vancouver Sun 
							<a href="http://blogs.vancouversun.com/2013/12/27/get-the-raw-data-for-our-bike-theft-and-auto-crime-series-right-here/" target="_blank">blog post</a>
							 by Chad Skelton.
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
			</div>

			<div class="myRow">	
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMC3.png">
							<img src="../../www/gallery/images/HMC3_low.png" alt="Example 3" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 3</h5>
							<em>
							The location of traffic signals in Toronto. The data was obtained from 
							<a href="http://www1.toronto.ca/wps/portal/contentonly?vgnextoid=9e56e03bb8d1e310VgnVCM10000071d60f89RCRD" target="_blank">Toronto Open Data</a>
							. The idea to use this data set comes from this 
							<a href="http://www.r-bloggers.com/heatmap-of-toronto-traffic-signals-using-rgooglemaps/" target="_blank">R-bloggers post</a>
							 by Myles Harrison.
							</em>
						</figcaption>
						
					 </figure>
				</div>
			</div>
			
			
		
		</div>
    </body>
</html>	
""",

"geomap": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
		<style>
			.border-img {
				border:0.2em solid black;
				width:100%;
				height:15em;
				border-radius:0.4em;
				max-width:20em;
				display: block;
				margin-left: auto;
				margin-right: auto;
			}
			
			
			figcaption {
				text-align:center;
				margin-bottom:0.5em;
			}

			.myRow {
				display:table-row;
			}
			.myCol {
				display:table-cell;
				width:33%;
			}
			.myTable {
				border-spacing:1em;
			}

		</style>
    </head>  
    <body>

		<div class="myTable">
			
			<div class="myRow">
				
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMG1.png">
							<img src="../../www/gallery/images/HMG1_low.png" alt="Example 1" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 1</h5>
							<em>
							Example data from a 
							<a href="http://open.canada.ca/data/en/dataset/23f028e8-424e-4c73-ace4-4e3614e0e3aa" target="_blank">carbon monoxide emissions study</a>
							 conducted by Environment Canada. The results displayed are from the 1990 dataset.
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
				
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMG2.png">
							<img src="../../www/gallery/images/HMG2_low.png" alt="Example 2" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 2</h5>
							<em>
							Example from Statistics Canada. Data adapted from 
							<a href="http://www5.statcan.gc.ca/cansim/pick-choisir?lang=eng&id=01030553&p2=33" target="_blank">New cases and age-standardized rate for primary cancer</a>
							 (based on the February 2014 CCR tabulation file), by cancer type and sex, Canada, provinces and territories. The columns represent new cancer cases (age-standardized rate per 100,000 population). This example is for 2006.
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
			</div>
				
			<div class="myRow">	

				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMG3.png">
							<img src="../../www/gallery/images/HMG3_low.png" alt="Example 3" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 3</h5>
							<em>
							Example from the 
							<a href="http://www.cdc.gov/" target="_blank">U.S. Centers for Disease Control and Prevention</a>
							. The data is from 
							<a href="http://gis.cdc.gov/grasp/diabetes/DiabetesAtlas.html" target="_blank">Diagnosed Diabetes, Age Adjusted Rate (per 100), Adults - Total, 2013.</a>
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
			</div>
			
			
		
		</div>
    </body>
</html>	
""",

"image": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
		<style>
			.border-img {
				border:0.2em solid black;
				width:100%;
				height:15em;
				border-radius:0.4em;
				max-width:20em;
				display: block;
				margin-left: auto;
				margin-right: auto;
			}
			
			
			figcaption {
				text-align:center;
				margin-bottom:0.5em;
			}

			.myRow {
				display:table-row;
			}
			.myCol {
				display:table-cell;
				width:33%;
			}
			.myTable {
				border-spacing:1em;
			}

		</style>
    </head>  
    <body>

		<div class="myTable">
			
			<div class="myRow">
				
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMI1.png">
							<img src="../../www/gallery/images/HMI1_low.png" alt="Example 1" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 1</h5>
							<em>
							X-ray CT scan of a rat treated with polyethylene glycol (PEG)-protected gold nanorods to allow visualization of tumors (from 
							<a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2712876/" target="_blank">Maltzahn et al.</a>
							). Example grid overlay: Temperature heat map example (artifical data, not taken from the paper).
							</em>
						</figcaption>
						
						
					 </figure>
				</div>

				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMI2.png">
							<img src="../../www/gallery/images/HMI2_low.png" alt="Example 2" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 2</h5>
							<em>
							A 'Square' overlay representation of the above data, showing the non-linear grid with the respective intensity values.
							</em>
						</figcaption>
						
					 </figure>
				</div>
				
			</div>
			
			
		
		</div>
    </body>
</html>	
""",

"pairwise": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css"/>
		<style>
			.border-img {
				border:0.2em solid black;
				width:100%;
				height:15em;
				border-radius:0.4em;
				max-width:20em;
				display: block;
				margin-left: auto;
				margin-right: auto;
			}
			
			
			
			figcaption {
				text-align:center;
				margin-bottom:0.5em;
			}

			.myRow {
				display:table-row;
			}
			.myCol {
				display:table-cell;
				width:33%;
			}
			.myTable {
				border-spacing:1em;
			}

		</style>
    </head>  
    <body>

		<div class="myTable">
			
			<div class="myRow">
				
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMP1.png">
							<img src="../../www/gallery/images/HMP1_low.png" alt="Example 1" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 1</h5>
							<em>
							NMR structure of Contryphan-Vc1 (PDB: 2n24)
							</em>
						</figcaption>
						
						
					 </figure>
				</div>

				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMP2.png">
							<img src="../../www/gallery/images/HMP2_low.png" alt="Example 2" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 2</h5>
							<em>
							Interactive mode of a plot section for Contryphan-Vc1
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
			</div>	

			<div class="myRow">	
				<div class="well myCol">
					<figure>
						
						<a href="../../www/gallery/images/HMP3.png">
							<img src="../../www/gallery/images/HMP3_low.png" alt="Example 3" class="border-img">
						</a>
						
						<figcaption>
							<h5>Example 3</h5>
							<em>
							Metabolite concentrations of 39 rumen samples measured by proton NMR from dairy cows fed with different proportions of barley grain. (Ametaj BN, et al. (2010) "Metabolomics reveals unhealthy alterations in rumen metabolism with increased proportion of cereal grain in the diet of dairy cows", Metabolomics 6-4:583-594)
							</em>
						</figcaption>
						
						
					 </figure>
				</div>
				
				
			</div>
			
			
		
		</div>
    </body>
</html>	
"""
}