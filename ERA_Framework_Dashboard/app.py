# ------- Program: ERA Framework Dashboard ---------
# ------- Developed by: Tim Huse  ------------------
# ------- Date: 12.08.2020 -------------------------
# -*----- coding: utf-8 --------------------------*-


# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

# TODO: Upload Dialog for JSON File
# TODO: Preparing JSON Data File for Cytoscape

# Imports
import dash
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import dash_bootstrap_components as dbc
import json

# TODO: Delete
from tkinter import Tk
from tkinter.filedialog import askopenfilename,asksaveasfilename

# Constants
TITLE = 'EAM Risk Assessment Framework'


# Main method to create the Dash application
def main():
    # TODO: Remove this
    #Tk().withdraw()
    #era_model_json: str = askopenfilename(
    #    title="Please select an JSON File that contains your ERA model",
    #    filetypes=[("JSON files", "*.json")])
    era_model_json = 0

    # Create the Dash app object
    # Implement Dash Bootstrap (local CSS files are integrated as well from /assets-folder)
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

    # Create the app layout
    app.layout = create_main_layout(title=TITLE, era_model=era_model_json)

    # Start the local server
    app.run_server(debug=True)


# Load main Layout of Dash App
def create_main_layout(title: str, era_model: json) -> html.Div:
    layout = html.Div(children=[
        dbc.Jumbotron(
            [
                html.H1(title, className="display-3"),
                html.P(
                    "An interactive Dashboard Application to display your ERA framework",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    "EAM risk assessment (ERA) is a framework developed by Dr. Daniel Fuerstenau, Dr. Carson Woo"
                    " and Tim Huse"
                ),
                html.P(dbc.Button("Learn more", color="primary"), className="lead"),
            ]
        ),

        # TODO: add DCC Upload Component

        # Generate Cytoscape Graph
        implement_cyto_graph(era_model)
    ])
    return layout


# Load Cytoscape Graph for Dashboard
def implement_cyto_graph(era_model: json) -> cyto.Cytoscape:
    # Load defined stylesheet and transformed era model (to cytoscape graph)
    graph = cyto.Cytoscape(
                id='cytoscape-era-model',
                stylesheet=get_stylesheet_cyto(),
                style={'width': '100%', 'height': '800px'},
                layout={
                    'name': 'breadthfirst',
                    'roots': '[class = "Process"]'
                },
                elements=transform_json_to_cyto(era_model)
            )
    return graph


# Transform ERA JSON model to cytoscape graph format
def transform_json_to_cyto(era_model: json) -> list:
    nodes = [
        {'data': {'id': '10001', 'class': 'Process', 'label': 'Beteiligungen managen', 'era_score': 9,
                  'count_affecting_vulnerabilities': 53}},
        {'data': {'id': '20001', 'class': 'Process', 'label': 'Medialer Vertrieb managen', 'era_score': 10,
                  'count_affecting_vulnerabilities': 65}},
        {'data': {'id': '10076', 'class': 'Application', 'label': 'AMI Beteiligungsmanagement', 'era_score': 4.2,
                  'count_affecting_vulnerabilities': 25}},
        {'data': {'id': '11184', 'class': 'Application', 'label': 'ArciSoft Aktenverwaltung', 'era_score': 6.3,
                  'count_affecting_vulnerabilities': 25}},
        {'data': {'id': '9200114', 'class': 'Application', 'label': 'Internet-Filiale Module', 'era_score': 6.9,
                  'count_affecting_vulnerabilities': 40}},
        {'data': {'id': '9200254', 'class': 'Application', 'label': 'Solvemate', 'era_score': 9.3,
                  'count_affecting_vulnerabilities': 14}},
        {'data': {'id': '713000', 'class': 'Technology', 'label': 'Microsoft Windows 2000', 'era_score': 2.3,
                  'count_affecting_vulnerabilities': 26}},
        {'data': {'id': '582000', 'class': 'Technology', 'label': 'Oracle Solaris', 'era_score': 1.3,
                  'count_affecting_vulnerabilities': 45}},
        {'data': {'id': 'CVE-2020-15658', 'class': 'Vulnerability', 'label': 'CVE-2020-15658', 'era_score': 0,
                  'vulnerability_access_vector': 'NETWORK'}},
        {'data': {'id': 'CVE-2020-15659', 'class': 'Vulnerability', 'label': 'CVE-2020-15659', 'era_score': 10,
                  'vulnerability_access_vector': 'NETWORK'}},
        {'data': {'id': 'CVE-2020-15670', 'class': 'Vulnerability', 'label': 'CVE-2020-15670', 'era_score': 6,
                  'vulnerability_access_vector': 'NETWORK'}},
        {'data': {'id': 'CVE-2020-15688', 'class': 'Vulnerability', 'label': 'CVE-2020-15688', 'era_score': 3,
                  'vulnerability_access_vector': 'NETWORK'}}
    ]

    edges = [
        {'data': {'source': '10001', 'target': '10076', 'label': 'Process 10001 to Application 10076',
                  'impact score': 0.5, 'rater': 'Test'}},
        {'data': {'source': '10001', 'target': '11184', 'label': 'Process 10001 to Application 11184',
                  'impact score': 0.2, 'rater': 'Test'}},
        {'data': {'source': '20001', 'target': '9200114', 'label': 'Process 20001 to Application 9200114',
                  'impact score': 0.8, 'rater': 'Test'}},
        {'data': {'source': '20001', 'target': '9200254', 'label': 'Process 20001 to Application 9200254',
                  'impact score': 0.7, 'rater': 'Test'}},
        {'data': {'source': '10076', 'target': '713000', 'label': 'Application 10076 to Technology 713000',
                  'impact score': 0.3, 'rater': 'Test'}},
        {'data': {'source': '11184', 'target': '713000', 'label': 'Application 20001 to Technology 713000',
                  'impact score': 0.3, 'rater': 'Test'}},
        {'data': {'source': '9200114', 'target': '582000', 'label': 'Application 9200254 to Technology 582000',
                  'impact score': 0.85, 'rater': 'Test'}},
        {'data': {'source': '9200254', 'target': '582000', 'label': 'Application 9200254 to Technology 582000',
                  'impact score': 0.7, 'rater': 'Test'}},
        {'data': {'source': '582000', 'target': 'CVE-2020-15658',
                  'label': 'Technology 582000 to Vulnerability CVE-2020-15658',
                  'impact score': 0.1, 'rater': 'Test'}},
        {'data': {'source': '582000', 'target': 'CVE-2020-15659',
                  'label': 'Technology 582000 to Vulnerability CVE-2020-15659',
                  'impact score': 0.25, 'rater': 'Test'}},
        {'data': {'source': '713000', 'target': 'CVE-2020-15688',
                  'label': 'Technology 713000 to Vulnerability CVE-2020-15688',
                  'impact score': 0.75, 'rater': 'Test'}},
        {'data': {'source': '713000', 'target': 'CVE-2020-15670',
                  'label': 'Technology 713000 to Vulnerability CVE-2020-15670',
                  'impact score': 0.9, 'rater': 'Test'}},
        {'data': {'source': '9200114', 'target': '11184',
                  'label': 'Application 9200114 to Application 11184',
                  'impact score': 0.6, 'rater': 'Test'}}
    ]

    graph = nodes + edges
    return graph


def get_stylesheet_cyto() -> list:
    stylesheet = [
        # Group selectors
        # Define the node and edge styles
        {
            'selector': 'node',
            'style': {
                'label': 'data(label)'
            }
        },
        {
            'selector': 'edge',
            'style': {
                'curve-style': 'bezier',
                'line-color': 'grey',
                'target-arrow-color': 'grey',
                'target-arrow-shape': 'triangle',
                'label': 'data(impact_score)'
            }
        },


        # Class selectors
        # Design the shapes for each asset type
        {
            'selector': '[class ^= "Process"]',
            'style': {
                'shape': 'rectangle'
            }
        },
        {
            'selector': '[class ^= "Application"]',
            'style': {
                'shape': 'triangle'
            }
        },
        {
            'selector': '[class ^= "Technology"]',
            'style': {
                'shape': 'circle'
            }
        },
        {
            'selector': '[class ^= "Vulnerability"]',
            'style': {
                'shape': 'vee'
            }
        },
        # Design the color of assets according to era score
        {
            'selector': '[era_score < 7.0]',
            'style': {
                'background-color': 'yellow'
            }
        },
        {
            'selector': '[era_score < 4.0]',
            'style': {
                'background-color': 'green'
            }
        },
        {
            'selector': '[era_score >= 7.0]',
            'style': {
                'background-color': 'red'
            }
        }
    ]
    return stylesheet


# Start the Dash application on local server
if __name__ == '__main__':
    main()
