from flask import Flask, request, jsonify, send_from_directory
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS
import database
from datetime import datetime
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # Enable CORS for all routes
api = Api(app)
app.config.from_object('config.Config')

# Serve static files
@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

# Request parsers with improved validation
user_parser = reqparse.RequestParser()
user_parser.add_argument('first_name', type=str, required=True, help='First name is required')
user_parser.add_argument('age', type=int, required=True, help='Age is required')
user_parser.add_argument('sex', type=str, required=True, choices=['M', 'F', 'O'], help='Sex must be M, F, or O')
user_parser.add_argument('username', type=str, required=True, help='Username is required')

fitness_log_parser = reqparse.RequestParser()
fitness_log_parser.add_argument('user_id', type=int, required=True, help='User ID is required')
fitness_log_parser.add_argument('activity_date', type=str, required=True, help='Activity date is required')
fitness_log_parser.add_argument('activity_minutes', type=int, required=True, help='Activity minutes is required')
fitness_log_parser.add_argument('miles', type=float, required=True, help='Miles is required')
fitness_log_parser.add_argument('av_cadence', type=float, required=True, help='Average cadence is required')
fitness_log_parser.add_argument('av_speed', type=float, required=True, help='Average speed is required')
fitness_log_parser.add_argument('exercise_strain', type=int, required=True, help='Exercise strain is required')
fitness_log_parser.add_argument('sleep_hours', type=float, required=True, help='Sleep hours is required')

competition_parser = reqparse.RequestParser()
competition_parser.add_argument('competition_date', type=str, required=True, help='Competition date is required')
competition_parser.add_argument('competition_location', type=str, required=True, help='Competition location is required')

# Resource Classes
class UserResource(Resource):
    def get(self, user_id=None):
        if user_id:
            query = "SELECT * FROM users WHERE user_id = %s"
            result = database.execute_query(query, (user_id,))
            if not result:
                abort(404, message=f"User with ID {user_id} not found")
            return result[0]
        else:
            query = "SELECT * FROM users"
            return database.execute_query(query)

    def post(self):
        args = user_parser.parse_args()
        query = """
            INSERT INTO users (first_name, age, sex, username) 
            VALUES (%s, %s, %s, %s)
        """
        try:
            database.execute_query(query, (args['first_name'], args['age'], args['sex'], args['username']))
            return {'message': 'User created successfully'}, 201
        except Exception as e:
            abort(400, message=str(e))

    def put(self, user_id):
        args = user_parser.parse_args()
        query = """
            UPDATE users 
            SET first_name = %s, age = %s, sex = %s, username = %s
            WHERE user_id = %s
        """
        try:
            result = database.execute_query(query, (args['first_name'], args['age'], args['sex'], args['username'], user_id))
            if not result:
                abort(404, message=f"User with ID {user_id} not found")
            return {'message': 'User updated successfully'}, 200
        except Exception as e:
            abort(400, message=str(e))

    def delete(self, user_id):
        query = "DELETE FROM users WHERE user_id = %s"
        try:
            result = database.execute_query(query, (user_id,))
            if not result:
                abort(404, message=f"User with ID {user_id} not found")
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            abort(400, message=str(e))

class FitnessLogResource(Resource):
    def get(self, log_id=None):
        if log_id:
            query = "SELECT * FROM fitness_watch WHERE log_id = %s"
            result = database.execute_query(query, (log_id,))
            if not result:
                abort(404, message=f"Fitness log with ID {log_id} not found")
            return result[0]
        else:
            query = "SELECT * FROM fitness_watch"
            return database.execute_query(query)

    def post(self):
        args = fitness_log_parser.parse_args()
        try:
            activity_date = datetime.strptime(args['activity_date'], '%Y-%m-%d').date()
            query = """
                INSERT INTO fitness_watch 
                (user_id, activity_date, activity_minutes, miles, av_cadence, av_speed, exercise_strain, sleep_hours) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            database.execute_query(query, (
                args['user_id'], 
                activity_date, 
                args['activity_minutes'],
                args['miles'],
                args['av_cadence'],
                args['av_speed'],
                args['exercise_strain'],
                args['sleep_hours']
            ))
            database.call_stored_procedure('update_weekly_leaderboard', (activity_date,))
            return {'message': 'Fitness log created successfully'}, 201
        except ValueError:
            abort(400, message="Invalid date format. Use YYYY-MM-DD")
        except Exception as e:
            abort(400, message=str(e))

    def delete(self, log_id):
        query = "DELETE FROM fitness_watch WHERE log_id = %s"
        try:
            result = database.execute_query(query, (log_id,))
            if not result:
                abort(404, message=f"Fitness log with ID {log_id} not found")
            return {'message': 'Fitness log deleted successfully'}, 200
        except Exception as e:
            abort(400, message=str(e))

class LeaderboardResource(Resource):
    def get(self):
        week_start_date = request.args.get('week_start_date')
        if not week_start_date:
            abort(400, message="Week start date is required")
        
        try:
            datetime.strptime(week_start_date, '%Y-%m-%d')
        except ValueError:
            abort(400, message="Invalid date format. Use YYYY-MM-DD")
        
        query = """
            SELECT 
                u.username, 
                wl.fitness_score, 
                wl.total_exercise_minutes, 
                wl.total_miles, 
                wl.total_cad_speed_ratio, 
                wl.total_sleep_hours,
                wl.days_yet
            FROM weekly_leaderboard wl
            JOIN users u ON wl.user_id = u.user_id
            WHERE wl.week_start_date = %s
            ORDER BY wl.fitness_score DESC
        """
        try:
            results = database.execute_query(query, (week_start_date,))
            return results
        except Exception as e:
            abort(400, message=str(e))

class PersonalReportResource(Resource):
    def get(self, user_id):
        week_start_date = request.args.get('week_start_date')
        if not week_start_date:
            abort(400, message="Week start date is required")
        
        try:
            datetime.strptime(week_start_date, '%Y-%m-%d')
        except ValueError:
            abort(400, message="Invalid date format. Use YYYY-MM-DD")
        
        query = """
            SELECT 
                AVG(f.activity_minutes) AS avg_activity_minutes,
                AVG(f.sleep_hours) AS avg_sleep_hours,
                AVG(f.av_cadence) AS avg_cadence,
                AVG(f.av_speed) AS avg_speed,
                AVG(f.exercise_strain) AS avg_strain,
                SUM(f.miles) AS total_miles,
                COUNT(DISTINCT f.activity_date) AS days_active
            FROM fitness_watch f
            WHERE f.user_id = %s AND f.activity_date >= %s
        """
        try:
            results = database.execute_query(query, (user_id, week_start_date))
            if results:
                return results[0]
            else:
                abort(404, message="No report available for the specified period")
        except Exception as e:
            abort(400, message=str(e))

# API Routes
api.add_resource(UserResource, '/api/users', '/api/users/<int:user_id>')
api.add_resource(FitnessLogResource, '/api/fitness-logs', '/api/fitness-logs/<int:log_id>')
api.add_resource(LeaderboardResource, '/api/leaderboard')
api.add_resource(PersonalReportResource, '/api/personal-report/<int:user_id>')

if __name__ == '__main__':
    print("Starting Flask server...")
    app.run(host='0.0.0.0', port=5000, debug=True) 