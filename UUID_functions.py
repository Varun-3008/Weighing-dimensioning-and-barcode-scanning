import uuid
import psycopg2

def generate_and_insert_uuid(conn,cursor):
    # Generate a UUID
    uuid_value = str(uuid.uuid4())

    try:
        # Execute SQL INSERT statement to insert the UUID into the database
        cursor.execute("INSERT INTO profiling (id) VALUES (%s)", (uuid_value,))
        
        # Commit the transaction
        conn.commit()
        
        print("UUID inserted successfully into the database:", uuid_value)
    except Exception as e:
        # Rollback the transaction in case of error
        conn.rollback()
        print("Error inserting UUID into the database:", e)
    finally:
        # Close cursor and connection

        return  uuid_value