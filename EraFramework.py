# ------- Program: ERA Framework ---------
# ------- Developed by: Tim Huse  --------
# ------- Date: 12.07.2020 ---------------

# TODO: Sort all Imports
# imports
from ExcelParser import BskExcelParser
from Process import Process
from Application import Application
from Technology import Technology
from Vulnerability import Vulnerability
from tkinter.filedialog import askopenfilename
from tkinter import Tk
import pandas as pd


# Main Function to calculate an ERA Model by importing EA Data via Excel Upload
def main():
    # ask for file upload of EA Data
    inputfiles = input_file_dialog()
    # parsing the Excel files into process, application and technology classes
    excel_parser = BskExcelParser(inputfiles[0], inputfiles[1], inputfiles[2]).generate_era_classes()
    # excel_parser.generate_era_classes()

    # TODO: Excelklassen erstellen

    # TODO: Eingangsgrade/ Ausgangsgrade berechnen
    # TODO: Anbindung an CVSS API
    # TODO: Berechnung des ERA Scores
    # TODO: Aufbau des JSON Files


# ask for file upload of EA Data
def input_file_dialog() -> list:
    Tk().withdraw()
    # TODO: uncomment filepicker and delete the static references
    # TODO: add exception handling for files (need to be .csv)
    file_applications = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\SystemListe_Erweitert.csv"
    file_technologies = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\Technologieliste.csv"
    file_informationflows = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\Infoflussliste.csv"
    # file_applications: str = askopenfilename(title="Please select an Excel File that contains your process and application data")
    # fileTechnologies: str = askopenfilename(title="Please select an Excel File that contains your technology data")
    # fileInformationflows: str = askopenfilename(title="Please select an Excel File that contains your information flow data")
    return [file_applications, file_technologies, file_informationflows]


if __name__ == '__main__':
    main()

