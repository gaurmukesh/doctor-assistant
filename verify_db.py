import sqlite3

def show_table(table_name):
    conn = sqlite3.connect("clinic.db")
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
