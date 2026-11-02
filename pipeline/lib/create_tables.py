import os
from pyspark.sql import SparkSession

# Load data into spark
def create_bronze_tables(target_dir: str) -> None:
    # For each raw_data file, load it into bronze without any typing
    spark = SparkSession.builder.getOrCreate()
    errors = []
    for file in os.listdir(target_dir):
        try:
            file_name = str(file.split('.')[0])
            df = spark.read.csv(os.path.join(target_dir, file), header=True, inferSchema=False)        
            df.write.format('delta').mode('overwrite').saveAsTable(f'workspace.baseball.bronze_{file_name}')
            print(f'Successfully loaded table bronze_{file}!')
        except Exception as e:
            print(f'Error loading file {file}. Exception {e}')
            errors.append(e)
    if not errors:
        print('All bronze tables created!')
    else:
        print(f'{len(errors)} errors encountered when creating bronze tables.')

    print("\n" + "─" * 40)

def create_silver_tables(query_path: str) -> None:
    # For each query in the query_path, execute the query to create silver tables.
    spark = SparkSession.builder.getOrCreate()
    errors = []
    for file in os.listdir(query_path):
        file_name = str(file.split('.')[0])
        with open(os.path.join(query_path, file)) as query_file:
            query = query_file.read()
            try:
                df = spark.sql(query)
            except Exception as e:
                print(f'There was an error executing the query: {file}.')
                print(f'Skipping...')
                errors.append(e)
                continue
            try:
                df.write.format('delta').mode('overwrite').saveAsTable(f'workspace.baseball.{file_name}')
                print(f'Successfully created table {file_name}!')
            except Exception as e:
                print(f'There was an error creating table {file_name}.')
                print('Skipping...')
                errors.append(e)
                continue
    if not errors:
        print('All silver tables created!')
    else:
        print(f'{len(errors)} errors encountered when creating silver tables.')

    print("\n" + "─" * 40)