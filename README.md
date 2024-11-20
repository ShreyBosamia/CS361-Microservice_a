# Microservice A: Calorie Tracker Microservice

## Description
This microservice allows users to:
1. Import food logs via a CSV file.
2. Generate calorie summaries for a specified date range.
3. Export all logs as a CSV file.

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

---

## UML Sequence Diagram
The following diagram shows how to interact with the microservice:

```plaintext
Client                          Microservice
   |                                  |
   |  POST /import-logs (CSV File)    |
   |--------------------------------->|
   |                                  |
   |       File processed and data    |
   |<---------------------------------|
   |                                  |
   |  POST /calorie-summary (JSON)    |
   |--------------------------------->|
   |                                  |
   |    JSON with calorie summary     |
   |<---------------------------------|
   |                                  |
   |     GET /export-logs             |
   |--------------------------------->|
   |                                  |
   |        CSV File downloaded       |
   |<---------------------------------|

