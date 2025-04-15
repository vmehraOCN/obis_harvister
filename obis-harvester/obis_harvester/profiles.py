from dataclasses import dataclass

@dataclass
class ProfilesSchema:
    """Class for keeping track of profiles csv creation"""
    url: str = None
    dataset_id: str = None
    timeseries_id: str = None
    profile_id: str = None
    latitude: str = None
    longitude: str = None
    depth_min: str = None
    depth_max: str = None
    time_min: str = None
    time_max: str = None
    n_records: str = None
    records_per_day: str = None

    def toIterable(self):
        return iter(
            [
                self.url,
                self.dataset_id,
                self.timeseries_id,
                self.profile_id,
                self.latitude,
                self.longitude,
                self.depth_min,
                self.depth_max,
                self.time_min,
                self.time_max,
                self.n_records,
                self.records_per_day,
            ]
        )

@dataclass
class ProfilesSchemaList:
    """Class of profiles schema list"""
    dataset_schema_list: list[ProfilesSchema] = None

    def toHeader(self):
        return [
            "url",
            "dataset_id",
            "self.ckan_id",
            "timeseries_id",
            "profile_id",
            "latitude",
            "longitude",
            "depth_min",
            "depth_max",
            "time_min",
            "time_max",
            "n_records",
            "records_per_day",
        ]

