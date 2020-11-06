from ERA_Framework_Generator.Asset import Asset


class Technology(Asset):

    # Constructor
    def __init__(self, id: int, vendor: str, product: str, version: str):
        super().__init__(id, str(vendor) + ' ' + str(product))
        self.protection_requirements = 'Standard'
        self.vendor = vendor
        self.product = product
        self.version = version
        self.dependent_on_vulnerabilities: dict[str, str] = {}  # save the CVE ID as key and value
        self.impacting_asset_impact_score = 1.0

    # Definition of Getters and Setters
    @property
    def vendor(self) -> str:
        return self._vendor

    @vendor.setter
    def vendor(self, vendor: str):
        self._vendor = vendor

    @property
    def product(self) -> str:
        return self._product

    @product.setter
    def product(self, product: str):
        self._product = product

    @property
    def version(self) -> str:
        return self._version

    @version.setter
    def version(self, version: str):
        self._version = version

    @property
    def dependent_on_vulnerabilities(self) -> dict:
        return self._dependent_on_vulnerabilities

    @dependent_on_vulnerabilities.setter
    def dependent_on_vulnerabilities(self, dependent_on_vulnerabilities: dict):
        self._dependent_on_vulnerabilities = dependent_on_vulnerabilities





