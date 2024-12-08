from kafka import KafkaConsumer
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import json
import uuid
from datetime import datetime

# Kafka configuration
KAFKA_BROKER = 'localhost:9094'
KAFKA_TOPIC = 'RAWLOG'
CONSUMER_GROUP_ID = 'result-consumer-group'  # Define a new consumer group for results

# Cassandra configuration
CASSANDRA_HOSTS = ['127.0.0.1']  # Replace with your Cassandra node IPs
CASSANDRA_KEYSPACE = 'logspace'

# Connect to Cassandra
cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect()
session.set_keyspace(CASSANDRA_KEYSPACE)

# Create the RESULTS table if it doesn’t exist
session.execute("""
CREATE TABLE IF NOT EXISTS RESULTS (
    id UUID PRIMARY KEY,
    batch_or_realtime TEXT,
    processed_data TEXT,
    source_ip TEXT,
    summary TEXT,
    timestamp TIMESTAMP
)
""")

# Connect to Kafka consumer
consumer = KafkaConsumer(
    KAFKA_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id=CONSUMER_GROUP_ID,  # Assign the consumer group
    auto_offset_reset='earliest',  # Start consuming from the earliest message
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))  # Deserialize JSON messages
)

print(f"Listening to Kafka topic: {KAFKA_TOPIC}")

# Process messages
for message in consumer:
    try:
        log_data = message.value  # The log message as a dictionary

        # Process log data for RESULTS table
        timestamp = datetime.utcnow()
        batch_or_realtime = "realtime"
        processed_data = f"Top N Pages Data"  # Placeholder for processed results
        source_ip = log_data.get('remote_addr', 'unknown')
        summary = f"Processed log from source IP {source_ip}"  # Example summary

        # Insert data into Cassandra RESULTS table
        session.execute("""
        INSERT INTO RESULTS (id, batch_or_realtime, processed_data, source_ip, summary, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (uuid.uuid4(), batch_or_realtime, processed_data, source_ip, summary, timestamp))

        # Print to the screen
        print(f"Inserted result: ID={uuid.uuid4()}, Processed Data={processed_data}, Source IP={source_ip}, Time={timestamp}")

    except Exception as e:
        print(f"Error processing message: {e}")

# Close the Cassandra session and Kafka consumer (optional)
cluster.shutdown()
consumer.close()

