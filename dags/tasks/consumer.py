from kafka import KafkaConsumer
from time import sleep
from json import dumps,loads
import json
from s3fs import S3FileSystem

#################################
####    unused arhitecture   ####
#################################

consumer = KafkaConsumer(
    's3_consumer',
     bootstrap_servers=[':9092'],
    value_deserializer=lambda x: loads(x.decode('utf-8')))

s3 = S3FileSystem()

for count, i in enumerate(consumer):
    # TODO unused arhitecture
    with s3.open("".format(count), 'w') as file:
        json.dump(i.value, file)   