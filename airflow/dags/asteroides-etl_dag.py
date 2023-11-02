from airflow.decorators import task, dag
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.operators.bash import BashOperator
from datetime import datetime

@dag(start_date=datetime(2023,11,1), schedule_interval='@daily', catchup=False)

def asteroides_etl_dag():

    asteroides_etl_task = DockerOperator(
        task_id = 'asteroides_etl_task',
        image='asteroides-etl:latest',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        do_xcom_push=True,
    )
    
    asteroides_etl_task

dag = asteroides_etl_dag()