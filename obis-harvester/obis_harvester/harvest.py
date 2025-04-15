from dataclasses import dataclass
from obis_harvester.ckan import CkanSchemaList, CkanSchema
from obis_harvester.datasets import DatasetsSchemaList, DatasetsSchema
from obis_harvester.profiles import ProfilesSchemaList, ProfilesSchema
from obis_harvester.skipped import SkippedSchemaList, SkippedSchema
import requests
import json
import ast 

#Make dataclass for request results
@dataclass
class HarvestObisData:
    """Class for keeping track of CKAN csv creation"""
    ckan_list: CkanSchemaList = None
    dataset_list: DatasetsSchemaList = None
    profile_list: ProfilesSchemaList = None
    skipped_list: SkippedSchemaList = None

    def create_ckan_row(self, raw_data):
        pass
    def create_dataset_row(self, raw_data):
        pass
    def create_profiles_row(self, raw_data):
        pass
    def create_skipped_row(self, raw_data):
        pass

@dataclass
class HarvistObisRow:
    """Class for each singular row of csv data"""
    ckan_row: CkanSchema = None
    dataset_row: DatasetsSchema = None
    profile_row: ProfilesSchema = None
    skipped_row: SkippedSchema = None

    def _init(self):
        self.ckan_row = CkanSchema
        self.dataset_row = DatasetsSchema
        self.profile_row = ProfilesSchema
        self.skipped_row = SkippedSchema
        return self

    def extract_row_data(self, data):
        if type(data) == dict:
            self.extract_url(data)
            self.extract_ckan_id(data)
            self.extract_dataset_id(data)
            self.extract_organization(data)
            self.extract_title_en_fr(data)
            self.extract_summary_en_fr(data)
            self.extract_dataset_cdm_data_type(data)
        elif type(data) == list:
            for item in data:
                self.extract_row_data(item)
    
    def extract_url(self, item):
        url = item['url']
        #find contrary condition for skipped schema
        if url is not None and type(url) is str and 'obis' in url:
            self.ckan_row.url = url
            self.dataset_row.url = url
            self.profile_row.url = url
        else:
            pass
    
    def extract_ckan_id(self, item):
        ckan_id = item['id']
        if ckan_id is not None:
            self.ckan_row.ckan_id = ckan_id
            self.dataset_row.ckan_id = ckan_id

    def extract_dataset_id(self, item):
        if 'citation_en' in item.keys():
            _temp = item['citation_en']
            _temp =  _temp.replace("\"", "'")
            _temp =  _temp.replace("\\", "")
            _temp =  ast.literal_eval(_temp)
            _temp = self.find_obj_via_key(_temp, 'id')
            dataset_id = _temp.replace("ca.cioos_", "")
            self.ckan_row.dataset_id = dataset_id
            self.dataset_row.dataset_id = dataset_id
            self.profile_row.dataset_id = dataset_id
    
    def extract_organization(self, item):
        if 'organization_title' and 'organization_is_organization' in item.keys():
            if item['organization_is_organization']:
                self.ckan_row.ckan_organizations = item['organization_title']

    def extract_title_en_fr(self, item):
        if 'title_translated_en' and 'title_translated_fr' and 'dataset-reference-date' in item.keys():
            self.ckan_row.ckan_title = item['title_translated_en'] + ' ' + str(item['dataset-reference-date'][0]['value'])
            self.ckan_row.title_fr = item['title_translated_fr'] + ' ' + str(item['dataset-reference-date'][0]['value'])
    
    def extract_summary_en_fr(self, item):
        if 'notes_translated_en' and 'notes_translated_fr' in item.keys():
            self.dataset_row.summary = item['notes_translated_en']
            self.dataset_row.summary_fr = item['notes_translated_fr']
    
    def extract_dataset_cdm_data_type(self,item):
        if 'format' in item.keys() and item['format'] is not None:
            self.dataset_row.cdm_data_type += str(item['format'])

    def find_obj_via_key(self, obj, key):
        for item in obj:
            try:
                if key in item.keys():
                    return item[key]
                else:
                    self.find_obj_via_key(item, key)
            except KeyError:
                pass

@dataclass
class CkanHarvestObis:
    """Class for keeping track of all returned objects from Ckan query""" 
    #harvist_ckan_data: HarvestObisData = ([], [], [], [])
    #harvist_ckan_row: HarvistObisRow = (None, None, None, None)
    raw_data: json = None
    unpacked_data: list = None
    rows: int = 1000
    start: int = 0
    url: str = f'https://catalogue.cioos.ca/api/3/action/package_search?rows={rows}&start={start}&q=obis'
    obis_url: str = None

    #Request all obis data from national ckan
    def query_ckan_for_obis_data(self):
        request = requests.get(self.url)
        self.raw_data = request.json()['result']
    
    def assemble_extracted_data(self):
        self.unpacked_data = self.unpack_raw_data(self.raw_data)
        harvest_ckan_row = HarvistObisRow()._init()
        harvest_ckan_row.extract_row_data(self.unpacked_data)
        return harvest_ckan_row

    def unpack_raw_data(self, raw_data):
        val = None
        second_nested = None
        list_data = []

        for result in raw_data['results']:
            val = self.extract_nested_values(result)
            
            #the 'resources' key has a list of nested items and needs to further be flattened
            for item in val['resources']:
                second_nested = self.extract_nested_values(item)
                list_data.append(second_nested)
            break
            # for dev purposes, there is a break here to only have one value of the 32 used
            
        return([val, list_data])
    
    def extract_nested_values(self, itterable):
        flattened_dict = {}
        stack = [(itterable, '')]  # Stack holds tuples of (current_dict, current_key)

        while stack:
            c, p = stack.pop()

            for k, v in c.items():
                new_key = f"{p}_{k}" if p else k

                if isinstance(v, dict):
                    stack.append((v, new_key))  # Push the nested dictionary onto the stack
                else:
                    flattened_dict[new_key] = v  # Add to the flattened dictionary
        return flattened_dict

#Go through each item and break it up into chunks needed on csv


#Develop tests to ensure this is done correctly