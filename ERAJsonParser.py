# imports
from Application import Application
import json
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

    def save_era_model_to_json(self, filepath, filename):
        # main two entries in the JSON are nodes and edges
        self.json_file['Nodes'] = []
        self.json_file['Edges'] = []
        # load all objects (nodes) into the json file
        # TODO: Klassenspezifische Daten mitgeben ins JSON
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
                'count_affecting_vulnerabilites': process.count_affecting_vulnerabilites
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
                'count_affecting_vulnerabilites': app.count_affecting_vulnerabilites
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
                'count_affecting_vulnerabilites': tech.count_affecting_vulnerabilites
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
                'count_affecting_vulnerabilites': ''
            })

    def __load_edges_to_json(self):
        # TODO: Implementieren
        pass

    def __save_json_file(self, filepath, filename):
        # Abspeichern mit Filepath überprüfen
        with open(filename, 'w') as outfile:
            json.dump(self.json_file, outfile)

