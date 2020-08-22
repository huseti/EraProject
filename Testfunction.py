# imports
from Process import Process
from Application import Application
from Technology import Technology
from Vulnerability import Vulnerability
from ERAScoreCalculator import ERAScoreCalculator
from CVEConnector import NVDConnector
from ExcelParser import BskExcelParser
from ERAJsonParser import ERAJsonParser


def main():

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
    tech1 = Technology(1, 'Mozilla', 'Firefox', '66.0.2')
    tech1.dependent_on_vulnerabilities[vul1.id] = vul1.id
    tech2 = Technology(2, 'Adobe', 'Flash Player', '32.0.0.207')
    tech2.dependent_on_vulnerabilities[vul2.id] = vul2.id
    tech2.dependent_on_vulnerabilities[vul3.id] = vul3.id
    tech3 = Technology(3, 'Test', 'Testproduct', '3.4.2')
    tech3.dependent_on_vulnerabilities[vul4.id] = vul4.id

    # Generate Test Applications
    app1 = Application(1, 'Testanwendung')
    app1.protection_requirements = 'Standard'
    app1.dependent_on_technologies[1] = 0.75
    app1.dependent_on_technologies[2] = 0.5
    app2 = Application(2, 'Testanwendung2')
    app2.protection_requirements = 'Standard'
    app2.dependent_on_technologies[3] = 1
    app2.dependent_on_applications[1] = 0.5
    app3 = Application(3, 'Testanwendung3')
    app3.protection_requirements = 'High'
    app3.dependent_on_technologies[3] = 0.5

    # Generate Test Processes
    pro1 = Process(1, "TestprozessA")
    pro1.protection_requirements = 'Very High'
    pro1.dependent_on_applications[1] = 1.0
    pro1.dependent_on_applications[2] = 0.75
    pro2 = Process(2, "TestprozessB")
    pro2.dependent_on_applications[3] = 1.0
    pro2.protection_requirements = 'High'

    # fill objects in dictionaries
    v = {vul1.id: vul1, vul2.id: vul2, vul3.id: vul3, vul4.id: vul4}
    t = {tech1.id: tech1, tech2.id: tech2, tech3.id: tech3}
    a = {app2.id: app2, app1.id: app1, app3.id: app3}
    p = {pro1.id: pro1, pro2.id: pro2}

    era = ERAScoreCalculator(p, a, t, v)
    era.calculate_era_scores()
    print(era.in_degrees)
    print(era.applications[1].era_score)
    print(era.applications[1].impacting_asset_id)
    print(era.applications[1].affecting_vulnerabilites)
    print(era.applications[1].count_affecting_vulnerabilites)
    print(era.applications[2].era_score)
    print(era.applications[2].impacting_asset_id)
    print(era.applications[2].affecting_vulnerabilites)
    print(era.applications[2].count_affecting_vulnerabilites)
    print(era.applications[3].era_score)
    print(era.applications[3].impacting_asset_id)
    print(era.applications[3].impacting_asset_class)
    print(era.applications[3].affecting_vulnerabilites)
    print(era.applications[3].count_affecting_vulnerabilites)

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

    parser = ERAJsonParser(p, a, t, v)
    parser.save_era_model_to_json(r"C:\Users\thuse\Google Drive\Dokumente\Beruf\FU\4. Semester\Quellen\EAM Datensatz\Bearbeitet\"", 'Test.json')
    print(parser.json_file)


if __name__ == '__main__':
    main()
