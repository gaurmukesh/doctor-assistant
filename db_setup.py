import sqlite3

conn = sqlite3.connect("clinic.db")
cur = conn.cursor()

# --- Create Tables ---
cur.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    doctor_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    specialty TEXT NOT NULL
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS availability (
    id INTEGER PRIMARY KEY,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    is_booked INTEGER DEFAULT 0,
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS patients (
    patient_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT,
    email TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    appointment_id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    FOREIGN KEY (patient_id) REFERENCES patients(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctors(doctor_id)
)
""")

# --- Insert Sample Data Safely ---
# Doctors
cur.execute("SELECT COUNT(*) FROM doctors")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO doctors (name, specialty) VALUES ('Dr X', 'Orthopedics')")
    cur.execute("INSERT INTO doctors (name, specialty) VALUES ('Dr Y', 'Orthopedics')")

# Availability
cur.execute("SELECT COUNT(*) FROM availability")
if cur.fetchone()[0] == 0:
    # Dr X — no slots today, available tomorrow
    cur.execute("INSERT INTO availability (doctor_id, date, time, is_booked) VALUES (1, '2026-03-24', '10:00', 1)")  # tomorrow, pre-booked
    cur.execute("INSERT INTO availability (doctor_id, date, time) VALUES (1, '2026-03-24', '10:30')")                # tomorrow, free
    cur.execute("INSERT INTO availability (doctor_id, date, time) VALUES (1, '2026-03-24', '11:00')")                # tomorrow, free
    # Dr Y — available today and tomorrow
    cur.execute("INSERT INTO availability (doctor_id, date, time) VALUES (2, '2026-03-23', '11:00')")                # today, free
    cur.execute("INSERT INTO availability (doctor_id, date, time) VALUES (2, '2026-03-24', '11:00')")                # tomorrow, free

# Patients
cur.execute("SELECT COUNT(*) FROM patients")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO patients (name, phone, email) VALUES ('Caller1', '9876543210', 'caller1@mail.com')")

# Appointments
cur.execute("SELECT COUNT(*) FROM appointments")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (1, 1, '2026-03-24', '10:00')")

conn.commit()
conn.close()