## NarrativeWave App
 
This application has two primary features:
1. Utilizes a REST API service to collect data from parquet files and provides the data in json 'record' format.
2. Consumes the REST API service and returns the json-formatted data in the browser.

Other features of the app include:
* Asset and column models with a one-asset-to-many-column  relation
* Page that shows all possible parquet queries

A function has also been developed in the 'read_csv_and_store_parquet.py' that uses PySpark to convert csv data into wide-formatted parquet files partitioned by asset, year, and month.

Pertaining to Django testing, Form, Model, and View tests have been developed and provide 100% coverage.

### Additional Files

Two files have been included in this repo that provide additional explanatory context to the Django app:

1. A Google Colaboratory notebook explaining the steps to process long-formatted csv files into wide-formatted partitioned parquet files.
2. A screen capture video where I walk through development and use of the app.

###### Credits

Developed by Stephen Utlak.

###### License

This software is available under the MIT license.
