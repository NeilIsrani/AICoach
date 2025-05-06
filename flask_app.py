from flask import Flask, render_template, request, jsonify, redirect, url_for
import database
from datetime import datetime
from kafka_producer import send_weekly_leaderboard

app = Flask(__name__)
app.config.from_object('config.Config')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'POST':
        first_name = request.form['first_name']
        age = int(request.form['age'])
        sex = request.form['sex']
        username = request.form['username']
        
        query = """
            INSERT INTO users (first_name, age, sex, username) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            database.execute_query(query, (first_name, age, sex, username))
            return redirect(url_for('users'))
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    query = "SELECT * FROM users"
    users = database.execute_query(query)
    return render_template('users.html', users=users)

@app.route('/fitness-logs', methods=['GET', 'POST'])
def fitness_logs():
    if request.method == 'POST':
        try:
            user_id = int(request.form['user_id'])
            activity_date = datetime.strptime(request.form['activity_date'], '%Y-%m-%d').date()
            activity_minutes = int(request.form['activity_minutes'])
            miles = float(request.form['miles'])
            av_cadence = float(request.form['av_cadence'])
            av_speed = float(request.form['av_speed'])
            exercise_strain = float(request.form['exercise_strain'])
            sleep_hours = float(request.form['sleep_hours'])
            
            query = """
                INSERT INTO fitness_watch (
                    user_id, activity_date, activity_minutes, miles, 
                    av_cadence, av_speed, exercise_strain, sleep_hours
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            database.execute_query(query, (
                user_id, activity_date, activity_minutes, miles,
                av_cadence, av_speed, exercise_strain, sleep_hours
            ))
            
            # Update weekly leaderboard
            database.call_stored_procedure('update_weekly_leaderboard', (activity_date,))
            
            # Send leaderboard data to Kafka for model training
            week_start_date = activity_date.strftime('%Y-%m-%d')
            send_weekly_leaderboard(week_start_date)
            
            return redirect(url_for('fitness_logs'))
            
        except ValueError as e:
            return jsonify({'error': f'Invalid input format: {str(e)}'}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    query = """
        SELECT fw.*, u.username 
        FROM fitness_watch fw
        JOIN users u ON fw.user_id = u.user_id
        ORDER BY fw.activity_date DESC
    """
    logs = database.execute_query(query)
    return render_template('fitness_logs.html', logs=logs)

@app.route('/weekly-leaderboard')
def weekly_leaderboard():
    try:
        week_start_date = request.args.get('week_start_date')
        if not week_start_date:
            week_start_date = datetime.now().strftime('%Y-%m-%d')
        
        query = """
            SELECT 
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
            ORDER BY wl.ranking
        """
        results = database.execute_query(query, (week_start_date,))
        return render_template('leaderboard.html', 
                             leaderboard=results, 
                             week_start_date=week_start_date)
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True) 