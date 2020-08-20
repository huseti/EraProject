# imports
import json
import requests
import pandas as pd
from Technology import Technology
from Vulnerability import Vulnerability


class CVEConnector:

    def __get_vulnerabilities(self, product: str, vendor: str, version: str) -> json:
        """Send a request to the CVE DB to receive all vulnerabilities for a product to a vendor and a version"""
        pass

    def __parse_response_into_vulnerabilities(self, file: json) -> dict[str, Vulnerability]:
        """Parse the response JSON and create Vulnerability objects"""
        pass

    def get_all_vulnerabilities_per_technology(self, technologies: dict[int, Technology]) -> dict[str, Vulnerability]:
        """Loop over all technologies and get all vulnerabilites and their dependencies within the techn. objects"""
        pass


class NVDConnector(CVEConnector):

    # Constructor
    def __init__(self):
        self.HOST = 'https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString=cpe:2.3:*:'

    def __get_vulnerabilities(self, product: str, vendor: str, version: str) -> json:

        # replace empty chars with "_" and lower case the product and vendor names
        product = product.replace(" ", "_").lower()
        vendor = vendor.replace(" ", "_").lower()

        # build the request
        request = self.HOST + vendor + ':' + product + ':' + version
        response = requests.get(request)
        return response.json()

    def __parse_response_into_vulnerabilities(self, file: json) -> dict[str, Vulnerability]:
        # TODO: Loop über die Vuls
        # TODO: Je Vul ein Vulnerability Instanz erstellen in dictionary
        # TODO: Werte setzen in der Instanz aus JSON heraus
        # TODO: Prüfung ob Werte für CVSS Score V3 existieren -> Ansonsten V2
        # TODO: Dictionary returnen
        pass

    def get_all_vulnerabilities_per_technology(self, technologies: dict[int, Technology]) -> dict[str, Vulnerability]:
        # TODO: Schleife über dictionary technologies
        # TODO: vulnerabilities dictionary = Aufruf parse_response_into_vulnerabilites(Aufruf get_vulnerabilites)
        # TODO: Vulnerabilites an gesamt_dictionary hängen - Was tun falls Eintrag schon enthalten?
        # TODO: Vulnerabilites an die Technologie hängen in das dict dependent_on_vulnerabilities
        pass
