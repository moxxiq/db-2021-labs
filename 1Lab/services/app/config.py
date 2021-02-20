import os
import glob

# year: filepath
datasets = dict((path[-12:-8], path) for path in glob.glob('../data/dataset/*.csv'))

# connection to DB
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DBPORT = os.getenv('DBPORT')

DATABASE_NETWORK = os.getenv('DATABASE_NETWORK')
