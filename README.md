Data Simulator
==============

This tool hlps to generate massive amount of random data that can be used for testing or various demos that require massive chunks of data.

Currrently it suports Random Data Generation to a CSV file. In Intger and float datatypes.
New feature to Support String datatype as well as pushing data to Cassandra will be added soon.

In order to run the generator a template xml file is requied that contains all details required by the generator.

A sample template is present in test\templatefiles\csv_random_sample_template.xml. 
This file contains all details you will need to configure and generate the output.

To run the Simulator you will need to go inside src folder and execute the main.py using the below command.
python main.py absolute path to congiguration template 

To execute the sample :
python main.py Absolute path/test/templatefiles/csv_random_sample_template.xml 
