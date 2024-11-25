from flask import Flask, request, render_template, jsonify
import pandas as pd
from db import get_local_db_connection


app = Flask(__name__)

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

        # reads CSV/Excel into dataframe, else returns error
        file = request.files['file']
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith('.xlsx'):
            df = pd.read_excel(file)
        else:
            return jsonify({'error': 'Unsupported file format'}), 400

        # ensure required columns present in file
        required_columns = {'date', 'consumed_weight', 'consumed_fat',
                            'consumed_carbs', 'consumed_protein', 'consumed_cal', 'food_id', 'user_id'}
        if not required_columns.issubset(df.columns):
            return jsonify({'error': f'Missing columns: {required_columns - set(df.columns)}'}), 400

        # connect to database
        conn = get_local_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        cursor = conn.cursor()

        # inserts each row into the logs table
        for _, row in df.iterrows():
            cursor.execute("""
                INSERT INTO logs (date, consumed_weight, consumed_fat, consumed_carbs, consumed_protein, consumed_cal, user_id, food_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (row['date'], row['consumed_weight'], row['consumed_fat'], row['consumed_carbs'], row['consumed_protein'], row['consumed_cal'], row['user_id'], row['food_id']
                  ))
        conn.commit()
        cursor.close()
        conn.close()

        return "File uploaded and data imported successfully."

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/calorie-summary', methods=['GET'])
def calorie_summary():
    try:
        # get dates from URL parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if not start_date or not end_date:
            return jsonify({'error': 'Both start_date and end_date are required'}), 400

        # connect to database
        conn = get_local_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500

        # query to calculate sums
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                SUM(consumed_fat) AS total_fat, 
                SUM(consumed_carbs) AS total_carbs,        
                SUM(consumed_protein) AS total_protein, 
                SUM(consumed_cal) AS total_calories 
                FROM logs
            WHERE date BETWEEN %s AND %s
        """, [start_date, end_date])
        row = cursor.fetchone()
        cursor.close()
        conn.close()

        # edge case where no data found
        if not row or all(value is None for value in row):
            summary = {
                'total_fat': 0,
                'total_carbs': 0,
                'total_protein': 0,
                'total_calories': 0,
            }
        else:
            summary = {
                'total_fat': row[0] if row[0] is not None else 0,
                'total_carbs': row[1] if row[1] is not None else 0,
                'total_protein': row[2] if row[2] is not None else 0,
                'total_calories': row[3] if row[3] is not None else 0,
            }

        return jsonify({
            'total_fat': summary['total_fat'],
            'total_carbs': summary['total_carbs'],
            'total_protein': summary['total_protein'],
            'total_calories': summary['total_calories'],
            'start_data': start_date,
            'end_data': end_date
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# tests database connection when Flask server starts
try:
    conn = get_local_db_connection()
    print("Microservice A connected to database!")
    conn.close()
except Exception as e:
    print(f"Microservice A unable to connect to database: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8031, debug=True)
