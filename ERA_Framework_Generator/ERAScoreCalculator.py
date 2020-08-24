# imports
from ERA_Framework_Generator.Application import Application
import numpy as np
from ERA_Framework_Generator.Process import Process
from ERA_Framework_Generator.Technology import Technology


class ERAScoreCalculator:

    # Constructor
    def __init__(self, processes: dict, applications: dict,
                 technologies: dict, vulnerabilities: dict):
        self.in_degrees: dict[int, list] = {}
        self.processes = processes
        self.applications = applications
        self.technologies = technologies
        self.vulnerabilities = vulnerabilities
        # Multiplier for protection requirements
        self.MULTIPLIER = {'Standard': 1.0, 'High': 1.25, 'Very High': 1.5}
        # Maximum ERA Score
        self.MAXIMUM_ERA_SCORE = 10.0

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
        technology.impacting_asset_era_score = max_score

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
        # Initializing helper variables
        max_score = 0.0
        max_asset_id = ''
        max_asset_class = ''
        max_impact_score = 0.0
        max_impacting_era_score = 0.0

        # loop over technologies per application and define the ERA score according to highest Product of impact score
        # and ERA Score - start with the  technologies and loop afterwards over the "dependent on"-applications
        for tech in application.dependent_on_technologies.keys():
            calculated_era_score = self.technologies[tech].era_score * \
                                   application.dependent_on_technologies[tech] * \
                                   self.MULTIPLIER[application.protection_requirements]
            if self.technologies[tech].era_score * application.dependent_on_technologies[tech] > max_score:
                max_score = calculated_era_score
                max_asset_id = tech
                max_asset_class = 'Technology'
                max_impact_score = application.dependent_on_technologies[tech]
                max_impacting_era_score = self.technologies[tech].era_score

        # Same logic with loop over the "dependent on"-applications
        for app in application.dependent_on_applications.keys():
            calculated_era_score = self.applications[app].era_score * application.dependent_on_applications[app] * \
                                   self.MULTIPLIER[application.protection_requirements]
            if calculated_era_score > max_score:
                max_score = calculated_era_score
                max_asset_id = app
                max_asset_class = 'Application'
                max_impact_score = application.dependent_on_applications[app]
                max_impacting_era_score = self.applications[app].era_score

        # set the ERA Score and save the vulnerability that affected the era score (Maximum: 10.0)
        application.era_score = min(max_score, self.MAXIMUM_ERA_SCORE)
        application.impacting_asset_id = max_asset_id
        application.impacting_asset_era_score = max_impacting_era_score
        application.impacting_asset_class = max_asset_class
        application.impacting_asset_impact_score = max_impact_score

    def __calculate_affecting_vulnerabilities_application(self, application: Application):
        # save all the vulnerabilites that affect an application by its underlying technologies and applications
        for tech in application.dependent_on_technologies.keys():
            application.affecting_vulnerabilites.extend(self.technologies[tech].affecting_vulnerabilites)
        for app in application.dependent_on_applications.keys():
            application.affecting_vulnerabilites.extend(self.applications[app].affecting_vulnerabilites)

        # save the count of all affecting vulnerabilities (only unique values
        application.count_affecting_vulnerabilites = len(np.unique(application.affecting_vulnerabilites))

    def __calculate_era_score_process(self, process: Process):
        # Initializing helper variables
        max_score = 0.0
        max_asset_id = ''
        max_impact_score = 0.0
        max_impacting_era_score = 0.0

        # loop over applications per process and define the ERA score according to highest Product of impact score
        # and ERA Score multiplied with the "protection requirements" Mutliplier
        for app in process.dependent_on_applications.keys():
            calculated_era_score = self.applications[app].era_score * process.dependent_on_applications[app] * \
                                   self.MULTIPLIER[process.protection_requirements]
            if calculated_era_score > max_score:
                max_score = calculated_era_score
                max_asset_id = app
                max_impact_score = process.dependent_on_applications[app]
                max_impacting_era_score = self.applications[app].era_score

        # set the ERA Score and save the vulnerability that affected the era score (Maximum: 10.0)
        process.era_score = min(max_score, self.MAXIMUM_ERA_SCORE)
        process.impacting_asset_class = 'Application'
        process.impacting_asset_id = max_asset_id
        process.impacting_asset_era_score = max_impacting_era_score
        process.impacting_asset_impact_score = max_impact_score

    def __calculate_affecting_vulnerabilities_process(self, process: Process):
        # save all the vulnerabilites that affect a process by its underlying applications
        for app in process.dependent_on_applications.keys():
            process.affecting_vulnerabilites.extend(self.applications[app].affecting_vulnerabilites)

        # save the count of all affecting vulnerabilities (only unique values
        process.count_affecting_vulnerabilites = len(np.unique(process.affecting_vulnerabilites))

    def calculate_era_scores(self):
        # calculate the in-degrees of applications to determine the order to calculate ERA scores for applications
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


