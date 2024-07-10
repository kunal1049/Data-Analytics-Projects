import os
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.contrib.operators.gcs_to_bq import GoogleCloudStorageToBigQueryOperator

# Custom Python logic for derriving data value
yesterday = datetime.combine(datetime.today() - timedelta(1), datetime.min.time())

# Default arguments
default_args = {
    'start_date': yesterday,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# DAG definitions
with DAG(dag_id='GCS_to_BQ_AND_AGG',
         catchup=False,
         schedule_interval=timedelta(days=1),
         default_args=default_args
         ) as dag:

# Dummy strat task   
    start = DummyOperator(
        task_id='start',
        dag=dag,
    )

# GCS to BigQuery data load Operator and task
    gcs_to_bq_load = GoogleCloudStorageToBigQueryOperator(
                task_id='gcs_to_bq_load',
                bucket='data_engineer_project',
                source_objects=['food_daily.csv'],
                destination_project_dataset_table='bigquery-project-420319.Dataset1.gcs_to_bq_table',
                schema_fields=[
                                {'name': 'Customer', 'type': 'STRING', 'mode': 'NULLABLE'},
                                {'name': 'date', 'type': 'STRING', 'mode': 'NULLABLE'},
                                {'name': 'time', 'type': 'STRING', 'mode': 'NULLABLE'},
                                {'name': 'order_id', 'type': 'STRING', 'mode': 'NULLABLE'},
                                {'name': 'items', 'type': 'STRING', 'mode': 'NULLABLE'},
                                {'name': 'amount', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                                {'name': 'mode', 'type': 'STRING', 'mode': 'NULLABLE'},
                                {'name': 'restaurnt', 'type': 'STRING', 'mode': 'NULLABLE'},
                                {'name': 'Status', 'type': 'STRING', 'mode': 'NULLABLE'},
                                {'name': 'rating', 'type': 'INTEGER', 'mode': 'NULLABLE'},
                                {'name': 'feedback', 'type': 'STRING', 'mode': 'NULLABLE'}
                              ],
                skip_leading_rows=1,
                create_disposition='CREATE_IF_NEEDED',
                write_disposition='WRITE_TRUNCATE', 
    dag=dag)

# BigQuery task, operator
    create_aggr_bq_table = BigQueryOperator(
    task_id='create_aggr_bq_table',
    use_legacy_sql=False,
    allow_large_results=True,
    sql="CREATE OR REPLACE TABLE Dataset1.bq_table_aggr AS \
         SELECT \
                date,\
                mode,\
                restaurnt,\
                Status\
         FROM bigquery-project-420319.Dataset1.gcs_to_bq_table\
            GROUP BY \
                date,\
                mode,\
                restaurnt,\
                Status", 
    dag=dag)

# Dummy end task
    end = DummyOperator(
        task_id='end',
        dag=dag,
    )

# Settting up task  dependency
start >> gcs_to_bq_load >> create_aggr_bq_table >> end