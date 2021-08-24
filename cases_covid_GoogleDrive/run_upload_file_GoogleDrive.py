from airflow.models import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime
from airflow.operators.python import PythonOperator


default_args = {'start_date': datetime(2021,7,12)}

with DAG('run_upload_GoogleDrive', schedule_interval='@daily', 
default_args=default_args, 
catchup = False, tags=['Cases Coronavirus Guatemala']) as dag:
    run_test = BashOperator(
        task_id = 'run_test',
        bash_command = 'echo "Load file Google Drive"'
    )
    run_py = BashOperator(
        task_id = 'run_py',
        bash_command = 'cd /home/juancacorps/Escritorio/selenium && source venv/bin/activate && python3 upload_file_GoogleDrive.py')
    

    run_test>>run_py
