# ------- Program: ERA Framework ---------
# ------- Developed by: Tim Huse  --------
# ------- Date: 12.07.2020 ---------------

# TODO: Sort all Imports
# imports
from CVEConnector import NVDConnector
from ExcelParser import BskExcelParser
from Process import Process
from Application import Application
from Technology import Technology
from Vulnerability import Vulnerability
from tkinter.filedialog import askopenfilename
from tkinter import Tk


# Main Function to calculate an ERA Model by importing EA Data via Excel Upload
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

    # TODO: Berechnung des ERA Scores - erst Technologies, dann Apps (Logik mit Eingangsgraden), dann Prozesse
    # TODO: Aufbau des JSON Files -> JSON File abspeichern


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


if __name__ == '__main__':
    main()

