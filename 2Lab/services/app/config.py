import os

table_name = 'odata'

# connection to DB
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
DBPORT = os.getenv('DBPORT')

DATABASE_NETWORK = os.getenv('DATABASE_NETWORK')

output_folder = '../output/'

profile_time_filename = 'profie_time.txt'
