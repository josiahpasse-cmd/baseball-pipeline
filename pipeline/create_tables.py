import os
import pyspark.sql.functions as F

# Load data into spark
def create_tables(target_dir: str) -> None:
    for file in os.listdir(target_dir):
        df = spark.read.csv(os.path.join(target_dir, file), header=True, inferSchema=False)
        df.show(5)
        quit()

if __name__ == '__main__':
    create_tables('/Volumes/workspace/baseball/baseball_raw/')