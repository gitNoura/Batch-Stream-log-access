import requests
from concurrent.futures import ThreadPoolExecutor

def simulate_requests():
    # Configuration
    url = "http://localhost:8080/product5"  # Replace with your load balancer's IP/hostname
    num_threads = 10  # Number of concurrent threads
    requests_per_thread = 5  # Number of requests per thread

    def send_request(thread_id):
        for i in range(requests_per_thread):
            try:
                response = requests.get(url)
                print(f"Thread {thread_id}: Request {i + 1} - Status {response.status_code}")
            except Exception as e:
                print(f"Thread {thread_id}: Request {i + 1} - Failed with error {e}")

    # Simulate Traffic
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        executor.map(send_request, range(num_threads))

