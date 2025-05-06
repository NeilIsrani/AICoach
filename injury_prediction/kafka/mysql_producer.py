from kafka import KafkaProducer
import mysql.connector
import json
from datetime import datetime, timedelta
import time
from config import Config

class MySQLKafkaProducer:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        self.db_connection = mysql.connector.connect(
            host=Config.MYSQL_HOST,
            user=Config.MYSQL_USER,
            password=Config.MYSQL_PASSWORD,
            database='health'  # Updated database name
        )

    def fetch_fitness_data(self):
        cursor = self.db_connection.cursor(dictionary=True)
        query = """
            SELECT 
                fw.log_id,
                fw.user_id,
                fw.activity_date,
                fw.activity_minutes,
                fw.miles,
                fw.av_cadence,
                fw.av_speed,
                fw.exercise_strain,
                fw.sleep_hours,
                u.age,
                u.sex
            FROM fitness_watch fw
            JOIN users u ON fw.user_id = u.user_id
            ORDER BY fw.activity_date DESC
            LIMIT 1000
        """
        cursor.execute(query)
        return cursor.fetchall()

    def produce_to_kafka(self):
        while True:
            try:
                data = self.fetch_fitness_data()
                for record in data:
                    # Convert date to string for JSON serialization
                    record['activity_date'] = record['activity_date'].isoformat()
                    
                    # Send to raw data topic
                    self.producer.send('fitness_raw_data', value=record)
                    
                    # Calculate and send derived features
                    features = self.calculate_features(record)
                    self.producer.send('fitness_features', value=features)
                
                print(f"Produced {len(data)} records to Kafka")
                time.sleep(60)  # Wait for 1 minute before next batch
                
            except Exception as e:
                print(f"Error: {e}")
                time.sleep(5)

    def calculate_features(self, record):
        # Calculate derived features for injury prediction
        features = {
            'user_id': record['user_id'],
            'activity_date': record['activity_date'],
            'cadence_speed_ratio': record['av_cadence'] / record['av_speed'] if record['av_speed'] > 0 else 0,
            'strain': record['exercise_strain'],
            'activity_intensity': record['activity_minutes'] * record['av_speed'],
            'recovery_ratio': record['sleep_hours'] / record['activity_minutes'] if record['activity_minutes'] > 0 else 0,
            'age': record['age'],
            'sex': record['sex']
        }
        return features

if __name__ == "__main__":
    producer = MySQLKafkaProducer()
    producer.produce_to_kafka() 