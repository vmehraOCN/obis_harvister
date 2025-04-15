from dataclasses import dataclass

@dataclass
class DatasetsSchema:
    """Class for keeping track of datasets csv creation"""
    url: str = None
    dataset_id: str = None
    summary: str = None
    summary_fr: str = None
    cdm_data_type: str = ""
    platform: str = None
    eovs: str = None
    organizations: str = None
    nprofiles: str = None
    profile_variables: str = None
    timeseries_id_variable: str = None
    profile_id_variable: str = None
    trajectory_id_variable: str = None
    num_columns: str = None
    first_eov_column: str = None
    ckan_id: str = None
    title: str = None
    title_fr: str = None

    def toIterable(self):
        return iter(
            [
                self.url,
                self.dataset_id,
                self.summary,
                self.summary_fr,
                self.cdm_data_type,
                self.platform,
                self.eovs,
                self.organizations,
                self.nprofiles,
                self.profile_variables,
                self.timeseries_id_variable,
                self.profile_id_variable,
                self.trajectory_id_variable,
                self.num_columns,
                self.first_eov_column,
                self.ckan_id,
                self.title,
                self.title_fr,
            ]
        )

@dataclass
class DatasetsSchemaList:
    """Class of datasets schema list"""
    dataset_schema_list: list[DatasetsSchema] = None
    
    def toHeader(self):
        return [
            "url",
            "dataset_id",
            "summary",
            "summary_fr",
            "cdm_data_type",
            "platform",
            "eovs",
            "organizations",
            "nprofiles",
            "profile_variables",
            "timeseries_id_variable",
            "profile_id_variable",
            "trajectory_id_variable",
            "num_columns",
            "first_eov_column",
            "ckan_id",
            "title",
            "title_fr",
        ]

