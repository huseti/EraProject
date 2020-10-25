# ------- Module: View ERA  ------------------------
# ------- Layouts of ERA framework -----------------
# ------- Generating the layouts of ERA framework --
# -*----- coding: utf-8 --------------------------*-

# imports
import dash_core_components as dcc
import dash_cytoscape as cyto
import dash_html_components as html
import dash_bootstrap_components as dbc
import ERA_Framework_Dashboard.assets.Stylesheets as style_era
import ERA_Framework_Dashboard.Model_ERA as model_era
import pandas as pd


# Load main Layout of Dash App
def create_main_layout(title: str, era_model_path: str) -> html.Div:
    layout = html.Div(children=[
        # Jumbotron Title and Information
        create_jumbotron(title),

        # TODO: add DCC Upload Component
        # Upload Component
        dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop your ERA File in JSON Format or ',
                html.A('Select JSON File', id='Upload_Link')
            ]),
            style=style_era.get_style_upload(),
            # Forbid multiple files to be uploaded
            multiple=False
        ),

        # Layout 3 Columns
        html.Div(
            [
                dbc.Row(
                    [  # Generate Left Column of Layout with legend and form
                        dbc.Col(create_left_column(), width=2),

                        # Generate Cytoscape Graph
                        dbc.Col(create_cyto_graph(era_model_path)),

                        # Generate Right Column of Layout with details and info bar
                        dbc.Col(create_right_column(), width=3),
                    ]
                ),
            ]
        ),
    ])
    return layout


# Load Cytoscape Graph for Dashboard
def create_cyto_graph(era_json_path: str) -> cyto.Cytoscape:
    # Load defined stylesheet and transformed era model (to cytoscape graph)
    graph = cyto.Cytoscape(
        id='cytoscape-era-model',
        stylesheet=style_era.get_stylesheet_cyto(),
        style={'width': '100%', 'height': '500px'},
        layout={
            'name': 'breadthfirst',
            'roots': '[class = "Process"]'
        },
        elements=model_era.transform_json_to_cyto(era_json_path)
    )
    return graph


# Load Left column of layout with legend and form
def create_right_column():
    layout = html.Div(children=[
        create_detail_info_node(),
        create_detail_info_edge(),
        create_info_bar()
    ])
    return layout


# Load detail information on the right side (of
def create_detail_info_node():
    layout = html.Div([
        html.H6('Details Node'),
        html.Hr(className="my-2"),
    ],
        style={'width': '100%', 'height': '250px', 'paddingBottom': '5%', 'paddingTop': '7%',
               'paddingRight': '5%', 'paddingLeft': '10%', 'overflow-y': 'scroll'})
    return layout


# Load detail information on the right side (of
def create_detail_info_edge():
    layout = html.Div([
        html.H6('Details Edge'),
        html.Hr(className="my-2"),
    ],
        style={'width': '100%', 'height': '150px', 'paddingBottom': '5%', 'paddingTop': '7%',
               'paddingRight': '5%', 'paddingLeft': '10%', 'overflow-y': 'scroll'})
    return layout


# Load info bar on the right side (of
def create_info_bar():
    layout = html.Div([
        html.H6('Info Bar'),
        html.Hr(className="my-2"),
        dbc.ListGroup(
            [
                dbc.ListGroupItem("Item 1"),
                dbc.ListGroupItem("Item 2"),
                dbc.ListGroupItem("Item 3"),
            ],
            horizontal=True,
            className="mb-2",
        ),
    ],
        style={'width': '100%', 'height': '100px', 'paddingBottom': '5%', 'paddingTop': '7%',
               'paddingRight': '5%', 'paddingLeft': '10%', 'overflow-y': 'scroll'})
    return layout


# Load Left column of layout with legend and form
def create_left_column():
    layout = html.Div(children=[
        create_form(),
        create_legend()
    ])
    return layout


# Load form
def create_form():
    search_input = dbc.FormGroup(
        [
            dbc.Label("Search", html_for="search-element", style={'margin-top': '20px'}),
            dbc.Input(type="search", id="search-element", placeholder="Enter asset ID ..."),
            dbc.Button("Search", color="primary", size="sm", style={'margin-top': '10px'}),
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
                },),
            dbc.FormText(
                "Only show assets with the selected asset class",
                color="secondary",
            ),
        ]
    )

    form = dbc.Form([search_input, score_range_slider, class_range_slider])

    layout = html.Div([
        html.H6('Options'),
        html.Hr(className="my-2"),
        form
    ],
        style={'width': '100%', 'height': '250px', 'paddingBottom': '5%', 'paddingTop': '7%',
               'paddingRight': '5%', 'paddingLeft': '10%', 'overflow-y': 'scroll'})
    return layout


# Load legend
def create_legend():
    df = pd.DataFrame(
        {
            "Element": ["X -> Y", "Green asset", "Yellow asset", "Red asset", "Rectangle", "Triangle", "Circle", "Vee"],
            "Description": ["X is dependent on Y",  "ERA Score 0.0 - 3.9", "ERA Score 4.0 - 6.9", "ERA Score 7.0 - 10.0",
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
               'paddingRight': '1%', 'paddingLeft': '10%', 'overflow-y': 'scroll'})
    return layout


# Load Jumbotron Title and Information
def create_jumbotron(title: str):
    layout = dbc.Jumbotron(
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
    )
    return layout
