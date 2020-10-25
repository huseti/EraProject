# ------- Program: ERA Framework Dashboard ---------
# ------- Developed by: Tim Huse  ------------------
# ------- Date: 12.08.2020 -------------------------
# -*----- coding: utf-8 --------------------------*-


# Run this app with `python EraDashboard_Main.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# TODO: Upload Dialog for JSON File

# Imports
import dash
import dash_bootstrap_components as dbc
import ERA_Framework_Dashboard.View_ERA as view_era
import ERA_Framework_Dashboard.Controller_ERA as controller_era


# Main method to create the Dash application
def main():
    # TODO: Remove this
    #Tk().withdraw()
    #era_json_path: str = askopenfilename(
    #    title="Please select an JSON File that contains your ERA model",
    #    filetypes=[("JSON files", "*.json")])
    era_json_path = r'C:/Users/thuse/Google Drive/Dokumente/Beruf/FU/4. Semester/Quellen/EAM Datensatz/Bearbeitet/ERA_Model_2020_10_24.json'

    # Create the Dash app object
    # Implement Dash Bootstrap (local CSS files are integrated as well from /assets-folder)
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])
    app.title = 'ERA Framework'

    # Create the app layout
    app.layout = view_era.create_main_layout(title="EAM Risk Assessment Framework", era_model_path=era_json_path)
    # Connect the callbacks of controller Class
    controller_era.register_callbacks(app)

    # Start the local server
    app.run_server(debug=True)


# Start the Dash application on local server
if __name__ == '__main__':
    main()
