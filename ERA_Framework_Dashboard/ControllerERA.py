# ------- Class: Controller ERA  ------------------
# ------- Controller of ERA framework --------------
# ------- Contains all callbacks of Dash app -------
# -*----- coding: utf-8 --------------------------*-

# imports
import dash
from dash.dependencies import Output, Input, State
import dash_bootstrap_components as dbc
import json
import ERA_Framework_Dashboard.ModelERA as modelERA
import pandas as pd
import dash_html_components as html
import dash_cytoscape as cyto
import ERA_Framework_Dashboard.assets.Stylesheets as styleERA


class ControllerERA:

    # Constructor
    def __init__(self, dash_app: dash.Dash, era_model: modelERA):
        self.app = dash_app
        self.era_model = era_model

    # Connecting all callbacks to the Dash application
    def register_callbacks(self):

        # Callback for Clicking on Node
        @self.app.callback(Output('table-tapNodeData-json', 'children'),
                           [Input('cytoscape-era-model', 'tapNodeData')])
        def displayTapNodeData(data):
            if data:
                return dbc.Table.from_dataframe(self.__generate_table_details_node(data),
                                                id='table_infonode', striped=True, bordered=True, hover=True,
                                                size='sm', style={'margin-top': '20px', 'margin-right': '10px'})
            else:
                return html.P('Please tap on a Node to get detailed information')

        # Callback for Clicking on Edge
        @self.app.callback(Output('table-tapEdgeData-json', 'children'),
                           [Input('cytoscape-era-model', 'tapEdgeData')])
        def displayTapEdgeData(data):
            if data:
                return dbc.Table.from_dataframe(self.__generate_table_details_edge(data),
                                                id='table_infonode', striped=True, bordered=True, hover=True,
                                                size='sm', style={'margin-top': '20px', 'margin-right': '10px'})
            else:
                return html.P('Please tap on an Edge to get detailed information')

        # Callback for Uploading JSON File
        @self.app.callback(Output('cytoscape-era-model', 'elements'),
                      [Input('upload-data', 'contents')],
                      [State('upload-data', 'filename'),
                       State('upload-data', 'last_modified')])
        def update_output(list_of_contents, list_of_names, list_of_dates):
            if list_of_contents is not None:
                # TODO: Upload Dialog for JSON File
                #Check if file is JSOn
                #print("list of contents: " + list_of_contents)
                #print("list of names: " + list_of_names)
                #print("list of dates: " + list_of_dates)

                self.era_model.era_json_path = r'C:/Users/thuse/Google Drive/Dokumente/Beruf/FU/4. Semester/Quellen/EAM Datensatz/' \
                             r'Bearbeitet/ERA_Model_2020_10_22.json'
                return self.era_model.transform_json_to_cyto()
            else:
                return self.era_model.transform_json_to_cyto()

        # TODO: Learn more Button

        # TODO: Form Callbacks

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
