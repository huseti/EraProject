# imports
import collections
from Process import Process
from Application import Application
from Technology import Technology
from Vulnerability import Vulnerability


class ERAScoreCalculator:

    # Multiplier for protection requirements
    MULTIPLIER = {'Standard': 1.0, 'High': 1.25, 'Very High': 1.5}

    # Constructor
    def __init__(self, processes: dict, applications: dict,
                 technologies: dict, vulnerabilities: dict):
        self.in_degrees: dict[int, list] = {}
        self.processes = processes
        self.applications = applications
        self.technologies = technologies
        self.vulnerabilities = vulnerabilities

    def __calculate_era_score_technology(self, technology: Technology):
        max_score = 0.0
        max_asset_id = ''
        # loop over vulnerabilites per technology and define the ERA score according to the highest CVSS Score of vul.
        for vulnerability_id in technology.dependent_on_vulnerabilities.keys():
            if self.vulnerabilities[vulnerability_id].cvss_score > max_score:
                max_score = self.vulnerabilities[vulnerability_id].cvss_score
                max_asset_id = self.vulnerabilities[vulnerability_id].id

        # set the ERA Score and save the vulnerability that affected the era score
        technology.era_score = max_score
        technology.impacting_asset_class = 'Vulnerability'
        technology.impacting_asset_id = max_asset_id

    def __calculate_affecting_vulnerabilities_technology(self, technology: Technology):
        # save all the vulnerabilites that affect a technology
        technology.affecting_vulnerabilites = list(technology.dependent_on_vulnerabilities.keys())
        # save the count of all affecting vulnerabilities
        technology.count_affecting_vulnerabilites = len(technology.dependent_on_vulnerabilities)

    def __calculate_in_degree(self):
        # calculate the in degrees of applications (focusing on the dependencies from application to application)
        # this is needed to calculate the ERA Score of applications with a lower in degree first
        for app in self.applications.values():
            if not len(app.dependent_on_applications) in self.in_degrees:
                self.in_degrees[len(app.dependent_on_applications)] = [app.id]
            else:
                self.in_degrees[len(app.dependent_on_applications)] += [app.id]

    def __calculate_era_score_application(self, application: Application):
        # TODO: Berechnung des ERA Scores der Anwendungen
        pass

    def __calculate_affecting_vulnerabilities_application(self, application: Application):
        # TODO: Berechnung der totalen vulnerabilitäten der Anwendungen
        pass

    def __calculate_era_score_process(self, process: Process):
        # TODO: Berechnung des ERA Scores der Prozesse
        pass

    def __calculate_affecting_vulnerabilities_process(self, process: Process):
        # TODO: Berechnung der totalen vulnerabilitäten der prozesse
        pass

    def calculate_era_scores(self):
        # calculate the indegrees of applications to determine the order to calculate ERA scores for applications
        self.__calculate_in_degree()

        # calculate the era scores for each technology and calculate the total affecting vulnerabilities
        for technology in self.technologies.values():
            self.__calculate_era_score_technology(technology)
            self.__calculate_affecting_vulnerabilities_technology(technology)

        # calculate the era scores for each application - start with the lowest in-degree and
        # calculate total affecting vulnerabilities
        for in_degree in sorted(self.in_degrees.keys()):
            for application_id in self.in_degrees[in_degree]:
                self.__calculate_era_score_application(self.applications[application_id])
                self.__calculate_affecting_vulnerabilities_application(self.applications[application_id])

        # calculate the era scores for each process and calculate the total affecting vulnerabilities
        for process in self.processes.values():
            self.__calculate_era_score_process(process)
            self.__calculate_affecting_vulnerabilities_process(process)


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


if __name__ == '__main__':
    main()


