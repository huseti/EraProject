from ERA_Framework_Generator.Asset import Asset


class Application(Asset):

    # Constructor
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.description = ''
        self.protection_requirements = ''
        self.responsible_system = ''
        self.department_responsible_system = ''
        self.responsible_business = ''
        self.department_responsible_business = ''
        self.start_date = ''
        self.vendor = ''
        self.operator = ''
        self.total_user = ''
        self.availability_requirements = ''
        self.integrity_requirements = ''
        self.confidentiality_requirements = ''
        self.dependent_on_technologies: dict[int, dict] = {}  # save the Technology ID and the impact score data
        self.dependent_on_applications: dict[int, dict] = {}  # save the Application ID and the impact score data

    # Definition of Getters and Setters
    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, description: str):
        self._description = description

    @property
    def responsible_system(self) -> str:
        return self._responsible_system

    @responsible_system.setter
    def responsible_system(self, responsible_system: str):
        self._responsible_system = responsible_system

    @property
    def department_responsible_system(self) -> str:
        return self._department_responsible_system

    @department_responsible_system.setter
    def department_responsible_system(self, department_responsible_system: str):
        self._department_responsible_system = department_responsible_system

    @property
    def responsible_business(self) -> str:
        return self._responsible_business

    @responsible_business.setter
    def responsible_business(self, responsible_business: str):
        self._responsible_business = responsible_business

    @property
    def department_responsible_business(self) -> str:
        return self._department_responsible_business

    @department_responsible_business.setter
    def department_responsible_business(self, department_responsible_business: str):
        self._department_responsible_business = department_responsible_business

    @property
    def start_date(self) -> str:
        return self._start_date

    @start_date.setter
    def start_date(self, start_date: str):
        self._start_date = start_date

    @property
    def vendor(self) -> str:
        return self._vendor

    @vendor.setter
    def vendor(self, vendor: str):
        self._vendor = vendor

    @property
    def operator(self) -> str:
        return self._operator

    @operator.setter
    def operator(self, operator: str):
        self._operator = operator

    @property
    def total_user(self) -> str:
        return self._total_user

    @total_user.setter
    def total_user(self, total_user: str):
        self._total_user = total_user

    @property
    def availability_requirements(self) -> str:
        return self._availability_requirements

    @availability_requirements.setter
    def availability_requirements(self, availability_requirements: str):
        self._availability_requirements = availability_requirements

    @property
    def integrity_requirements(self) -> str:
        return self._integrity_requirements

    @integrity_requirements.setter
    def integrity_requirements(self, integrity_requirements: str):
        self._integrity_requirements = integrity_requirements

    @property
    def confidentiality_requirements(self) -> str:
        return self._confidentiality_requirements

    @confidentiality_requirements.setter
    def confidentiality_requirements(self, confidentiality_requirements: str):
        self._confidentiality_requirements = confidentiality_requirements

    @property
    def dependent_on_technologies(self) -> dict:
        return self._dependent_on_technologies

    @dependent_on_technologies.setter
    def dependent_on_technologies(self, dependent_on_technologies: dict):
        self._dependent_on_technologies = dependent_on_technologies

    @property
    def dependent_on_applications(self) -> dict:
        return self._dependent_on_applications

    @dependent_on_applications.setter
    def dependent_on_applications(self, dependent_on_applications: dict):
        self._dependent_on_applications = dependent_on_applications

