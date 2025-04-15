from dataclasses import dataclass

@dataclass
class CkanSchema:
    """Class for keeping track of CKAN csv creation"""
    url: str = None
    dataset_id: str = None
    ckan_id: str = None
    ckan_organizations: list[str] = None
    ckan_title: str = None
    title_fr: str = None

    def toIterable(self):
        return iter(
            [
                self.url,
                self.dataset_id,
                self.ckan_id,
                self.ckan_organizations,
                self.ckan_title,
                self.title_fr,
            ]
        )


@dataclass
class CkanSchemaList:
    """Class of ckan schema list"""
    ckan_schema_list: list[CkanSchema] = None

    def toHeader(self):
        return [
            "url",
            "dataset_id",
            "ckan_id",
            "ckan_organizations",
            "ckan_title",
            "title_fr",
        ]

