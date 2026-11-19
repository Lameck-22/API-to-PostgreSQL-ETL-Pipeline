import json
import os
import psycopg2
import requests
from dotenv import load_dotenv
from datetime import datetime

#Extraction
API_URL = "https://jsonplaceholder.typicode.com/users"

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

#download and return as a list

def extract():
    print(f"[EXTRACT] GET {API_URL}")

    response = requests.get(API_URL, timeout=10)
    print(f"[EXTRACT] status code: {response.status_code}")

    raw_data = response.json()

    if not isinstance(raw_data, list) or len(raw_data) == 0:
        raise ValueError("The API returns no users")

    print(f"[EXTRACT] Recieved {len(raw_data)} raw records")
    print(f"[EXTRACT] first raw record, exactly as recieved")
    print(json.dumps(raw_data[0],indent=2))

    return raw_data

#Transformation
def clean_text(value):
    if value is None:
        return None
    value =" ".join(str(value).split())

    return value or None

def transform(raw_data):
    print("[TRANSFORM] Cleaning records....")

    clean_user =[]

    for user in raw_data:
        address = user.get("address", "Unknown")

        record = {
            "user_id" : user.get("id"),
            "full_name": clean_text(user.get("name")),
            "username": clean_text(user.get("username")),
            "email": clean_text(user.get("email")),
            "phone" : clean_text(user.get("phone")),
            "city" : clean_text(address.get("city")),
            "website": clean_text(user.get("website"))
        }

        #validating data
        if record["user_id"] is None or record["full_name"] is None:
            print(f"[TRANSFORM] skipped user{record["user_id"]}: missing id or name")
            continue
        if record["email"] is None or "@" not in record["email"]:
            print(f"[TRANSFORMATION] skipped user: {record['email']}: invalid email")
            continue
        record["email"] = record["email"].lower()

        clean_user.append(record)

    print(f"[TRANSFORMATION] {len(clean_user)} clean records")    
    return clean_user
        


#Loading data
#Creating SQL table to help us loadour data
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS users(
     user_id INTEGER PRIMARY KEY,
     full_name TEXT NOT NULL,
     username TEXT,
     email TEXT NOT NULL,
     phone TEXT,
     city TEXT,
     website TEXT,
     loaded_at TIMESTAMPTZ DEFAULT NOW ()
     );
"""

#Upsert (insert new users and updating users incase already exists on the database)
UPSERT_SQL = """
INSERT INTO users(user_id, full_name, username, email, phone, city, website)
VALUES (%(user_id)s, %(full_name)s, %(username)s, %(email)s, %(phone)s, %(city)s, %(website)s)
ON CONFLICT(user_id) DO UPDATE SET
full_name = EXCLUDED.full_name,
username = EXCLUDED.username,
email = EXCLUDED.email,
phone = EXCLUDED.phone,
city = EXCLUDED.city,
website = EXCLUDED.website,
loaded_at = NOW();

"""

#Python script to load data
def load(clean_users):
    print("[LOAD] Connecting to PostgreSQL...")
    conn = psycopg2.connect(DATABASE_URL)

    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute(CREATE_TABLE_SQL)
                cur.executemany(UPSERT_SQL, clean_users)
            print(f"[LOAD] {len(clean_users)} rows updated or rows inserted in table users")

    finally:
        conn.close()

if __name__ =="__main__":
    raw_data = extract()
    clean_users = transform(raw_data)
    load_data = load(clean_users)
    #print(clean_users)



