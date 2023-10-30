from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
#from airflow.providers.docker.operators.docker import DockerOperator


default_args = {
    'owner': 'Norman Ruiz',
    'retries':4,
    'retry_delay': timedelta(minutes = 2)
}

with DAG(
    default_args = default_args,
    dag_id = 'asteroides-etl-dag',
    description = 'Actualiza la tabla asteroides en Redshift',
    start_date = datetime(2023,6,1,2),
    schedule_interval = '@daily'
    ) as dag:
    
    task1 = BashOperator(
       task_id = 'asteroides-etl-task',
       bash_command = 'echo "Corrio !!!!"',
    )

    # task1 = DockerOperator(
    #     dag=dag,
    #     task_id='asteroides-etl-task',
    #     image='python:3.10-slim',
    #     container_name='asteroides-etl',
    #     auto_remove=True,
    #     docker_url='unix://var/run/docker.sock',
    #     network_mode='bridge'
    # )

task1

