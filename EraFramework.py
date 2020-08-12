# ------- Program: ERA Framework ---------
# ------- Developed by: Tim Huse  --------
# ------- Date: 12.07.2020 ---------------

# imports tbd
from ExcelParser import BskExcelParser
from tkinter.filedialog import askopenfilename
from tkinter import Tk


# Main Function to calculate an ERA Model by importing EA Data via Excel Upload
def main():
    # ask for file upload of EA Data
    inputfiles = inputFileDialog()
    # parsing the Excel files into classes
    excel_parser = BskExcelParser(inputfiles[0], inputfiles[1], inputfiles[2])
    print(excel_parser.fileTechnologies)

    # TODO: Eingangsgrade/ Ausgangsgrade berechnen
    # TODO: Anbindung an CVSS API
    # TODO: Berechnung des ERA Scores
    # TODO: Aufbau des JSON Files


def inputFileDialog() -> list:
    Tk().withdraw()
    # TODO: uncomment filepicker and delete the static references
    # TODO: add exception handling for files (need to be .csv)
    fileApplications = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\SystemListe_Erweitert.csv"
    fileTechnologies = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\Technologieliste.csv"
    fileInformationflows = r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\Infoflussliste.csv"
    # fileApplications: str = askopenfilename(title="Please select an Excel File that contains your process and application data")
    # fileTechnologies: str = askopenfilename(title="Please select an Excel File that contains your technology data")
    # fileInformationflows: str = askopenfilename(title="Please select an Excel File that contains your information flow data")
    return [fileApplications, fileTechnologies, fileInformationflows]


if __name__ == '__main__':
    main()

