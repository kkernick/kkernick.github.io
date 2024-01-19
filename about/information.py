information = {
	"expression": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
		<style>
			td {padding:0.5em;}

			.opt {
				text-align: center;
			}		

			.desc {
				text-align: left;
				width: 50%;
			}

			.desc_table {
				text-align: left;
				width: 70%;
			}

		</style>
    </head>  
    <body>
		<div class = "well">
			The expression function within Heatmapper allows the user to view unclustered
			expression data, such as that from transcriptomic (microarray or RNAseq),
			proteomic or metabolomic experiments.
			
			<h4>Accepted File Formats</h4>
			<ul>
				<li>Tab separated with extensions <em>.txt</em>, .<em>dat</em>, <em>.tsv</em>, or <em>.tab</em></li>
				<li>First sheet of an Excel workbook with extension <em>.xlsx</em></li>
			</ul>
			
			<h4>Data Structure</h4>
			<ul>
				<li>The first (header) row is used to assign column names.</li>
				<li>A column labeled UNIQID is required.</li>
				<li>If a column labeled "NAME" exists (optional), it will be used to assign row names.</li>
				<li>Any additional columns containing non-numeric data will be ignored.</li>
				<li>Data values can be positive or negative numbers.</li>
			</ul>
			<h4>Range</h4>
			<ul>
				<li>First row: column names</li>
				<li>NAME column: row names</li>
				<li>Other Columns: any positive or negative number</li>
				<li>Input data can have up to 2,500 rows and 300 columns</li>
			</ul>
			
			<h4>Example</h4>
			
			Download an example input file <a href="../../../about/www/input/examples/expression_example1.txt" target="_blank">here</a> (Example 1).
			<br /><br />
			
			Example layout (snippet, with tabs replaced by spaces to make the columns apparent):
			<br />
			
<code style="white-space: pre;">
UNIQID     NAME                                             1             1             1             2             2             2
Hs.9305    angiotensin receptor-like 1            0.533865724   2.667389535    1.98516763   4.832817262   3.590801314   3.309607441
Hs.181307  H3 histone, family 3A                 -0.942951315  -0.500171526  -0.705453196   -0.32191231   -0.14030858  -0.427467964
Hs.83484   SRY (sex determining region Y)-box 4  -3.418094026  -3.181358856  -3.276305367  -2.392780506  -1.740889988  -2.248737455
...</code>
			
			<br />
			<br />
			
			Tab-delimited version:
			<br />
			
<code style="white-space: pre;">
UNIQID	NAME	1	1	1	2	2	2
Hs.9305	angiotensin receptor-like 1	0.533865724	2.667389535	1.98516763	4.832817262	3.590801314	3.309607441
Hs.181307	H3 histone, family 3A	-0.942951315	-0.500171526	-0.705453196	-0.32191231	-0.14030858	-0.427467964
Hs.83484	SRY (sex determining region Y)-box 4	-3.418094026	-3.181358856	-3.276305367	-2.392780506	-1.740889988	-2.248737455
...</code>
			
			<br />
			<br />
			
			In this example, because the 'NAME' column is present, it is used to assign row names
			instead of the 'UNIQID' column. Since the column names are not unique, Heatmapper will
			automatically modify them to create unique column names.
			
			<br />
			<br />
			
			With the Import Existing Clusters option, one may also
			upload existing clusters from a file in <a href='http://evolution.genetics.washington.edu/phylip/newicktree.html' target="_blank">Newick Tree Format</a>. The node names in the tree must match the label names in the data file and must not include  blanks, colons, semicolons, parentheses, or square brackets. 
			The following are example cluster files for Example 1 (linked above): <a href="../../../about/www/input/examples/expression_example1_column_clusters.txt" target="_blank">column_clusters</a> and <a href="../../../about/www/input/examples/expression_example1_row_clusters.txt" target="_blank">row_clusters</a>
			
		</div>

<div>
<h5>An example of expression functionality: data from the Ashley Lab <a href="http://ashleylab.stanford.edu/tools/tools-scripts.html">Heatmap Builder</a></h5>
<p>You may use the data file given above for this example.</p>
<br></br>
<p>Click on the Expression tab on the main header and select the Upload File radio button, followed by the Choose File button. Alternatively, you may choose the 'Example File' radio button. Note: details about the example may be viewed by clicking the Information Icon. The following plot is created.</p>
<br></br>
<center><img src="../../../about/www/input/images/HME1.png" width="70%" height="70%"</body></img></center>
<br></br>


<p class="opt">The following menu shows the available options. Each option is reviewed below.</p>
<br></br>
<center><img src="../../../about/www/input/images/HME2.png" width="40%" height="40%"</body></img></center>
<br></br>

<center><img src="../../../about/www/input/images/HME3.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Scale Type:</strong> Select direction to scale values in. There are three options: 'Row', 'Column', 'None'. The <strong>Row</strong> option is the default, which scales values by data rows. The <strong>Column</strong> option scales values by columns, as shown on the plot.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME4.png" width="50%" height="50%"</body></img>
<p class="desc">The <strong>None</strong> scaling option does not scale the values, as seen on the plot.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME5.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Color Brightness:</strong> Adjust the brightness of the colors on the plot. The default value is 0. By increasing it, to '30' for example, the plot is brighter. Some regions are more easily distinguished.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME6.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Number of Shades:</strong> Change the number of colors to be used on the plot. A lower value, such as 3, would group the data into only 3 categories by color as seen in the plot, and a more general pattern is observed. A higher value would divide the data further by color and more detail would be seen.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME7.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Color:</strong> Change the colors to be used for the plot. The Low Color, Middle Color, and High Color color boxes can be used to adjust the gradient. For example, by selecting a yellow from the 'Low Color' palette and a purple from the 'Middle Color' pallete, data values now progress from yellow to purple, to red. With this option, the very low and very high values are more visibly distinguishable.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME11.png" width="50%" height="50%"</body></img>
<p class="desc">Another color scheme with light grey, dark grey, and red results in this plot. Now the high values are more distinguishable than all the rest.</p>
</center>
<br></br>

<center>
<p class="desc"><strong>Clustering Method:</strong> Choose the method to be used for computing hierarchical clustering. The data would be grouped by similar expression levels.</p>
<p class="desc"><strong>Average Linkage</strong> - The distance between two clusters is the mean distance between all objects of the clusters (the default option).</p>
<p class="desc"><strong>Centroid Linkage</strong> - The distance between two clusters is the distance between their centroid values, as shown in this plot.</p>
<p class="desc"><strong>Complete Linkage</strong> - The distance between two clusters is the largset distance between the objects of the clusters.</p>
<p class="desc"><strong>Single Linkage</strong> - The distance between two clusters is the smallest distance between an objects of one cluster and another object of the other cluster.</p>
<p class="desc"><strong>Import Existing Clusters</strong> - Upload existing clusters from a file in <a href='http://evolution.genetics.washington.edu/phylip/newicktree.html' target="_blank">Newick Tree Format</a>. The node names in the tree must match the label names in the data file and must not include  blanks, colons, semicolons, parentheses, or square brackets. The following are example cluster files for Example 1: <a href="../../../about/www/input/examples/expression_example1_column_clusters.txt" target="_blank">column_clusters</a> and <a href="../../../about/www/input/examples/expression_example1_row_clusters.txt" target="_blank">row_clusters</a></p>
<p class="desc"><strong>None</strong> - No clustering method is applied to the data. No dendrogram is created (either by row/column). Also, the Distance Measurement Method option is no longer applicable.</p>
</center>
<br></br>

<center>
<p class="desc"><strong>Distance Measurement Method:</strong> Choose the method to be used for computing distance between rows and columns. The selected distance method is used by the selected clustering algorithm to compute distances.
<p class="desc"><strong>Eucledian</strong> - The distance is computed as the length of the line segment connecting two values.</p>
<p class="desc"><strong>Pearson</strong> - The distance is the absolute value of the Pearson correlation coefficient (between 0 and 1).</p>
<p class="desc"><strong>Kendall's Tau</strong> - The distance is the number of pairwise disagreements between two groups of values. The larger the distance, the more dissimillar the two clusters are.</p>
<p class="desc"><strong>Spearman Rank Correlation</strong> - The distance is measured as the strength of association between two ranked values/groups.</p>
<p class="desc"><strong>Manhattan</strong> - The distance is the sum of distances (along each dimension) between two values.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME8.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Apply Clustering to Rows/Columns:</strong> Cluster the data by rows, columns, or both by selecting/removing the appropriate tabs. The default option is 'Rows'. As with this example, row clustering would group the genes by similar expression patterns, while column clustering would group the samples with similar expression levels. Row and column clustering would do both. This plot shows Column clustering, with the default 'Average Linkage' clustering method and 'Eucledian' distance method (compare with the first image on this page, clustered by rows).</p>
</center>
<br></br>



<center><img src="../../../about/www/input/images/HME9.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Show Dendrogram:</strong> Choose to display the row/column clustering on the plot. For exmaple, after applying the clustering to both 'Rows' and 'Columns', choosing to show both 'Rows' and 'Columns' dendrograms with display the clustering information for both rows and columns on the plot, as seen in the image.</p>
</center>
<br></br>

<p>There are two Download options that may be used to download the plot/data at any step during the experience. The <strong>Plot</strong> option will download the an image of the plot as seen on the webpage (as PNG, PDF, PNG, or TIFF). The <strong>Table</strong> option will download the raw data in table format (as TXT or CSV).</p>

<p class="opt">Further fine tuning may be performed with the <strong>Show Advanced Options</strong> tab. The seven available options are described below.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMArrow.png" width="40%" height="40%"</body></img>
<p></p>
</center>

<center><img src="../../../about/www/input/images/HMEAdvanced.png" width="40%" height="40%"</body></img>
</center>
<br></br>

<center>
<p class="desc"><strong>Plot Width:</strong> By expanding the plot width, the size of the individual cells will increase horizontally. Similarly, by decreasing the width, the cells will be more compact.</p>
<p class="desc"><strong>Plot Heigth:</strong> By expanding the plot height, the size of the individual cells will increase vertically. Similarly, by decreasing the height, the cells will be more compact.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME10.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Preview Full Height:</strong> Expand the plot vertically (the cells will have a minimum height). This improves visualization. A portion of the plot is shown here.</p>
</center>
<br></br>

<center>
<p class="desc"><strong>Title:</strong> Name the plot.</p>
<p class="desc"><strong>X Axis Label:</strong> Name the x-axis.</p>
<p class="desc"><strong>Y Axis Label:</strong> Name the y-axis.</p>
</center>
<br></br>

<center>
<p class="desc"><strong>Missing Data Color:</strong> Choose a color to distinguish the cells that have no value (for example if a chip was damaged at particular pixels). For this example, since the 'Middle Color' of the plot is also set to black, changing the missing color to yellow would display the empty cells with yellow, in contrast to the red/green on the plot. This is also a good way to check that there is no missing data, as is the case for this exmaple.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME12.png" width="70%" height="70%"</body></img>
<p class="desc_table">To view a section of the plot in more detail click on the <strong>Interactive</strong> tab next to the 'Plot' tab. Click and drag a portion of the plot to zoom in (by clicking once more anywhere on the plot, it will zoom back out). Hovering over the plot will display specific cell information, as shown in the image.</p>
</center>
<br></br>


<center><img src="../../../about/www/input/images/HME13.png" width="70%" height="70%"</body></img>
<p class="desc_table">To view the full Row Dendrogram click on the <strong>Row Dendrogram</strong> tab next to the 'Interactive' tab. This will display the clustering relationships by row (in this case by expression levels between genes). Note that the clustering must be applied to 'Rows' for a dendrogram to be computed.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME14.png" width="70%" height="70%"</body></img>
<p class="desc_table">To view the full Column Dendrogram click on the <strong>Column Dendrogram</strong> tab next to the 'Row Dendrogram' tab. This will display the clustering relationships by column (in this case by expression levels between samples). Note that the clustering must be applied to 'Columns' for a dendrogram to be computed.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME15.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may also view the data in Table format by clicking on the <strong>Table</strong> tab next to the 'Column Dendrogram' tab. This will display the expression values for all genes and samples.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME16.png" width="70%" height="70%"</body></img>
<p class="desc_table">The table is searchable, by the gene name/id, or expression value. The user may enter a search value in the main <strong>Search</strong> box above the table, or in a column specific search box directly below the table. For example, by entering the name 'cathepsin O' in the <strong>NAME</strong> search box, all sample values for 'cathepsin O' are retrieved.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HME17.png" width="70%" height="70%"</body></img>
<p class="desc_table">The table is also sortable, with the arrows located next to each header. For example, by clicking once on the NAME arrow, the table is sorted alphabetically by gene name.</p>
</center>


<br></br><br></br>
</div>

    </body>
</html>
""",

	"geocoordinate": """
	<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
		<style>
			td {padding:0.5em;}

			.opt {
				text-align: center;
			}		

			.desc {
				text-align: left;
				width: 50%;
			}

			.desc_table {
				text-align: left;
				width: 70%;
			}


		</style>
    </head>  
    <body>
		<div class = "well">
			<h4>Accepted File Formats</h4>
			<ul>
				<li>Comma-Separated Value with extension <em>.csv</em></li>
				<li>Tab separated with extensions <em>.txt</em>, <em>.dat</em>, <em>.tsv</em>, or <em>.tab</em></li>
				<li>First sheet of an Excel workbook with extension <em>.xls</em> or <em>.xlsx</em></li>
			</ul>
			<h4>Data Structure</h4>
			The data input must contain at least 2 columns with valid latitude and longitude coordinates. 
			An optional 3rd column containing values can be included for calculating a weighted density estimation instead of basing the estimation on density of points. 
			At least one value must be strictly greater than 0 if the value column is used. 
			The first row must contain the names for each column, "Latitude", "Longitude", and (when applicable) "Value".
			<h4>Range</h4>
			Latitude: any number between -180 and +180 <br />
			Longitude: any number between -90 and +90 <br />
			Value: any positive number<br />
			Input data can have up to 8,000 data points
			
			<h4>Example</h4>
			
			Download an example input file <a href="../../../about/www/input/examples/geocoordinate_example1.txt" target="_blank">here</a>.
			<br /><br />
			
			Example layouts:<br />
			
<code style="white-space: pre;">
Longitude	Latitude	Value
-0.13793	51.513418	3
-0.137883	51.513361	2
-0.137853	51.513317	1
-0.137812	51.513262	1
-0.137767	51.513204	4
...</code>

<br /><br />
or
<br />

<code style="white-space: pre;">
Value	Longitude	Latitude
3	-0.13793	51.513418
2	-0.137883	51.513361
1	-0.137853	51.513317
1	-0.137812	51.513262
4	-0.137767	51.513204
...</code>

<br /><br />
or
<br />

<code style="white-space: pre;">
Longitude	Latitude
-0.13793	51.513418
-0.137883	51.513361
-0.137853	51.513317
-0.137812	51.513262
-0.137767	51.513204
...</code>

		</div>

<div>
<h5>An example of geocoordinate functionality: Deaths from a cholera outbreak in 1854</h5>
<p>
John Snow used this data in conjunction with local pump locations as evidence that cholera is spread by contaminated water. A <a href="https://www.google.com/fusiontables/DataSource?docid=147wlDisDp6NnpNxHQpbnjAQ-iW4dR2MAmFdQxYc#map:id=3">digitised version</a> of the data is available online, courtesy of Robin Wilson (robin@rtwilson.com).
</p>
<p>You may use the data file given above for this example.</p>
<p>Click on the <strong>Geocoordinate</strong> tab on the main header and select the Upload File radio button, followed by the Choose File button. Alternatively, you may choose the 'Example File' radio button. Note: details about the example may be viewed by clicking the Information Icon. The following map is created. You may zoom in or out by clinking on the <strong>'+'</strong> or <strong>'-'</strong> icons.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMC1.png" width="70%" height="70%"</body></img></center>
<br></br>

<p class="opt">The following menu shows the available options. Each option is reviewed below.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMC2.png" width="40%" height="40%"</body></img></center>
<br></br>

<center><img src="../../../about/www/input/images/HMC3.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Show/Hide Layers:</strong> Add or remove heatmap layers on the image. By deleting the <strong>Heatmap</strong> layer for example, only the area outline will display without the heatmap intensity visualization.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC4.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Map Type:</strong> Change the format of the map displayed. The three options besides 'Default' are 'Positron', 'Toner', and 'Watercolor'. The <strong>Positron</strong> view is a grey-scale mapping style.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC5.png" width="50%" height="50%"</body></img>
<p class="desc"> The <strong>Toner</strong> view is a black and white mapping style. This may be useful for clearly identifying jurisdictional areas/borders.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC6.png" width="50%" height="50%"</body></img>
<p class="desc"> The <strong>Watercolor</strong> view is a mapping style that uses a watercolor palette to differentiate features on the map.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC7.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Gaussian Radius Multiplier:</strong> Adjust the bandwidth for kernel density estimation. By increasing the value to 0.8, this image will be displayed. This may be useful to more clearly define areas of differing intensities and transitions.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC8.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Contour Smoothness:</strong> Adjust the number of grid points in each direciton for kernel density estimation. Lowering the value to 10 would limit the number of points that form the contour lines on the map. A more rugged outline is observed as follows. Increasing the value, on the other hand, would result in a more detailed outline.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC9.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Heatmap Opacity:</strong> Adjust the opacity of the outlined area. With an opacity of 1, the heatmap displays solid colors with no transparency. This option may be used to more clearly identity the affected area. By decreasing the opacity, the map features on the affected become more visible.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC10.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Number of Shades:</strong> Adjust the number of colors used for intensity transition. Increasing the value to 50 would result in a more detailed intensity progression on the map. This is a useful visual tool for displaying more detailed distributions.</p>
</center>
<br></br>


<center><img src="../../../about/www/input/images/HMC11.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Color Scheme:</strong> Change the color progression scheme. The two options besides 'Default' are 'Rainbow' and 'Topo'. The 'Default' view uses the 'Low Color' and 'High Color' settings to create a gradient for intensity. The <strong>Rainbow</strong> scheme does not use a color gradient,but instead assigns rainbow colors to different intensities, as shown in the image. This may be useful to better differentiate the areas of the distribution.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC12.png" width="50%" height="50%"</body></img>
<p class="desc">Similarly, the <strong>Topo</strong> color scheme assigns a different color to each kernel, with lighter colors representing higher values.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC13.png" width="50%" height="50%"</body></img>
<p class="desc">For the <strong>Default</strong> color scheme, the user may change the colors of the gradient. For example, by clicking on the <strong>Low Color</strong> colored box and choosing a light green value from the palette, this distribution is observed.</p>
</center>
<br></br>

<p>There are two Download options that may be used to download the map/data at any step during the experience. The <strong>Download Plot</strong> option will download the heatmap view in html format. The <strong>Download Table</strong> option will download a text format of the data in table format, containing the values for the given map divisions/dataset.</p>



<p class="opt">Further fine tuning may be performed with the <strong>Show Advanced Options</strong> tab. The two available options are described below.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMArrow.png" width="40%" height="40%"</body></img>
<p></p>
</center>

<center><img src="../../../about/www/input/images/HMCAdvanced.png" width="40%" height="40%"</body></img>
</center>
<br></br>


<center><img src="../../../about/www/input/images/HMC14.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Contour Line Width:</strong> Adjust the thickness of the kernel outlines. Increasing the value to '3' for example, will better differentiate the regions, as shown in the image.</p>
</center>
<br></br>



<center><img src="../../../about/www/input/images/HMC15.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Point Width:</strong> Adjust the size of the data points displayed on the map. Increasing the value to 4, for example, would more clearly display the points on the map, as shown in the image.</p>
</center>
<br></br>


<center><img src="../../../about/www/input/images/HMC16.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Point Opacity:</strong> Adjust the opacity of the data points displayed on the map. To remove the data points from the map, the opacity may be set to 0, as shown in the image. A higher opacity, on the other hand, would more clearly mark the points in a more solid color.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC17.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may also view the data in table format, by clicking the <strong>Table</strong> plot tab next to the 'Interactive' tab.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC18.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may search the Table values, using the Search functionality, either by using the main 'Search box' at the top of the table, or the three 'Longitute', 'Latitude', and 'Value' text boxes directly below the table. For example, by entering the value '15' in the <strong>Value search box</strong>, the above position is retrieved.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMC19.png" width="70%" height="70%"</body></img>
<p class="desc_table">The Table can be sorted by 'Longitute', 'Latitude', or 'Value' by clicking on the arrows next to these headings. For example, by cliking twice on the <strong>Value arrow</strong>, the table is sorted by decreasing intensity values to display the locations with higher values first, as shown in the image.</p>
</center>
<br></br>


<br></br><br></br>
</div>

    </body>
</html>
""",

"geomap": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
		<style>
			td {padding:0.5em;}

			.opt {
				text-align: center;
			}		

			.desc {
				text-align: left;
				width: 50%;
			}

			.desc_table {
				text-align: left;
				width: 70%;
			}

		</style>
    </head>  
    <body>
		<div class = "well">
			<h4>Accepted File Formats</h4>
			<ul>
				<li>Comma-Separated Value with extension <em>.csv</em></li>
				<li>Tab separated with extensions <em>.txt</em>, <em>.dat</em>, <em>.tsv</em>, or <em>.tab</em></li>
				<li>First sheet of an Excel workbook with extension <em>.xls</em> or <em>.xlsx</em></li>
			</ul>
			<h4>Data Structure</h4>
			The data input must contain at least 2 columns with region names in the first column and numeric values in the second. 
			More than one column of numeric values can be included. 
			The second column is selected by default to generate the heatmap.
			The selected column can be changed using a dropdown menu, which references different columns by the corresponding entry in the first row. 
			
			<h4>Range</h4>
			Region Names: names of regions which match the selected map region names<br />
			Other Columns: any positive or negative number<br />
			Input data can have up to 50 data columns
			
			<h4>Example</h4>
			
			Download an example input file <a href="../../../about/www/input/examples/geomap_example1.txt" target="_blank">here</a>.
			<br /><br />
			
			Example layout (with tabs replaced by spaces to make the columns apparent):
			<br />
			
<code style="white-space: pre;">
Province or territory              emissions 1990 (kt)  emissions 2000 (kt)   emissions 2013 (kt)
Newfoundland and Labrador          1520.3               844.2                 261.6
Prince Edward Island               152.3                83.4                  34.8
Nova Scotia                        315.2                218.5                 179.9
New Brunswick                      329.3                216.6                 147.4
Quebec                             2968                 2254.2                1713.8
Ontario                            3985                 2707.8                1500.4
Manitoba                           920.9                532.5                 228.8
Saskatchewan                       1138.7               686.5                 291.9
Alberta                            2416.6               1662.3                1191.3
British Columbia                   2475.1               1276.8                692.2
Yukon                              90                   43.3                  12.4
Northwest Territories and Nunavut  500.4                245.8                 46.7</code>
			
			<br /><br />
			Tab-delimited version (can be copied and pasted for use in Heatmapper):
			<br />
			
<code style="white-space: pre;">
Province or territory	emissions 1990 (kt)	emissions 2000 (kt)	emissions 2013 (kt)
Newfoundland and Labrador	1520.3	844.2	261.6
Prince Edward Island	152.3	83.4	34.8
Nova Scotia	315.2	218.5	179.9
New Brunswick	329.3	216.6	147.4
Quebec	2968	2254.2	1713.8
Ontario	3985	2707.8	1500.4
Manitoba	920.9	532.5	228.8
Saskatchewan	1138.7	686.5	291.9
Alberta	2416.6	1662.3	1191.3
British Columbia	2475.1	1276.8	692.2
Yukon	90	43.3	12.4
Northwest Territories and Nunavut	500.4	245.8	46.7</code>
			
			<br /><br />
			The name of the first column ("Province or territory" in this example) can be
			anything you like. Names of regions can be adjusted later on in Heatmapper under
			the Table tab if they do not match Heatmapper's region names exactly.
			
		</div>
<div>
<h5>An example of geomap functionality: A carbon monoxide <a href="http://open.canada.ca/data/en/dataset/23f028e8-424e-4c73-ace4-4e3614e0e3aa">emissions study</a> conducted by Environment Canada</h5>
<p>You may use the data file given above for this example.</p>
<p>Click on the <strong>Geomap</strong> tab on the main header and select the Upload File radio button, followed by the Choose File button. Alternatively, you may choose the 'Example File' radio button. Note: details about the example may be viewed by clicking the Information Icon. The following map is created. You may hover over an area to view the value for that specific region. Also, clicking the <strong>'+'</strong> and <strong>'-'</strong> icons allows zooming in or out on the map.</p>
<center><img src="../../../about/www/input/images/HMG1.png" width="70%" height="70%"</body></img></center>
<br></br>

<p class="opt">The following menu shows the available options. Each option is reviewed below.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMG2.png" width="40%" height="40%"</body></img></center>
<br></br>

<center><img src="../../../about/www/input/images/HMG3.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Area to Use:</strong> Select the map to display according to area of interest. In this example, 'Canada' is selected as the dataset includes values only for regions of Canada. A few options include the world or a continent divided by countries (such as 'Africa: By Country') which would display data by each country, while others allow for specific country divisions (such as 'Japan'). Also note that the average value for each region can be viewed on the map by hovering over the region of interest. Note the Region Information box in the image, with a value of 2968 for emissions in Quebec.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG4.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Range of Interest:</strong> Adjust the color assignment cutoff values, to group together or better differentiate certain value ranges. For exmaple, by choosing the range '90' to '880' on the bar, and clicking the <strong>Submit Range</strong> button, all values above 880 are grouped together. All regions on the map that exceed that emissions value are clearly displayed in the same dark pink color.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG5.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Column to Use:</strong> Select the column from the input file to display. In this example, there are three data sets, for the years '1990', '2000', and '2013'. To compare the data from 1990 with the data from 2013, the user may change the option to 'X2013..emissions.in.kilotonnes.'. By selecting the same range as above (90-880), it can be seen that emissions have substantially decreased for most regions.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG6.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Show/Hide Layers:</strong> Add or remove heatmapp layers to display or remove certain features of the map. Deleting the 'Contour Lines' tab, for example, will remove the region outlines on the map, as shown on the image. This option may be a useful visual aid for viewing an the overall map pattern (especially for smooth transitions).</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG7.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Heatmap Opcaity:</strong> Adjust the opacity of the heatmap on the map display. An opacity of 1 displays the heatmap with fully solid colors, to more fully distinguish the regions. A lower opacity, such as 0.4, would make the heatmap more transparent and the colors lighter as shown in the image. This may be useful in order to make underlying map features more visible.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG8.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Number of Shades:</strong> Adjust the number of colors to be used for the progression of values. A lower value such as 2 would group together more ranges under one color as shown in the image, while a larger value would further divide the ranges by color and better differentiate values on the map.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG9.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Color:</strong> The user may choose the <strong>Low Color</strong> and <strong>High Color</strong> according to preference to create the gradient for the value ranges displayed, by cliking on the colored box and choosing a color from the palette. For example, by choosing a light green for the 'Low Color' would result in this image. Regions with low, average, and high values are now more distinguishable as a whole when looking at the map.</p>
</center>
<br></br>


<p>There are two Download options that may be used to download the map/data at any step during the experience. The <strong>Download Plot</strong> option will download the heatmap view in html format. The <strong>Download Table</strong> option will download a text format of the data in table format, containing the values for the given latitude/longitute positions.</p>

<p class="opt">Further fine tuning may be performed with the <strong>Show Advanced Options</strong> tab. The two available options are described below.</p>
<br></br>

<center><img src="../../../about/www/input/images/HMArrow.png" width="40%" height="40%"</body></img>
<p></p>
</center>

<center><img src="../../../about/www/input/images/HMGAdvanced.png" width="40%" height="40%"</body></img>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG10.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Custom Legend Title:</strong> The user may give the legend a meaningful name. In this example, 'Emissions in Kilotonnes' is appropriate. Notice the legend box on the map.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG11.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Contour Line Width:</strong> Adjust the thickness of the region outlines on the map. A higher value would better distinguish the regions the data is devided by on the map. A value of 4, for example, would display borders as seen on the image. A lower value would make region borders less obvious.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG12.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may also view the data in table format, by clicking the <strong>Table</strong> plot tab next to the 'Interactive' tab. Values for all regions under each data set (by year in this exmaple) are clearly outlined.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG13.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may also search the data by entering a region name, or value in the <strong>Search box</strong> above the table. By entering the region 'Alberta', for example, the emission values for all three years are retrieved for the province of Alberta in Canada.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG14.png" width="70%" height="70%"</body></img>
<p class="desc_table">The table is also sortable, by regions or values. To sort the table by a column, click on the arrows next to the column header. For example, clicking twice on the 'X2013..' column arrow will display the table sorted by regions in decreasing order of emissions for the year 2013.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG15.png" width="70%" height="70%"</body></img>
<p class="desc_table">A list of the regions for the data may be viewed by clicking the <strong>Region Names</strong> tab next to the 'Table' plot tab.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMG16.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may also find out if a region is included, by using the <strong>Search box</strong> above the table. For example, entering 'Alberta' will retrieve that region name.</p>
</center>
<br></br>

<br></br><br></br>
</div>

</body>
</html>
""",

"image": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
		<style>
			td {padding:0.5em;}
			.opt {
				text-align: center;
			}		

			.desc {
				text-align: left;
				width: 50%;
			}

			.desc_table {
				text-align: left;
				width: 70%;
			}
		</style>
    </head>  
    <body>
		<div class = "well">
		
			<h4>Accepted File Formats</h4>
			
			<ul>
			<li>For the background image, Heatmapper accepts:
			<ul>
				<li>A JPEG image with extension <em>.jpg</em> or .<em>jpeg</em></li>
				<li>A PNG image with extension <em>.png</em></li>
				<li>A TIFF image with extension <em>.tif</em> or .<em>tiff</em></li>
			</ul>
			</li>
			
			<li>For the overlaid grid data, Heatmapper accepts:
			<ul>
				<li>Comma-Separated Value with extension <em>.csv</em></li>
				<li>Tab separated with extensions <em>.txt</em>, <em>.dat</em>, <em>.tsv</em>, or <em>.tab</em></li>
				<li>First sheet of an Excel workbook with extension <em>.xls</em> or <em>.xlsx</em></li>
			</ul>
			</li>
			</ul>
			
			<br />
			
			<h4>Data Structure</h4>
			There are two acceptable formats for the grid data, long-format or wide-format: 
			<br /><br />
			
			<em>Long-Format:</em>
			<br />
			
			<ul>
				<li>Specifies grid or "temperature" values by <i>x</i> and <i>y</i> coordinate. Each combination of <i>x</i> and <i>y</i> coordinates must be in the data set.</li>
				<li>Must contain header row with columns "x", "y", and "value".</li>
			</ul>
			
			<em>Wide-Format:</em>
			
			<ul>
				<li>Includes only grid or "temperature" values, with implied <i>x</i> and <i>y</i> coordinates. Values are given as a matrix that is mapped onto the image.</li>
				<li>Must have no header row.</li>
			</ul>
			
			<br />
			
			<h4>Acceptable data values</h4>
			
			<ul>
				<li><i>x</i> and <i>y</i>: positive numbers ranging from 1 to the number of grid columns/rows.</li>
				<li><i>value</i>: any positive number.</li>
				<li>Input data can have up to 200 x and 200 y coordinates.</li>
			</ul>
			
			<br />
			
			<h4>Examples</h4>
			
			<h5>Long-format</h5>
			
			Download an example in long-format <a href="../../../about/www/input/examples/image_example_long.txt" target="_blank">here</a>.
			<br /><br />
			
			Example layout:
			<br />
			
<code style="white-space: pre;">
value	x	y
7.0	1	1
7.0	1	2
17.8	1	3
17.8	2	1
19.5	2	2
15.7	2	3
5.0	3	1
13.5	3	2
5.2	3	3</code>

<br /><br />
or<br />

<code style="white-space: pre;">
x	y	value
1	1	7.0
1	2	7.0
1	3	17.8
2	1	17.8
2	2	19.5
2	3	15.7
3	1	5.0
3	2	13.5
3	3	5.2</code>

<h5>Wide-format</h5>

			Download an example in wide-format <a href="../../../about/www/input/examples/image_example_wide.txt" target="_blank">here</a>.
			<br /><br />

			Example layout:
			<br />

<code style="white-space: pre;">
11.6	3.6	12.9	8.7
0.9	15.9	0.6	1.4
8.7	19.8	2.9	10.3
12.0	10.0	16.9	15.3
</code>

		</div>

<div>
<h5>An example of image overlay functionality: X-ray CT scan of a rat treated with polyethylene glycol (PEG)-protected gold nanorods to allow visualization of tumors</h5>
<p>Data from <a href="http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2712876/">Maltzahn et al.</a> Example grid overlay: Temperature heat map example (artifical data, not taken from the paper).
</p>
<p>You may use the data files given above for this example.</p>
<br></br>
<p>Click on the <strong>Image Overlay</strong> tab on the main header and select the Upload File radio button for the <strong>Select Image File</strong> section, followed by the Choose File button (use the "long" example here). Alternatively, you may choose the 'Example File' radio button. Note: details about the example may be viewed by clicking the Information Icon.</p>
<p>Do the same for the <strong>Select Grid File</strong> section to view an overlay(use the "wide" example here). Alternatively, you may choose the 'Example File' radio button. The following image will display.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMI1.png" width="70%" height="70%"</body></img></center>
<br></br>

<p class="opt">The following menu shows the available options. Each option is reviewed below.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMI2.png" width="40%" height="40%"</body></img></center>
<br></br>

<center><img src="../../../about/www/input/images/HMI3.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Show/Hide Layers:</strong> Add or remove heatmap layers to display or remove certain features of the heatmap, such as contour lines, axis labels, or the heatmap itself. For example, by choosing to display only the <strong>Heatmap</strong>, <strong>Grid Lines</strong>, and <strong>Axis Labels</strong>, the plot changes to this image to display the grid and the distribution on a readable graph.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI4.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Display:</strong> Choose the distribution for the overlaying grid. The default is <strong>Gaussian</strong>, which smoothes the distribution, while the <strong>Square</strong> display does not (as shown in this image). For this example, the heatmap opacity has been changed to 30 (this option is explained below).</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI5.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Gaussian Radius Multiplier:</strong> Adjust the bandwidth for kernel density estimation. A higher value smoothes the graph further. For example, a value of 1.5 displays this distribution.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI6.png" width="50%" height="50%"</body></img>
<p class="desc">Almost no smoothing occurs with a Gaussian Radius Multiplier value of 0.5, and individual data points are distinctly observed (for this example heatmap opacity was increased to 0.2).</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI7.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Contour Smoothness:</strong> Adjust the number of grid points in each direction for kernel density estimation. A high value of 400 would extensively smooth the kernel outlines, as seen in the image (for this example the 'Contour Lines' layer was selected to be shown).</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI8.png" width="50%" height="50%"</body></img>
<p class="desc">For a Contour Smoothness value of 25, only a minimal set of 25 points are used for density estimation and kernel outlining, which the result seen on the image (for this example the 'Contour Lines' layer was selected to be shown).</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI9.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Heatmap Opacity:</strong> Adjust the opacity of the grid overlay. A higher value would more clearly display the heatmap distribution. For example, increasing the opacity to 0.15, results in this image (compared to the initially uploaded image). A maximum opacity will display the grid distribution in solid colors, without the underlying image.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI10.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Number of Shades:</strong> Adjust the number of colors used for the distribution. A lower value of 7, for example, would divide the distribution into fewer regions as seen in the image (for this example heatmapp opacity was set to 0.15). A higher value, however, would identify regions of transition in more detail.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI11.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Color Scheme:</strong> Change the color progression scheme. The two options besides 'Custom' are 'Rainbow' and 'Topo'. The 'Custom' view uses the 'Low Color' and 'High Color' settings to create a gradient for the distribution. The <strong>Rainbow</strong> scheme does not use a color gradient, but instead assigns rainbow colors to different intensities, as shown in the image. This may be useful to better differentiate the areas of the distribution.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI12.png" width="50%" height="50%"</body></img>
<p class="desc">Similarly, the <strong>Topo</strong> color scheme assigns a different color to each kernel, with lighter colors representing higher values.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI13.png" width="50%" height="50%"</body></img>
<p class="desc">For the <strong>Custom</strong> color scheme, the user may change the colors of the gradient. For example, by clicking on the <strong>Low Color</strong> colored box and choosing a light blue value from the palette, this distribution is observed.</p>
</center>
<br></br>

<p>There are two Download options that may be used to download the image/data at any step during the experience. The <strong>Plot</strong> option will download the image as seen on the webpage. The <strong>Table</strong> option will download a text format of the data in table format, containing the positions and values for overlayed grid.</p>

<p class="opt">Further fine tuning may be performed with the <strong>Show Advanced Options</strong> tab. The three available options are described below.</p>
<br></br>

<center><img src="../../../about/www/input/images/HMArrow.png" width="40%" height="40%"</body></img>
<p></p>
</center>

<center><img src="../../../about/www/input/images/HMIAdvanced.png" width="40%" height="40%"</body></img>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI14.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Stretch Image to Fit Grid:</strong> The image is stretched to fill the available grid space on the plot (for this example, the 'Axis Labels' layer was selected to be shown).</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI15.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Plot Width:</strong> The width of the plot/grid is increased with a higher value (such as 900), to stretch the distribution on the grid as shown in the image.</p>
<p class="desc"><strong>Plot Height:</strong> Increasing the plot height would have a similar effect in the vertical direction.</p>
</center>
<br></br>


<center><img src="../../../about/www/input/images/HMI16.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may also add a new point on the heatmap or change the value of an existing point using the <strong>Selected Point</strong> feature directly above the image. For exmaple, by entering the values for x=10, and y=20 and checking the <strong>Show</strong> option, the point is identified with a yellow square as shown in the image below. By changing the <strong>Value</strong> to 200, for example, the intensity of the point is changed along with the overall distribution, as shown below.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI17.png" width="50%" height="50%"</body></img>
<p class="desc">Changing the value of a point on the heatmap, as described above.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI18.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may also view the data in table format, by clicking the <strong>Table</strong> tab next to the 'Plot' tab. Values for all positions of the overlayed grid are displayed.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI19.png" width="70%" height="70%"</body></img>
<p class="desc_table">The table is sortable, by clicking on the arrows next to the table headers. For example, to view the table in order of decreasing value, click the <strong>Value</strong> arrow twice. The points with highest intensity are now displayed.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMI20.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may search the table by value and/or position by entering a value in the search text boxes, either the <strong>Search</strong> box at the top of the table, or the <strong>X</strong>, <strong>Y</strong>, or <strong>Value</strong> search boxes directly below the table columns. For example, entering '45' in the 'Value' text box, will retireve all the positions with a value of '45'.</p>
</center>

<br></br><br></br>
</div>

    </body>
</html>
""",

"introduction": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
    </head>  
    <body>
		<div class = "well">
			<h4>Heatmapper Overview</h4>
			
			Welcome to Heatmapper! -- a free online application for visualizing various types of data as heat maps. Heatmapper is the first tool of its kind that allows the user to display many different classes of heat maps in one easy-to-use web application. <br />
			<br />
			
			Heatmapper has five different classes of heatmap (click the links in the left column
			for detailed instructions):
			
			<ul>
				<li><b>Expression Heatmaps</b>: Displays unclustered (or previously clustered) data from transcriptomic (microarray or RNAseq), proteomic or metabolomic experiments.</li>
				<li><b>Pairwise Comparison Heatmaps</b>: Displays two sub-classes of heatmaps:</li>
					<ol>
						<li>Pairwise distance heatmaps (or matrices): Display all pairwise distances between the points in a data set.</li>
						<li>Pairwise correlation heatmaps: Display correlations between all pairs of variables in a data set.</li>
					</ol>
					Also allows data to be displayed "as-is" in a heatmap.
				<li><b>Image Overlay Heatmaps</b>: Display a heatmap over any image.</li>
				<li><b>Geomap Heatmaps</b>: Display a heatmap based on country, state, province etc. political boundaries.</li>
				<li><b>Geocoordinate Heatmaps</b>: Display data on geospatial coordinates (latitude and longitude).</li>
			</ul>
 			
			<em>Please select a heatmap type from the sidebar to view its specific file input instructions.</em>
		</div>
    </body>
</html>	
""",

"pairwise": """
<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
		<style>
			td {padding:0.5em;}
			code { white-space: pre; }

			.opt {
				text-align: center;
			}		

			.desc {
				text-align: left;
				width: 50%;
			}

			.desc_table {
				text-align: left;
				width: 70%;
			}

		</style>
    </head>  
    <body>
		<div class = "well">
			<h4>Accepted File Formats</h4>
			
			<ul>
				<li>Generic data table</li>
					<ul>
						<li>Comma-Separated Value with extension <em>.csv</em></li>
						<li>Tab separated with extensions <em>.txt</em>, <em>.dat</em>, <em>.tsv</em>, or <em>.tab</em></li>
						<li>First sheet of an Excel workbook with extension <em>.xls</em> or <em>.xlsx</em></li>
					</ul>
				<li>PDB file upload</li>
					<ul>
						<li>Protein Data Bank file, as used by the <a href="http://www.rcsb.org" target="_blank">RCSB Protein Data Bank</a>.
						The atom coordinates from the first chain are used.
						A distance matrix of the protein's coordinates can provide insight into the protein's structure.
						</li>
					</ul>
				<li>Multi-FASTA file upload</li>
					<ul>
						<li>Users can upload a set of DNA sequences in a single file in
						<a href="http://www.metagenomics.wiki/tools/fastq/multi-fasta-format" target="_blank">multi-FASTA format</a>.
						Heatmapper will compute k-mer frequencies for each sequence, which may be
						compared in a distance matrix for the purpose of alignment-free phylogenetic analysis.</li>
					</ul>
			</ul>
			
			<br />
			<h4>Data Structure</h4>
			
			<ul>
				<li>For distance matrix calculation: File should contain n data columns, where n &ge; 1, with each row representing a point in n-dimensional space.</li>
				<li>For correlation matrix calculation: File should contain n data columns, where n &gt; 1, with columns representing variables whose correlations to one another will be calculated.</li>
				<li>Note on labels: Optionally, the first row and/or first column may consist of data labels. If both contain data labels, a label of some sort (which will not be displayed) must also be present in the upper-left cell.
				If any non-numeric values are present in the first row or column, data labels are assumed to be present. If only numeric data labels are present, select the appropriate check box so that they are treated as labels.
				</li>
			</ul>
			
			<br />
			<h4>Acceptable Data Values</h4>
			
			<ul>
				<li>Any real numbers.</li>
				<li>For distance matrix calculation: Input data can have up to 300 rows and 500 columns.</li>
				<li>For correlation matrix calculation: Input data can have up to 500 rows and 300 columns.</li>
			</ul>
			
			<br />
			<h4>Examples</h4>

			<h5>For Distance Matrix</h5>

			The distance matrix option calculates all pairwise distances between spatial points
			(in rows) and presents the distances as a matrix.<br /><br />

			Download an example input file <a href="../../../about/www/input/examples/pairwise_dm_example1.txt" target="_blank">here</a>.
			<br /><br />

			Example 1:<br />

<code style="white-space: pre;">
27.340	24.430	2.614
26.266	25.413	2.842
26.913	26.639	3.531
27.886	26.463	4.263
25.112	24.880	3.649
</code>

			<br />
			Example 2:<br />

<code style="white-space: pre;">
placeholderLabel	x	y	z
point1	27.340	24.430	2.614
point2	26.266	25.413	2.842
point3	26.913	26.639	3.531
point4	27.886	26.463	4.263
point5	25.112	24.880	3.649
</code>

			<br />
			In this second example, we have included labels in both the header and first column, but
			labels in only the header or only the first column are also acceptable.

			<br /><br />
			<h5>For Correlation Matrix</h5>

			The correlation matrix option calculates all correlations between pairs of variables
			(in columns) and presents the correlation values as a matrix.<br /><br />

			Download an example input file <a href="../../../about/www/input/examples/pairwise_corr_example1.txt" target="_blank">here</a>.
			<br /><br />

			Example 1:<br />
			
<code style="white-space: pre;">
SAMPLE	depth (m)	pH	temp (C)	biomass (ug/kg)
sample0001	0.500	6.3	5.43	8.1
sample0002	1.000	6.4	4.29	7.5
sample0003	2.000	6.5	3.65	6.3
sample0004	5.000	6.9	3.19	5.6
sample0005	10.000	7.1	2.80	5.9
</code>

		</div>
<div>
<h5>An example of pairwise functionality: Dairy cows diet</h5>
<p>You may use the following data file for this example - Metabolite concentrations of 39 rumen samples measured by proton NMR from dairy cows fed with different proportions of barley grain (Ametaj BN, et al. (2010) "Metabolomics reveals unhealthy alterations in rumen metabolism with increased proportion of cereal grain in the diet of dairy cows", Metabolomics 6-4:583-594). Group label - 0, 15, 30, or 45 - indicating the percentage of grain in diet.</p>

<a href="../../../about/www/input/CowDiet.csv" download><p>CowDiet.csv</p>
</a>
<br></br>
<p>Click on the <strong>Pairwise</strong> tab on the main header and select the Upload File radio button, followed by the Choose File button. The following plot is created. Note that there are two <strong>Upload Format</strong> options, <strong>Generic Data Table</strong> and <strong>PDB Format</strong>. For this example, 'Generic Data Table' is set.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMP1.png" width="70%" height="70%"</body></img></center>
<br></br>

<p class="opt">The following menu shows the available options. Each option is reviewed below.</p>
<br></br>
<center><img src="../../../about/www/input/images/HMP2.png" width="40%" height="40%"</body></img></center>
<br></br>

<center>
<p class="desc"><strong>Labels in First Row</strong> and <strong>Labels in First Column:</strong> Treat entries of the first row or column in the data as headers. For this example, the file has only numeric values in the first row and Heatmapper thinks they are data values. To treat them as header values, the 'Lables in First Row' is selected.</p>
</center>
<br></br>


<center><img src="../../../about/www/input/images/HMP3.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Choose Matrix Type to Calculate:</strong> There are three matrix options that can be used. With the Distance Matrix (the default matrix used as seen for the first image on this page), each row is treated as a point, and Euclidean distances between points are calculated. With the Correlation Matrix, correlations between the variables in each data column are calculated. This plot is created with this option.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP4.png" width="50%" height="50%"</body></img>
<p class="desc">With the <strong>Display Data As-Is</strong> option, no matrix is applied and the values are directly mapped on the plot.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP12.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Set Aspect Ratio = 1:</strong> This option is set by default, with a ratio of 1. The aspect ratio describes the proportional relationship between the image height and width. By unchecking the option, the resulting plot has a less proportional width vs height layout. Compare with the plot above.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP5.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Show/Hide Layers:</strong> Add or remove heatmap layers to display or remove certain features of the plot, such as the Legend, or the Axis Labels. For example, removing the 'Axis Label' layer will only display the plot cells without the labels.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP6.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Number of Shades:</strong> Adjust the number of colors to be used for the plot. A lower value, such as '3', would categorize the data within larger ranges based on color. As shown in the image, a general distribution of the values is more readily visible. A higher value, on the other hand, would use more colors for smaller ranges of the dataset.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP7.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Color Scheme:</strong> Change the color progression scheme. The two options besides 'Custom' are 'Rainbow' and 'Topo'. The 'Custom' view uses the 'Low Color' and 'High Color' settings to create a gradient for value ranges. The <strong>Rainbow</strong> scheme does not use a color gradient, but instead assigns rainbow colors to different value ranges, as shown in the image.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP8.png" width="50%" height="50%"</body></img>
<p class="desc">Similarly, the <strong>Topo</strong> color scheme assigns a different color to each value range, with lighter colors representing higher values.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP9.png" width="50%" height="50%"</body></img>
<p class="desc">For the <strong>Custom</strong> color scheme, the user may change the colors of the gradient. For example, by clicking on the <strong>Low Color</strong> colored box and choosing a yellow value from the palette, as well as a purple <strong>High Color</strong>, the gradient is changed as shown on the plot and the contrast is improved.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP10.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Reverse Data Order:</strong> Change the order of the x and y axes values. The plot is reversed, as shown in the image (compare with the first image on this page).</p>
</center>
<br></br>

<p>There are two Download options that may be used to download the map/data at any step during the experience. The <strong>Plot</strong> option will download the plot image as seen on the webpage. The <strong>Table</strong> option will download the raw data in table format, with values for each row/column pair.</p>



<p class="opt">Further fine tuning may be performed with the <strong>Show Advanced Options</strong> tab. The five available options are described below.</p>
<br></br>

<center><img src="../../../about/www/input/images/HMArrow.png" width="40%" height="40%"</body></img>
<p></p>
</center>

<center><img src="../../../about/www/input/images/HMPAdvanced.png" width="40%" height="40%"</body></img>
</center>
<br></br>

<center>
<p class="desc"><strong>Plot Width:</strong> Adjust the size of the plot in the horizontal direction. A larger plot has better resolution.</p>
<p class="desc"><strong>Plot Height:</strong> Adjust the size of the plot in the vertical direction.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP11.png" width="50%" height="50%"</body></img>
<p class="desc"><strong>Title:</strong> Name the plot.</p>
<p class="desc"><strong>X Axis Label:</strong> Name the x-axis.</p>
<p class="desc"><strong>Y Axis Label:</strong> Name the y-axis.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP13.png" width="70%" height="70%"</body></img>
<p class="desc_table">To view a section of the plot in more detail click on the <strong>Interactive</strong> tab next to the 'Plot' tab. Click and drag a portion of the plot to zoom in (by clicking once more anywhere on the plot, it will zoom back out). Hovering over the plot will display specific cell information, as shown in the image.</p>
</center>
<br></br>


<center><img src="../../../about/www/input/images/HMP14.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may also view the data in table format, by clicking the <strong>Table</strong> plot tab next to the 'Interactive' tab.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP15.png" width="70%" height="70%"</body></img>
<p class="desc_table">The user may search the Table values, using the <strong>Search</strong> box at the top of the table, or the column specific search boxes directly below the table. For example, by entering a correlation coefficient value of '4656' in the main search box, all rows and columns that contain that value are retrieved.</p>
</center>
<br></br>

<center><img src="../../../about/www/input/images/HMP16.png" width="70%" height="70%"</body></img>
<p class="desc_table">The Table can be sorted by any one of the columns, using the arrows next to each header. For example, by cliking twice on the '0_1_1' arrow, the table is sorted in decreasing order of values for the '0_1_1' sample column.</p>
</center>

<br></br><br></br>
</div>
    </body>
</html>
"""
}