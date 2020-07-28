import os
from kafka import KafkaConsumer
from influxdb import InfluxDBClient
import json

KAFKA_TOPIC = os.environ.get('KAFKA_TOPIC') or print("KAFKA_TOPIC Not defined") 
KAFKA_SERVER = os.environ.get('KAFKA_SERVER') or print("KAFKA_SERVER Not defined")
INFLUXDB_SERVER = os.environ.get('INFLUXDB_SERVER') or print("INFLUXDB_SERVER Not defined")
print("KAFKA_TOPIC " + KAFKA_TOPIC)
print("KAFKA_SERVER " + KAFKA_SERVER)
print("INFLUXDB_SERVER" + INFLUXDB_SERVER)

client = InfluxDBClient(host=INFLUXDB_SERVER, port=8086)

if 'WeatherHistory' in str(client.get_list_database()):
    client.switch_database('WeatherHistory')
else:
    client.create_database('WeatherHistory')
    client.switch_database('WeatherHistory')

consumer = KafkaConsumer(
    KAFKA_TOPIC, 
    bootstrap_servers=KAFKA_SERVER,
    auto_offset_reset='earliest',
    enable_auto_commit=True,
    group_id='simple-consumers')

for msg in consumer:
    print (msg)
    data = json.loads(msg.value)
    value = [
        {"measurement":"weather",
            "tags": {
                        "Area": "Sweden",
                        "Location": "Tullinge"
                    },
            "fields":
            {
                    str(data['measurement']): float(data['value'])
            }       
        }
    ]
    client.write_points(value)
    print("Data written to DB")
    