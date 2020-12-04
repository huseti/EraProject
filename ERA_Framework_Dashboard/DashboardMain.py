# ------- Program: ERA Framework Dashboard ---------
# ------- Developed by: Tim Huse  ------------------
# ------- Date: 12.08.2020 -------------------------
# -*----- coding: utf-8 --------------------------*-


# Run this app with `python DashboardMain.py` and
# visit http://127.0.0.1:8050/ in your web browser.


# Imports
import dash
import dash_bootstrap_components as dbc
import ERA_Framework_Dashboard.ViewERA as viewEra
import ERA_Framework_Dashboard.ControllerERA as controllerEra
import ERA_Framework_Dashboard.ModelERA as modelERA


class DashboardMain:

    # Constructor
    def __init__(self):

        # Create the Dash app object
        # integrate Bootstrap Stylesheet local / CSS files are integrated as well from /assets-folder
        self.app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
        self.app.title = 'ERA Framework'

        # Create the Model Object
        self.model = modelERA.ModelERA()

        # Create the View Object and generate the Main Layout
        self.view = viewEra.ViewEra(title="EAM Risk Assessment Framework", era_model=self.model, dash_app=self.app)
        self.app.layout = self.view.create_main_layout()

        # Connect the Controller and register the callbacks for View
        self.controller = controllerEra.ControllerERA(dash_app=self.app, era_model=self.model, era_view=self.view)
        self.controller.register_callbacks()

    # Main method to start the Plotly Dash Server
    def main(self):
        # Run the local server
        self.app.run_server(debug=True)


if __name__ == '__main__':
    DashboardMain().main()
