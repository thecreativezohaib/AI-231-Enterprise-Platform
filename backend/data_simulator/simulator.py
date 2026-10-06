import json
import time
import random
from confluent_kafka import Producer

conf = {'bootstrap.servers': 'localhost:9092'}
producer = Producer(conf)

TOPIC = 'infrastructure-telemetry'

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        pass # print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def simulate_events():
    assets = [f'asset-{i:04d}' for i in range(1, 101)] # 100 assets
    print("Starting data simulator...")
    try:
        while True:
            asset = random.choice(assets)
            event = {
                "asset_id": asset,
                "timestamp": int(time.time()),
                "cpu_usage": random.uniform(10.0, 99.0),
                "memory_usage": random.uniform(10.0, 99.0),
                "temperature": random.uniform(30.0, 95.0),
                "network_latency": random.uniform(1.0, 500.0)
            }
            # Occasionally inject an anomaly
            if random.random() < 0.01:
                event["temperature"] = random.uniform(95.0, 120.0)
                event["network_latency"] = random.uniform(500.0, 2000.0)
            
            producer.produce(TOPIC, key=asset, value=json.dumps(event), callback=delivery_report)
            producer.poll(0)
            time.sleep(0.1) # 10 events per second
    except KeyboardInterrupt:
        print("Simulator stopped.")
    finally:
        producer.flush()

if __name__ == '__main__':
    simulate_events()
