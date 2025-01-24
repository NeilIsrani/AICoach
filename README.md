Coach Buddy is an intelligent fitness tracking and injury prevention platform that transforms raw workout data into personalized insights. Leverage advanced machine learning to optimize your training, predict injury risks, and achieve your fitness goals smarter, not harder.
Prerequisites

Python (Version 3.10 or later)
MySQL (Version 8.0 or later)
Required Python Packages:

mysql-connector-python
tabulate
torch
scikit-learn
pandas
numpy



Setup and Installation

Clone the repository
Copygit clone [your-repository-url]
cd coach-buddy

Install Required Packages
Copypip install mysql-connector-python tabulate torch scikit-learn pandas numpy

Database Setup

Open MySQL and import the database:
Copymysql -u root -p < coachdatabase.sql

Replace root with your MySQL username



Running the Application

Launch the Coach Buddy menu-driven interface:
Copypython coachapp.py

When prompted, enter:

Database username
Database password
