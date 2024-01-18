from airflow.decorators import dag
from datetime import datetime
from tasks.producer import produce

@dag(
    dag_id="linkedin_job_collector_dag",
    start_date=datetime(2023, 1, 1),
    description="Collects jobs from LinkedIn",
    catchup=False,
    schedule='0 0 * * *',
    tags=["data"],
    max_active_runs=1,
    is_paused_upon_creation=False,
)
def linkedin_job_collector_dag():
    produce()

linkedin_job_collector_dag()