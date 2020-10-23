# ------- Program: ERA Framework ---------
# ------- Developed by: Tim Huse  --------
# ------- Date: 12.08.2020 ---------------

# imports
from ERA_Framework_Generator.Application import Application
from ERA_Framework_Generator.CVEConnector import NVDConnector
from datetime import datetime
from ERA_Framework_Generator.ERAJsonParser import ERAJsonParser
from ERA_Framework_Generator.ERAScoreCalculator import ERAScoreCalculator
from ERA_Framework_Generator.ExcelParser import BskExcelParser
import os
from ERA_Framework_Generator.Process import Process
from ERA_Framework_Generator.Technology import Technology
import timeit
from tkinter import Tk
from tkinter.filedialog import askopenfilename,asksaveasfilename
from ERA_Framework_Generator.Vulnerability import Vulnerability


# Main Function to calculate an ERA Model by importing EA Data via Excel Upload and to save it to a JSON File
def main():
    # ask for file upload of EA Data
    input_files = input_file_dialog()

    # ask for filepath to save ERA Model JSON
    save_file = save_file_dialog()

    # count the runtime of the program and give feedback to the console
    start_time = timeit.default_timer()
    print("Execution started - ERA Model is being generated")

    # parsing the Excel files into process, application and technology objects
    excel_parser = BskExcelParser(input_files['applications'], input_files['technologies'], input_files['infoflows'])
    excel_parser.generate_era_classes()

    # get the dictionaries of the Process, Application and Technology objects
    processes: dict[int, Process] = excel_parser.processes
    applications: dict[int, Application] = excel_parser.applications
    technologies: dict[int, Technology] = excel_parser.technologies

    # get the dictionary with all vulnerabilites objects from the CVE API
    vulnerabilities: dict[str, Vulnerability] = NVDConnector().get_all_vulnerabilities_per_technology(technologies)
    # calculate the ERA Scores for each Asset and calculate the total number of affecting vulnerabilities per layer
    era_score_calculator = ERAScoreCalculator(processes, applications, technologies, vulnerabilities)
    era_score_calculator.calculate_era_scores()

    # Save the ERA model to JSON
    json_parser = ERAJsonParser(processes, applications, technologies, vulnerabilities)
    json_parser.save_era_model_to_json(save_file["filepath"], save_file["filename"])

    # Generate a information message to the console
    print("\nERA Model was successful saved to: {}".format(save_file["filepath"] + save_file["filename"]))

    # count the runtime of the program and give feedback to the console
    stop_time = timeit.default_timer()
    print('Program took {:.2f} seconds to execute.'.format(stop_time - start_time))


# ask for file upload of EA Data
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
    return {'applications': file_applications, 'technologies': file_technologies, 'infoflows': file_informationflows}


# ask for filepath to save ERA Model JSON
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
    main()

