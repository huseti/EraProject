# ------- Class: Controller ERA  ------------------
# ------- Controller of ERA framework --------------
# ------- Contains all callbacks of Dash app -------
# -*----- coding: utf-8 --------------------------*-

# imports
import dash
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import ERA_Framework_Dashboard.ModelERA as modelERA
import pandas as pd
import dash_html_components as html
import ERA_Framework_Dashboard.ViewERA as viewERA
import ERA_Framework_Dashboard.assets.Stylesheets as styleERA
import dash_cytoscape as cyto


class ControllerERA:

    # Constructor
    def __init__(self, dash_app: dash.Dash, era_model: modelERA, era_view: viewERA):
        self.app = dash_app
        self.era_model = era_model
        self.era_view = era_view

    # Connecting all callbacks to the Dash application
    def register_callbacks(self):

        # Callback for Clicking on Node
        @self.app.callback(Output('table-tapNodeData-json', 'children'),
                           [Input('cytoscape-era-model', 'tapNodeData')])
        def displayTapNodeData(data):
            if data:
                return dbc.Table.from_dataframe(self.__generate_table_details_node(data),
                                                id='table_infonode', striped=True, bordered=True, hover=True,
                                                size='sm', style={'margin-top': '10px', 'margin-right': '10px',
                                                                  'background-color': 'white'})
            else:
                return html.P('Please tap on a Node to get detailed information', className="text-muted",
                              style={
                                  'textAlign': 'center',
                                  'margin-top': '20px'
                              })

        # Callback for Clicking on Edge
        @self.app.callback(Output('table-tapEdgeData-json', 'children'),
                           [Input('cytoscape-era-model', 'tapEdgeData')])
        def displayTapEdgeData(data):
            if data:
                return dbc.Table.from_dataframe(self.__generate_table_details_edge(data),
                                                id='table_infonode', striped=True, bordered=True, hover=True,
                                                size='sm', style={'margin-top': '10px', 'margin-right': '10px',
                                                                  'background-color': 'white'})
            else:
                return html.P('Please tap on an Edge to get detailed information', className="text-muted",
                              style={
                                  'textAlign': 'center',
                                  'margin-top': '20px'
                              })

        # Callback for Uploading JSON File and Updating the cyto graph and info bar
        @self.app.callback(
            [Output('graph-div', 'children'),
             Output('table-info-bar', 'children'),
             Output('search_button', 'disabled'),
             Output('filter_button', 'disabled')],
            [Input('upload-data', 'contents')],
            [State('upload-data', 'filename')])
        def update_output(list_of_contents, list_of_names):

            if list_of_contents is not None:
                search_disabled = False
                filter_disabled = False
                self.era_model.parse_contents_to_json(list_of_contents, list_of_names)
            else:
                search_disabled = True
                filter_disabled = True
                return html.P("Upload ERA data above to see a graph model of your data here", className="text-muted",
                              style={
                                  'textAlign': 'center',
                                  'margin-top': '240px',
                                  'paddingBottom': '440px'
                              }), \
                       html.P("Upload ERA data above to see information here", className="text-muted",
                              style={
                                  'textAlign': 'center',
                                  'margin-top': '20px'
                              }), search_disabled, filter_disabled

            cyto_graph = cyto.Cytoscape(
                id='cytoscape-era-model',
                stylesheet=styleERA.get_stylesheet_cyto(),
                zoomingEnabled=True,
                minZoom=0.3,
                maxZoom=2.5,
                style={'width': '100%', 'height': '700px'},
                layout={
                    'name': 'breadthfirst',
                    'roots': '[class = "Process"]'
                },
                elements=self.era_model.transform_json_to_cyto()
            )

            # Generate the infobar
            info_bar = self.__generate_infobar()

            return cyto_graph, info_bar, search_disabled, filter_disabled

        # Callback for open the Modal with more information about the ERA framework
        @self.app.callback(
            Output("modal-info", "is_open"),
            [Input("open", "n_clicks"), Input("close", "n_clicks")],
            [State("modal-info", "is_open")])
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        # Form callbacks to filter the Graph
        @self.app.callback(
            [Output('cytoscape-era-model', 'elements'),
             Output('cytoscape-era-model', 'layout'),
             Output('score-range-slider', 'value'),
             Output('class-range-slider', 'value'),
             Output('search-element', 'value'),
             Output('cytoscape-era-model', 'stylesheet')],
            [Input('search_button', 'n_clicks'),
             Input('filter_button', 'n_clicks')],
            [State('score-range-slider', 'value'),
             State('class-range-slider', 'value'),
             State('search-element', 'value')])
        def filter_or_search_update_graph_layout(n_clicks_search, n_clicks_filter, value_score_slider,
                                                 value_class_slider, value_search_element):

            # access the global context variable for callbacks
            ctx = dash.callback_context

            # determine if filter button was pressed
            if ctx.triggered[0]['prop_id'] == 'filter_button.n_clicks':

                # Filter the Graph with input filter criteria
                filtered_graph = self.era_model.filter_cyto(value_score_slider, value_class_slider)

                # Empty the search-bar
                search_text = ''

                # Update the graph layout
                layout_update = {}
                # If a search term is entered, Score Range Slider is not initial or only vulnerabilities are shown
                # switch to random layout
                if value_score_slider != [0, 10] or value_class_slider[0] == 3:
                    layout_update = {'name': 'circle'}
                # If processes are the lowest class show tree with process as root
                elif value_class_slider[0] == 0:
                    layout_update = {'name': 'breadthfirst', 'roots': '[class = "Process"]'}
                # If applications are the lowest class show tree with applications as root
                elif value_class_slider[0] == 1:
                    layout_update = {'name': 'breadthfirst', 'roots': '[class = "Application"]'}
                # If technologies are the lowest class show tree with technologies as root
                elif value_class_slider[0] == 2:
                    layout_update = {'name': 'breadthfirst', 'roots': '[class = "Technology"]'}

                return filtered_graph, layout_update, value_score_slider, value_class_slider, search_text, \
                       styleERA.get_stylesheet_cyto()

            # determine if search button was pressed
            elif ctx.triggered[0]['prop_id'] == 'search_button.n_clicks':

                # Reset sliders to default
                value_score_slider = [0, 10]
                value_class_slider = [0, 3]

                # update layout if search term is entered
                if value_search_element == '':
                    layout_update = {'name': 'breadthfirst', 'roots': '[class = "Process"]'}
                    stylesheet_cyto = styleERA.get_stylesheet_cyto()
                else:
                    layout_update = {'name': 'concentric'}
                    stylesheet_cyto = styleERA.get_stylesheet_cyto_search()

                search_result_graph = self.era_model.search_elements_cyto(value_search_element)

                if search_result_graph == []:
                    search_result_graph = [{'data': {'id': 'one', 'label': 'No element found.'}}]

                return search_result_graph, layout_update,\
                    value_score_slider, value_class_slider, value_search_element, stylesheet_cyto

            # return basic initial graph if no button was pressed
            else:
                return self.era_model.filter_cyto(), \
                       {'name': 'breadthfirst', 'roots': '[class = "Process"]'}, \
                       [0, 10], [0, 3], '', styleERA.get_stylesheet_cyto()

    # Generate the table details for a node
    def __generate_table_details_node(self, data):
        df_general = pd.DataFrame(
            {
                "Key": ["Name", "ERA Score", "Asset Type", "ID", "Protection Req.", "Affecting vulnerab.",
                        "Description"
                        ],
                "Value": [data['label'], '{0:.3g}'.format(data['era_score']), data['class'], data['id'],
                          data['protection_requirements'],
                          data['count_affecting_vulnerabilities'], data['description']
                          ],
            }
        )
        # Merge the data frame with process data
        if data['class'] == 'Process':
            df_process = pd.DataFrame({
                "Key": [
                    "Imp. ERA Score", "Imp. Impact Score", "Imp. Asset ID", "Imp. Asset Class", "Process Responsible"
                ],
                "Value": [
                    '{0:.3g}'.format(data['impacting_asset_era_score']),
                    '{0:.3g}'.format(data['impacting_asset_impact_score']),
                    data['impacting_asset_id'], data['impacting_asset_class'], data['process_responsible']
                    ]
                })
            return pd.concat([df_general, df_process])

        # Merge the data frame with application data
        elif data['class'] == 'Application':
            df_application = pd.DataFrame(
                {"Key": [
                    "Imp. ERA Score", "Imp. Impact Score", "Imp. Asset ID", "Imp. Asset Class",
                    "System Responsible", "Department Syst. Resp.", "Business Responsible", "Department Bus. Resp.",
                    "Start Date", "Vendor", "Operator", "Total User", "Availability Req.", "Integrity Req.",
                    "Confidentiality Req."
                ],
                 "Value": [
                     '{0:.3g}'.format(data['impacting_asset_era_score']),
                     '{0:.3g}'.format(data['impacting_asset_impact_score']),
                     data['impacting_asset_id'], data['impacting_asset_class'],
                     data['application_responsible_system'], data['application_department_responsible_system'],
                     data['application_responsible_business'], data['application_department_responsible_business'],
                     data['application_start_date'], data['application_vendor'], data['application_operator'],
                     data['application_total_user'], data['application_availability_requirements'],
                     data['application_integrity_requirements'], data['application_confidentiality_requirements']
                 ]
                 })
            return pd.concat([df_general, df_application])

        # Merge the data frame with technology data
        elif data['class'] == 'Technology':
            df_technology = pd.DataFrame(
                {"Key": [
                    "Imp. ERA Score", "Imp. Impact Score", "Imp. Asset ID", "Imp. Asset Class",
                    "Vendor", "Product", "Version"
                ],
                    "Value": [
                        '{0:.3g}'.format(data['impacting_asset_era_score']),
                        '{0:.3g}'.format(data['impacting_asset_impact_score']),
                        data['impacting_asset_id'], data['impacting_asset_class'],
                        data['technology_vendor'], data['technology_product'],
                        data['technology_version']
                    ]
                })
            df_general["Value"][0] = data['technology_vendor'] + ' ' + data['technology_product']
            return pd.concat([df_general, df_technology])

        # Merge the data frame with vulnerability data
        elif data['class'] == 'Vulnerability':
            df_vulnerability = pd.DataFrame(
                {"Key": [
                    "CVSS Score", "Access Vector", "Access Complexity", "Authentication",
                    "User Interaction req.", "Severity", "Confidentiality Impact", "Integrity Impact",
                    "Availability Impact", "CVSS Exploitability Score", "CVSS Impact Score", "Vulnerability Date",
                    "Obtain all privileges", "Obtain user privileges", "Obtain other privileges"
                ],
                    "Value": [
                        data['vulnerability_cvss_score'], data['vulnerability_access_vector'],
                        data['vulnerability_access_complexity'], data['vulnerability_authentication'],
                        data['vulnerability_user_interaction_required'], data['vulnerability_severity'],
                        data['vulnerability_confidentiality_impact'], data['vulnerability_integrity_impact'],
                        data['vulnerability_availability_impact'], data['vulnerability_cvss_exploitability_score'],
                        data['vulnerability_cvss_impact_score'], data['vulnerability_date'],
                        data['vulnerability_obtain_all_privilege'], data['vulnerability_obtain_user_privilege'],
                        data['vulnerability_obtain_other_privilege']
                    ]
                })
            df_general["Key"][1] = "CVSS Score"
            df_general["Value"][0] = data['id']
            return pd.concat([df_general, df_vulnerability])

        else:
            pass

    # Generate the table details for a edge
    def __generate_table_details_edge(self, data):
        df = pd.DataFrame(
            {
                "Key": ["Impact Score", "Label", "Rater of Impact Score", "Criticality", "Non-Substitutability",
                        "Indegree Centrality", "Outdegree Centrality", "Impact on availability",
                        "Impact on confidentiality", "Impact on integrity"
                        ],
                "Value": ['{0:.3g}'.format(data['impact score']), data['label'], data['rater'], data['criticality'],
                          data['non-substitutability'], data['indegree centrality'], data['outdegree centrality'],
                          data['impact on availability'], data['impact on confidentiality'], data['impact on integrity']
                          ],
            }
        )
        return df

    # Generate the Cards for the infobar
    def __generate_infobar(self):

        card_content_score = [
            dbc.CardBody(
                [
                    html.H5('{0:.3g}'.format(self.era_model.average_era_score_assets), className="card-title"),
                    html.P(
                        "Ø ERA Score",
                        className="card-text",
                    ),
                ]
            ),
        ]

        # Determine the color of the Card depending on the era score
        if self.era_model.average_era_score_assets >= 7.0:
            color_card_score = "danger"
        elif self.era_model.average_era_score_assets < 4.0:
            color_card_score = "success"
        else:
            color_card_score = "warning"

        card_content_vul = [
            dbc.CardBody(
                [
                    html.H5(str(self.era_model.total_vulnerabilities), className="card-title"),
                    html.P(
                        "Vulnerabilities",
                        className="card-text",
                    ),
                ]
            ),
        ]

        # Determine the color of the Card depending on the amount of vulnerabilities
        if self.era_model.total_vulnerabilities >= 100:
            color_card_vul = "danger"
        elif self.era_model.total_vulnerabilities < 25:
            color_card_vul = "success"
        else:
            color_card_vul = "warning"

        card_content_assets = [
            dbc.CardBody(
                [
                    html.H5(str(self.era_model.amount_nodes), className="card-title"),
                    html.P(
                        "Assets",
                        className="card-text",
                    ),
                ]
            ),
        ]

        card_content_path = [
            dbc.CardBody(
                [
                    html.P(
                        self.era_model.filename,
                        className="card-text", style={"font-weight": "bold"}
                    ),
                    html.P(
                        "Current Filepath",
                    ),
                ]
            ),
        ]

        cards = html.Div(
            [
                dbc.CardColumns(
                    [
                        dbc.Card(card_content_score, color=color_card_score, inverse=True),
                        dbc.Card(card_content_vul, color=color_card_vul, inverse=True),
                        dbc.Card(card_content_assets, color="secondary"),
                    ],
                ),
                dbc.Card(card_content_path, color="secondary"),
            ]
        )

        return cards


