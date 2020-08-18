class Process:

    # Constructor
    def __init__(self, id: str, name: str):
        self.id = id
        self.name = name
        self.responsible = ''
        self.protection_requirements = ''

    # Definition of Getters and Setters
    @property
    def id(self) -> str:
        return self._id

    @id.setter
    def id(self, id: str):
        self._id = id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, name: str):
        self._name = name

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

