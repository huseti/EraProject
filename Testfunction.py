# imports
from Process import Process
from Application import Application
from Technology import Technology
from Vulnerability import Vulnerability
from ERAScoreCalculator import ERAScoreCalculator
from CVEConnector import NVDConnector
from ExcelParser import BskExcelParser
from ERAJsonParser import ERAJsonParser
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from datetime import datetime
import os
import timeit


def main():
    start = timeit.default_timer()

    # Generate Test Vulnerabilities
    vul1 = Vulnerability(id='CVE_1', name="Hacker")
    vul1.cvss_score = 8.9
    vul2 = Vulnerability(id='CVE_2', name="Hacker")
    vul2.cvss_score = 2.8
    vul3 = Vulnerability(id='CVE_3', name="Hacker")
    vul3.cvss_score = 5.2
    vul4 = Vulnerability(id='CVE_4', name="Hacker")
    vul4.cvss_score = 6.1

    # Generate Test Technologies
    tech1 = Technology(100, 'Mozilla', 'Firefox', '66.0.2')
    tech1.dependent_on_vulnerabilities[vul1.id] = vul1.id
    tech2 = Technology(200, 'Adobe', 'Flash Player', '32.0.0.207')
    tech2.dependent_on_vulnerabilities[vul2.id] = vul2.id
    tech2.dependent_on_vulnerabilities[vul3.id] = vul3.id
    tech3 = Technology(300, 'Test', 'Testproduct', '3.4.2')
    tech3.dependent_on_vulnerabilities[vul4.id] = vul4.id

    # Generate Test Applications
    app1 = Application(10, 'Testanwendung')
    app1.protection_requirements = 'Standard'
    app1.dependent_on_technologies[100] = 0.75
    app1.dependent_on_technologies[200] = 0.5
    app2 = Application(20, 'Testanwendung2')
    app2.protection_requirements = 'Standard'
    app2.dependent_on_technologies[300] = 1
    app2.dependent_on_applications[10] = 0.5
    app3 = Application(30, 'Testanwendung3')
    app3.protection_requirements = 'High'
    app3.dependent_on_technologies[300] = 0.5

    # Generate Test Processes
    pro1 = Process(1, "TestprozessA")
    pro1.protection_requirements = 'Very High'
    pro1.dependent_on_applications[10] = 1.0
    pro1.dependent_on_applications[20] = 0.75
    pro2 = Process(2, "TestprozessB")
    pro2.dependent_on_applications[30] = 1.0
    pro2.protection_requirements = 'High'

    # fill objects in dictionaries
    v = {vul1.id: vul1, vul2.id: vul2, vul3.id: vul3, vul4.id: vul4}
    t = {tech1.id: tech1, tech2.id: tech2, tech3.id: tech3}
    a = {app2.id: app2, app1.id: app1, app3.id: app3}
    p = {pro1.id: pro1, pro2.id: pro2}

    era = ERAScoreCalculator(p, a, t, v)
    era.calculate_era_scores()
    print(era.in_degrees)
    print(era.applications[10].era_score)
    print(era.applications[10].impacting_asset_id)
    print(era.applications[10].affecting_vulnerabilites)
    print(era.applications[10].count_affecting_vulnerabilites)
    print(era.applications[20].era_score)
    print(era.applications[20].impacting_asset_id)
    print(era.applications[20].affecting_vulnerabilites)
    print(era.applications[20].count_affecting_vulnerabilites)
    print(era.applications[30].era_score)
    print(era.applications[30].impacting_asset_id)
    print(era.applications[30].impacting_asset_class)
    print(era.applications[30].affecting_vulnerabilites)
    print(era.applications[30].count_affecting_vulnerabilites)

    print("-----------------------------------------------")
    print(era.processes[1].era_score)
    print(era.processes[1].impacting_asset_era_score)
    print(era.processes[1].impacting_asset_impact_score)
    print(era.processes[1].impacting_asset_class)
    print(era.processes[1].impacting_asset_id)
    print(era.processes[1].affecting_vulnerabilites)
    print(era.processes[1].count_affecting_vulnerabilites)
    print("-----------------------------------------------")
    print(era.processes[2].era_score)
    print(era.processes[2].impacting_asset_era_score)
    print(era.processes[2].impacting_asset_impact_score)
    print(era.processes[2].impacting_asset_class)
    print(era.processes[2].impacting_asset_id)
    print(era.processes[2].affecting_vulnerabilites)
    print(era.processes[2].count_affecting_vulnerabilites)

    save_file = save_file_dialog()

    parser = ERAJsonParser(p, a, t, v)
    parser.save_era_model_to_json(save_file["filepath"], save_file["filename"])
    print(parser.json_file)

    stop = timeit.default_timer()
    print('\nProgram took {:.2f} seconds to execute.'.format(stop-start))


def save_file_dialog() -> dict:
    Tk().withdraw()

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

