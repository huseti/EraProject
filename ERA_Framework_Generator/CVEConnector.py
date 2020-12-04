# imports
from abc import ABC, abstractmethod
import json
import requests
from ERA_Framework_Generator.Vulnerability import Vulnerability


class CVEConnector(ABC):

    @abstractmethod
    def _get_vulnerabilities(self, product: str, vendor: str, version: str) -> json:
        """Send a request to the CVE DB to receive all vulnerabilities for a product to a vendor and a version"""
        pass

    @abstractmethod
    def _parse_response_into_vulnerabilities(self, file: json) -> dict:
        """Parse the response JSON and create Vulnerability objects"""
        pass

    @abstractmethod
    def get_all_vulnerabilities_per_technology(self, technologies: dict) -> dict:
        """Loop over all technologies and get all vulnerabilites and their dependencies within the techn. objects"""
        pass


class NVDConnector(CVEConnector):

    # Constructor
    def __init__(self):
        self.HOST = 'https://services.nvd.nist.gov/rest/json/cves/1.0?cpeMatchString=cpe:2.3:*:'
        self.vulnerabilities: dict = {}

    def _get_vulnerabilities(self, product: str, vendor: str, version: str) -> json:

        # replace empty chars with "_" and lower case the product and vendor names
        product = product.replace(" ", "_").lower()
        vendor = vendor.replace(" ", "_").lower()

        # build the request
        request = self.HOST + vendor + ':' + product + ':' + version
        try:
            response = requests.get(request, timeout=20)
            json_response = response.json()
        except:
            print("No connection to the CVSS Database possible.")
            json_response = {}
        return json_response

    def _parse_response_into_vulnerabilities(self, file: json) -> dict:
        # helper dictionary to store vulnerabilites per technology
        vulnerabilities_technology: dict = {}

        if file != {}:

            # Loop over the vulnerabilities in the JSON File
            for vul in file["result"]["CVE_Items"]:
                id_cve = vul["cve"]["CVE_data_meta"]["ID"]

                # Generate Vulnerability objects and add them to the Library. Then set all attributes from the JSON
                vulnerabilities_technology[id_cve] = Vulnerability(id_cve, id_cve)
                try:
                    vulnerabilities_technology[id_cve].description = vul["cve"]["description"]["description_data"][0]["value"]
                except:
                    vulnerabilities_technology[id_cve].description = 'No description'
                vulnerabilities_technology[id_cve].date = vul["publishedDate"]
                vulnerabilities_technology[id_cve].cvss_score = vul["impact"]["baseMetricV2"]["cvssV2"]["baseScore"]
                vulnerabilities_technology[id_cve].access_vector = vul["impact"]["baseMetricV2"]["cvssV2"]["accessVector"]
                vulnerabilities_technology[id_cve].access_complexity = vul["impact"]["baseMetricV2"]["cvssV2"]["accessComplexity"]
                vulnerabilities_technology[id_cve].confidentiality_impact = vul["impact"]["baseMetricV2"]["cvssV2"]["confidentialityImpact"]
                vulnerabilities_technology[id_cve].integrity_impact = vul["impact"]["baseMetricV2"]["cvssV2"]["integrityImpact"]
                vulnerabilities_technology[id_cve].availability_impact = vul["impact"]["baseMetricV2"]["cvssV2"]["availabilityImpact"]
                vulnerabilities_technology[id_cve].authentication = vul["impact"]["baseMetricV2"]["cvssV2"]["authentication"]
                vulnerabilities_technology[id_cve].user_interaction_required = vul["impact"]["baseMetricV2"]["userInteractionRequired"]
                vulnerabilities_technology[id_cve].obtain_all_privilege = vul["impact"]["baseMetricV2"]["obtainAllPrivilege"]
                vulnerabilities_technology[id_cve].obtain_user_privilege = vul["impact"]["baseMetricV2"]["obtainUserPrivilege"]#
                vulnerabilities_technology[id_cve].obtain_other_privilege = vul["impact"]["baseMetricV2"]["obtainOtherPrivilege"]
                vulnerabilities_technology[id_cve].severity = vul["impact"]["baseMetricV2"]["severity"]
                vulnerabilities_technology[id_cve].cvss_exploitability_score = vul["impact"]["baseMetricV2"]["exploitabilityScore"]
                vulnerabilities_technology[id_cve].cvss_impact_score = vul["impact"]["baseMetricV2"]["impactScore"]

        return vulnerabilities_technology

    def get_all_vulnerabilities_per_technology(self, technologies: dict) -> dict:

        # Loop over all technologies to get their dependencies on vulnerabilites
        for technology in technologies.keys():

            tech_obj = technologies[technology]

            # get all vulnerabilites in a dictionary for one specific technology
            vulnerabilities_help = self._parse_response_into_vulnerabilities(
                self._get_vulnerabilities(tech_obj.product, tech_obj.vendor, tech_obj.version))

            # add the vulnerabilites from one technology to all vulnerabilites
            self.vulnerabilities.update(vulnerabilities_help)

            # add the vulnerabilites from one specific technology to its list of dependent_on vulnerabilites
            for vul in vulnerabilities_help.keys():
                technologies[technology].dependent_on_vulnerabilities[vul] = vul

        return self.vulnerabilities
