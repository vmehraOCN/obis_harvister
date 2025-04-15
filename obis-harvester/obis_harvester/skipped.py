from dataclasses import dataclass

@dataclass
class SkippedSchema:
    """Class for keeping track of skipped csv creation"""
    url: str = None
    dataset_id: str = None
    reason_code: str = None

    def toIterable(self):
        return iter(
            [
                self.url,
                self.dataset_id,
                self.reason_code,
            ]
        )

@dataclass
class SkippedSchemaList:
    """Class of skipped schema list"""
    skipped_schema_list: list[SkippedSchema] = None

    def toHeader(self):
        return [
            "url",
            "dataset_id",
            "reason_code",
        ]

