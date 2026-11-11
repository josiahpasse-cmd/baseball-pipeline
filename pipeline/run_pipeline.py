from lib.create_tables import create_bronze_tables, create_layer_tables
from lib.download_retrosheet_files import download_retrosheet_data

# Download all files from Retrosheet
# First, set the target directory
TARGET_DIR = '/Volumes/workspace/baseball/baseball_raw/'
if download_retrosheet_data(target_dir = TARGET_DIR):
    print('Errors encountered downloading from Retrosheet. Quiting...')

# Create Bronze Tables
if create_bronze_tables(target_dir = TARGET_DIR):
    print('Errors encountered creating bronze tables. Quiting...')

# Create Silver Tables
if create_layer_tables(layer = 'silver', query_path = 'queries'):
    print('Errors encountered creating silver tables. Quiting...')

# Create Gold Tables
if create_layer_tables(layer = 'gold', query_path = 'queries'):
    print('Errors encountered creating gold tables. Quiting...')