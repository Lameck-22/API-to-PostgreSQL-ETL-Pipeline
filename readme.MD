# API-to-PostgreSQL ETL Pipeline

## Overview

This project implements a simple ETL (Extract, Transform, Load) pipeline using Python. It extracts user data from the JSONPlaceholder REST API, cleans and validates the records, and loads the processed data into a PostgreSQL database.

The pipeline demonstrates fundamental data engineering concepts, including API data extraction, data cleaning, data validation, database connectivity, SQL table creation, and UPSERT operations for handling duplicate records.

## Project Objectives

- Extract user data from a REST API.
- Clean and standardize text fields.
- Validate user records before loading.
- Connect Python to PostgreSQL.
- Create a database table automatically.
- Insert new records and update existing records using UPSERT.
- Prevent duplicate records using `user_id` as the primary key.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | ETL development and data processing |
| Requests | API data extraction |
| PostgreSQL | Relational database storage |
| Psycopg2 | Python-to-PostgreSQL connection |
| python-dotenv | Loading environment variables |
| JSON | API response data format |
| SQL | Table creation and UPSERT operations |

## ETL Workflow

The pipeline consists of three main stages:

### 1. Extract

The pipeline retrieves user data from the JSONPlaceholder API.

API endpoint:

`https://jsonplaceholder.typicode.com/users`

The extraction process:

- Sends an HTTP GET request to the API.
- Retrieves the JSON response.
- Converts the response into Python data.
- Validates that the response contains a non-empty list.
- Prints the number of records retrieved.
- Displays the first raw record for inspection.

### 2. Transform

The transformation stage prepares the extracted records for database storage.

#### Text cleaning

The `clean_text()` function:

- Handles `None` values.
- Converts values to strings.
- Removes unnecessary whitespace.
- Returns `None` for empty strings.

#### Data extraction

The pipeline extracts the following fields:

- `user_id`
- `full_name`
- `username`
- `email`
- `phone`
- `city`
- `website`

The city is extracted from the nested address object in the API response.

#### Data validation

The pipeline performs the following checks:

- Ensures the user has a valid ID.
- Ensures the user has a full name.
- Checks that an email address exists.
- Checks that the email contains the `@` symbol.
- Converts email addresses to lowercase.

Records that fail validation are skipped.

### 3. Load

The loading stage transfers the cleaned records into PostgreSQL.

The pipeline:

- Connects to PostgreSQL using `psycopg2`.
- Creates the `users` table if it does not already exist.
- Inserts new records using `executemany()`.
- Updates existing records using `ON CONFLICT`.
- Updates the `loaded_at` timestamp whenever an existing record is updated.
- Closes the database connection after execution.

## Database Schema

The pipeline creates a table named `users`.

| Column | Data Type | Description |
|---|---|---|
| `user_id` | INTEGER | Primary key and unique user identifier |
| `full_name` | TEXT | User's full name |
| `username` | TEXT | User's username |
| `email` | TEXT | User's email address |
| `phone` | TEXT | User's phone number |
| `city` | TEXT | User's city |
| `website` | TEXT | User's website |
| `loaded_at` | TIMESTAMPTZ | Timestamp when the record was loaded |

The `loaded_at` column uses `NOW()` as its default value.

## UPSERT Strategy

The pipeline uses PostgreSQL's `ON CONFLICT(user_id) DO UPDATE` functionality.

This allows the pipeline to:

- Insert new users when their `user_id` does not exist.
- Update existing users when their `user_id` already exists.
- Avoid duplicate records.
- Refresh the `loaded_at` timestamp when a record is updated.

This makes the pipeline safe to rerun without creating duplicate user records.

## Project Structure

```text
etl/
│
├── etl_pipeline.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

| File | Description |
|---|---|
| `etl_pipeline.py` | Contains extraction, transformation and loading logic |
| `.env` | Stores PostgreSQL connection credentials |
| `.gitignore` | Prevents sensitive and unnecessary files from being committed |
| `requirements.txt` | Lists project dependencies |
| `README.md` | Project documentation |

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-username/your-repository.git
```

Navigate into the project directory:

```bash
cd your-repository
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

### 3. Activate the virtual environment

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Windows Command Prompt:

```cmd
venv\Scripts\activate
```

### 4. Install dependencies

```bash
pip install requests psycopg2-binary python-dotenv
```

### 5. Configure environment variables

Create a `.env` file in the project root directory.

Add your PostgreSQL connection string:

```dotenv
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/users_db
```

Replace the placeholders with your actual PostgreSQL credentials and database name.

### 6. Create the PostgreSQL database

Ensure PostgreSQL is installed and running.

Create the database if it does not already exist:

```sql
CREATE DATABASE users_db;
```

The pipeline will automatically create the `users` table when it runs.

## Running the Pipeline

Execute the Python script from your terminal:

```bash
python etl_pipeline.py
```

The script will:

1. Extract users from the API.
2. Transform and validate the records.
3. Connect to PostgreSQL.
4. Create the users table if necessary.
5. Insert or update records.
6. Close the database connection.

## Expected Output

```text
[EXTRACT] GET https://jsonplaceholder.typicode.com/users
[EXTRACT] status code: 200
[EXTRACT] Received 10 raw records
[EXTRACT] first raw record, exactly as received
...
[TRANSFORM] Cleaning records....
[TRANSFORMATION] 10 clean records
[LOAD] Connecting to PostgreSQL...
[LOAD] 10 rows updated or rows inserted in table users
```

The exact output may vary depending on the execution and records processed.

## Verifying the Data

After the pipeline runs, execute the following SQL queries in PostgreSQL using DBeaver or pgAdmin.

### Retrieve all users

```sql
SELECT *
FROM users
ORDER BY user_id;
```

### Count loaded records

```sql
SELECT COUNT(*) AS total_users
FROM users;
```

### Inspect loading timestamps

```sql
SELECT user_id, full_name, email, city, loaded_at
FROM users
ORDER BY user_id;
```

### Check for duplicate user IDs

```sql
SELECT user_id, COUNT(*)
FROM users
GROUP BY user_id
HAVING COUNT(*) > 1;
```

## Error Handling and Limitations

The current implementation includes basic validation of the API response and user records.

However, further improvements could include:

- HTTP error handling using `raise_for_status()`.
- API retry mechanisms.
- More comprehensive email validation.
- Structured logging instead of `print()`.
- Database connection error handling.
- Data quality checks.
- Configuration validation.
- Monitoring and alerting.

## Future Improvements

- Implement structured logging.
- Add retry logic for failed API requests.
- Introduce automated data quality checks.
- Containerize the pipeline using Docker.
- Schedule ETL execution using Apache Airflow.
- Implement incremental data loading.
- Add automated tests using pytest.

## Conclusion

This project demonstrates a basic end-to-end ETL pipeline that extracts data from a REST API, transforms and validates the records using Python, and loads them into PostgreSQL.

It provides a practical foundation for learning API integration, data cleaning, SQL operations, database management, and ETL pipeline development.

**Key concepts demonstrated:** API extraction, Python data transformation, validation, PostgreSQL, UPSERT, database connectivity, and ETL workflow design.
