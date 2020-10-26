# ------- Class: Model ERA  -----------------------
# ------- Data Model of ERA framework --------------
# ------- Parsing input JSON into model ------------
# -*----- coding: utf-8 --------------------------*-

# imports
import json


class ModelERA:

    # TODO: Remove json path and change to ''
    # Constructor
    def __init__(self):
        # Files/ Filepath
        self.era_json_file = []
        self.era_json_path = r'C:/Users/thuse/Google Drive/Dokumente/Beruf/FU/4. Semester/Quellen/EAM Datensatz/' \
                             r'Bearbeitet/ERA_Model_2020_10_24.json'
        self.filepath_updated = True
        self.era_cyto_graph = []
        # Model Information
        self.average_era_score_assets = 0.0
        self.total_vulnerabilities = 0
        self.amount_nodes = 0

    # Definition of Getters and Setters
    @property
    def era_json_path(self) -> str:
        return self._era_json_path

    @era_json_path.setter
    def era_json_path(self, era_json_path: str):
        self.filepath_updated = True
        self._era_json_path = era_json_path


    @property
    def era_json_file(self) -> json:
        return self._era_json_file

    @era_json_file.setter
    def era_json_file(self, era_json_file: json):
        self._era_json_file = era_json_file

    @property
    def era_cyto_graph(self) -> list:
        return self._era_cyto_graph

    @era_cyto_graph.setter
    def era_cyto_graph(self, era_cyto_graph: list):
        self._era_cyto_graph = era_cyto_graph

    # Load JSON File
    def __load_json(self):
        if self.era_json_path == '':
            self.filepath_updated = False
        else:
            with open(self.era_json_path) as file:
                self.era_json_file = json.load(file)
                self.filepath_updated = False

    # Transform ERA JSON model to cytoscape graph format
    def transform_json_to_cyto(self) -> list:
        # Check if Filepath was updated
        if self.filepath_updated:
            # Load the JSON File
            self.__load_json()

            # Initialize model info
            self.total_vulnerabilities = 0
            self.average_era_score_assets = 0

            # Transform the JSON File
            # Import nodes for Cyto file
            nodes = []
            for node in self.era_json_file['Nodes']:
                # Append Process Objects
                if node['class'] == 'Process':
                    self.average_era_score_assets += node['era_score']
                    nodes.append({'data': {
                        'id': node['id'], 'class': node['class'], 'label': node['label'], 'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_era_score':
                            node['impacting_asset_era_score'], 'impacting_asset_id': node['impacting_asset_id'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'], 'impacting_asset_class':
                            node['impacting_asset_class'], 'affecting_vulnerabilities': node['affecting_vulnerabilities'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'], 'description':
                            node['description'], 'process_responsible': node['process_responsible']
                    }})

                # Append Application Objects
                if node['class'] == 'Application':
                    self.average_era_score_assets += node['era_score']
                    nodes.append({'data': {
                        'id': node['id'], 'class': node['class'], 'label': node['label'], 'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_id':
                            node['impacting_asset_id'], 'impacting_asset_era_score': node['impacting_asset_era_score'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'], 'impacting_asset_class':
                            node['impacting_asset_class'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'], 'description':
                            node['description'], 'application_responsible_system': node['application_responsible_system'],
                        'application_department_responsible_system': node['application_department_responsible_system'],
                        'application_responsible_business': node['application_responsible_business'],
                        'application_department_responsible_business': node['application_department_responsible_business'],
                        'application_start_date': node['application_start_date'], 'application_vendor':
                            node['application_vendor'], 'application_operator': node['application_operator'],
                        'application_total_user': node['application_total_user'], 'application_availability_requirements':
                            node['application_availability_requirements'], 'application_integrity_requirements':
                            node['application_integrity_requirements'], 'application_confidentiality_requirements':
                            node['application_confidentiality_requirements']
                    }})

                # Append Technology Objects
                if node['class'] == 'Technology':
                    self.average_era_score_assets += node['era_score']
                    nodes.append({'data': {
                        'id': node['id'], 'class': node['class'], 'label': node['label'], 'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_era_score':
                            node['impacting_asset_era_score'], 'impacting_asset_id': node['impacting_asset_id'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'], 'impacting_asset_class':
                            node['impacting_asset_class'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'], 'description':
                            node['description'], 'technology_vendor': node['technology_vendor'], 'technology_product':
                            node['technology_product'], 'technology_version': node['technology_version']
                    }})

                # Append Vulnerability Objects
                if node['class'] == 'Vulnerability':
                    self.total_vulnerabilities += 1
                    nodes.append({'data': {
                        'id': node['id'], 'class': node['class'], 'label': node['label'], 'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_era_score':
                            node['impacting_asset_era_score'], 'impacting_asset_id': node['impacting_asset_id'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'], 'impacting_asset_class':
                            node['impacting_asset_class'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'], 'description':
                            node['description'], 'vulnerability_cvss_score': node['vulnerability_cvss_score'],
                        'vulnerability_access_vector': node['vulnerability_access_vector'], 'vulnerability_access_complexity':
                            node['vulnerability_access_complexity'], 'vulnerability_authentication':
                            node['vulnerability_authentication'], 'vulnerability_user_interaction_required':
                            node['vulnerability_user_interaction_required'], 'vulnerability_severity':
                            node['vulnerability_severity'], 'vulnerability_confidentiality_impact':
                            node['vulnerability_confidentiality_impact'], 'vulnerability_integrity_impact':
                            node['vulnerability_integrity_impact'], 'vulnerability_availability_impact':
                            node['vulnerability_availability_impact'], 'vulnerability_cvss_exploitability_score':
                            node['vulnerability_cvss_exploitability_score'], 'vulnerability_cvss_impact_score':
                            node['vulnerability_cvss_impact_score'], 'vulnerability_date': node['vulnerability_date'],
                        'vulnerability_obtain_all_privilege': node['vulnerability_obtain_all_privilege'],
                        'vulnerability_obtain_user_privilege': node['vulnerability_obtain_user_privilege'],
                        'vulnerability_obtain_other_privilege': node['vulnerability_obtain_other_privilege']
                    }})

            # Import edges for Cyto file
            edges = []
            for edge in self.era_json_file['Edges']:
                edges.append({'data': {
                    'source': edge['source'], 'target': edge['target'], 'source_class': edge['source_class'], 'target_class':
                        edge['target_class'], 'label': str(edge['source_class'] + ' ' + edge['source'] + ' to ' +
                                                           edge['target_class'] + ' ' + edge['target']),
                    'impact score': edge['impact_score'], 'rater': edge['rater'], 'criticality': edge['criticality'],
                    'non-substitutability': edge['non-substitutability'], 'indegree centrality': edge['indegree centrality'],
                    'outdegree centrality': edge['outdegree centrality'], 'impact on availability':
                        edge['impact on availability'], 'impact on confidentiality': edge['impact on confidentiality'],
                    'impact on integrity': edge['impact on integrity']
                }})

            self.era_cyto_graph = nodes + edges

            # Calculate model info
            self.amount_nodes = len(self.era_json_file['Nodes']) - self.total_vulnerabilities
            self.average_era_score_assets = self.average_era_score_assets / self.amount_nodes

        return self.era_cyto_graph
