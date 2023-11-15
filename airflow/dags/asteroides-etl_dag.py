from airflow.decorators import dag
from airflow.providers.docker.operators.docker import DockerOperator
from airflow.providers.amazon.aws.operators.redshift_sql import RedshiftSQLOperator
from airflow.operators.email_operator import EmailOperator
from datetime import datetime

@dag(start_date=datetime(2023,11,1), schedule_interval='@daily', catchup=False)

def asteroides_etl_dag():

    asteroides_etl = DockerOperator(
        task_id = 'asteroides_etl',
        image='asteroides-etl:latest',
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
    )

    validate_miss_distance_kilometers = RedshiftSQLOperator(
        task_id='validate_miss_distance_kilometers', 
        sql="""
                SELECT TOP 1 main.name
                FROM norman_ruiz_coderhouse.asteroides AS main
                WHERE main.miss_distance_kilometers < 5000000
                ORDER BY main.miss_distance_kilometers ASC;
            """,
        show_return_value_in_logs=True,
        do_xcom_push=True
    )

    enviar_mail_alerta = EmailOperator(
       task_id='enviar_mail_alerta',
       to='norman.ruiz@outlook.com.ar',
       subject='Alerta de asteroide',
       html_content=""" El asteriode llamado '{{ti.xcom_pull(task_ids=[\'validate_miss_distance_kilometers\'])}}' a superado la distancia de cautela y se encauntra a menos de 5.000.000 de kilometros de la tierra.""",
       )
    
    asteroides_etl >> validate_miss_distance_kilometers >> enviar_mail_alerta

dag = asteroides_etl_dag()
