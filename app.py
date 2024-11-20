from flask import Flask, request, render_template, jsonify, send_file
from dotenv import load_dotenv
import os
import mysql.connector
import pandas as pd

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MySQL configuration
db_config = {
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'user': os.getenv('MYSQL_USER', 'root'),
    'password': os.getenv('MYSQL_PASSWORD', ''),
    'database': os.getenv('MYSQL_DB', 'calorietracker')
}

# Database connection helper
def get_db_connection():
    try:
        conn = mysql.connector.connect(**db_config)
        if conn.is_connected():
            print("Connected to mysql database")
            return conn
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

# Index Page Route
@app.route('/')
def index():
    return render_template('index.html')

# Route to render Import Logs form
@app.route('/import-logs-form', methods=['GET'])
def render_import_logs_form():
    return render_template('import_logs.html')

# Route to render Calorie Summary form
@app.route('/calorie-summary-form', methods=['GET'])
def render_calorie_summary_form():
    return render_template('calorie_summary.html')

# Existing routes for POST endpoints
@app.route('/import-logs', methods=['POST'])
def import_logs():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

        required_columns = {'food_name', 'amount', 'calories_per_unit', 'consumption_date'}
        if not required_columns.issubset(df.columns):
            return jsonify({'error': f'Missing columns: {required_columns - set(df.columns)}'}), 400

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        cursor = conn.cursor()
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO food_logs (food_name, amount, calories_per_unit, consumption_date)
                VALUES (%s, %s, %s, %s)
            """, (row['food_name'], row['amount'], row['calories_per_unit'], row['consumption_date']))
        conn.commit()
        conn.close()

        return "File uploaded and data imported successfully."

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/calorie-summary', methods=['POST'])
def calorie_summary():
    try:
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        query = """
            SELECT food_name, amount, calories_per_unit
            FROM food_logs
            WHERE consumption_date BETWEEN %s AND %s
        """
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (start_date, end_date))
        logs = cursor.fetchall()
        conn.close()

        total_calories = sum(log['amount'] * log['calories_per_unit'] for log in logs)
        average_calories = total_calories / len(logs) if logs else 0

        return jsonify({
            'total_calories': total_calories,
            'average_calories': average_calories,
            'logs': logs
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
