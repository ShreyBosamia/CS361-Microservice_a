# Microservice A: Calorie Tracker Microservice

## Description
This microservice allows users to:
1. **Import food logs** via a CSV file.
2. **Generate calorie summaries** for a specified date range.
3. **Export all food logs** as a CSV file.

The microservice is designed to interact with a MySQL database that stores the food logs. It can be accessed programmatically using tools like Postman, curl, or custom scripts.

---

## Setup Instructions

### Prerequisites:
1. **Python 3.9+**
   - Install Flask and required libraries:
     ```bash
     pip install flask pandas mysql-connector-python python-dotenv
     ```

2. **MySQL Database**
   - Ensure you have a running MySQL server.
   - Install MySQL Workbench if needed.

3. **Postman (Optional)**
   - Download and install [Postman](https://www.postman.com/downloads/) for testing.

---

### MySQL Database Setup

1. **Create the Database**:
   Run the following SQL commands in MySQL Workbench to set up the database and table:
   ```sql
   CREATE DATABASE calorietracker;

   USE calorietracker;

   CREATE TABLE food_logs (
       id INT AUTO_INCREMENT PRIMARY KEY,
       food_name VARCHAR(255) NOT NULL,
       amount FLOAT NOT NULL,
       calories_per_unit FLOAT NOT NULL,
       consumption_date DATE NOT NULL
   );

   INSERT INTO food_logs (food_name, amount, calories_per_unit, consumption_date)
   VALUES
       ('Apple', 1, 52, '2024-01-01'),
       ('Banana', 2, 89, '2024-01-02'),
       ('Chicken', 200, 2.5, '2024-01-03');
Configure .env File: Create a file named .env in the project root and configure the following details:
plaintext
Copy code
MYSQL_HOST=localhost
MYSQL_USER=your_username
MYSQL_PASSWORD=your_password
MYSQL_DB=calorietracker
Running the Microservice
Start the Flask App:

bash
Copy code
python app.py
Access the Web Pages: Open your browser and navigate to:

Import Logs Form: http://127.0.0.1:5000/import-logs-form
Calorie Summary Form: http://127.0.0.1:5000/calorie-summary-form
Export Logs: http://127.0.0.1:5000/export-logs
Using Postman to Test the Endpoints
1. Import Logs:
Method: POST
URL: http://127.0.0.1:5000/import-logs
Body: Use form-data with the following key:
Key: file
Value: Attach your food_logs.csv file.
2. Calorie Summary:
Method: POST
URL: http://127.0.0.1:5000/calorie-summary
Body: Use raw JSON with the following format:
json
Copy code
{
    "start_date": "2024-01-01",
    "end_date": "2024-01-31"
}
3. Export Logs:
Method: GET
URL: http://127.0.0.1:5000/export-logs
Response: A CSV file containing all logs will be downloaded.
UML Sequence Diagram
The following diagram illustrates how the microservice interacts with the client and the MySQL database:

plaintext
Copy code
Client                          Microservice                          MySQL Database
   |                                  |                                     |
   |  POST /import-logs (CSV File)    |                                     |
   |--------------------------------->|                                     |
   |                                  |  Insert logs into `food_logs`       |
   |                                  |------------------------------------>|
   |                                  |                                     |
   |       Success message            |                                     |
   |<---------------------------------|                                     |
   |                                  |                                     |
   |  POST /calorie-summary (JSON)    |                                     |
   |--------------------------------->|                                     |
   |                                  |  Query `food_logs` for calorie data |
   |                                  |------------------------------------>|
   |                                  |                                     |
   |      JSON with calorie data      |                                     |
   |<---------------------------------|                                     |
   |                                  |                                     |
   |       GET /export-logs           |                                     |
   |--------------------------------->|                                     |
   |                                  |  Query `food_logs` for all data     |
   |                                  |------------------------------------>|
   |                                  |                                     |
   |        CSV file response         |                                     |
   |<---------------------------------|                                     |
Communication Contract
Accessing the Microservice:

Clone the repository: [GitHub Repo Link].
Install dependencies and configure the .env file.
Start the Flask app and test endpoints via Postman, curl, or the provided forms.
Backup Plan:

If there are issues with accessing the microservice, contact me at [your email/contact method].
I will be available during [your availability times].
If the microservice cannot be accessed by [specific date], please inform me immediately.
Assumptions:

MySQL server is running locally, and credentials in the .env file are correct.
The user has basic knowledge of REST APIs or is using tools like Postman.
