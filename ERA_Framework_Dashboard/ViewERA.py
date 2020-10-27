# ------- Class: View ERA  ------------------------
# ------- Layouts of ERA framework -----------------
# ------- Generating the layouts of ERA framework --
# -*----- coding: utf-8 --------------------------*-

# imports
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import dash_bootstrap_components as dbc
import ERA_Framework_Dashboard.assets.Stylesheets as styleERA
import ERA_Framework_Dashboard.ModelERA as modelERA
import pandas as pd


class ViewEra:

    # Constructor
    def __init__(self, title: str, era_model: modelERA):
        self.title = title
        self.era_model = era_model

    # Load main Layout of Dash App
    def create_main_layout(self) -> html.Div:
        layout = html.Div(children=[
            # Jumbotron Title and Information
            self.__create_jumbotron(),

            # Modal Element
            dbc.Modal(
                [
                    dbc.ModalHeader("EAM Risk Assessment Framework (ERA)"),
                    dbc.ModalBody("The ERA framework is an assessment framework that provides a comprehensive view of "
                                  "existing IT security risks across the entire enterprise architecture of companies on"
                                  " a technological level applying EAM. The framework is intended to identify and asses"
                                  "s the technological threats according to the protection goals of the company."
                                  "For further information contact Mr. Tim Huse via tim.huse@fu-berlin.de"),
                    dbc.ModalFooter(
                        dbc.Button("Close", id="close", color='danger', className="ml-auto")
                    ),
                ],
                id="modal-info",
                size="xl",
            ),

            # Upload Component
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop your ERA File in JSON Format or ',
                    html.A('Select JSON File', id='Upload_Link')
                ]),
                style=styleERA.get_style_upload(),
                # Forbid multiple files to be uploaded
                multiple=False
            ),

            # Layout 3 Columns
            html.Div(
                [
                    dbc.Row(
                        [  # Generate Left Column of Layout with legend and form
                            dbc.Col(self.__create_left_column(), width=3),

                            # Generate Cytoscape Graph
                            dbc.Col(self.__create_cyto_graph()),

                            # Generate Right Column of Layout with details and info bar
                            dbc.Col(self.__create_right_column(), width=3),
                        ]
                    ),
                ]
            ),
        ])
        return layout

    # Load Cytoscape Graph for Dashboard
    def __create_cyto_graph(self):
        graph = html.Div(
            [
                cyto.Cytoscape(
                    id='cytoscape-era-model',
                    stylesheet=styleERA.get_stylesheet_cyto(),
                    zoomingEnabled=True,
                    minZoom=0.5,
                    style={'width': '100%', 'height': '700px'},
                    layout={
                        'name': 'breadthfirst',
                        'roots': '[class = "Process"]'
                    },
                    elements=[]
                ),

            ],
            id='graph-div')
        return graph


    # Load Left column of layout with legend and form
    def __create_right_column(self):
        layout = html.Div(children=[
            self.__create_detail_info_node(),
            self.__create_detail_info_edge(),
            self.__create_info_bar()
        ])
        return layout

    # Load detail information on the right side (of
    def __create_detail_info_node(self):
        layout = html.Div([
            html.H6('Details Node'),
            html.Hr(className="my-2"),
            html.Div(id='table-tapNodeData-json')
        ],
            style={'width': '100%', 'height': '300px', 'paddingBottom': '5%', 'paddingTop': '7%',
                   'paddingRight': '5%', 'paddingLeft': '10%', 'margin-bottom': '30px', 'overflow-y': 'scroll'})
        return layout

    # Load detail information on the right side (of
    def __create_detail_info_edge(self):
        layout = html.Div([
            html.H6('Details Edge'),
            html.Hr(className="my-2"),
            html.Div(id='table-tapEdgeData-json')
        ],
            style={'width': '100%', 'height': '250px', 'paddingBottom': '5%', 'paddingTop': '7%',
                   'paddingRight': '5%', 'paddingLeft': '10%', 'overflow-y': 'scroll'})
        return layout

    # Load info bar on the right side (of
    def __create_info_bar(self):
        layout = html.Div([
            html.H6('Info Bar'),
            html.Hr(className="my-2"),
            dbc.ListGroup(
                [
                    dbc.ListGroupItem(str(self.era_model.total_vulnerabilities) + "\nVulnerabil."),
                    dbc.ListGroupItem('{0:.3g}'.format(self.era_model.average_era_score_assets) + "\nAvg. Score"),
                    dbc.ListGroupItem(str(self.era_model.amount_nodes) + "\nAssets"),
                ],
                horizontal=True,
                className="mb-2",
                id='table-info-bar',
            ),
            html.Div(id='filepath')
        ],
            style={'width': '100%', 'height': '150px', 'paddingBottom': '5%', 'paddingTop': '7%',
                   'paddingRight': '5%', 'paddingLeft': '10%'})
        return layout

    # Load Left column of layout with legend and form
    def __create_left_column(self):
        layout = html.Div(children=[
            self.__create_form(),
            self.__create_legend()
        ])
        return layout

    # Load form
    def __create_form(self):
        search_input = dbc.FormGroup(
            [
                dbc.Label("Asset Search", html_for="search-element", style={'margin-top': '20px'}),
                dbc.Input(type="search", id="search-element", placeholder="Enter asset name ..."),
            ],
            className="mr-3",
        )

        score_range_slider = dbc.FormGroup(
            [
                dbc.Label("ERA Score Range", html_for="score-range-slider", style={'margin-top': '20px'}),
                dcc.RangeSlider(
                    id="score-range-slider",
                    marks={
                        0: {'label': '0', 'style': {'color': '#77b0b1'}},
                        1: {'label': '1', 'style': {'color': '#77b0b1'}},
                        2: {'label': '2', 'style': {'color': '#77b0b1'}},
                        3: {'label': '3', 'style': {'color': '#77b0b1'}},
                        4: {'label': '4', 'style': {'color': 'orange'}},
                        5: {'label': '5', 'style': {'color': 'orange'}},
                        6: {'label': '6', 'style': {'color': 'orange'}},
                        7: {'label': '7', 'style': {'color': '#f50'}},
                        8: {'label': '8', 'style': {'color': '#f50'}},
                        9: {'label': '9', 'style': {'color': '#f50'}},
                        10: {'label': '10', 'style': {'color': '#f50'}}
                    },
                    min=0,
                    max=10,
                    value=[0, 10],
                    allowCross=False
                ),
                dbc.FormText(
                    "Only show assets with the selected ERA score range",
                    color="secondary",
                ),
            ]
        )

        class_range_slider = dbc.FormGroup(
            [
                dbc.Label("Class Range", html_for="class-range-slider", style={'margin-top': '20px'}),
                dcc.RangeSlider(id="class-range-slider", min=0, max=3, value=[0, 3], allowCross=False, marks={
                    0: {'label': 'Proc.'},
                    1: {'label': 'App.'},
                    2: {'label': 'Tech.'},
                    3: {'label': 'Vul.'}
                }, ),
                dbc.FormText(
                    "Only show assets with the selected asset class",
                    color="secondary",
                ),
            ]
        )
        buttons = html.Div([
            dbc.Button("Submit", id="submit_button", color="primary", size="sm",
                       style={'margin-top': '10px', 'margin-right': '60px'}),
            html.A(dbc.Button("Reset all", id="reset_button", color="danger", size="sm",
                       style={'margin-top': '10px'}), href='/'),


        ])

        form = dbc.Form([score_range_slider, class_range_slider, search_input, buttons])

        layout = html.Div([
            html.H6('Options'),
            html.Hr(className="my-2"),
            form
        ],
            style={'width': '100%', 'height': '250px', 'paddingBottom': '5%', 'paddingTop': '7%',
                   'paddingRight': '5%', 'paddingLeft': '10%', 'overflow-y': 'scroll'})
        return layout

    # Load legend
    def __create_legend(self):
        df = pd.DataFrame(
            {
                "Element": ["X -> Y", "Green asset", "Orange asset", "Red asset", "Rectangle", "Triangle", "Circle",
                            "Vee"],
                "Description": ["X is dependent on Y", "ERA Score 0.0 - 3.9", "ERA Score 4.0 - 6.9",
                                "ERA Score 7.0 - 10.0",
                                "Process", "Application", "Technology", "Vulnerability"
                                ],
            }
        )

        layout = html.Div([
            html.H6('Legend'),
            html.Hr(className="my-2"),
            dbc.Table.from_dataframe(df, id='table_legend', striped=True, bordered=True, hover=True, size='sm',
                                     style={'margin-top': '20px', 'margin-right': '10px'})
        ],
            style={'width': '100%', 'height': '250px', 'paddingBottom': '5%', 'marginTop': '15%', 'paddingTop': '7%',
                   'paddingRight': '1%', 'paddingLeft': '10%'})
        return layout

    # Load Jumbotron Title and Information
    def __create_jumbotron(self):
        layout = dbc.Jumbotron(
            [
                html.H1(self.title, className="display-3"),
                html.P(
                    "An interactive Dashboard Application to display your ERA framework",
                    className="lead",
                ),
                html.Hr(className="my-2"),
                html.P(
                    "EAM risk assessment (ERA) is a framework developed by Dr. Daniel Fuerstenau, Dr. Carson Woo"
                    " and Tim Huse"
                ),
                html.P(dbc.Button("Learn more", color="primary", id="open"), className="lead"),
            ]
        )
        return layout
