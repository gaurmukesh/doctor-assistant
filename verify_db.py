import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def show_table(table_name):
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table_name}")
    rows = cur.fetchall()
    conn.close()

    print(f"\n--- {table_name.upper()} ---")
    for row in rows:
        print(row)

if __name__ == "__main__":
    show_table("doctors")
    show_table("availability")
    show_table("patients")
    show_table("appointments")
