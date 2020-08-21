class Asset:

    # Constructor
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name
        self.protection_requirements = 'Standard'
        self.era_score = 0.0
        self.impacting_asset_era_score = 0.0
        self.impacting_asset_impact_score = 0.0
        self.impacting_asset_class = ''
        self.impacting_asset_id = ''
        self.affecting_vulnerabilites = {}
        self.count_affecting_vulnerabilites = 0

    # ToString Method
    def __str__(self):
        return 'Asset {self.id}'.format(self=self)

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
    def era_score(self) -> float:
        return self._era_score

    @era_score.setter
    def era_score(self, era_score: float):
        self._era_score = era_score

    @property
    def impacting_asset_era_score(self) -> float:
        return self._impacting_asset_era_score

    @impacting_asset_era_score.setter
    def impacting_asset_era_score(self, impacting_asset_era_score: float):
        self._impacting_asset_era_score = impacting_asset_era_score

    @property
    def impacting_asset_impact_score(self) -> float:
        return self._impacting_asset_impact_score

    @impacting_asset_impact_score.setter
    def impacting_asset_impact_score(self, impacting_asset_impact_score: float):
        self._impacting_asset_impact_score = impacting_asset_impact_score

    @property
    def impacting_asset_class(self) -> str:
        return self._impacting_asset_class

    @impacting_asset_class.setter
    def impacting_asset_class(self, impacting_asset_class: str):
        self._impacting_asset_class = impacting_asset_class

    @property
    def impacting_asset_id(self) -> str:
        return self._impacting_asset_id

    @impacting_asset_id.setter
    def impacting_asset_id(self, impacting_asset_id: str):
        self._impacting_asset_id = impacting_asset_id

    @property
    def affecting_vulnerabilites(self) -> list:
        return self._affecting_vulnerabilites

    @affecting_vulnerabilites.setter
    def affecting_vulnerabilites(self, affecting_vulnerabilites: list):
        self._affecting_vulnerabilites = affecting_vulnerabilites

    @property
    def count_affecting_vulnerabilites(self) -> int:
        return self._count_affecting_vulnerabilites

    @count_affecting_vulnerabilites.setter
    def count_affecting_vulnerabilites(self, count_affecting_vulnerabilites: int):
        self._count_affecting_vulnerabilites = count_affecting_vulnerabilites

