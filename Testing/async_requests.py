import aiohttp
import asyncio

async def send_request(session, i, url):
    try:
        async with session.get(url) as response:
            print(f"Request {i + 1}: Status {response.status}")
    except Exception as e:
        print(f"Request {i + 1}: Failed with error {e}")

async def simulate_async_requests():
    url = "http://localhost:8080/product5"
    num_requests = 100

    async with aiohttp.ClientSession() as session:
        tasks = [send_request(session, i, url) for i in range(num_requests)]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(simulate_async_requests())

