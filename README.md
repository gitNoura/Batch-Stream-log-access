# Real-time and Batch Access Log Processing Pipeline

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

### 3. **Creating and Managing Topics**:
  1. **Create the RAWLOG Topic: Create a topic for log streaming:**
     ```bash
      bin/kafka-topics.sh --create --topic RAWLOG --bootstrap-server localhost:9093 --partitions 3 --replication-factor 1
2. **List Available Topics: Verify that the topic has been created:**
   ```bash
    bin/kafka-topics.sh --list --bootstrap-server localhost:9093

### 4. **Testing the Kafka Cluster**
**Consume Messages:**
- Start a Kafka consumer to verify logs are being received on the RAWLOG topic:
  ```bash
    bin/kafka-console-consumer.sh --bootstrap-server localhost:9094 --topic RAWLOG --from-beginning
  
--- 

## 7. Configure Streaming of Logs to Kafka (`RAWLOG` Topic)

To enable streaming of Nginx logs to the Kafka topic `RAWLOG`, we integrated Nginx and Kafka using **Filebeat**. This section details the configuration and verification process.

---

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
    
## 2. Verify Log Streaming to Kafka

### Send Traffic Using JMeter
Use the configured JMeter test plan to simulate HTTP requests to Nginx. Ensure the requests are distributed across endpoints as specified:
```bash
./bin/jmeter
```
### Consume Logs from the Kafka Topic

Start a Kafka consumer to verify that logs are being received on the `RAWLOG` topic:

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9093 --topic RAWLOG --from-beginning
```
### Validate Log Format

The logs streamed from Nginx should appear in the console output. Verify that the logs are formatted correctly as per the Nginx `json_logs` format:

```json
{
    "time_local": "26/Nov/2024:15:42:01 +0000",
    "remote_addr": "192.168.1.1",
    "request": "GET /product1 HTTP/1.1",
    "status": "200",
    "body_bytes_sent": "512",
    "http_referer": "-",
    "http_user_agent": "Mozilla/5.0"
}

