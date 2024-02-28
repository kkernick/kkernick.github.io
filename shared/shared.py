from shiny import App, Inputs, Outputs, Session, reactive, render, ui

Table = ui.nav_panel("Table",
					ui.layout_columns(
						ui.input_numeric("TableRow", "Row", 0),
						ui.input_numeric("TableCol", "Column", 0),
						ui.input_text("TableVal", "Value", 0),
						ui.input_select(id="Type", label="Datatype", choices=["Integer", "Float", "String"]),
						col_widths=[2,2,6,2],
					),
					ui.layout_columns(
						ui.input_action_button("Update", "Update"),
						ui.input_action_button("Reset", "Reset Values"),
					),
					ui.output_data_frame("LoadedTable"),
				)