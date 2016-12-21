Data Simulator
==============

This tool hlps to generate massive amount of random data that can be used for testing or various demos that require massive chunks of data.

# Demo

App Link : http://demo.serendio.com/bigsim

# Blog Post
Link : http://subhasisproject.blogspot.com/2015/10/data-simulation-tool-using-distributed.html


Currrently it suports Random Data Generation to a CSV file. In Intger and float datatypes.
New feature to Support String datatype as well as pushing data to Cassandra will be added soon.

In order to run the generator a template xml file is requied that contains all details required by the generator.

A sample template is present in test\templatefiles\csv_random_sample_template.xml. 
This file contains all details you will need to configure and generate the output.

To run the Simulator you will need to go inside src folder and execute the main.py using the below command.
python main.py absolute path to congiguration template 

To execute the sample :
python main.py Absolute path/test/templatefiles/csv_random_sample_template.xml 

Some of the important files are :
test/templatefiles/cassandra_random_sample_template.xml - This is the file that has to be given as input to the main.py file. this file will have all configuration deails. 
test/templatefiles/Cql_for_Cassandra_random_sample_template.cql - For the above template . The Data simulator code will assume that this table is created in the cassandra database.
src/datasimu/service/DataGenerator.py - This file takes care of making calls to different modules to validate the template(yet to do this), generating the data(currently it generates the Int and float data) and routing the generated data to the appropriate code that persists the data in the storage of choice.
src/datasimu/manager/CassandraManager.py - This file takes care of pushing the generated data to cassandra database. Current implementation will allow data to be pushed to only one table. And the table should have a primary key as id of type uuid.
src/datasimu/manager/CSVFileManager.py - This file takes care of pushing the data to csv file.
