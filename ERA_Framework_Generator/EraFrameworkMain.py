# ------- Program: ERA Framework ---------
# ------- Developed by: Tim Huse  --------
# ------- Date: 12.08.2020 ---------------

# imports
from datetime import datetime
import os
import timeit
from tkinter import Tk
from tkinter.filedialog import askopenfilename,asksaveasfilename
from ERA_Framework_Generator.Application import Application
from ERA_Framework_Generator.CVEConnector import NVDConnector
from ERA_Framework_Generator.ERAJsonParser import ERAJsonParser
from ERA_Framework_Generator.ERAScoreCalculator import ERAScoreCalculator
from ERA_Framework_Generator.ExcelParser import TestbankExcelParser
from ERA_Framework_Generator.Process import Process
from ERA_Framework_Generator.Technology import Technology
from ERA_Framework_Generator.Vulnerability import Vulnerability


class EraFrameworkMain:

    # Constructor
    def __init__(self):
        self.era_score_calculator: ERAScoreCalculator = None
        self.excel_parser: TestbankExcelParser = None
        self.json_parser: ERAJsonParser = None
        self.processes: dict[int, Process] = {}
        self.applications: dict[int, Application] = {}
        self.technologies: dict[int, Technology] = {}
        self.vulnerabilities: dict[str, Vulnerability] = {}
        self.input_files: dict = {}
        self.save_file: dict = {}
        self.start_time: float = 0.0
        self.stop_time: float = 0.0

    # Main Function to calculate an ERA Model by importing EA Data via Excel Upload and to save it to a JSON File
    def main(self):
        # ask for file upload of EA Data
        self.input_files = self.input_file_dialog()

        # ask for filepath to save ERA Model JSON
        self.save_file = self.save_file_dialog()

        # count the runtime of the program and give feedback to the console
        self.start_time = timeit.default_timer()
        print("Execution started - ERA Model is being generated")

        # parsing the Excel files into process, application and technology objects
        self.excel_parser = TestbankExcelParser(self.input_files['applications'], self.input_files['technologies'],
                                                self.input_files['infoflows'])
        self.excel_parser.generate_era_classes()

        # get the dictionaries of the Process, Application and Technology objects
        self.processes = self.excel_parser.processes
        self.applications = self.excel_parser.applications
        self.technologies = self.excel_parser.technologies

        # get the dictionary with all vulnerabilites objects from the CVE API
        self.vulnerabilities = NVDConnector().get_all_vulnerabilities_per_technology(self.technologies)
        # calculate the ERA Scores for each Asset and calculate the total number of affecting vulnerabilities per layer
        self.era_score_calculator = ERAScoreCalculator(self.processes, self.applications, self.technologies,
                                                       self.vulnerabilities)
        self.era_score_calculator.calculate_era_scores()

        # Save the ERA model to JSON
        self.json_parser = ERAJsonParser(self.processes, self.applications, self.technologies, self.vulnerabilities)
        self.json_parser.save_era_model_to_json(self.save_file["filepath"], self.save_file["filename"])

        # Generate a information message to the console
        print("\nERA Model was successful saved to: {}".format(self.save_file["filepath"] + self.save_file["filename"]))

        # count the runtime of the program and give feedback to the console
        self.stop_time = timeit.default_timer()
        print('Program took {:.2f} seconds to execute.'.format(self.stop_time - self.start_time))

    # ask for file upload of EA Data
    @staticmethod
    def input_file_dialog() -> dict:

        Tk().withdraw()
        # open file dialog to get the name and path for the Excel files with ERA Model data to read them in
        file_applications: str = askopenfilename(
            title="Please select an Excel File that contains your process and application data",
            filetypes=[("CSV files", "*.csv")])
        file_technologies: str = askopenfilename(
            title="Please select an Excel File that contains your technology data",
            filetypes=[("CSV files", "*.csv")])
        file_informationflows: str = askopenfilename(
            title="Please select an Excel File that contains your information flow data",
            filetypes=[("CSV files", "*.csv")])
        return {'applications': file_applications, 'technologies': file_technologies,
                'infoflows': file_informationflows}

    # ask for filepath to save ERA Model JSON
    @staticmethod
    def save_file_dialog() -> dict:

        # generate a initial file and directory
        date_obj = datetime.now()
        file_path = "C:/Users/thuse/Google Drive/Dokumente/Beruf/FU/4. Semester/Quellen/EAM Datensatz/Bearbeitet/"
        file_name = "ERA_Model_" + str(date_obj.year) + '_' + str(date_obj.month) + '_' + str(date_obj.day) + '.json'

        # save file dialog to get the name and path for the JSON ERA File
        filepath_json = asksaveasfilename(initialdir=file_path, initialfile=file_name,
                                          title="Please select a filepath to save the ERA Model as JSON file",
                                          filetypes=[("JSON files", "*.json")], defaultextension="*.json")

        # save the filepath and the filename individually
        file_path = os.path.split(filepath_json)[0]
        file_name = os.path.split(filepath_json)[1]

        return {'filename': file_name, 'filepath': file_path}


if __name__ == '__main__':
    EraFrameworkMain().main()
