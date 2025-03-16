import mysql.connector
import requests
import pandas as pd
import matplotlib.pyplot as plt
import pymysql


# Database config
DB_CONFIG = {
    'user': 'teamdog',
    'password': 'teamdog',
    'host': '64.23.196.47',
    'database': 'dog_data' 
}

# Connect to the database
def connect_to_db():
    """Establishes a database connection."""
    return pymysql.connect(**DB_CONFIG)

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
        breed_group = dog.get('breed_group', 'Unknown')

        # Insert breed data into breed table
        cursor.execute('''
            INSERT INTO breed (breed_name, breed_age, breed_group)
            VALUES (%s, %s, %s)
        ''', (breed_name, breed_age, breed_group))
        #this captures the last row id in our loop
        breed_id = cursor.lastrowid

        # Insert lifespan data into lifespan table (with the associated breed_id)
        lifespan = dog.get('life_span', '').split()  # should read like: '12 - 14 years'
        if len(lifespan) == 4:  # Check if we have a valid lifespan range
            min_lifespan = int(lifespan[0])
            max_lifespan = int(lifespan[2].replace('years', '').strip())  # Clean 'years'
            cursor.execute('''
                INSERT INTO lifespan (breed_id, min_lifespan, max_lifespan)
                VALUES (%s, %s, %s)
            ''', (breed_id, min_lifespan, max_lifespan))

    conn.commit()
    cursor.close()
    conn.close()

# Analyzing and plotting data into graphs
def analyze_and_plot_data():
    """Fetches data from the database and plots the 30 longest and 30 shortest living breeds."""
    conn = connect_to_db()
    cursor = conn.cursor()

    # Query tables to get breed names and lifespans
    cursor.execute('''
        SELECT breed.breed_name, AVG(lifespan.min_lifespan) AS avg_min_lifespan, AVG(lifespan.max_lifespan) AS avg_max_lifespan
        FROM breed
        JOIN lifespan ON breed.id = lifespan.breed_id
        GROUP BY breed.breed_name
    ''')

    # Fetch results, load into pandas
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns=['Breed Name', 'Average Min Lifespan', 'Average Max Lifespan'])

    # Calculate the average lifespan as the midpoint between min and max years
    df['Average Lifespan'] = (df['Average Min Lifespan'] + df['Average Max Lifespan']) / 2

    # Sort by lifespan
    df_sorted = df.sort_values(by='Average Lifespan', ascending=True)

    shortest_living = df_sorted.head(30)

    longest_living = df_sorted.tail(30)

    # Graph shortest living breeds
    plt.figure(figsize=(12, 6))
    plt.barh(shortest_living['Breed Name'], shortest_living['Average Lifespan'], color='blue')
    plt.xlabel('Average Lifespan (Years)')
    plt.ylabel('Breed Name')
    plt.title('Top 30 Shortest-Living Dog Breeds')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show(block=False) #This block allows 2nd graph to show without having to close the first

    # Graph longest living breeds
    plt.figure(figsize=(12, 6))
    plt.barh(longest_living['Breed Name'], longest_living['Average Lifespan'], color='green')
    plt.xlabel('Average Lifespan (Years)')
    plt.ylabel('Breed Name')
    plt.title('Top 30 Longest-Living Dog Breeds')
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

    cursor.close()
    conn.close()

if __name__ == "__main__":
    create_tables()  # Ensure tables are created
    insert_data()    # Insert data from API into the database
    analyze_and_plot_data()   # Perform the analysis on the data
