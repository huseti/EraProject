# ------- Program: ERA Framework ---------
# ------- Developed by: Tim Huse  --------
# ------- Date: 12.08.2020 ---------------

# imports
from Application import Application
from CVEConnector import NVDConnector
from datetime import datetime
from ERAJsonParser import ERAJsonParser
from ERAScoreCalculator import ERAScoreCalculator
from ExcelParser import BskExcelParser
from Process import Process
from Technology import Technology
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from Vulnerability import Vulnerability


# Main Function to calculate an ERA Model by importing EA Data via Excel Upload and to save it to a JSON File
def main():
    # ask for file upload of EA Data
    input_files = input_file_dialog()

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

    # TODO: LÖSCHEN
    print(era_score_calculator.in_degrees)
    print(technologies[586000].era_score)
    print(technologies[586000].impacting_asset_era_score)
    print(technologies[586000].impacting_asset_impact_score)
    print(technologies[586000].impacting_asset_class)
    print(technologies[586000].impacting_asset_id)
    print(technologies[586000].affecting_vulnerabilites)
    print(technologies[586000].count_affecting_vulnerabilites)
    print('---------------------------------------------------')
    print(applications[11201].era_score)
    print(applications[11201].impacting_asset_era_score)
    print(applications[11201].impacting_asset_impact_score)
    print(applications[11201].impacting_asset_class)
    print(applications[11201].impacting_asset_id)
    print(applications[11201].affecting_vulnerabilites)
    print(applications[11201].count_affecting_vulnerabilites)
    print('---------------------------------------------------')
    print(processes[30001].era_score)
    print(processes[30001].impacting_asset_era_score)
    print(processes[30001].impacting_asset_impact_score)
    print(processes[30001].impacting_asset_class)
    print(processes[30001].impacting_asset_id)
    print(processes[30001].affecting_vulnerabilites)
    print(processes[30001].count_affecting_vulnerabilites)

    # ask for filepath to save ERA Model JSON
    save_file = save_file_dialog()

    # TODO: Aufbau des JSON Files -> JSON File abspeichern
    # Save the ERA model to JSON
    json_parser = ERAJsonParser(processes, applications, technologies, vulnerabilities)
    json_parser.save_era_model_to_json(filename=save_file["filename"], filepath=save_file["filepath"])


# ask for file upload of EA Data
def input_file_dialog() -> dict:
    Tk().withdraw()
    # TODO: uncomment filepicker and delete the static references
    # TODO: add exception handling for files (need to be .csv)
    file_applications = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\SystemListe_Erweitert.csv"
    file_technologies = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\Technologieliste.csv"
    file_informationflows = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\Infoflussliste.csv"
    # file_applications: str = askopenfilename(title="Please select an Excel File that contains your process and application data")
    # fileTechnologies: str = askopenfilename(title="Please select an Excel File that contains your technology data")
    # fileInformationflows: str = askopenfilename(title="Please select an Excel File that contains your information flow data")
    return {'applications': file_applications, 'technologies': file_technologies, 'infoflows': file_informationflows}


# ask for filepath to save ERA Model JSON
def save_file_dialog() -> dict:
    Tk().withdraw()
    # TODO: Speicherdialog entwickeln
    date_obj = datetime.now()
    file_path = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\""
    file_name = "ERA_Model_" + str(date_obj.year) + '_', str(date_obj.month) + '_' + str(date_obj.day)
    return {'filename': file_name, 'filepath': file_path}


if __name__ == '__main__':
    main()

