from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

CONVERTER_SCRIPT = "/home/omer/Documents/Data_Engineer/projects/Wikipedia_Crawler/etl/converter.py"
EXTRACT_METADATA_SCRIPT = "/home/omer/Documents/Data_Engineer/projects/Wikipedia_Crawler/etl/extract_wikipedia_metadata.py"
MYSQL_JAR = "/home/omer/spark-jars/mysql-connector-java-8.0.28.jar"

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'depends_on_past': False
}

with DAG(
    "wikipedia_processing",
    default_args=default_args,
    schedule_interval="@daily",
    start_date=datetime(2024, 2, 10),
    catchup=False,
) as dag:

    convert_task = SparkSubmitOperator(
        task_id='convert_to_text',
        application=CONVERTER_SCRIPT,
        conn_id='spark_default',
        conf={
            'spark.master': 'local[*]',  # Move master here
            'spark.driver.memory': '2g',
            'spark.executor.memory': '2g',
            'spark.hadoop.fs.defaultFS': 'hdfs://localhost:9000'
        }
    )

    metadata_task = SparkSubmitOperator(
        task_id='extract_metadata',
        application=EXTRACT_METADATA_SCRIPT,
        conn_id='spark_default',
        conf={
            'spark.master': 'local[*]',  # Move master here
            'spark.driver.memory': '2g',
            'spark.executor.memory': '2g'
        },
        jars=MYSQL_JAR
    )

    [convert_task, metadata_task]
