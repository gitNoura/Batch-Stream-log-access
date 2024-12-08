from kafka import KafkaConsumer

def consume_logs():
    topic = "RAWLOG"  # Kafka topic for raw logs
    bootstrap_servers = ["localhost:9094"]  # Replace with your Kafka broker IP

    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=bootstrap_servers,
        auto_offset_reset="earliest",
        enable_auto_commit=True,
    )
    
    print(f"Consuming messages from topic: {topic}")
    log_count = 0  # Counter to track the number of messages processed
    max_logs = 5  # Maximum number of logs to print

    for message in consumer:
        print(f"Received message: {message.value.decode('utf-8')}")
        log_count += 1  # Increment the counter

        if log_count >= max_logs:  # Stop after printing 5 logs
            break

    #print(f"Consuming messages from topic: {topic}")
    #for message in consumer:
     #   print(f"Received message: {message.value.decode('utf-8')}")

consume_logs()

