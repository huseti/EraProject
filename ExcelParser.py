# imports
import pandas as pd
from Process import Process
from Application import Application
from Technology import Technology
from Vulnerability import Vulnerability


class ExcelParser:

    def __load_applications_file(self, path: str, file_name: str):
        """Load in the file for applications and processes and generate the objects."""
        pass

    def __load_technologies_file(self, full_file_name: str):
        """Load in the file for technologies and generate the technology objects."""
        pass

    def __load_informationflows_file(self):
        """Load in the file for information flows and generate the dependencies."""
        pass

    def generate_era_classes(self):
        """Callable method from outside to generate classes with Excel input"""
        pass

    def __generate_processes(self, row):
        """Generate a process object for each excel line if the process does not exist yet"""
        pass

    def __generate_applications(self, row):
        """Generate a process object for each excel line if the process does not exist yet"""
        pass


class BskExcelParser(ExcelParser):

    # Constructor
    def __init__(self, file_applications: str, file_technologies: str, file_informationflows: str):
        self.file_applications = file_applications
        self.file_technologies = file_technologies
        self.file_informationflows = file_informationflows
        self.processes: list[Process] = []
        self.applications: list[Application] = []
        self.technologies: list[Technology] = []

    def __load_applications_file(self):
        # load the excel file
        self._excel_applications = pd.read_csv(filepath_or_buffer=self.file_applications, sep=';',
                                               encoding='unicode_escape')

        # loop over excel rows and generate the application and process objects
        for index, row in self._excel_applications.iterrows():
            self.__generate_processes(row)
            self.__generate_applications(row)
            # TODO: Generate the dependencies

        # TODO: Entfernen
        for x in self.processes:
            print(x.id)
            print(x.name)
            print(x.responsible)
            print(x.protection_requirements)
        print("")
        for x in self.applications:
            print(x.id)
            print(x.name)
            print(x.protection_requirements)
            print(x.responsible_system)



    def __load_technologies_file(self):
        pass

    def __load_informationflows_file(self):
        pass

    def __generate_applications(self, row):
        # only append the applications object, if a object with this id does not exist
        if not [x for x in self.applications if x.id == row['Xeam_ID']]:
            # set all properties
            self.applications.append(Process(id=row['Xeam_ID'], name=row['Name']))
            self.applications[-1].description = row['Beschreibung']
            self.applications[-1].protection_requirements = row['Schutzbedarf']
            self.applications[-1].responsible_system = row['Systemverantwortlicher']
            # TODO: Erweitern der Klasse

    def __generate_processes(self, row):
        # only append the process object, if a object with this id does not exist
        if not [x for x in self.processes if x.id == row['Prozess_ID']]:
            # set all properties
            self.processes.append(Process(id=row['Prozess_ID'], name=row['Prozess']))
            self.processes[-1].responsible = row['ProzessVerantwortlich']
            self.processes[-1].protection_requirements = row['Schutzbedarf_Prozess']

    def generate_era_classes(self):
        self.__load_applications_file()
        self.__load_technologies_file()
        self.__load_informationflows_file()
