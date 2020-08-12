class ExcelParser:

    def __load_applications_file(self, path: str, file_name: str) -> list:
        """Load in the file for applications and processes and generate the objects."""
        pass

    def __load_technologies_file(self, full_file_name: str) -> list:
        """Load in the file for technologies and generate the technology objects."""
        pass

    def __load_informationflows_file(self) -> list:
        """Load in the file for information flows and generate the dependencies."""
        pass

    def generate_era_classes(self) -> list:
        """Callable method from outside to generate classes with Excel input"""
        pass


class BskExcelParser(ExcelParser):

    # Constructor
    def __init__(self, file_applications: str, file_technologies: str, file_informationflows: str):
        self.file_applications = file_applications
        self.file_technologies = file_technologies
        self.file_informationflows = file_informationflows

    def __load_applications_file(self):
        pass

    def __load_technologies_file(self):
        pass

    def __load_informationflows_file(self):
        pass

    def generate_era_classes(self):
        pass