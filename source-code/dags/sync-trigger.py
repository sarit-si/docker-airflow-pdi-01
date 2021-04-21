# To illustrate synchronous task triggers from Airflow container to PDI container

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator
from utils.execute_pdi import execute_trans

args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "wait_for_downstream": False,
    "catchup": False,
}


with DAG(
    dag_id="sync-trigger",
    default_args=args,
    schedule_interval=None,
    catchup=False,
    description=f"To illustrate synchronous task triggers from Airflow container to PDI container",
) as dag:

    t1 = DummyOperator(
        task_id='Start',
    )

    t2 = BashOperator(
        task_id='Task_1',
        bash_command=execute_trans(
            rep="test-repo",
            task="task1",
            dir="/process1/",
            param=""
        )
    )

    t3 = BashOperator(
        task_id='Task_2',
        bash_command=execute_trans(
            rep="test-repo",
            task="task2",
            dir="/process1/",
            param=""
        )
    )

    t4 = DummyOperator(
        task_id='Stop',
    )

    t1 >> t2 >> t3 >> t4