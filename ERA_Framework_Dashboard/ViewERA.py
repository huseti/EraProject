# ------- Class: View ERA  ------------------------
# ------- Layouts of ERA framework -----------------
# ------- Generating the layouts of ERA framework --
# -*----- coding: utf-8 --------------------------*-

# imports
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import ERA_Framework_Dashboard.assets.Stylesheets as styleERA
import ERA_Framework_Dashboard.ModelERA as modelERA


class ViewEra:

    # Constructor
    def __init__(self, title: str, era_model: modelERA, dash_app: dash.Dash):
        self.title = title
        self.era_model = era_model
        self.app = dash_app

    # Load main Layout of Dash App
    def create_main_layout(self) -> html.Div:

        layout = html.Div(children=[
            # Header Layout
            html.Div([
                # Jumbotron Title and Information
                self.__create_jumbotron()
            ]),

            # Modal for "Learn more"-button
            self.__create_modal_further_information(),

            # Layout 3 Columns
            html.Div(
                [
                    dbc.Row(
                        [  # Generate Left Column of Layout with legend and form
                            dbc.Col(self.__create_left_column(), width=3),

                            # Generate Central Column with Upload Component and Cytoscape Graph
                            dbc.Col(self.__create_central_column()),

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
                # Div to upload the graph via callback
                cyto.Cytoscape(
                    id='cytoscape-era-model',
                    stylesheet=styleERA.get_stylesheet_cyto(),
                    style={'width': '1px%', 'height': '1px'},
                    elements=[]
                )

            ],
            id='graph-div', style={'border': '1px solid rgba(0, 0, 0, 0.08)'}
        )
        return graph

    # Load Left column of layout with legend and form
    def __create_central_column(self):
        layout = html.Div(children=[
            self.__create_upload_component(),
            self.__create_cyto_graph(),
        ])
        return layout

    # Load Left column of layout with legend and form
    def __create_right_column(self):
        layout = html.Div(children=[
            self.__create_search_bar(),
            self.__create_form(),
            self.__create_info_bar()
        ])
        return layout

    # Load detail information of node
    def __create_detail_info_node(self):
        layout = html.Div([
            html.H6(['Details Node',
                    html.Span("?",
                              id="tooltip-tg-node", className="text-info")
                     ]),
            dbc.Tooltip(
                "This window displays further information about a selected asset. Tap on a node within the ERA model "
                "graph to select it.",
                target="tooltip-tg-node",
            ),
            html.Hr(className="my-2"),
            html.Div(id='table-tapNodeData-json', style={'overflow-y': 'scroll', 'height': '400px',
                                                         'padding': '5%'})
        ],
            className="blocks_areas",
            style={'width': '100%', 'paddingRight': '5%', 'paddingLeft': '10%', 'paddingTop': '5%',
                   'paddingBottom': '20px', 'margin-bottom': '20px'})
        return layout

    # Load detail information of edge
    def __create_detail_info_edge(self):
        layout = html.Div([
            html.H6(['Details Edge',
                    html.Span("?",
                              id="tooltip-tg-edge", className="text-info")
                     ]),
            dbc.Tooltip(
                "This window displays further information about a selected connection between two assets. Tap on a edge"
                " within the ERA model graph to select it.",
                target="tooltip-tg-edge",
            ),
            html.Hr(className="my-2"),
            html.Div(id='table-tapEdgeData-json', style={'overflow-y': 'scroll', 'height': '300px',
                                                         'padding': '5%'})
        ],
            className="blocks_areas",
            style={'width': '100%', 'paddingTop': '5%', 'paddingBottom': '20px',
                   'paddingRight': '5%', 'paddingLeft': '10%', 'margin-bottom': '20px'})
        return layout

    # Load info bar on the right side (of
    def __create_info_bar(self):
        layout = html.Div([
            html.H6(['Info Bar',
                    html.Span("?",
                              id="tooltip-tg-info", className="text-info")
                     ]),
            dbc.Tooltip(
                "This info bar displays further information about the ERA model. The first card displays the average "
                "ERA score of all assets (excl. Vulnerabilities). The second card shows all detected vulnerabilities. "
                "The third card displays the total amount of assets (excl. Vulnerabilities)."
                "Additionally, the filename of the currently displayed ERA model is shown.",
                target="tooltip-tg-info",
            ),
            html.Hr(className="my-2"),
            html.Div([],
                     id='table-info-bar',
                     )
        ],
            className="blocks_areas",
            style={'width': '100%', 'height': '320px', 'paddingBottom': '5%', 'paddingTop': '5%',
                   'paddingRight': '5%', 'margin-top': '20px', 'paddingLeft': '10%', 'margin-bottom': '20px'})
        return layout

    # Load Left column of layout with detail info of nodes
    def __create_left_column(self):
        layout = html.Div(children=[
            self.__create_detail_info_node(),
            self.__create_detail_info_edge(),
        ])
        return layout

    # Load Left column of layout with detail info of nodes
    def __create_upload_component(self):
        layout = html.Div(children=[
            dcc.Upload(
                id='upload-data',
                children=html.Div([
                    'Drag and Drop your ERA File in JSON Format here or ',
                    html.A('click here', id='Upload_Link')
                ]),
                style=styleERA.get_style_upload(),
                # Forbid multiple files to be uploaded
                multiple=False
            )
        ])
        return layout

    # Create Search Bar
    def __create_search_bar(self):

        search_input = dbc.FormGroup(
            [
                dbc.Input(type="search", id="search-element", placeholder="Enter asset name or id ...",
                          style={'margin-top': '10px', 'width': '230px', 'float': 'left'}),
            ],
            className="mr-3",
        )

        button = dbc.Button("Submit", id="search_button", color="primary", size="sm", disabled=True,
                            style={'margin-top': '18px', 'margin-left': '30px'})

        form = dbc.Form([search_input, button])

        layout = html.Div([
            html.H6(['Search',
                    html.Span("?",
                              id="tooltip-tg-search", className="text-info")
                     ]),
            dbc.Tooltip(
                "Search for an asset by entering its ID or name. All assets are shown in lightblue border that contain "
                "the entered search term. Additionally, all connected assets are displayed in a slightly darker color. "
                "The search can not be combined with the filter settings below!",
                target="tooltip-tg-search",
            ),
            html.Hr(className="my-2"),
            form
        ],
            className="blocks_areas",
            style={'width': '100%', 'height': '140px', 'paddingBottom': '5%', 'paddingTop': '5%',
                   'paddingRight': '5%', 'paddingLeft': '10%'})

        return layout

    # Load form
    def __create_form(self):
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
                dbc.Label("Asset Class Range", html_for="class-range-slider", style={'margin-top': '20px'}),
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
        apply_button = dbc.Button("Apply Filter", id="filter_button", color="primary", size="sm", disabled=True,
                                  style={'margin-top': '20px', 'margin-right': '20px', 'float': 'left'})
        button = html.Div([
            html.A(dbc.Button("Reset all", id="reset_button", color="danger", size="sm",
                              style={'margin-top': '20px'}), href='/'),


        ])

        form = dbc.Form([score_range_slider, class_range_slider, apply_button, button])

        layout = html.Div([
            html.H6(['Filter Options',
                    html.Span("?",
                              id="tooltip-tg-form", className="text-info")
                     ]),
            dbc.Tooltip(
                "Filter the ERA model graph by using the below sliders and press the Submit-Button. "
                "Press the Reset-Button to reset the whole settings to the initial model. "
                "These filter can not be combined with the asset search!",
                target="tooltip-tg-form",
            ),
            html.Hr(className="my-2"),
            form
        ],
            className="blocks_areas",
            style={'width': '100%', 'height': '370px', 'paddingBottom': '5%', 'paddingTop': '5%',
                   'paddingRight': '5%', 'paddingLeft': '10%', 'margin-top': '20px'})
        return layout

    # Load Jumbotron Title and Information
    def __create_jumbotron(self):
        layout = dbc.Jumbotron(
            [
                html.H4(self.title, className="display-4"),
                html.Hr(className="my-2", id="hr-header"),
                html.P(
                    "EAM risk assessment (ERA) is a framework developed by Dr. Daniel Fuerstenau, Dr. Carson Woo"
                    " and Tim Huse", style={"color": "white"}
                ),
                html.P(dbc.Button("Learn more", color="secondary", id="open"), className="lead"),
            ],
            style={"background-color": "#3d3d3d", "padding-bottom": "15px", "padding-top": "30px"}
        )
        return layout

    # Load Modal for "Learn more"-Button
    def __create_modal_further_information(self):
        # Modal Element
        layout = dbc.Modal(
            [
                dbc.ModalHeader("EAM Risk Assessment Framework (ERA)"),
                dbc.ModalBody(["The ERA framework is an assessment framework that provides a comprehensive view of "
                              "existing IT security risks across the entire enterprise architecture of companies on"
                               " a technological level applying EAM. The framework is intended to identify and asses"
                               "s the technological threats according to the protection goals of the company.",
                               html.Hr(),
                               html.H6("The ERA Process:"),
                               html.P(),
                               html.Img(src=self.app.get_asset_url('eraProcess.png'), width="900px", alt="ERAProcess",
                                        title="ERAProcess", style={"margin-bottom": "30px"}),
                               html.P(),
                               html.Hr(),
                               html.H6("Legend of the ERA Graph:"),
                               html.P(),
                               html.Img(src=self.app.get_asset_url('legend.png'), width="550px", alt="LegendERAModel",
                                        title="LegendERAModel", style={"margin-bottom": "30px"}),
                               html.P("For further information contact Mr. Tim Huse via tim.huse@fu-berlin.de")]
                              ),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", color='danger', className="ml-auto")
                ),
            ],
            id="modal-info",
            size="xl",
            scrollable=True,
        )
        return layout

