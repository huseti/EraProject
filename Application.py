class Application:

    # Constructor
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.description = ''
        self.protection_requirements = ''
        self.responsible_system = ''

    # Definition of Getters and Setters
    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, id: int):
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def name(self, description: str):
        self.description = description

    @property
    def protection_requirements(self) -> str:
        return self._protection_requirements

    # Mapping of Protection requirements
    @protection_requirements.setter
    def protection_requirements(self, protection_requirements: str):
        if protection_requirements == 'Standard':
            self._protection_requirements = 'Standard'
        elif protection_requirements == 'Hoch':
            self._protection_requirements = 'High'
        elif protection_requirements == 'High':
            self._protection_requirements = 'High'
        elif protection_requirements == 'Sehr Hoch':
            self._protection_requirements = 'Very High'
        elif protection_requirements == 'Very High':
            self._protection_requirements = 'Very High'

    @property
    def responsible_system(self) -> str:
        return self._responsible_system

    @responsible_system.setter
    def name(self, responsible_system: str):
        self.responsible_system = responsible_system

