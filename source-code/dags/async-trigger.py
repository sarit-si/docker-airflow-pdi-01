# To illustrate asynchronous data processing triggers from Airflow container to PDI container

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy import DummyOperator

args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "depends_on_past": False,
    "wait_for_downstream": False,
    "catchup": False,
}


with DAG(
    dag_id="async-trigger",
    default_args=args,
    schedule_interval=None,
    catchup=False,
    description=f"To illustrate asynchronous task triggers from Airflow container to PDI container",
) as dag:

    t1 = DummyOperator(
        task_id='Start',
    )

    t2 = BashOperator(
        task_id='Task_1',
        bash_command='curl "${PDI_CONN_STR}/kettle/executeTrans/?rep=test-repo&d&trans=/process1/task1"'
    )

    t3 = BashOperator(
        task_id='Task_2',
        bash_command='curl "${PDI_CONN_STR}/kettle/executeTrans/?rep=test-repo&trans=/process1/task2"'
    )

    t4 = DummyOperator(
        task_id='Stop',
    )

    t1 >> t2 >> t3 >> t4