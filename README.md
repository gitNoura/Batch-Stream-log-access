# Real-time and Batch Access Log Processing Pipeline
<div align="center">
  <img src="https://github.com/user-attachments/assets/eadf39d5-9cac-4b5d-b973-09b6ef09f665" alt="Image Description">
</div>

## 📖 Project Overview
This project implements a scalable pipeline for processing web server access logs in both **real-time** and **batch** modes. The system identifies the **N most visited web pages** every **P minutes** and generates daily reports of the most accessed pages. The architecture includes Kafka, Cassandra, Filebeat, and Nginx, and the project was implemented on **Arch Linux** but can be adapted to other Linux distributions or operating systems.

---

## 🎯 Key Features
- **Real-Time Analytics**: Displays the top N most visited pages every P minutes.
- **Batch Processing**: Produces daily reports at 8 PM for the most accessed pages.
- **Customizable Parameters**: `N` (number of pages) and `P` (time interval) can be adjusted.
- **Scalability**: Configurable for multiple Kafka brokers and Nginx clusters.
- **Integration Testing**: JMeter simulates high-traffic environments.

---

## 📋 Prerequisites
Before starting, ensure the following tools are installed and configured on your preferred operating system:
- **JMeter**: For generating HTTP requests.
- **Apache Kafka**: Configured with multiple brokers.
- **Apache Cassandra**: As a NoSQL database.
- **Filebeat**: For log shipping from Nginx to Kafka.
- **Python**: Version 3.x with `kafka-python` and `cassandra-driver` packages.
- **Nginx**: Configured as a load balancer and web server.
  
The implementation was tested on **Arch Linux**, but any Linux distribution or other operating systems capable of running these tools can be used.

---

## 🚀 Installation and Deployment

## 1. Install Nginx
- Install **Nginx**:
  ```bash
  sudo pacman -S nginx
#### Configuration Files

We have provided the necessary configuration files for the Nginx load balancer and backend servers. Download them directly from this repository:

- [nginx.conf (Load Balancer Configuration)](nginx-configs/nginx.conf)
- [nginx-server1.conf (Backend Server 1 Configuration)](nginx-configs/nginx-server1.conf)
- [nginx-server2.conf (Backend Server 2 Configuration)](nginx-configs/nginx-server2.conf)

---

#### Apply the Configuration

1. **Place Configuration Files**:
   - Move the `nginx.conf` file to the default Nginx configuration directory:
     ```bash
     sudo mv /path/to/nginx.conf /etc/nginx/nginx.conf
     ```
   - Place the backend configuration files (`nginx-server1.conf` and `nginx-server2.conf`) in suitable directories, or reference them directly when starting the servers.

2. **Start Nginx Servers**:
   - Start the Nginx load balancer:
     ```bash
     sudo nginx -c /etc/nginx/nginx.conf
     ```
   - Start the backend servers using their respective configuration files:
     ```bash
     sudo nginx -c /path/to/nginx-server1.conf
     sudo nginx -c /path/to/nginx-server2.conf
     ```

---

#### Verify Load Balancer

1. **Test the Configuration**:
   - Check if the Nginx configuration is valid:
     ```bash
     sudo nginx -t
     ```

2. **Access the Load Balancer**:
   - Open a browser and navigate to `http://localhost:8080/`.
   - Test the product endpoints:
     - `/product1`
     - `/product2`
     - `/product3`
     - `/product4`
     - `/product5`

   Ensure the load balancer distributes requests to the appropriate backend servers.
   
<div align="center">
  <img src="https://github.com/user-attachments/assets/f18b3ca7-6126-4a50-b4af-08820ef620e1" alt="Image Description">
</div>

---

## 2. JMeter Installation and Configuration

#### Installation
1. **Download JMeter**:
   - Visit the official Apache JMeter website: [https://jmeter.apache.org/](https://jmeter.apache.org/).
   - Download the latest version of JMeter (binary archive).

2. **Extract and Set Up**:
   - Extract the downloaded archive:
     ```bash
     tar -xvzf apache-jmeter-X.X.X.tgz -C /path/to/destination
     ```
   - Navigate to the JMeter directory:
     ```bash
     cd /path/to/destination/apache-jmeter-X.X.X
     ```

3. **Run JMeter**:
   - Open JMeter in GUI mode:
     ```bash
     ./bin/jmeter
     ```

---

#### Configuring JMeter for the Project
To simulate HTTP requests to the Nginx load balancer, JMeter was configured to distribute traffic to the product endpoints with the following proportions:
- `/product1`: **50%**
- `/product2`: **25%**
- `/product3`: **15%**
- `/product4`: **8%**
- `/product5`: **2%**

##### Steps:
1. **Create a Test Plan**:
   - Open JMeter and create a new Test Plan.

2. **Add a Thread Group**:
   - Right-click on the Test Plan → Add → Threads (Users) → Thread Group.
   - Configure the thread group:
     - Set the number of threads (users).
     - Define the ramp-up period.
     - Specify the loop count (or set it to "forever" for continuous testing).

3. **Add an HTTP Request Sampler**:
   - Right-click on the Thread Group → Add → Sampler → HTTP Request.
   - Configure the HTTP Request:
     - Server Name: `localhost`
     - Port Number: `8080` (or the port of your load balancer)
     - Path: `/productX` (e.g., `/product1` for the first request)
   - Add multiple HTTP Request Samplers, each targeting a different product path (`/product1`, `/product2`, etc.).

4. **Set Traffic Distribution**:
   - For each HTTP Request, adjust the thread group or add a throughput controller to define the proportion of requests:
     - `/product1`: **50%**
     - `/product2`: **25%**
     - `/product3`: **15%**
     - `/product4`: **8%**
     - `/product5`: **2%**

5. **Add Listeners**:
   - To monitor the results, add listeners to the Test Plan:
     - Right-click on the Test Plan → Add → Listener → View Results Tree.
     - Add additional listeners like "Summary Report" or "Aggregate Report" for performance metrics.

---

#### Running the Test
1. Save the Test Plan.
2. Click the green **Start** button in the JMeter toolbar to run the test.
3. Monitor the traffic in the configured listeners to ensure the requests are distributed as expected.

---

#### Validation
Below is an attached screenshot of the successful JMeter test plan execution, showing the traffic distribution and results:

![Image](https://github.com/user-attachments/assets/0fef6ecd-058b-4fcf-b1ba-1eb1c9c60d86)

---

## 3. Kafka Cluster Setup

To handle log streaming, we configured a Kafka cluster with multiple brokers. Below are the steps to set up and validate the Kafka cluster.

---

### Installation
1. **Download Kafka**:
   - Visit the official Apache Kafka website: [https://kafka.apache.org/](https://kafka.apache.org/).
   - Download the latest binary version.

2. **Extract and Set Up**:
   - Extract the downloaded archive:
     ```bash
     tar -xvzf kafka_2.X-X.tgz -C /path/to/destination
     ```
   - Navigate to the Kafka directory:
     ```bash
     cd /path/to/destination/kafka_2.X-X
     ```

---

### Configuring the Kafka Cluster
1. **Start Zookeeper**:
   Kafka requires Zookeeper to manage cluster metadata.
   ```bash
   bin/zookeeper-server-start.sh config/zookeeper.properties
### 2. Set Up Kafka Brokers

To set up multiple brokers in the Kafka cluster, follow these steps:

1. **Copy the Default Configuration File**:
   Copy the `server.properties` file to create separate configuration files for each broker:
   ```bash
   cp config/server.properties config/server1.properties
   cp config/server.properties config/server2.properties
   cp config/server.properties config/server3.properties
2. **Modify Configuration Files**:
   Update each configuration file to include a unique broker.id, port, and log directory:

- server1.properties:
  ```bash
  broker.id=1
  log.dirs=/tmp/kafka-logs-1
  port=9093
- server2.properties:
  ```bash
  broker.id=2
  log.dirs=/tmp/kafka-logs-2
  port=9094

- server3.properties:
  ```bash
  broker.id=3
  log.dirs=/tmp/kafka-logs-3
  port=9095

- And don't forget to create the logs:
![WhatsApp Image 2024-12-08 at 02 53 16_1492d977](https://github.com/user-attachments/assets/20d21793-98e5-4e8a-9f56-1a76303f8ee4)

### 3. **Creating and Managing Topics**:
  1. **Create the RAWLOG Topic: Create a topic for log streaming:**
     ```bash
      bin/kafka-topics.sh --create --topic RAWLOG --bootstrap-server localhost:9093 --partitions 3 --replication-factor 1
2. **List Available Topics: Verify that the topic has been created:**
   ```bash
    bin/kafka-topics.sh --list --bootstrap-server localhost:9093

### 4. **Testing the Kafka Cluster**
**Consume Messages:**
- Start a Kafka consumer to verify logs are being received on the RAWLOG topic (Fan-Out Mode):
  ```bash
    bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic RAWLOG --group group1 --from-beginning
    bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic RAWLOG --group group2 --from-beginning


![WhatsApp Image 2024-12-08 at 03 04 57_6cf1f125](https://github.com/user-attachments/assets/5a7a98b8-7f27-487f-a948-b6b2a4dece07)
--- 

## 4. Configure Streaming of Logs to Kafka (`RAWLOG` Topic) -Filebeat-

To enable streaming of Nginx logs to the Kafka topic `RAWLOG`, we integrated Nginx and Kafka using **Filebeat**. This section details the configuration and verification process.

### 1. Install and Configure Filebeat
Filebeat is used to ship Nginx logs to the Kafka broker.

1. **Install Filebeat**:
  Install Filebeat using your system's package manager. For example:
   ```bash
   sudo pacman -S filebeat
2. **Grant Permissions to Nginx Logs**:
  Filebeat needs read permissions on the Nginx log directory:
    ```bash
    sudo chmod -R 755 /var/log/nginx/
    sudo chown -R filebeat:filebeat /etc/filebeat
    
3. **Edit the Filebeat Configuration**:
  Update the Filebeat configuration file (typically located at /etc/filebeat/filebeat.yml) to forward logs to Kafka:
    ```bash
      filebeat.inputs:
        - type: log
          enabled: true
          paths:
            - /var/log/nginx/access.log
          fields:
            log_type: nginx_access 
      output.kafka:
        hosts: ["localhost:9093"]
        topic: "RAWLOG"
        partition.round_robin:
          reachable_only: false
        required_acks: 1
        compression: gzip

4. **Start Filebeat**:
 Start the Filebeat service and check its status:
    ```bash
      sudo systemctl start filebeat
      sudo systemctl status filebeat

![WhatsApp Image 2024-12-08 at 03 08 52_f4b3373b](https://github.com/user-attachments/assets/5ee78974-4c48-4370-8464-9e9237c56015)  

## 5. Kafka Stream
Kafka Streams was used to process the log data in real-time and produce insights such as the N most visited pages every P minutes. Below are the steps to set up and run the Kafka Streams application.

1. **Install Gradle**
Kafka Streams requires Gradle to build and manage the application.

 - Install Gradle:
     ```bash
     sudo pacman -S gradle
     ```   
 - Verify Installation: Ensure Gradle is installed correctly:
     ```bash
     gradle -v
     ```
2. **Initialize the Kafka Streams Project**
 - Navigate to the Kafka Directory:
     ```bash
     cd /opt/kafka
     ```
 - Create a Directory for the Kafka Streams Project:
     ```bash
     sudo mkdir /kafka_streams
     cd /kafka_streams
     ```
3. **Initialize a Gradle Project**:
     ```bash
     sudo gradle init
     ```
During the initialization process, you will be prompted to select options:

  - Select type of build to generate: 1 (Basic Gradle project).
  - Select implementation language: 1 (Java).
  - Enter target Java version: 11.
  - Project name: kafka_streams.
  - Select Application Structure: 1 (Single Application Project).
  - Select Build Script DSL: 1 (Kotlin).
  - Select Test Framework: 4 (JUnit Jupiter).
  - Generate build using new APIs and behavior? No.
4. **Build the Project**
     ```bash
     sudo gradle build
     ```

5. **Run the Kafka Streams Application**
   To run the application, use the following command with the desired parameters (N and P):
     ```bash
     sudo gradle run --args="3 5"
     ```
- 3: The number of top visited pages (N).
- 5: The interval in minutes (P).

![WhatsApp Image 2024-12-08 at 15 44 44_16e04bd2](https://github.com/user-attachments/assets/3ad73e32-0b19-4bfb-adf4-0479c25fb4ca)

## 6. Cassandra
### Installation Steps
1. **Download and Install Apache Cassandra**:
   - Visit the official [Cassandra Download Page](https://cassandra.apache.org/download/) to get the latest version.
   - Extract the downloaded archive:
     ```bash
     tar -xvzf apache-cassandra-<version>-bin.tar.gz
     cd apache-cassandra-<version>
     ```

2. **Add Cassandra to Your PATH**:
   - Export Cassandra's `bin` directory to your system's PATH:
     ```bash
     export PATH=$PATH:/path/to/apache-cassandra/bin
     ```
3. **Start Cassandra**:
   - Use the following command to start Cassandra:
     ```bash
     sudo bin/cassandra -R -f
     nodotool status #to check the status
     ```
![WhatsApp Image 2024-12-08 at 03 31 46_1f562641](https://github.com/user-attachments/assets/d542dbb0-96ab-4354-a64e-5d7f24d0530d)

4. **Deployement**:
   - Create a folder call it Kafka-cassandra-integration:
     ```bash
     cd /home/q/kafka-cassandra-integration
     ```
   - Create a Python Virtual Environment:
     ```bash
     python -m venv kafka-env
     ```
   - Activate the Python Environment:
     ```bash
     source kafka-env/bin/activate
     ```
   - Open Cassandra Query Language Shell (CQLSH):
      ```bash
      cqlsh
      ```
5. **Create the keyspace logspace**:
   - Create the keyspace logspace with SimpleStrategy and a replication factor of 1:
      ```bash
      CREATE KEYSPACE logspace WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1};
      ```
   - Use the created keyspace:
      ```bash
      USE logspace;
      ```   
6. **Table Definitions**:
 - **LOG Table**: This table stores raw log entries from the Nginx servers.
      ```bash
      CREATE TABLE LOG (
          id UUID PRIMARY KEY,
          timestamp TIMESTAMP,
          source_ip TEXT,
          request TEXT,
          status_code INT,
          user_agent TEXT,
          raw_message TEXT
      );
      ```   
  - **RESULTS Table**: This table stores the processed results from both batch and real-time pipelines.
      ```bash
      CREATE TABLE RESULTS (
          id UUID PRIMARY KEY,
          timestamp TIMESTAMP,
          batch_or_realtime TEXT,
          source_ip TEXT,
          processed_data TEXT,
          summary JSON
      );
      ```   
![WhatsApp Image 2024-12-08 at 14 59 49_a4f8cb95](https://github.com/user-attachments/assets/27371e27-1d25-42cb-82d3-720839e84e83)


## 7. Real-Time Writing Results to Cassandra (STREAM PROCESSING)

This step involves writing the processed results from the **Kafka Streams** application to the Cassandra database in real-time. A Python script is used to insert the data into the Cassandra `RESULTS` table.

## **1. Activate the Python Environment**
Ensure that the Python virtual environment used for Kafka and Cassandra integration is activated:

1. Navigate to the project directory and activate the virtual environment:
   ```bash
   cd
   pyenv global 3.11.6
   source kafka-env/bin/activate
   ```
2. Execute the script:
   Run the Python script to write the real-time processing results into the Cassandra RESULTS table:
   ```bash
   python write_results_to_cassandra.py
   ```
3. Testing the Results
   ```bash
   cqlsh
   ```
   - Query the RESULTS table to view the inserted data:
   ```bash
   SELECT * FROM logspace.RESULTS;
   ```
![WhatsApp Image 2024-12-08 at 15 48 54_1093bd66](https://github.com/user-attachments/assets/b5f713ce-1190-475d-9ea4-7e575467776f)

## 8. Batch Processing and Scheduling with Cron

This step involves configuring a **consumer pool in fan-out mode** to process logs in real-time and execute a **batch process** that analyzes the logs stored in the Cassandra `LOG` table. The batch program identifies the **N most visited pages** for the day and writes the results into the Cassandra `RESULTS` table. The batch process is scheduled to run daily at 8 PM using `cron`.

---

### **1. Configure a Consumer Pool in Fan-Out Mode**

To enable a fan-out architecture:
1. Start two Kafka consumers in **different consumer groups**:
   - **Consumer 1** writes raw logs to the Cassandra `LOG` table.
   - **Consumer 2** handles other real-time tasks or additional processing.

    - Start Consumer 1:
      ```bash
      bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic RAWLOG --group consumer-group-1
      ```
    - Start Consumer 2:
      ```bash
      bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic RAWLOG --group consumer-group-2
      ```
Each consumer group processes the same messages independently, achieving fan-out.

---

2. Batch Processing Program
A Python script, batch_process_logs.py, processes the Cassandra LOG table and writes results to the RESULTS table.

  - Navigate to the project directory and run the script:
    ```bash
    cd /home/q/kafka-cassandra-integration
    python batch_process_logs.py
    ```
  - Query Cassandra to validate results (in cqlsh):
    ```bash
    SELECT * FROM logspace.LOG;
    SELECT * FROM logspace.RESULTS;
    ```
    
3. Schedule the Batch Process Using Cron
To schedule the batch program to run daily at 8 PM:

  - Start and Enable Cron Service:
   ```bash
    sudo systemctl start cron
    sudo systemctl enable cron
    systemctl status cron
   ```
  - Edit the Crontab File: Open the crontab editor:
    ```bash
    crontab -e
    ```
  - Add the Scheduled Task: Add the following line to schedule the batch process:
    ```bash
    0 20 * * * /usr/bin/python3 /home/q/kafka-cassandra-integration/batch_process_logs.py >> /home/q/kafka-cassandra-integration/batch_process_logs.log 2>&1
    ```
Explanation:
   - 0 20 * * *: Runs the task daily at 8:00 PM.
   - /usr/bin/python3: Full path to the Python 3 executable.
   - /home/q/kafka-cassandra-integration/batch_process_logs.py: Full path to the script.
   - '>> /home/q/kafka-cassandra-integration/batch_process_logs.log': Redirects the output and errors to a log file for debugging.
  - Save and Exit: Save the crontab file and exit. The batch process will now run daily at the scheduled time.
    
4. Validation
After the scheduled time or manual execution, verify the results:

 - Check the LOG table in Cassandra:
   ```bash
   SELECT * FROM logspace.LOG;
   ```
 - Check the RESULTS table for batch processing results:
   ```bash
   SELECT * FROM logspace.RESULTS;
   ```
![WhatsApp Image 2024-12-08 at 16 27 11_d9a677d8](https://github.com/user-attachments/assets/a53f4629-9b0e-4f76-b73f-bad0278e841a)



+ and the batch one show the log table (cronie for sync)
+ finally the test thing (include the python files used)
+ the rest of screenshots + organize the files and add the scripts
