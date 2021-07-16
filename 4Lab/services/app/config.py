import os
import glob

# year: filepath
datasets_files = '../data/dataset/Odata*.csv'
test_files = '../data/dataset/test*.csv'
datasets = dict((path[-12:-8], path) for path in glob.glob(
    # datasets_files
    # testing
    test_files
))
table_name = 'odata'

# connection to DB
MONGO_INITDB_DATABASE = os.getenv('MONGO_INITDB_DATABASE')

MONGO_INITDB_ROOT_USERNAME = os.getenv('MONGO_INITDB_ROOT_USERNAME')
MONGO_INITDB_ROOT_PASSWORD = os.getenv('MONGO_INITDB_ROOT_PASSWORD')

MONGODB_USER = os.getenv('MONGODB_USER')
MONGODB_PASS = os.getenv('MONGODB_PASS')

DBPORT = int(os.getenv('DBPORT'))

DATABASE_NETWORK = os.getenv('DATABASE_NETWORK')

output_folder = '../output/'

profile_time_filename = 'profie_time.txt'
