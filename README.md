# HealthBud - Sports Injury Prediction System

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0.1-lightgrey)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)
![Kafka](https://img.shields.io/badge/Kafka-1.8.2-orange)
![scikit-learn](https://img.shields.io/badge/scikit--learn-0.24.2-green)

HealthBud is a comprehensive sports injury prediction system that leverages machine learning to predict potential injuries based on athlete data. The system uses a microservices architecture with Kafka for real-time data processing and Flask for the web interface.

## 🚀 Features

- Real-time injury prediction using machine learning models
- RESTful API endpoints for data management
- Kafka-based event streaming for data processing
- MySQL database for persistent storage
- Interactive web interface for data visualization
- Coach and athlete management system

## 📋 Prerequisites

- Python 3.8 or higher
- MySQL Server
- Apache Kafka
- Virtual environment (recommended)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/healthbud.git
cd healthbud
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
mysql -u your_username -p < coachdatabase.sql
```

5. Configure environment variables:
Create a `.env` file in the root directory with the following variables:
```
DB_HOST=localhost
DB_USER=your_username
DB_PASSWORD=your_password
DB_NAME=healthbud
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

## 🏃‍♂️ Running the Application

1. Start the Kafka consumer:
```bash
python kafka_consumer.py
```

2. Start the Flask application:
```bash
python flask_app.py
```

3. Start the Kafka producer (in a separate terminal):
```bash
python kafka_producer.py
```

The application will be available at `http://localhost:5000`


