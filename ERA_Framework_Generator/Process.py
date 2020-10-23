from ERA_Framework_Generator.Asset import Asset


class Process(Asset):

    # Constructor
    def __init__(self, id: str, name: str):
        super().__init__(id, name)
        self.responsible = ''
        self.dependent_on_applications: dict[int, dict] = {}   # save the Application ID and the impact score data

    # Definition of Getters and Setters
    @property
    def dependent_on_applications(self) -> dict:
        return self._dependent_on_applications

    @dependent_on_applications.setter
    def dependent_on_applications(self, dependent_on_applications: dict):
        self._dependent_on_applications = dependent_on_applications


