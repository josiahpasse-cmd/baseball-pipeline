import os

# Load data into spark
def create_tables(target_dir: str) -> None:
    for file in os.listdir(target_dir):
        try:
            file_name = str(file.split('.')[0])
            df = spark.read.csv(os.path.join(target_dir, file), header=True, inferSchema=False)        
            df.write.format('delta').mode('append').saveAsTable(f'workspace.baseball.raw_{file_name}')
            print(f'Successfully loaded file {file}')
        except Exception as e:
            print(f'Error loading file {file}. Exception {e}')

if __name__ == '__main__':
    create_tables('/Volumes/workspace/baseball/baseball_raw/')