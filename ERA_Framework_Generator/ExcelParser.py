# imports
from abc import ABC, abstractmethod
import pandas as pd
from ERA_Framework_Generator.Application import Application
from ERA_Framework_Generator.Process import Process
from ERA_Framework_Generator.Technology import Technology


class ExcelParser(ABC):

    @abstractmethod
    def _load_applications_file(self, path: str, file_name: str):
        """Load in the file for applications and processes and generate the objects."""
        pass

    @abstractmethod
    def _load_technologies_file(self, full_file_name: str):
        """Load in the file for technologies and generate the technology objects."""
        pass

    @abstractmethod
    def _load_informationflows_file(self):
        """Load in the file for information flows and generate the dependencies."""
        pass

    @abstractmethod
    def generate_era_classes(self):
        """Callable method from outside to generate classes with Excel input"""
        pass

    @abstractmethod
    def _generate_process(self, row):
        """Generate a process object for each excel line if the process does not exist yet"""
        pass

    @abstractmethod
    def _generate_application(self, row):
        """Generate a process object for each excel line if the process does not exist yet"""
        pass

    @abstractmethod
    def _generate_dependencies_process_application(self, row):
        """Generate the dependencies between processes and applications"""
        pass

    @abstractmethod
    def _generate_technology(self, row):
        """Generate a technology object for each excel line if the technology does not exist yet"""
        pass

    @abstractmethod
    def _generate_dependencies_application_technology(self, row):
        """Generate the dependencies between processes and applications"""
        pass

    @abstractmethod
    def _generate_dependencies_application_application(self, row):
        """Generate the dependencies between applications and applications"""
        pass


class TestbankExcelParser(ExcelParser):

    # Constructor
    def __init__(self, file_applications: str, file_technologies: str, file_informationflows: str):
        self.file_applications = file_applications
        self.file_technologies = file_technologies
        self.file_informationflows = file_informationflows
        self.processes: dict[int, Process] = {}
        self.applications: dict[int, Application] = {}
        self.technologies: dict[int, Technology] = {}

    def _load_applications_file(self):
        # load the excel file
        self._excel_applications = pd.read_csv(filepath_or_buffer=self.file_applications, sep=';',
                                               encoding='unicode_escape')

        # loop over excel rows and generate the application and process objects and the dependencies
        for index, row in self._excel_applications.iterrows():
            self._generate_process(row)
            self._generate_application(row)
            self._generate_dependencies_process_application(row)

    def _load_technologies_file(self):
        # load the excel file
        self._excel_technologies = pd.read_csv(filepath_or_buffer=self.file_technologies, sep=';',
                                               encoding='unicode_escape')

        # loop over excel rows and generate the technology objects and dependencies
        for index, row in self._excel_technologies.iterrows():
            self._generate_technology(row)
            self._generate_dependencies_application_technology(row)

    def _load_informationflows_file(self):
        # load the excel file
        self._excel_informationflows = pd.read_csv(filepath_or_buffer=self.file_informationflows, sep=';',
                                                   encoding='unicode_escape')

        # loop over excel rows and generate dependencies
        for index, row in self._excel_informationflows.iterrows():
            self._generate_dependencies_application_application(row)

    def generate_era_classes(self):
        self._load_applications_file()
        self._load_technologies_file()
        self._load_informationflows_file()

    def _generate_application(self, row):
        # only append the applications object, if a object with this id does not exist
        if not row['Xeam_ID'] in self.applications.keys():
            # set all properties
            self.applications[row['Xeam_ID']] = Application(id=row['Xeam_ID'], name=row['Name'])
            self.applications[row['Xeam_ID']].description = row['Beschreibung']
            self.applications[row['Xeam_ID']].protection_requirements = row['Schutzbedarf']
            self.applications[row['Xeam_ID']].responsible_system = row['Systemverantwortlicher']
            self.applications[row['Xeam_ID']].department_responsible_system = row['Abteilung Systemverantwortlicher']
            self.applications[row['Xeam_ID']].responsible_business = row['Fachlicher_Ansprechpartner']
            self.applications[row['Xeam_ID']].department_responsible_business = row['Abteilung Fachlicher_Ansprechpartner']
            self.applications[row['Xeam_ID']].start_date = row['Start_Datum']
            self.applications[row['Xeam_ID']].vendor = row['Hersteller']
            self.applications[row['Xeam_ID']].operator = row['Betrieb']
            self.applications[row['Xeam_ID']].total_user = row['Benutzer']
            self.applications[row['Xeam_ID']].availability_requirements = row['Verfuegbarkeit']
            self.applications[row['Xeam_ID']].integrity_requirements = row['Integritaet']
            self.applications[row['Xeam_ID']].confidentiality_requirements = row['Vertraulichkeit']

    def _generate_process(self, row):
        # only append the process object, if a object with this id does not exist
        if not row['Prozess_ID'] in self.processes.keys():
            # set all properties
            self.processes[row['Prozess_ID']] = Process(id=row['Prozess_ID'], name=row['Prozess'])
            self.processes[row['Prozess_ID']].responsible = row['ProzessVerantwortlich']
            self.processes[row['Prozess_ID']].protection_requirements = row['Schutzbedarf_Prozess']

    def _generate_dependencies_process_application(self, row):
        # only append the dependency to the process object, if it does not exist yet
        if not row['Xeam_ID'] in self.processes[row['Prozess_ID']].dependent_on_applications.keys():
            # build the dictionary with relevant information about the impact score
            dict_impact_score = {'Impact Score': row['Impact Score Applikation zu Prozess'], 'Rater':
                row['Bewerter Impact Score'], 'Criticality': row['Criticality'], 'Non-substitutability':
                                     row['Non-substitutability'], 'Indegree Centrality': row['Indegree Centrality'],
                                 'Outdegree Centrality':
                                     row['Outdegree Centrality'],
                                 'Impact on availability': row['Impact on availability'],
                                 'Impact on confidentiality': row['Impact on confidentiality'], 'Impact on integrity':
                                     row['Impact on integrity']}

            # assign the application id to the dependency list of the process object with the impact score data as dict
            self.processes[row['Prozess_ID']].dependent_on_applications[row['Xeam_ID']] = dict_impact_score

    def _generate_technology(self, row):
        # only append the technology object, if a object with this id does not exist
        if not row['Technologie_ID'] in self.technologies.keys():
            # set all properties
            self.technologies[row['Technologie_ID']] = Technology(id=row['Technologie_ID'],
                                                                  vendor=row['Technologie_Vendor'],
                                                                  product=row['Technologie_Product'],
                                                                  version=row['Technologie_Version'])

    def _generate_dependencies_application_technology(self, row):
        # only append the dependency to the application object, if it does not exist yet
        if not row['Technologie_ID'] in self.applications[row['Xeam_ID']].dependent_on_technologies.keys():
            # build the dictionary with relevant information about the impact score
            dict_impact_score = {'Impact Score': row['Impact Score Technologie zu Applikation'], 'Rater':
                row['Bewerter Impact Score'], 'Criticality': row['Criticality'], 'Non-substitutability':
                row['Non-substitutability'], 'Indegree Centrality': row['Indegree Centrality'],'Outdegree Centrality':
                row['Outdegree Centrality'], 'Impact on availability': row['Impact on availability'],
                'Impact on confidentiality': row['Impact on confidentiality'], 'Impact on integrity':
                row['Impact on integrity']}

            # assign the technology id to the dependency list of the appl. object with relevant impact score values
            self.applications[row['Xeam_ID']].dependent_on_technologies[row['Technologie_ID']] = dict_impact_score

    def _generate_dependencies_application_application(self, row):
        # only append the dependency to the application object, if it does not exist yet
        # dependencies to applications that don't exist in our concept are ignored
        if row['QUELLE_ID'] in self.applications.keys() and row['ZIEL_ID'] in self.applications.keys():

            # build the dictionary with relevant information about the impact score
            dict_impact_score = {'Impact Score': row['Impact Score Quelle Ziel'], 'Rater':
                row['Bewerter Impact Score'], 'Criticality': row['Criticality'], 'Non-substitutability':
                row['Non-substitutability'], 'Indegree Centrality': row['Indegree Centrality'], 'Outdegree Centrality':
                row['Outdegree Centrality'], 'Impact on availability': row['Impact on availability'],
                'Impact on confidentiality': row['Impact on confidentiality'], 'Impact on integrity':
                row['Impact on integrity']}

            # assign the application id to the dependency list of the appl. object with the impact score data as dict
            self.applications[row['ZIEL_ID']].dependent_on_applications[row['QUELLE_ID']] = dict_impact_score

    @property
    def processes(self) -> dict:
        return self._processes

    @processes.setter
    def processes(self, processes: dict):
        self._processes = processes

    @property
    def applications(self) -> dict:
        return self._applications

    @applications.setter
    def applications(self, applications: dict):
        self._applications = applications

    @property
    def technologies(self) -> dict:
        return self._technologies

    @technologies.setter
    def technologies(self, technologies: dict):
        self._technologies = technologies

