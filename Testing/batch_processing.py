import schedule
import time

def batch_job():
    print("Batch processing started...")
    # Add code to process logs and update Cassandra tables
    print("Batch processing completed.")

def schedule_batch_job():
    schedule.every().day.at("20:00").do(batch_job)

    while True:
        schedule.run_pending()
        time.sleep(1)

