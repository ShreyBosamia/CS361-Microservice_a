# Microservice A: Calorie Tracker Microservice

## Description
This microservice allows users to:
1. Import food logs via a CSV file.
2. Generate calorie summaries for a specified date range.
3. Export all logs as a CSV file.

---

## Prerequisites and Setup

### 1. Setting Up MySQL Database
- Install MySQL and set up a database named **calorietracker**.
- Create the `food_logs` table using the following SQL script:

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
    ```

### 2. Setting Up the `.env` File
- Create a `.env` file in the root of the project directory with the following variables:
    ```
    MYSQL_HOST=localhost
    MYSQL_USER=your_mysql_username
    MYSQL_PASSWORD=your_mysql_password
    MYSQL_DB=calorietracker
    ```
  - Replace `your_mysql_username` and `your_mysql_password` with your actual MySQL credentials.

### 3. Running the Flask Server
- Install required dependencies using `pip`:
    ```bash
    pip install flask mysql-connector-python python-dotenv pandas
    ```
- Run the Flask application:
    ```bash
    python app.py
    ```
- The server will be hosted locally on `http://127.0.0.1:5000`.

---

## How to Use the Microservice

### Endpoints:

1. **Import Logs**
   - **URL**: `/import-logs`
   - **Method**: `POST`
   - **Input**: File (CSV)
   - **Example Call (Python)**:
     ```python
     import requests

     with open("food_logs.csv", "rb") as file:
         response = requests.post("http://127.0.0.1:5000/import-logs", files={"file": file})
         print(response.text)
     ```
   - **Using Postman**:
     1. Set the request method to **POST**.
     2. URL: `http://127.0.0.1:5000/import-logs`.
     3. Go to the **Body** tab, select **form-data**, and add a key named `file` with a file value.
     4. Select your CSV file to upload and click **Send**.

2. **Calorie Summary**
   - **URL**: `/calorie-summary`
   - **Method**: `POST`
   - **Input**: JSON with `start_date` and `end_date`.
   - **Example Call (Python)**:
     ```python
     import requests

     data = {
         "start_date": "2024-01-01",
         "end_date": "2024-01-31"
     }
     response = requests.post("http://127.0.0.1:5000/calorie-summary", json=data)
     print(response.json())
     ```
   - **Using Postman**:
     1. Set the request method to **POST**.
     2. URL: `http://127.0.0.1:5000/calorie-summary`.
     3. Go to the **Body** tab, select **raw**, and choose **JSON** format.
     4. Enter the following JSON:
        ```json
        {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31"
        }
        ```
     5. Click **Send**.

3. **Export Logs**
   - **URL**: `/export-logs`
   - **Method**: `GET`
   - **Example Call (Python)**:
     ```python
     import requests

     response = requests.get("http://127.0.0.1:5000/export-logs")
     with open("exported_logs.csv", "wb") as file:
         file.write(response.content)
     print("Exported logs saved to 'exported_logs.csv'")
     ```
   - **Using Postman**:
     1. Set the request method to **GET**.
     2. URL: `http://127.0.0.1:5000/export-logs`.
     3. Click **Send**. The CSV file will be downloaded.

---

## UML Sequence Diagram
The following diagram shows how to interact with the microservice and its connection to the MySQL database:

```plaintext
Client                          Microservice                         MySQL Database
   |                                  |                                      |
   |  POST /import-logs (CSV File)    |                                      |
   |--------------------------------->|                                      |
   |                                  |  Connect to MySQL                    |
   |                                  |------------------------------------->|
   |                                  |                                      |
   |                                  |   Insert file data into table        |
   |                                  |<-------------------------------------|
   |                                  |                                      |
   |       File processed and data    |                                      |
   |<---------------------------------|                                      |
   |                                  |                                      |
   |  POST /calorie-summary (JSON)    |                                      |
   |--------------------------------->|                                      |
   |                                  |  Connect to MySQL                    |
   |                                  |------------------------------------->|
   |                                  |                                      |
   |     Query logs and calculate     |                                      |
   |<---------------------------------|                                      |
   |                                  |                                      |
   |    JSON with calorie summary     |                                      |
   |<---------------------------------|                                      |
   |                                  |                                      |
   |     GET /export-logs             |                                      |
   |--------------------------------->|                                      |
   |                                  |  Connect to MySQL                    |
   |                                  |------------------------------------->|
   |                                  |                                      |
   |    Query logs and generate CSV   |                                      |
   |<---------------------------------|                                      |
   |                                  |                                      |
   |        CSV File downloaded       |                                      |
   |<---------------------------------|                                      |
