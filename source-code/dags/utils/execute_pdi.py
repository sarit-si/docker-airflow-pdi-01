"""
Summary: This module contains helper functions required to build
        the Carte API URL trigger for PDI Jobs/ Transformations.
Params:
    - rep: PDI repository containing the job/trans; value must exist in the <name> tag of repositories.xml
    - task: job/trans file name present in the <rep> folder; do not include .ktr/.kjb extension
    - dir: '/' if job/trans file is in root directory inside <rep>. Else '/subfolder1/subfolder2/.../'. Do not include job/trans file name
    - param: pass parameters for the job/trans. Add '&' if multiple,ex: param1=value&param2=value
"""


def execute_command(executionType, task_type, rep, task, dir, param):

    command = "bash /opt/airflow/execute-carte.sh "
    command += f'''{task} "{executionType}/?rep={rep}&{task_type}={dir}{task}&{param}"'''

    return command

def execute_trans(rep, task, dir, param=''):
    """Summary: Build executeTrans Carte API URL

    Args:
        rep (string): [PDI repository containing the transformation .ktr file. Value must exist in the <name> tag of repositories.xml]
        task ([string]): [transformation file name present in the <rep> folder. Do not include .ktr extension]
        dir ([string]): ['/' if file is in root directory inside <rep>. Else '/subfolder1/subfolder2/.../'. Do not include file name]
        param ([string]): [If required to pass parameters to the transformation. Add '&' if multiple, ex: param1=value&param2=value]

    Returns:
        [string]: [Carte executeTrans API URL for the transformation]
    """

    command = execute_command(
        executionType="executeTrans", task_type="trans",
        rep=rep, task=task, dir=dir,param=param
    )

    return command

def execute_job(rep, task, dir, param=''):
    """Summary: Build executeJob Carte API URL

    Args:
        rep (string): [PDI repository containing the job .kjb file. Value must exist in the <name> tag of repositories.xml]
        task ([string]): [job file name present in the <rep> folder. Do not include .kjb extension]
        dir ([string]): ['/' if file is in root directory inside <rep>. Else '/subfolder1/subfolder2/.../'. Do not include file name]
        param ([string]): [If required to pass parameters to the job. Add '&' if multiple, ex: param1=value&param2=value]

    Returns:
        [string]: [Carte executeJob API URL for the job]
    """
    command = execute_command(
        executionType="executeJob", task_type="job",
        rep=rep, task=task, dir=dir,param=param
    )

    return command