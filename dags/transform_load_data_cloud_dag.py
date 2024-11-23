from airflow import DAG
from airflow.providers.google.cloud.operators.dataproc import DataprocCreateClusterOperator, DataprocDeleteClusterOperator, DataprocSubmitJobOperator
from airflow.providers.google.cloud.transfers.gcs_to_gcs import GCSToGCSOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'start_date': days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define the DAG
with DAG(
    'dataproc_cluster_job_move_files',
    default_args=default_args,
    schedule_interval=timedelta(hours=7),  # Run every 7 hours
    catchup=False,
) as dag:

    # Task 1: Create a Dataproc cluster
    create_cluster = DataprocCreateClusterOperator(
        task_id="create_dataproc_cluster",
        project_id="dataengineering1-433721",
        cluster_name="crypto-etl-cluster",
        region="us-central1",
        cluster_config={
            "master_config": {
                "num_instances": 1,
                "machine_type_uri": "n1-standard-2"
            },
            "worker_config": {
                "num_instances": 2,
                "machine_type_uri": "n1-standard-2"
            },
        },
        gcp_conn_id="google_cloud_default",  # Added GCP connection
    )

    # Task 2: Submit a Spark job to the Dataproc cluster
    submit_job = DataprocSubmitJobOperator(
        task_id="submit_spark_job",
        job={
            'reference': {'project_id': 'dataengineering1-433721'},
            'placement': {'cluster_name': 'crypto-etl-cluster'},
            'pyspark_job': {
                'main_python_file_uri': 'gs://dataengineering1-433721_spark_files/dataproc_script/transform_load_data_proc_cloud.py',
                'jar_file_uris': [
                    'gs://dataengineering1-433721_spark_files/jars/gcs-connector-hadoop3-2.2.5.jar'
                ],
            },
        },
        region="us-central1",
        gcp_conn_id="google_cloud_default",  # Added GCP connection
    )

    # Task 3: Delete the Dataproc cluster
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_dataproc_cluster",
        project_id="dataengineering1-433721",
        cluster_name="crypto-etl-cluster",
        region="us-central1",
        trigger_rule="all_done",  # Ensure cluster is deleted even if the job fails
        gcp_conn_id="google_cloud_default",  # Added GCP connection
    )

     # Task 4: Move only JSON files from the processed folder to the archive folder
    move_files = GCSToGCSOperator(
        task_id="move_files_to_archive",
        source_bucket="dataengineering1-433721_crypto_data_raw",
        source_object="processed_files/*.json",  # Match only JSON files
        destination_bucket="dataengineering1-433721_crypto_data_archieve",
        destination_object="archieve_files/",
        move_object=True,  # Move instead of copying
        gcp_conn_id="google_cloud_default",  # Added GCP connection
    )


    # Define task dependencies
    create_cluster >> submit_job >> delete_cluster >> move_files
