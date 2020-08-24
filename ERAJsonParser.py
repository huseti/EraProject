# imports
from Application import Application
import json
import os
from Process import Process
from Technology import Technology
from Vulnerability import Vulnerability


class ERAJsonParser:

    # Constructor
    def __init__(self, processes: dict, applications: dict,
                 technologies: dict, vulnerabilities: dict):
        self.processes = processes
        self.applications = applications
        self.technologies = technologies
        self.vulnerabilities = vulnerabilities
        self.json_file = {}

    def save_era_model_to_json(self, filepath:str, filename: str):
        # main two entries in the JSON are nodes and edges
        self.json_file['Nodes'] = []
        self.json_file['Edges'] = []
        # load all objects (nodes) into the json file
        self.__load_processes_to_json()
        self.__load_applications_to_json()
        self.__load_technologies_to_json()
        self.__load_vulnerabilities_to_json()
        # load all edges (dependencies) into the json file
        self.__load_edges_to_json()
        # save the json file persistent
        self.__save_json_file(filepath, filename)

    def __load_processes_to_json(self):
        for process in self.processes.values():
            self.json_file['Nodes'].append({
                'class': 'Process',
                'id': str(process.id),
                'label': process.name,
                'era_score': process.era_score,
                'protection_requirements': process.protection_requirements,
                'impacting_asset_id': process.impacting_asset_id,
                'impacting_asset_era_score': process.impacting_asset_era_score,
                'impacting_asset_impact_score': process.impacting_asset_impact_score,
                'impacting_asset_class': process.impacting_asset_class,
                'affecting_vulnerabilites': process.affecting_vulnerabilites,
                'count_affecting_vulnerabilites': process.count_affecting_vulnerabilites,
                'description': '',
                'process_responsible': process.responsible,
                'application_responsible_system': '',
                'application_department_responsible_system': '',
                'application_responsible_business': '',
                'application_department_responsible_business': '',
                'application_start_date': '',
                'application_vendor': '',
                'application_operator': '',
                'application_total_user': '',
                'application_availability_requirements': '',
                'application_integrity_requirements': '',
                'application_confidentiality_requirements': '',
                'technology_vendor': '',
                'technology_product': '',
                'technology_version': '',
                'vulnerability_cvss_score': '',
                'vulnerability_access_vector': '',
                'vulnerability_access_complexity': '',
                'vulnerability_authentication': '',
                'vulnerability_user_interaction_required': '',
                'vulnerability_severity': '',
                'vulnerability_confidentiality_impact': '',
                'vulnerability_integrity_impact': '',
                'vulnerability_availability_impact': '',
                'vulnerability_cvss_exploitability_score': '',
                'vulnerability_cvss_impact_score': '',
                'vulnerability_date': '',
                'vulnerability_obtain_all_privilege': '',
                'vulnerability_obtain_user_privilege': '',
                'vulnerability_obtain_other_privilege': ''
            })

    def __load_applications_to_json(self):
        for app in self.applications.values():
            self.json_file['Nodes'].append({
                'class': 'Application',
                'id': str(app.id),
                'label': app.name,
                'era_score': app.era_score,
                'protection_requirements': app.protection_requirements,
                'impacting_asset_id': app.impacting_asset_id,
                'impacting_asset_era_score': app.impacting_asset_era_score,
                'impacting_asset_impact_score': app.impacting_asset_impact_score,
                'impacting_asset_class': app.impacting_asset_class,
                'affecting_vulnerabilites': app.affecting_vulnerabilites,
                'count_affecting_vulnerabilites': app.count_affecting_vulnerabilites,
                'description': app.description,
                'process_responsible': '',
                'application_responsible_system': app.responsible_system,
                'application_department_responsible_system': app.department_responsible_system,
                'application_responsible_business': app.responsible_business,
                'application_department_responsible_business': app.department_responsible_business,
                'application_start_date': app.start_date,
                'application_vendor': app.vendor,
                'application_operator': app.operator,
                'application_total_user': app.total_user,
                'application_availability_requirements': app.availability_requirements,
                'application_integrity_requirements': app.integrity_requirements,
                'application_confidentiality_requirements': app.confidentiality_requirements,
                'technology_vendor': '',
                'technology_product': '',
                'technology_version': '',
                'vulnerability_cvss_score': '',
                'vulnerability_access_vector': '',
                'vulnerability_access_complexity': '',
                'vulnerability_authentication': '',
                'vulnerability_user_interaction_required': '',
                'vulnerability_severity': '',
                'vulnerability_confidentiality_impact': '',
                'vulnerability_integrity_impact': '',
                'vulnerability_availability_impact': '',
                'vulnerability_cvss_exploitability_score': '',
                'vulnerability_cvss_impact_score': '',
                'vulnerability_date': '',
                'vulnerability_obtain_all_privilege': '',
                'vulnerability_obtain_user_privilege': '',
                'vulnerability_obtain_other_privilege': ''
            })

    def __load_technologies_to_json(self):
        for tech in self.technologies.values():
            self.json_file['Nodes'].append({
                'class': 'Technology',
                'id': str(tech.id),
                'label': tech.name,
                'era_score': tech.era_score,
                'protection_requirements': tech.protection_requirements,
                'impacting_asset_id': tech.impacting_asset_id,
                'impacting_asset_era_score': tech.impacting_asset_era_score,
                'impacting_asset_impact_score': tech.impacting_asset_impact_score,
                'impacting_asset_class': tech.impacting_asset_class,
                'affecting_vulnerabilites': tech.affecting_vulnerabilites,
                'count_affecting_vulnerabilites': tech.count_affecting_vulnerabilites,
                'description': '',
                'process_responsible': '',
                'application_responsible_system': '',
                'application_department_responsible_system': '',
                'application_responsible_business': '',
                'application_department_responsible_business': '',
                'application_start_date': '',
                'application_vendor': '',
                'application_operator': '',
                'application_total_user': '',
                'application_availability_requirements': '',
                'application_integrity_requirements': '',
                'application_confidentiality_requirements': '',
                'technology_vendor': tech.vendor,
                'technology_product': tech.product,
                'technology_version': tech.version,
                'vulnerability_cvss_score': '',
                'vulnerability_access_vector': '',
                'vulnerability_access_complexity': '',
                'vulnerability_authentication': '',
                'vulnerability_user_interaction_required': '',
                'vulnerability_severity': '',
                'vulnerability_confidentiality_impact': '',
                'vulnerability_integrity_impact': '',
                'vulnerability_availability_impact': '',
                'vulnerability_cvss_exploitability_score': '',
                'vulnerability_cvss_impact_score': '',
                'vulnerability_date': '',
                'vulnerability_obtain_all_privilege': '',
                'vulnerability_obtain_user_privilege': '',
                'vulnerability_obtain_other_privilege': ''
            })

    def __load_vulnerabilities_to_json(self):
        for vul in self.vulnerabilities.values():
            self.json_file['Nodes'].append({
                'class': 'Vulnerability',
                'id': vul.id,
                'label': vul.name,
                'era_score': vul.cvss_score,
                'protection_requirements': 'Standard',
                'impacting_asset_id': '',
                'impacting_asset_era_score': '',
                'impacting_asset_impact_score': '',
                'impacting_asset_class': '',
                'affecting_vulnerabilites': '',
                'count_affecting_vulnerabilites': '',
                'description': vul.description,
                'process_responsible': '',
                'application_responsible_system': '',
                'application_department_responsible_system': '',
                'application_responsible_business': '',
                'application_department_responsible_business': '',
                'application_start_date': '',
                'application_vendor': '',
                'application_operator': '',
                'application_total_user': '',
                'application_availability_requirements': '',
                'application_integrity_requirements': '',
                'application_confidentiality_requirements': '',
                'technology_vendor': '',
                'technology_product': '',
                'technology_version': '',
                'vulnerability_cvss_score': vul.cvss_score,
                'vulnerability_access_vector': vul.access_vector,
                'vulnerability_access_complexity': vul.access_complexity,
                'vulnerability_authentication': vul.authentication,
                'vulnerability_user_interaction_required': vul.user_interaction_required,
                'vulnerability_severity': vul.severity,
                'vulnerability_confidentiality_impact': vul.confidentiality_impact,
                'vulnerability_integrity_impact': vul.integrity_impact,
                'vulnerability_availability_impact': vul.availability_impact,
                'vulnerability_cvss_exploitability_score': vul.cvss_exploitability_score,
                'vulnerability_cvss_impact_score': vul.cvss_impact_score,
                'vulnerability_date': vul.date,
                'vulnerability_obtain_all_privilege': vul.obtain_all_privilege,
                'vulnerability_obtain_user_privilege': vul.obtain_user_privilege,
                'vulnerability_obtain_other_privilege': vul.obtain_other_privilege
            })

    def __load_edges_to_json(self):
        # load all dependencies from vulnerabilities to technologies incl. impact score
        for tech in self.technologies.values():
            for vul_id in tech.dependent_on_vulnerabilities.keys():
                self.json_file['Edges'].append({
                    'source': str(tech.id),
                    'target': vul_id,
                    'impact_score': 1.0,
                    'source_class': 'Technology',
                    'target_class': 'Vulnerability'
                })
        # load all dependencies from technologies to applications incl. impact score
        for app in self.applications.values():
            for tech in app.dependent_on_technologies.keys():
                self.json_file['Edges'].append({
                    'source': str(app.id),
                    'target': str(tech),
                    'impact_score': app.dependent_on_technologies[tech],
                    'source_class': 'Application',
                    'target_class': 'Technology'
                })
        # load all dependencies from applications to applications incl. impact score
            for app_id in app.dependent_on_applications.keys():
                self.json_file['Edges'].append({
                    'source': str(app.id),
                    'target': str(app_id),
                    'impact_score': app.dependent_on_applications[app_id],
                    'source_class': 'Application',
                    'target_class': 'Application'
                })

        # load all dependencies from applications to processes incl. impact score
        for process in self.processes.values():
            for app in process.dependent_on_applications.keys():
                self.json_file['Edges'].append({
                    'source': str(process.id),
                    'target': str(app),
                    'impact_score': process.dependent_on_applications[app],
                    'source_class': 'Process',
                    'target_class': 'Application'
                })

    def __save_json_file(self, filepath: str, filename:str):
        # create the total filepath
        total_filepath = os.path.join(filepath, filename)
        # if path does not exist, create it
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        # Save the json file in the selected directory
        with open(total_filepath, 'w') as outfile:
            json.dump(self.json_file, outfile)

