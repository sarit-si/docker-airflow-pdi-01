# To illustrate how we can trigger a job/transformation in the PDI container via Carte APIs
# Reference: https://help.pentaho.com/Documentation/9.1/Developer_center/REST_API_Reference/Carte

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
    dag_id="load-testing",
    default_args=args,
    schedule_interval=None,
    catchup=False,
    description=f"Run multiple tasks in parallel for load testing",
) as dag:

    start = DummyOperator(
        task_id='Start',
    )

    t1 = BashOperator(
        task_id='Trigger_Job1',
        bash_command='curl "${PDI_CONN_STR}/kettle/executeJob/?rep=test-repo&job=/helloworld/helloworld-job"'
    )

    t2 = BashOperator(
        task_id='Trigger_Job2',
        bash_command='curl "${PDI_CONN_STR}/kettle/executeJob/?rep=test-repo&job=/helloworld/helloworld-job"'
    )

    t3 = BashOperator(
        task_id='Trigger_Job3',
        bash_command='curl "${PDI_CONN_STR}/kettle/executeJob/?rep=test-repo&job=/helloworld/helloworld-job"'
    )

    t4 = BashOperator(
        task_id='Trigger_Transformation',
        bash_command='curl "${PDI_CONN_STR}/kettle/executeTrans/?rep=test-repo&trans=/helloworld/helloworld-trans"'
    )

    stop = DummyOperator(
        task_id='Stop',
    )

    start >> [t1, t2, t3, t4] >> stop