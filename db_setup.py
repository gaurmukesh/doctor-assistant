import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.getenv("DATABASE_URL"))
cur = conn.cursor()

# --- Create Tables ---
cur.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS availability (
    id SERIAL PRIMARY KEY,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    is_booked BOOLEAN DEFAULT false,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id SERIAL PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
)
""")

# --- Insert Sample Data Safely ---
cur.execute("SELECT COUNT(*) FROM doctors")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO doctors (name, specialty) VALUES ('Dr X', 'Orthopedics')")
    cur.execute("INSERT INTO doctors (name, specialty) VALUES ('Dr Y', 'Orthopedics')")

cur.execute("SELECT COUNT(*) FROM availability")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO availability (doctor_id, date, time, is_booked) VALUES (1, '2026-04-02', '10:00', true)")
    cur.execute("INSERT INTO availability (doctor_id, date, time) VALUES (1, '2026-04-02', '10:30')")
    cur.execute("INSERT INTO availability (doctor_id, date, time) VALUES (1, '2026-04-02', '11:00')")
    cur.execute("INSERT INTO availability (doctor_id, date, time) VALUES (2, '2026-04-01', '11:00')")
    cur.execute("INSERT INTO availability (doctor_id, date, time) VALUES (2, '2026-04-02', '11:00')")

cur.execute("SELECT COUNT(*) FROM patients")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO patients (name, phone, email) VALUES ('Caller1', '9876543210', 'caller1@mail.com')")

cur.execute("SELECT COUNT(*) FROM appointments")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (1, 1, '2026-04-02', '10:00')")

conn.commit()
conn.close()
print("Database setup complete.")
