import psycopg2

# Database connection parameters
DB_CONFIG = {
    "dbname": "test_db",
    "user": "test_user",
    "password": "test_password",
    "host": "localhost",
    "port": "5432",
}

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    print("Connected to the database!")

    # Create a new table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100),
            age INTEGER
        );
    """)
    conn.commit()
    print("Table created successfully.")

    # Insert some data
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Alice", 25))
    cur.execute("INSERT INTO users (name, age) VALUES (%s, %s)", ("Bob", 30))
    conn.commit()
    print("Data inserted successfully.")

    # Query the data
    cur.execute("SELECT * FROM users;")
    rows = cur.fetchall()
    print("\nQuery Results:")
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Age: {row[2]}")

except psycopg2.Error as e:
    print(f"Database error: {e}")

finally:
    # Close the connection
    if conn:
        cur.close()
        conn.close()
        print("\nDatabase connection closed.")
