This is to allow for harvesting OBIS data from CIOOS national catalog.

Workflow:
    1) query cioos national ckan for any obis tagged datasets
    2) break each result down to needed csv files to allow for db-loader to upload info into cde
        a) ckan.csv
        b) datasets.csv
        c) profiles.csv
        d) skipped.csv

This should plug output directly into db-loader for intigration into CDE.
