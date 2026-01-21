from .database import connect_to_db

def test_select_all(cursor):
    """Prints all data using an existing database cursor."""
    tables = ['teams', 'players', 'injuries']
    
    for table in tables:
        print(f"\n--- DATA FROM TABLE: {table.upper()} ---", flush=True)
        try:
            cursor.execute(f"SELECT * FROM {table} LIMIT 5;") # Limit 5 so logs aren't huge
            
            colnames = [desc[0] for desc in cursor.description]
            print(" | ".join(colnames), flush=True)
            
            rows = cursor.fetchall()
            if not rows:
                print("Table is currently empty.", flush=True)
            else:
                for row in rows:
                    print(row, flush=True)
        except Exception as e:
            print(f"Error reading {table}: {e}", flush=True)