import mysql.connector
from mysql.connector import Error
from getpass import getpass

# Connect to MySQL Database
def create_connection(username, password):
    """Establish connection to the MySQL database"""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user=username,
            password=password,
            database='coachdatabase' 
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"\nError: Unable to connect to database: {e}")
        return None

# Close the connection to the database
def close_connection(connection):
    if connection.is_connected():
        connection.close()
        print("MySQL connection is closed")

# Execute a query (create table, insert data, etc.)
def execute_query(connection, query, data=None):
    cursor = connection.cursor()
    try:
        if data:
            cursor.execute(query, data)
        else:
            cursor.execute(query)
        connection.commit()
    except Error as e:
        print("Error executing query", e)
    finally:
        cursor.close()

# Call stored procedure
def call_stored_procedure(connection, procedure_name, params=None):
    cursor = connection.cursor()
    try:
        if params:
            cursor.callproc(procedure_name, params)
        else:
            cursor.callproc(procedure_name)
        connection.commit()
    except Error as e:
        print("Error calling stored procedure", e)
    finally:
        cursor.close()

# Fetch data from a query
def fetch_query_results(connection, query, params=None):
    cursor = connection.cursor(dictionary=True)
    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        return cursor.fetchall()
    except Error as e:
        print("Error fetching query results", e)
    finally:
        cursor.close()


"""CREATE"""

# Insert a user
def insert_user(connection):
    first_name = input("Enter first name: ")
    age = int(input("Enter age: "))
    sex = input("Enter sex (Male/Female): ")
    username = input("Enter username: ")
    query = """
        INSERT INTO users (first_name, age, sex, username) 
        VALUES (%s, %s, %s, %s)
    """
    execute_query(connection, query, (first_name, age, sex, username))
    print("user created!")

# Insert fitness log
def insert_fitness_log(connection):
    user_id = int(input("Enter user ID: "))
    activity_date = input("Enter activity date (YYYY-MM-DD): ")
    activity_minutes = int(input("Enter activity minutes: "))
    sleep_hours = float(input("Enter sleep hours: "))
    query = """
        INSERT INTO fitness_watch (user_id, activity_date, activity_minutes, sleep_hours) 
        VALUES (%s, %s, %s, %s)
    """
    call_stored_procedure(connection, 'update_weekly_leaderboard', (activity_date,))
    execute_query(connection, query, (user_id, activity_date, activity_minutes, sleep_hours))
    print("fitness log created!")
# Call the stored procedure to assign rewards
def assign_rewards_for_week(connection):
    week_start_date = input("Enter week start date (YYYY-MM-DD): ")
    call_stored_procedure(connection, 'assign_rewards', (week_start_date,))
    print("reward created!")
# Create competition/ open applications
def create_competition(connection):
    comp_date = input("Enter competition date (YYYY-MM-DD): ")
    comp_location = input("Enter competition location: ")
    
    query = """
        INSERT INTO competition (competition_date, competition_location) 
        VALUES (%s, %s)
    """
    execute_query(connection, query, (comp_date, comp_location))
    print(f"Competition created on {comp_date} at {comp_location}.")
"""READ"""
# Fetch user metrics of average sleep and fitness for the week
def fetch_personal_report(connection, user_id, week_start_date):
    query = """
        SELECT 
            AVG(f.activity_minutes) AS avg_activity_minutes,
            AVG(f.sleep_hours) AS avg_sleep_hours
        FROM fitness_watch f
        WHERE f.user_id = %s AND f.activity_date >= %s
    """
    # OR call_stored_procedure(connection, 'personal_report', (week_start_date,))
    results = fetch_query_results(connection, query, (user_id, week_start_date))
    if results:
        return results[0]
    else:
        return "no report available"
    
# Weekly leaderboard- ranking of users on computer 'fitness score' 
def fetch_weekly_leaderboard(connection):
    week_start_date = input("Enter week start date (YYYY-MM-DD): ")
    query = """
        SELECT u.username, wl.fitness_score, wl.total_exercise_minutes, wl.total_sleep_hours, wl.ranking
        FROM weekly_leaderboard wl
        JOIN users u ON wl.user_id = u.user_id
        WHERE wl.week_start_date = %s
        ORDER BY wl.ranking
    """
    results = fetch_query_results(connection, query, (week_start_date,))
    for row in results:
        print(row)


# Fetch eligible users for a competition based on having reward points in the last 2 weeks 
def check_competition_eligibility(connection, competition_date):
    try:
        # Create a cursor 
        cursor = connection.cursor()
        cursor.callproc('check_competition_eligibility', [competition_date])

        # Fetch results from the procedure
        results_found = False
        for result in cursor.stored_results():
            rows = result.fetchall()
            if rows:
                results_found = True
                print(f"\nEligible Users for Competitions on {competition_date}:")
                for row in rows:
                    print(f"User ID: {row[0]}, Name: {row[1]}")
        
        if not results_found:
            print(f"No competitions or eligible users found for {competition_date}.")
    
    except Exception as e:
        print(f"")
    finally:
        cursor.close()

# Find rewards for a specific user 
def fetch_rewards_for_user(connection):
    user_id = int(input("Enter user ID: "))
    query = "SELECT * FROM rewards WHERE user_id = %s"
    results = fetch_query_results(connection, query, (user_id,))
    if results:
        for row in results:
            print(row) 
    else:
        print("No rewards at the moment")

def fetch_user_competition(connection, competition_id):
    try:
        cursor = connection.cursor(dictionary=True)
        
        query = """
            SELECT u.user_id, u.username
            FROM users u
            JOIN user_competition uc ON u.user_id = uc.user_id
            WHERE uc.competition_id = %s;
        """
        # Execute the query 
        cursor.execute(query, (competition_id,))
        users = cursor.fetchall()
        print("users in competiton:")
        return users
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None
    finally:
        cursor.close()

"""UPDATE"""

# Register a user for a competition
def register_user_for_competition(connection):
    user_id = input("Enter user id ")
    competition_date = input("Enter competition date (YYYY-MM-DD): ")
    call_stored_procedure(connection, 'register_user_for_competition', (user_id, competition_date))
    print("User registered for competition")

def update_activity(connection):
    try:
        log_id = int(input("Enter the ID of the fitness log to update: "))
        print("\nWhat would you like to update?")
        print("1. Activity Minutes")
        print("2. Sleep Hours")
        print("3. Activity Date (YYYY-MM-DD)")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            new_minutes = int(input("Enter the new activity minutes: ").strip())
            query = "UPDATE fitness_watch SET activity_minutes = %s WHERE log_id = %s"
            execute_query(connection, query, (new_minutes, log_id))
            print("Activity minutes updated successfully!")
        elif choice == '2':
            new_sleep_hours = float(input("Enter the new sleep hours: ").strip())
            query = "UPDATE fitness_watch SET sleep_hours = %s WHERE log_id = %s"
            execute_query(connection, query, (new_sleep_hours, log_id))
            print("Sleep hours updated successfully!")
        elif choice == '3':
            new_date = input("Enter the new activity date (YYYY-MM-DD): ").strip()
            call_stored_procedure(connection, 'update_weekly_leaderboard', (new_date,))
            query = "UPDATE fitness_watch SET activity_date = %s WHERE log_id = %s"
            execute_query(connection, query, (new_date, log_id))
            print("Activity date updated successfully!")  
        else:
            print("Invalid choice.")
    except Exception as e:
        print(f"Error updating activity: {e}")
    except ValueError:
        print("Invalid input. Please enter valid data.")

def update_user(connection):
    try:
        user_id = int(input("Enter the ID of the user to update: "))
        print("\nWhat would you like to update?")
        print("1. Name")
        print("2. Age")
        print("3. Email")
        print("4. Phone Number")
        print("5. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == '1':
            new_name = input("Enter new name: ").strip()
            query = "UPDATE users SET name = %s WHERE user_id = %s"
            execute_query(connection, query, (new_name, user_id))
            print("User's name updated successfully!")
        elif choice == '2':
            new_age = int(input("Enter new age: ").strip())
            query = "UPDATE users SET age = %s WHERE user_id = %s"
            execute_query(connection, query, (new_age, user_id))
            print("User's age updated successfully!")
        elif choice == '3':
            new_email = input("Enter new email: ").strip()
            query = "UPDATE users SET email = %s WHERE user_id = %s"
            execute_query(connection, query, (new_email, user_id))
            print("User's email updated successfully!")
        elif choice == '4':
            new_phone = input("Enter new phone number: ").strip()
            query = "UPDATE users SET phone_number = %s WHERE user_id = %s"
            execute_query(connection, query, (new_phone, user_id))
            print("User's phone number updated successfully!")
        elif choice == '5':
            print("Exiting update user operation.")
        else:
            print("Invalid choice. No updates were made.")
    except Error as e:
        print(f"Error updating user: {e}")
    except ValueError:
        print("Invalid input. Please enter valid details.")




"""DELETE"""

def delete_activity(connection):
    try:
        activity_id = int(input("Enter the ID of the activity to delete: "))
        query = "DELETE FROM activities WHERE activity_id = %s"
        execute_query(connection, query, (activity_id,))
        print("\nActivity deleted successfully!")
    except Error as e:
        print(f"\nError deleting activity: {e}")

def delete_user(connection):
    try:
        user_id = int(input("Enter user ID to delete: "))
        query = "DELETE FROM users WHERE user_id = %s"
        execute_query(connection, query, (user_id,))
        print(f"User with ID {user_id} deleted successfully!")
    except Error as e:
        print(f"\nError deleting user: {e}")
def delete_reward(connection):
    try:
        # Prompt the user for the reward ID to delete
        reward_id = int(input("Enter the reward ID to delete: "))
        query = "DELETE FROM rewards WHERE reward_id = %s"
        cursor = connection.cursor()
        cursor.execute(query, (reward_id,))
        connection.commit()
        
        if cursor.rowcount > 0:
            print(f"Reward with ID {reward_id} has been successfully deleted.")
        else:
            print(f"No reward found with ID {reward_id}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        cursor.close()


# Menu 
def menu():
    """Main application loop"""
    try:
        db_user = input("Enter database username: ").strip()
        db_password = getpass("Enter database password: ").strip()

        # Establish database connection
        connection = create_connection(db_user, db_password)

        if not connection:
            print("Failed to connect to the database.")
            return

        while True:
            print("\nSelect an option:\n")
            print(f"  1. Create User")
            print(f"  2. Create Fitness Log")
            print(f"  3. Create Rewards for the Week")
            print(f"  4. Create Competition")
            print(f"  5. View Weekly Leaderboard")
            print(f"  6. View Rewards for a User")
            print(f"  7. View Personal Report for a User")
            print(f"  8. View Competitors")
            print(f"  9. Update User")
            print(f" 10. Update Activity")
            print(f" 11. Check Competition Eligibility")
            print(f" 12. Register User for Competition")
            print(f" 13. Delete Activity")
            print(f" 14. Delete User")
            print(f" 15. Delete Reward")
            print(f" 16. Exit")

            choice = input("Enter your choice: ")

            if choice == '1':
                insert_user(connection)
                print("user created")
            elif choice == '2':
                insert_fitness_log(connection)
            elif choice == '3':
                assign_rewards_for_week(connection)
            elif choice == '4':
                create_competition(connection)
            elif choice == '5':
                fetch_weekly_leaderboard(connection)
            elif choice == '6':
                fetch_rewards_for_user(connection)
            elif choice == '7':
                user_id = int(input("Enter user ID: "))
                week_start_date = input("Enter week start date (YYYY-MM-DD): ")
                personal_report = fetch_personal_report(connection, user_id, week_start_date)
                if personal_report:
                    print(f"Average Activity Minutes: {personal_report['avg_activity_minutes']}")
                    print(f"Average Sleep Hours: {personal_report['avg_sleep_hours']}")
                else:
                    print("No data found for the given user and week.")
            elif choice == '8':
                competition_id = int(input("Enter competition ID: "))
                fetch_user_competition(connection, competition_id)
            elif choice == '9':
                update_user(connection)
            elif choice == '10':
                update_activity(connection)
            elif choice == '11':
                competition_date = input("Enter competition date (YYYY-MM-DD): ")
                check_competition_eligibility(connection, competition_date)
            elif choice == '12':
                register_user_for_competition(connection)
            elif choice == '13':
                delete_activity(connection)
            elif choice == '14':
                delete_user(connection)
            elif choice == '15':
                delete_reward(connection)
            elif choice == '16':
                close_connection(connection)
                break
            else:
                print("Invalid choice. Please try again.")
    except Exception as e:
        print(f"An error occurred: {e}")


def main():
    menu()

if __name__ == '__main__':
    main()

