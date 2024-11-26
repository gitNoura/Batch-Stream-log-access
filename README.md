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

### 1. Install Necessary Tools
- Install **Nginx**:
  ```bash
  sudo pacman -S nginx
