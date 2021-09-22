from airflow.models import DAG
import pathlib
import requests
import os
from airflow.operators import email_operator
from airflow.operators.python import PythonOperator
import json
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
        'start_date': datetime(2021,1,1),
        'email': ['juancacorps@gmail.com'],
        'email_on_failure': False,
        'email_on_retry': False}

with DAG("download_rocket_launches", default_args = default_args, catchup=False, schedule_interval='@daily',tags=['Rocket']) as dag:

    def _get_image_function():
        pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)
        path = '/tmp/launches.json'
        with open(path,'r', encoding='utf-8') as f:
            json_file = json.load(f)
        images_urls = [response["image"] for response in json_file["results"]]
        # Dowload image
        for url_image in images_urls:
            name_image = url_image.split('/')[-1]
            try:
                r = requests.get(url_image)
                if r.status_code == 200:
                    with open(f'/tmp/images/{name_image}','wb') as f:
                        f.write(r.content)
                    print(f'Download the image {name_image}')
            except Exception as e:
                print("*"*35)
                print(e)

    download_rocket_launches = BashOperator(
        task_id="download_rocket_launches",
        bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",
    )

    extract_image = PythonOperator(
        task_id = "extract_image",
        python_callable = _get_image_function,
    )

    email_success = email_operator.EmailOperator(
        task_id='email_success',
        to='juancacorps@gmail.com',
        subject='Download File Rocket',
        html_content="<h3> The images is success:) </h3>")

    download_rocket_launches>>extract_image>>email_success