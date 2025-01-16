import psycopg2
import hidden
import time
import myutils
import requests
import json

# Load the secrets
secrets = hidden.secrets()

conn = psycopg2.connect(host=secrets['host'],
        port=secrets['port'],
        database=secrets['database'],
        user=secrets['user'],
        password=secrets['pass'],
        connect_timeout=3)

cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS pokeapi (
    id INTEGER PRIMARY KEY,
    body JSONB
);
""")
conn.commit()

# Base URL for the PokéAPI
BASE_URL = "https://pokeapi.co/api/v2/pokemon/"

# Fetch and store the first 100 Pokémon data
for i in range(1, 101):
    url = f"{BASE_URL}{i}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()

        # Insert into the database
        cursor.execute("""
        INSERT INTO pokeapi (id, body)
        VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING;
        """, (i, json.dumps(data)))
    else:
        print(f"Failed to fetch data for Pokémon ID {i}, Status Code: {response.status_code}")

# Commit changes and close the connection
conn.commit()
cursor.close()
conn.close()

print("Data fetched and stored successfully!")
print('Closing database connection...')
