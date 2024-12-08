import time
import requests

def measure_performance():
    url = "http://localhost:8080/product5"
    num_requests = 100

    start_time = time.time()
    for i in range(num_requests):
        response = requests.get(url)
        print(f"Request {i + 1}: Status {response.status_code}")
    end_time = time.time()

    total_time = end_time - start_time
    throughput = num_requests / total_time

    print(f"Total Time: {total_time:.2f} seconds")
    print(f"Throughput: {throughput:.2f} requests/second")

