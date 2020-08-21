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

    def save_era_model_to_json(self, filepath, filename):
        pass
