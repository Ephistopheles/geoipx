from enum import Enum

class OutputType(Enum):
    JSON = "json"
    XML = "xml"
    CSV = "csv"

    @property
    def output_extension(self):
        return {
            OutputType.JSON: ".json",
            OutputType.XML: ".xml",
            OutputType.CSV: ".csv"
        }[self]