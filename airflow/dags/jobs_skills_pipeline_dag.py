from datetime import datetime, timedelta
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.operators.dummy_operator import DummyOperator

# Define the default_args dictionary
default_args = {
    "owner": "marton",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


@dag(
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    default_args=default_args,
    catchup=False,
    description="Pipeline for jobs data and skills extraction",
)
def jobs_skill_pipeline():
    @task()
    def task_1():
        print("Executing task 1")

    @task()
    def task_2():
        print("Executing task 2")

    task_1 >> task_2


jobs_skill_pipeline()
