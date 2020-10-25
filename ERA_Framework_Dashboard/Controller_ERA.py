# ------- Module: Controller ERA  ------------------
# ------- Controller of ERA framework --------------
# ------- Contains all callbacks of Dash app -------
# -*----- coding: utf-8 --------------------------*-

# imports
from dash.dependencies import Output, Input
import json


# Connecting all callbacks to the Dash application
def register_callbacks(app):
    pass
    # Callback for Clicking on Node
    # TODO: implement
    #@app.callback(Output('cytoscape-tapNodeData-json', 'children'),
    #             [Input('cytoscape-era-model', 'tapNodeData')])
    #def displayTapNodeData(data):
    #    if data:
    #        return json.dumps(data, indent=2)

    # Callback for Hovering over Node
    # TODO: implement
    #@app.callback(Output('cytoscape-tapNodeData-json', 'children'),
    #             [Input('cytoscape-era-model', 'mouseoverNodeData')])
    #def displayTapNodeData(data):
    #    if data:
    #       return "ERA Score: " + str(data['era_score']) + "/nLabel: " + data['label'] + "/n"

    # Callback for Clicking on Edge
    # TODO: implement
    #@app.callback(Output('cytoscape-tapEdgeData-json', 'children'),
    #              [Input('cytoscape-era-model', 'tapEdgeData')])
    #def displayTapEdgeData(data):
    #    return json.dumps(data, indent=2)

    # Callback for Hovering over Edge
    # TODO: implement

