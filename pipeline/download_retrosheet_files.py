import os
import io
import requests
from zipfile import ZipFile

BALLPARKS_URL = 'https://www.retrosheet.org/ballparks.zip'
GAMES_URL = 'https://retrosheet.org/downloads/gameinfo.zip'
BIOFILE_URL = 'https://www.retrosheet.org/biofile.zip'
BATTING_URL = 'https://retrosheet.org/downloads/batting.zip'
PITCHING_URL = 'https://retrosheet.org/downloads/pitching.zip'
FIELDING_URL = 'https://retrosheet.org/downloads/fielding.zip'

urls = [BALLPARKS_URL, GAMES_URL, BIOFILE_URL, BATTING_URL, PITCHING_URL, FIELDING_URL]

# Set the target directory
target_dir = '/Volumes/workspace/baseball/baseball_raw/'

for url in urls:
    try:
        # Retrieve data from Retrosheet
        response = requests.get(url)
        response.raise_for_status()
        print(f'Downloaded file {url}. Parsing data...')

        # Unzip response content to tempfile. Responses contain zipped files.
        content = response.content
        zipped = ZipFile(io.BytesIO(response.content))
        zipped.extractall(target_dir)
        print(f'Data Parsed Successful for {url}!')

    except requests.exceptions.HTTPError:
        print(f'Failed to download {url}. HTTP Error encountered. Status Code {response.status_code}')
    except Exception as e:
        print(f'Failed to download {url}. Exception {e}')
        raise

# List the files that were downloaded
print("Files Downloaded...")
for file in os.listdir(target_dir):
    print(f'  * {file}')


# Remove unneeded files
print("\n" + "─" * 40)
print("Cleaning up unneeded files...")

for file in os.listdir(target_dir):
    if file in ['coaches.csv', 'biofile0.csv', 'relatives.csv']:
        file_path = os.path.join(target_dir, file)
        os.remove(file_path)
        print(f'Removed unneeded file {file}')