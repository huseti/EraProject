# ------- Program: ERA Framework Dashboard ---------
# ------- Developed by: Tim Huse  ------------------
# ------- Date: 12.08.2020 -------------------------
# -*----- coding: utf-8 --------------------------*-


# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.


# Imports
import dash
import dash_bootstrap_components as dbc
import ERA_Framework_Dashboard.ViewERA as viewEra
import ERA_Framework_Dashboard.ControllerERA as controllerEra
import ERA_Framework_Dashboard.ModelERA as modelERA

# Create the Dash app object
# integrate Bootstrap Stylesheet local / CSS files are integrated as well from /assets-folder
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
app.title = 'ERA Framework'

# Create the Model Object
model = modelERA.ModelERA()

# Create the View Object and generate the Main Layout
view = viewEra.ViewEra(title="EAM Risk Assessment Framework", era_model=model, dash_app=app)
app.layout = view.create_main_layout()

# Connect the Controller and register the callbacks for View
controller = controllerEra.ControllerERA(dash_app=app, era_model=model, era_view=view)
controller.register_callbacks()


# Start the Dash application on local server
if __name__ == '__main__':
    # Run the local server
    app.run_server(debug=True)
