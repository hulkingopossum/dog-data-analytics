import mysql.connector
import requests
import pandas as pd

# Database config
DB_CONFIG = {
    'user': 'root',
    'password': '', 
    'host': 'localhost',
    'database': 'dog_data' 
}

# Connect to the database
def connect_to_db():
    """Establishes a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

# Function to create tables if they don't exist
def create_tables():
    """Creates the required tables in the database."""
    conn = connect_to_db()
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS breed (
            id INT AUTO_INCREMENT PRIMARY KEY,
            breed_name VARCHAR(255),
            breed_age INT,
            breed_group VARCHAR(255)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lifespan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            breed_id INT,
            min_lifespan INT,
            max_lifespan INT,
            FOREIGN KEY (breed_id) REFERENCES breed(id)
        )
    ''')

    conn.commit()
    cursor.close()
    conn.close()

# Function to fetch dog breed data from the API
def fetch_dog_data():
    """Fetches dog data from the API and returns it."""
    url = "https://api.thedogapi.com/v1/breeds"
    # NOTE: Put the api key here for now. I would still like to put this in a .env
    headers = {
        'x-api-key': 'live_NmkvbPTVvh0yJRHMRJRkjWXxDOULPvLSu8udrBNK3OcI9jWEfQUy0dOMQ3iK30Av'
    }

    response = requests.get(url, headers=headers)
    data = response.json()
    return data

# Function to insert breed and lifespan data
def insert_data():
    """Inserts dog breed and lifespan data into the database."""
    conn = connect_to_db()
    cursor = conn.cursor()

    # Fetch dog data from the API
    dog_data = fetch_dog_data()

    for dog in dog_data:
        breed_name = dog['name']
        breed_age = dog.get('life_span', '0').split()[0]  # Extract the first number in the life_span
        breed_group = dog.get('group', 'Unknown')

        # Insert breed data into breed table
        cursor.execute('''
            INSERT INTO breed (breed_name, breed_age, breed_group)
            VALUES (%s, %s, %s)
        ''', (breed_name, breed_age, breed_group))
        #this captures the last row id in our loop
        breed_id = cursor.lastrowid

        # Insert lifespan data into lifespan table (with the associated breed_id)
        lifespan = dog.get('life_span', '').split()  # should read like: '12 - 14 years'
        if len(lifespan) == 3:  # Check if we have a valid lifespan range
            min_lifespan = int(lifespan[0])
            max_lifespan = int(lifespan[2].replace('years', '').strip())  # Clean 'years'
            cursor.execute('''
                INSERT INTO lifespan (breed_id, min_lifespan, max_lifespan)
                VALUES (%s, %s, %s)
            ''', (breed_id, min_lifespan, max_lifespan))

    conn.commit()
    cursor.close()
    conn.close()

# Function to analyze the data (e.g., finding average lifespan per breed)
def analyze_data():
    """Analyzes lifespan data from the database."""
    conn = connect_to_db()
    cursor = conn.cursor()

    # Query to get breed names and avg lifespans
    cursor.execute('''
        SELECT breed.breed_name, AVG(lifespan.min_lifespan) AS avg_min_lifespan, AVG(lifespan.max_lifespan) AS avg_max_lifespan
        FROM breed
        JOIN lifespan ON breed.id = lifespan.breed_id
        GROUP BY breed.breed_name
    ''')

    # Fetch the results and load them into Pandas
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['Breed Name', 'Average Min Lifespan', 'Average Max Lifespan'])

    # Print the result
    print(df)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()  # Ensure tables are created
    insert_data()    # Insert data from API into the database
    analyze_data()   # Perform the analysis on the data
