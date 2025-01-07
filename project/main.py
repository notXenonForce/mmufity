import psycopg2

def main():
    # Step 1: Connect to the PostgreSQL database
    conn = psycopg2.connect('postgres://avnadmin:AVNS_NEWUHRbM3Cc5QKeCGZ9@mmufity-mmufity.k.aivencloud.com:24028/defaultdb?sslmode=require')
    cur = conn.cursor()

    # Step 2: Create the 'user_accounts' and 'artist_accounts' tables if they don't exist
    create_user_table_sql = '''
    CREATE TABLE IF NOT EXISTS user_accounts (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );
    '''
    
    create_artist_table_sql = '''
    CREATE TABLE IF NOT EXISTS artist_accounts (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) NOT NULL UNIQUE,
        email VARCHAR(100) NOT NULL UNIQUE,
        password VARCHAR(255) NOT NULL
    );
    '''

    cur.execute(create_user_table_sql)  # Execute the SQL query to create the user_accounts table
    cur.execute(create_artist_table_sql)  # Execute the SQL query to create the artist_accounts table
    conn.commit()  # Save changes to the database
    print("Tables 'user_accounts' and 'artist_accounts' created successfully.")

    # Step 3: Insert sample data into the 'user_accounts' and 'artist_accounts' tables
    insert_user_sql = '''
    INSERT INTO user_accounts (username, email, password)
    VALUES (%s, %s, %s)
    ON CONFLICT (username) DO NOTHING;  -- Avoid duplicate errors if the username already exists
    '''
    insert_artist_sql = '''
    INSERT INTO artist_accounts (username, email, password)
    VALUES (%s, %s, %s)
    ON CONFLICT (username) DO NOTHING;  -- Avoid duplicate errors if the username already exists
    '''

    sample_users = [
        ('cheezylo', 'losssyyyy0726@gmail.com', 'cheezylo0726'),
        ('testboi', 'testboi@testboi.com', 'usertestboi'),
    ]
    sample_artists = [
        ('xenonforce', 'xenonforce004@gmail.com', 'xenonforce004'),
    ]

    # Insert data into 'user_accounts' and 'artist_accounts' tables
    for user in sample_users:
        cur.execute(insert_user_sql, user)
    
    for artist in sample_artists:
        cur.execute(insert_artist_sql, artist)
    
    conn.commit()  # Save changes to the database
    print("Sample data inserted successfully.")

    # Step 4: Query all data from the 'user_accounts' and 'artist_accounts' tables
    select_user_sql = 'SELECT * FROM user_accounts;'
    select_artist_sql = 'SELECT * FROM artist_accounts;'

    cur.execute(select_user_sql)
    user_rows = cur.fetchall()
    print("\nUsers in the database:")
    for row in user_rows:
        print(row)

    cur.execute(select_artist_sql)
    artist_rows = cur.fetchall()
    print("\nArtists in the database:")
    for row in artist_rows:
        print(row)

    # Close the cursor and connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
