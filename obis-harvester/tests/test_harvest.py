import pytest
import unittest
from unittest import mock
import json
from obis_harvester.harvest import CkanHarvestObis 

class TestHarvestObis:
    data = CkanHarvestObis(None)
    
    # would regualrly not need to load json file, instead use the inbuilt request 
    # in CkanHarvistObis.query_ckan_for_obis_data
    with open('test_data/ckan_search_data_obis.json', 'r') as file:
        data.raw_data = json.load(file)['result']
    
    print(data.raw_data.keys())
    
    # data.query_ckan_for_obis_data() # use this to initalize data.raw_data

    # keep this test
    def test_minimum_one_obis_record_in_ckan(self):
        print(self.data.raw_data)
        assert self.data.raw_data['count'] >= 1
    
    def test_assign_resource(self):
        val = self.data.assemble_extracted_data()

        # ckan section
        assert val.ckan_row.url is not None
        assert val.ckan_row.ckan_id is not None
        assert val.ckan_row.dataset_id is not None
        # assert we have an organization or is an empty list
        # this one needs a bit more thought as to how to verify it since requierments are loose
        assert val.ckan_row.ckan_organizations is not None
        # assert ckan title and fr title exist
        assert val.ckan_row.ckan_title is not None
        assert val.ckan_row.title_fr is not None

        # dataset section
        assert val.dataset_row.url is not None
        assert val.dataset_row.dataset_id is not None
        assert val.dataset_row.ckan_id is not None
        assert val.dataset_row.summary is not None
        assert val.dataset_row.summary_fr is not None
        assert val.dataset_row.cdm_data_type is not None

        # profile section
        assert val.profile_row.url is not None
        assert val.profile_row.dataset_id is not None

        # mixed section
        # assert url exists and is the same
        assert val.ckan_row.url == val.dataset_row.url == val.profile_row.url
        # assert ckan id exists and is the same
        assert val.ckan_row.ckan_id == val.dataset_row.ckan_id
        # assert profile dataset_id and is the same
        assert val.ckan_row.dataset_id == val.dataset_row.dataset_id == val.profile_row.dataset_id

    def test_extract_summary_en_fn(self):
        self.data.assemble_extracted_data()
        val = self.data.assemble_extracted_data()
        assert 1 == 0
        

        
