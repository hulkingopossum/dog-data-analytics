import mysql.connector
import random
from datetime import datetime, timedelta

# db config
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "yourpassword",
    "database": "dog_data"
}

def connect_to_db():
    """Establishes a database connection."""
    return mysql.connector.connect(**DB_CONFIG)

def create_tables():
    """Creates tables based on the provided schema."""
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS owners (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            email VARCHAR(100) UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS breed (
            id INT AUTO_INCREMENT PRIMARY KEY,
            breed_name VARCHAR(100),
            breed_age INT,
            breed_group VARCHAR(50)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lifespan (
            id INT AUTO_INCREMENT PRIMARY KEY,
            breed_id INT,
            min_lifespan INT,
            max_lifespan INT,
            FOREIGN KEY (breed_id) REFERENCES breed(id) ON DELETE CASCADE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS dogs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100),
            breed_id INT,
            birth_date DATE,
            owner_id INT,
            FOREIGN KEY (breed_id) REFERENCES breed(id) ON DELETE CASCADE,
            FOREIGN KEY (owner_id) REFERENCES owners(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

def insert_owner(first_name, last_name, email):
    """Inserts an owner into the owners table."""
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO owners (first_name, last_name, email)
        VALUES (%s, %s, %s)
    """, (first_name, last_name, email))

    conn.commit()
    cursor.close()
    conn.close()

def insert_breed(breed_name, breed_age, breed_group):
    """Inserts a breed into the breed table."""
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO breed (breed_name, breed_age, breed_group)
        VALUES (%s, %s, %s)
    """, (breed_name, breed_age, breed_group))

    conn.commit()
    cursor.close()
    conn.close()

def insert_lifespan(breed_id, min_lifespan, max_lifespan):
    """Inserts lifespan data for a breed."""
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO lifespan (breed_id, min_lifespan, max_lifespan)
        VALUES (%s, %s, %s)
    """, (breed_id, min_lifespan, max_lifespan))

    conn.commit()
    cursor.close()
    conn.close()

def insert_dog(name, breed_id, birth_date, owner_id):
    """Inserts a dog into the dogs table."""
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO dogs (name, breed_id, birth_date, owner_id)
        VALUES (%s, %s, %s, %s)
    """, (name, breed_id, birth_date, owner_id))

    conn.commit()
    cursor.close()
    conn.close()

def get_dog_count_by_owner():
    """Retrieves the number of dogs owned by each owner."""
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT o.first_name, o.last_name, COUNT(d.id) AS dog_count
        FROM owners o
        LEFT JOIN dogs d ON o.id = d.owner_id
        GROUP BY o.id
        ORDER BY dog_count DESC;
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results

def get_average_lifespan_by_breed():
    """Retrieves the average lifespan for each breed."""
    conn = connect_to_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT b.breed_name, AVG((l.min_lifespan + l.max_lifespan) / 2) AS avg_lifespan
        FROM breed b
        JOIN lifespan l ON b.id = l.breed_id
        GROUP BY b.id
        ORDER BY avg_lifespan DESC;
    """)

    results = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return results

def seed_data():
    """Seeds the database with sample data."""
    owners = [
        ("Alice", "Smith", "alice@example.com"),
        ("Bob", "Johnson", "bob@example.com"),
        ("Charlie", "Brown", "charlie@example.com"),
    ]
    
    breeds = [
        ("Golden Retriever", 10, "Sporting"),
        ("Bulldog", 8, "Non-Sporting"),
        ("German Shepherd", 9, "Herding"),
    ]
    
    lifespans = [
        (1, 10, 12),
        (2, 8, 10),
        (3, 9, 13),
    ]
    
    dogs = [
        ("Buddy", 1, "2020-06-15", 1),
        ("Max", 2, "2019-07-22", 2),
        ("Bella", 3, "2021-01-05", 3),
        ("Charlie", 1, "2018-03-14", 1),
        ("Rocky", 2, "2020-09-10", 2),
    ]
    
    print("🌱 Seeding Owners...")
    for owner in owners:
        insert_owner(*owner)

    print("🌱 Seeding Breeds...")
    for breed in breeds:
        insert_breed(*breed)

    print("🌱 Seeding Lifespans...")
    for lifespan in lifespans:
        insert_lifespan(*lifespan)

    print("🌱 Seeding Dogs...")
    for dog in dogs:
        insert_dog(*dog)

def main():
    """Main execution function."""
    print("🚀 Setting up the database...")
    create_tables()

    print("\n🌱 Seeding initial data...")
    seed_data()

    print("\n📊 Dog Ownership Statistics:")
    for owner, last_name, count in get_dog_count_by_owner():
        print(f"{owner} {last_name} owns {count} dog(s).")

    print("\n🐶 Average Lifespan by Breed:")
    for breed, lifespan in get_average_lifespan_by_breed():
        print(f"{breed}: {lifespan:.1f} years")

if __name__ == "__main__":
    main()
