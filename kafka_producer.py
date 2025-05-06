from kafka_config import get_producer, LEADERBOARD_TOPIC
import json
import database

def send_weekly_leaderboard(week_start_date):
    try:
        # Get weekly leaderboard data
        query = """
            SELECT 
                u.user_id,
                u.username,
                wl.fitness_score,
                wl.total_exercise_minutes,
                wl.total_miles,
                wl.total_cad_speed_ratio,
                wl.total_sleep_hours,
                wl.ranking
            FROM weekly_leaderboard wl
            JOIN users u ON wl.user_id = u.user_id
            WHERE wl.week_start_date = %s
        """
        leaderboard_data = database.execute_query(query, (week_start_date,))
        
        # Convert to JSON and send to Kafka
        producer = get_producer()
        message = {
            'week_start_date': week_start_date,
            'leaderboard_data': leaderboard_data
        }
        
        producer.produce(
            LEADERBOARD_TOPIC,
            key=week_start_date.encode('utf-8'),
            value=json.dumps(message).encode('utf-8')
        )
        producer.flush()
        
        return True
    except Exception as e:
        print(f"Error sending leaderboard data to Kafka: {str(e)}")
        return False 