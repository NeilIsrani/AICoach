from kafka_config import get_consumer, LEADERBOARD_TOPIC, PREDICTION_TOPIC
import json
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os
import database

def get_weekly_strain_data(week_start_date):
    query = """
        SELECT 
            fw.user_id,
            u.username,
            fw.exercise_strain,
            fw.activity_minutes,
            fw.miles,
            fw.av_cadence,
            fw.av_speed,
            fw.sleep_hours
        FROM fitness_watch fw
        JOIN users u ON fw.user_id = u.user_id
        WHERE fw.activity_date >= %s 
        AND fw.activity_date < DATE_ADD(%s, INTERVAL 7 DAY)
    """
    return database.execute_query(query, (week_start_date, week_start_date))

def train_model(weekly_data):
    # Prepare features and target
    X = np.array([
        [
            data['activity_minutes'],
            data['miles'],
            data['av_cadence'],
            data['av_speed'],
            data['sleep_hours']
        ] for data in weekly_data
    ])
    
    # Use actual exercise_strain as target
    y = np.array([data['exercise_strain'] for data in weekly_data])
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Train model
    model = LinearRegression()
    model.fit(X_scaled, y)
    
    # Save model and scaler
    os.makedirs('models', exist_ok=True)
    joblib.dump(model, 'models/strain_predictor.joblib')
    joblib.dump(scaler, 'models/scaler.joblib')
    
    return model, scaler

def consume_leaderboard_data():
    consumer = get_consumer()
    consumer.subscribe([LEADERBOARD_TOPIC])
    
    try:
        while True:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue
            if msg.error():
                print(f"Consumer error: {msg.error()}")
                continue
            
            # Process message
            data = json.loads(msg.value().decode('utf-8'))
            week_start_date = data['week_start_date']
            
            # Get actual exercise strain data for the week
            weekly_data = get_weekly_strain_data(week_start_date)
            
            if not weekly_data:
                print(f"No data found for week starting {week_start_date}")
                continue
            
            # Train model
            model, scaler = train_model(weekly_data)
            
            # Calculate predictions for each user
            predictions = []
            for user_data in weekly_data:
                features = np.array([
                    user_data['activity_minutes'],
                    user_data['miles'],
                    user_data['av_cadence'],
                    user_data['av_speed'],
                    user_data['sleep_hours']
                ]).reshape(1, -1)
                
                features_scaled = scaler.transform(features)
                predicted_strain = model.predict(features_scaled)[0]
                
                predictions.append({
                    'user_id': user_data['user_id'],
                    'username': user_data['username'],
                    'predicted_strain': float(predicted_strain),
                    'actual_strain': user_data['exercise_strain']
                })
            
            # Send predictions back to Kafka
            producer = get_producer()
            prediction_message = {
                'week_start_date': week_start_date,
                'predictions': predictions
            }
            
            producer.produce(
                PREDICTION_TOPIC,
                key=week_start_date.encode('utf-8'),
                value=json.dumps(prediction_message).encode('utf-8')
            )
            producer.flush()
            
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

if __name__ == '__main__':
    consume_leaderboard_data() 