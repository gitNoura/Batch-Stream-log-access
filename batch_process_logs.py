from cassandra.cluster import Cluster
from datetime import datetime, timedelta
import uuid

# Cassandra configuration
CASSANDRA_HOSTS = ['127.0.0.1']  # Replace with your Cassandra node IPs
CASSANDRA_KEYSPACE = 'logspace'

# Connect to Cassandra
cluster = Cluster(CASSANDRA_HOSTS)
session = cluster.connect()
session.set_keyspace(CASSANDRA_KEYSPACE)

# Parameters
N = 5  # Top N pages
current_date = datetime.utcnow().date()  # Get today's date

# Query logs for the current day
query = """
SELECT request FROM LOG WHERE timestamp >= %s AND timestamp < %s ALLOW FILTERING
"""
start_time = datetime.combine(current_date, datetime.min.time())
end_time = start_time + timedelta(days=1)

print(f"Processing logs for {current_date}")

# Execute the query
rows = session.execute(query, (start_time, end_time))

# Count page visits
page_visits = {}
for row in rows:
    page = row.request
    if page in page_visits:
        page_visits[page] += 1
    else:
        page_visits[page] = 1

# Sort pages by visits and get the top N
sorted_pages = sorted(page_visits.items(), key=lambda x: x[1], reverse=True)
top_pages = sorted_pages[:N]

# Write results into the LOG table
timestamp = datetime.utcnow()
for page, visits in top_pages:
    source_ip = "batch-process"  # Example IP to identify batch results
    request = f"Page: {page}, Visits: {visits}"
    status_code = 200  # Example status code
    user_agent = "BatchProcessor/1.0"
    raw_message = f"Top {N} pages: {page}, Visits: {visits}"

    session.execute("""
    INSERT INTO LOG (id, raw_message, request, source_ip, status_code, timestamp, user_agent)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (uuid.uuid4(), raw_message, request, source_ip, status_code, timestamp, user_agent))

print(f"Batch process completed. Top {N} pages written back to LOG table.")

# Close Cassandra connection
cluster.shutdown()

