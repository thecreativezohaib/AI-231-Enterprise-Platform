import json
from confluent_kafka import Consumer, KafkaError, KafkaException
from backend.core.database import redis_client
from backend.core.ml_models import anomaly_detector

conf = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'ingestion-group-1',
    'auto.offset.reset': 'earliest'
}

consumer = Consumer(conf)
TOPIC = 'infrastructure-telemetry'

def consume_loop():
    consumer.subscribe([TOPIC])
    print("Ingestion worker started, waiting for messages...")
    
    # Try to load existing model
    anomaly_detector.load()
    
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None: continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    raise KafkaException(msg.error())
            
            data = json.loads(msg.value().decode('utf-8'))
            asset_id = data['asset_id']
            features = [data['cpu_usage'], data['memory_usage'], data['temperature'], data['network_latency']]
            
            # Predict anomaly
            is_normal = anomaly_detector.predict(features)
            
            # Update health score in Redis
            current_health = redis_client.get(f"health:{asset_id}") if redis_client else None
            health = float(current_health) if current_health else 100.0
            
            if is_normal == -1:
                health = max(0.0, health - 5.0) # Penalty for anomaly
                print(f"ANOMALY DETECTED on {asset_id}. Health dropped to {health}")
            else:
                health = min(100.0, health + 0.5) # Recovery
                
            if redis_client:
                redis_client.set(f"health:{asset_id}", health)
            
    except KeyboardInterrupt:
        print("Ingestion worker stopped.")
    finally:
        consumer.close()

if __name__ == '__main__':
    consume_loop()
