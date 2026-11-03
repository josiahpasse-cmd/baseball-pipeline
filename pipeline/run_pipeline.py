from lib.create_tables import create_bronze_tables, create_layer_tables
from lib.download_retrosheet_files import download_retrosheet_data

# Download all files from Retrosheet
# First, set the target directory
TARGET_DIR = '/Volumes/workspace/baseball/baseball_raw/'
download_retrosheet_data(target_dir = TARGET_DIR)

# Create Bronze Tables
create_bronze_tables(target_dir = TARGET_DIR)

# Create Silver Tables
create_layer_tables(layer = 'silver', query_path = 'queries')

#Create Gold Tables
create_layer_tables(layer = 'gold', query_path = 'queries')