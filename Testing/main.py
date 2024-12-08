from request_simulator import simulate_requests
from kafka_consumer import consume_logs
from performance_metrics import measure_performance

if __name__ == "__main__":
    # Step 1: Simulate Requests
    simulate_requests()

    # Step 2: Validate Kafka Log Streaming
    consume_logs()

    # Step 3: Measure Performance
    measure_performance()

