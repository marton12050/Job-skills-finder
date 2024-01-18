from airflow.decorators import task
from airflow.models import Variable

def send_s3(data):
    import boto3
    import json
    from datetime import date

    s3 = boto3.client('s3')
    bucket_name = 'jsf-bucket'
    s3_file_name = f'linkedin-{date.today()}.json'
    json_string = json.dumps(data)

    # Upload the file
    try:
        s3.put_object(Bucket=bucket_name, Key=s3_file_name, Body=json_string)
        print("Upload Successful")
    except Exception as e:
        print("Error uploading: ", e)

@task(task_id="collect_producer")
def produce():
    import requests
    from dotenv import load_dotenv
    import os
    from kafka import KafkaProducer
    from json import dumps

    load_dotenv()
    SCRAPER_API = Variable.get('SCRAPER_API')
    SCRAPER_KEY = Variable.get('SCRAPER_KEY')

    url = f"https://{SCRAPER_API}/jobs"

    payload = {
        "title": " ",
        "location": "Budapest",
        "rows": 300,
        "publishedAt": "Past24Hours"
    }
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": SCRAPER_KEY,
        "X-RapidAPI-Host": SCRAPER_API
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        send_s3(response.json())
        producer = KafkaProducer(bootstrap_servers=['localhost:9092'],
                                value_serializer=lambda x: dumps(x).encode('utf-8'))
        for job in response.json():
            producer.send('job_post', value=job)
        producer.flush()
    else:
        print("Error occurred during API call")
