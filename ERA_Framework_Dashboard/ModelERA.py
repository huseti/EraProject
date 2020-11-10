# ------- Class: Model ERA  -----------------------
# ------- Data Model of ERA framework --------------
# ------- Parsing input JSON into model ------------
# -*----- coding: utf-8 --------------------------*-

# imports
import json
import base64
import io


class ModelERA:

    # Constructor
    def __init__(self):
        # Files/ Filepath
        self.era_json_file = {}
        self.era_cyto_graph = []
        self.filename = ''
        # Model Information
        self.average_era_score_assets = 0.0
        self.total_vulnerabilities = 0
        self.amount_nodes = 0

    # Definition of Getters and Setters

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

    # Parse content to JSON Format
    def parse_contents_to_json(self, contents, filename):
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
        try:
            if 'json' in filename:
                io_file = io.StringIO(decoded.decode('utf-8'))
                self.era_json_file = json.load(io_file)
                self.filename = filename
            else:
                print("File is not JSON Format")
        except Exception as e:
            print(e)

    # Transform ERA JSON model to cytoscape graph format
    def transform_json_to_cyto(self) -> list:
        # Check JSON File is not initial
        if self._era_json_file != {}:

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
                        'id': node['id'], 'class': node['class'], 'label': node['technology_product'], 'era_score': node['era_score'],
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
                        'id': node['id'], 'class': node['class'], 'label': '', 'era_score': node['era_score'],
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

    # Filter the complete cytoscape graph for search terms of form and return the filtered graph
    def filter_cyto(self, score_range=[0, 10], class_range=[0, 3], search_term='') -> list:

        # Check if ERA Cyto Graph is initial
        if not self.era_cyto_graph:
            return []

        # Initialize Helper variables
        # Helper list for filtered Cytograph, helper list of included nodes and helper dict for Asset classes
        filtered_cyto = []
        included_nodes = []
        asset_classes = ['Process', 'Application', 'Technology', 'Vulnerability']
        lb_score_range = score_range[0]
        ub_score_range = score_range[1]
        lb_class_range = class_range[0]
        ub_class_range = class_range[1]
        nodes = []
        edges = []

        # Initialize search term
        if not search_term:
            search_term = ''

        # Check if Form Settings are initial and return the initial graph if so
        if score_range != [0, 10] or class_range != [0, 3] or search_term:

            # Loop over nodes in JSON File
            for node in self.era_json_file['Nodes']:

                # Only append nodes that are inside the filter criteria
                if node['class'] in asset_classes[lb_class_range:ub_class_range+1] and \
                        lb_score_range <= node['era_score'] <=  ub_score_range and \
                        search_term.upper() in node['label'].upper():

                    # Add the node to the included nodes list
                    included_nodes.append(node['id'])

                    # Append Process Objects
                    if node['class'] == 'Process':
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
                        nodes.append({'data': {
                            'id': node['id'], 'class': node['class'], 'label': node['technology_product'], 'era_score': node['era_score'],
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
                        nodes.append({'data': {
                            'id': node['id'], 'class': node['class'], 'label': '', 'era_score': node['era_score'],
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

            # Loop over edges in JSON File and only append the ones of nodes that are in the filtered graph
            for edge in self.era_json_file['Edges']:
                if edge['source'] in included_nodes and edge['target'] in included_nodes:
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

            filtered_cyto = nodes + edges

            return filtered_cyto
        else:
            # return initial graph as form settings haven't been changed
            return self.era_cyto_graph

    # Filter the complete cytoscape graph for a search terms and return the filtered graph
    def search_elements_cyto(self, search_term: str = '') -> list:

        # Check if ERA Cyto Graph is initial
        if not self.era_cyto_graph:
            return []

        # return initial graph as form settings haven't been changed
        if not search_term:
            return self.era_cyto_graph

        # Initialize Helper variables
        detected_nodes = []
        included_nodes = []
        filtered_cyto = []
        nodes = []
        edges = []

        # Loop over nodes in JSON File
        for node in self.era_json_file['Nodes']:

            # Only append nodes that are inside the filter criteria - set the "search_result"-Attribute
            if search_term.upper() in node['label'].upper() or search_term.upper() in str(node['id'].upper()):

                # Add the node to the included nodes list
                detected_nodes.append(node['id'])

                # Append Process Objects
                if node['class'] == 'Process':
                    nodes.append({'data': {
                        'id': node['id'], 'search_result': True, 'class': node['class'], 'label': node['label'],
                        'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_era_score':
                            node['impacting_asset_era_score'], 'impacting_asset_id': node['impacting_asset_id'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'], 'impacting_asset_class':
                            node['impacting_asset_class'],
                        'affecting_vulnerabilities': node['affecting_vulnerabilities'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'], 'description':
                            node['description'], 'process_responsible': node['process_responsible']
                    }})

                # Append Application Objects
                if node['class'] == 'Application':
                    nodes.append({'data': {
                        'id': node['id'], 'search_result': True, 'class': node['class'], 'label': node['label'],
                        'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_id':
                            node['impacting_asset_id'], 'impacting_asset_era_score': node['impacting_asset_era_score'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'], 'impacting_asset_class':
                            node['impacting_asset_class'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'], 'description':
                            node['description'],
                        'application_responsible_system': node['application_responsible_system'],
                        'application_department_responsible_system': node['application_department_responsible_system'],
                        'application_responsible_business': node['application_responsible_business'],
                        'application_department_responsible_business': node[
                            'application_department_responsible_business'],
                        'application_start_date': node['application_start_date'], 'application_vendor':
                            node['application_vendor'], 'application_operator': node['application_operator'],
                        'application_total_user': node['application_total_user'],
                        'application_availability_requirements':
                            node['application_availability_requirements'], 'application_integrity_requirements':
                            node['application_integrity_requirements'], 'application_confidentiality_requirements':
                            node['application_confidentiality_requirements']
                    }})

                # Append Technology Objects
                if node['class'] == 'Technology':
                    nodes.append({'data': {
                        'id': node['id'], 'search_result': True, 'class': node['class'], 'label': node['technology_product'],
                        'era_score': node['era_score'],
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
                    nodes.append({'data': {
                        'id': node['id'], 'search_result': True, 'class': node['class'], 'label': '', 'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_era_score':
                            node['impacting_asset_era_score'], 'impacting_asset_id': node['impacting_asset_id'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'], 'impacting_asset_class':
                            node['impacting_asset_class'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'], 'description':
                            node['description'], 'vulnerability_cvss_score': node['vulnerability_cvss_score'],
                        'vulnerability_access_vector': node['vulnerability_access_vector'],
                        'vulnerability_access_complexity':
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

        # Loop over edges in JSON File and only append the ones of nodes that connect the searched assets
        # with others
        for edge in self.era_json_file['Edges']:

            if edge['source'] in detected_nodes:
                included_nodes.append(edge['target'])

            if edge['target'] in detected_nodes:
                included_nodes.append(edge['source'])

            if edge['source'] in detected_nodes or edge['target'] in detected_nodes:
                edges.append({'data': {
                    'source': edge['source'], 'target': edge['target'],
                    'source_class': edge['source_class'], 'target_class':
                        edge['target_class'],
                    'label': str(edge['source_class'] + ' ' + edge['source'] + ' to ' +
                                 edge['target_class'] + ' ' + edge['target']),
                    'impact score': edge['impact_score'], 'rater': edge['rater'],
                    'criticality': edge['criticality'],
                    'non-substitutability': edge['non-substitutability'],
                    'indegree centrality': edge['indegree centrality'],
                    'outdegree centrality': edge['outdegree centrality'], 'impact on availability':
                        edge['impact on availability'],
                    'impact on confidentiality': edge['impact on confidentiality'],
                    'impact on integrity': edge['impact on integrity']
                }})

        # Loop over nodes in JSON File a second time and append all assets that are connected to detected assets
        for node in self.era_json_file['Nodes']:

            # Only append nodes that are connected to detected assets - set the "connected_to"-Attribute
            if node['id'] in included_nodes and node['id'] not in detected_nodes:

                # Append Process Objects
                if node['class'] == 'Process':
                    nodes.append({'data': {
                        'id': node['id'], 'connected_to': True, 'class': node['class'], 'label': node['label'],
                        'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_era_score':
                            node['impacting_asset_era_score'], 'impacting_asset_id': node['impacting_asset_id'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'],
                        'impacting_asset_class':
                            node['impacting_asset_class'],
                        'affecting_vulnerabilities': node['affecting_vulnerabilities'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'],
                        'description':
                            node['description'], 'process_responsible': node['process_responsible']
                    }})

                # Append Application Objects
                if node['class'] == 'Application':
                    nodes.append({'data': {
                        'id': node['id'], 'connected_to': True, 'class': node['class'], 'label': node['label'],
                        'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_id':
                            node['impacting_asset_id'],
                        'impacting_asset_era_score': node['impacting_asset_era_score'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'],
                        'impacting_asset_class':
                            node['impacting_asset_class'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'],
                        'description':
                            node['description'],
                        'application_responsible_system': node['application_responsible_system'],
                        'application_department_responsible_system': node[
                            'application_department_responsible_system'],
                        'application_responsible_business': node['application_responsible_business'],
                        'application_department_responsible_business': node[
                            'application_department_responsible_business'],
                        'application_start_date': node['application_start_date'], 'application_vendor':
                            node['application_vendor'], 'application_operator': node['application_operator'],
                        'application_total_user': node['application_total_user'],
                        'application_availability_requirements':
                            node['application_availability_requirements'], 'application_integrity_requirements':
                            node['application_integrity_requirements'],
                        'application_confidentiality_requirements':
                            node['application_confidentiality_requirements']
                    }})

                # Append Technology Objects
                if node['class'] == 'Technology':
                    nodes.append({'data': {
                        'id': node['id'], 'connected_to': True, 'class': node['class'],
                        'label': node['technology_product'],
                        'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_era_score':
                            node['impacting_asset_era_score'], 'impacting_asset_id': node['impacting_asset_id'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'],
                        'impacting_asset_class':
                            node['impacting_asset_class'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'],
                        'description':
                            node['description'], 'technology_vendor': node['technology_vendor'],
                        'technology_product':
                            node['technology_product'], 'technology_version': node['technology_version']
                    }})

                # Append Vulnerability Objects
                if node['class'] == 'Vulnerability':
                    nodes.append({'data': {
                        'id': node['id'], 'connected_to': True, 'class': node['class'], 'label': '',
                        'era_score': node['era_score'],
                        'protection_requirements': node['protection_requirements'], 'impacting_asset_era_score':
                            node['impacting_asset_era_score'], 'impacting_asset_id': node['impacting_asset_id'],
                        'impacting_asset_impact_score': node['impacting_asset_impact_score'],
                        'impacting_asset_class':
                            node['impacting_asset_class'],
                        'count_affecting_vulnerabilities': node['count_affecting_vulnerabilities'],
                        'description':
                            node['description'], 'vulnerability_cvss_score': node['vulnerability_cvss_score'],
                        'vulnerability_access_vector': node['vulnerability_access_vector'],
                        'vulnerability_access_complexity':
                            node['vulnerability_access_complexity'], 'vulnerability_authentication':
                            node['vulnerability_authentication'], 'vulnerability_user_interaction_required':
                            node['vulnerability_user_interaction_required'], 'vulnerability_severity':
                            node['vulnerability_severity'], 'vulnerability_confidentiality_impact':
                            node['vulnerability_confidentiality_impact'], 'vulnerability_integrity_impact':
                            node['vulnerability_integrity_impact'], 'vulnerability_availability_impact':
                            node['vulnerability_availability_impact'],
                        'vulnerability_cvss_exploitability_score':
                            node['vulnerability_cvss_exploitability_score'], 'vulnerability_cvss_impact_score':
                            node['vulnerability_cvss_impact_score'],
                        'vulnerability_date': node['vulnerability_date'],
                        'vulnerability_obtain_all_privilege': node['vulnerability_obtain_all_privilege'],
                        'vulnerability_obtain_user_privilege': node['vulnerability_obtain_user_privilege'],
                        'vulnerability_obtain_other_privilege': node['vulnerability_obtain_other_privilege']
                    }})

        filtered_cyto = nodes + edges

        return filtered_cyto

