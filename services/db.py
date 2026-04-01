import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_conn():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def getDoctorsBySpecialty(specialty):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT name FROM doctors WHERE LOWER(specialty) LIKE LOWER(%s)", (f"%{specialty}%",))
    doctors = [row[0] for row in cur.fetchall()]
    conn.close()
    return {"doctors": doctors}

def getDoctorAvailability(doctor_name, date, time):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT is_booked FROM availability a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE d.name=%s AND a.date=%s AND a.time=%s""",
        (doctor_name, date, time))
    result = cur.fetchone()
    conn.close()
    return {"available": result and result[0] == False}

def getAvailableSlots(doctor_name, date):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT a.time FROM availability a
        JOIN doctors d ON a.doctor_id = d.doctor_id
        WHERE d.name=%s AND a.date=%s AND a.is_booked=false""",
        (doctor_name, date))
    slots = [row[0] for row in cur.fetchall()]
    conn.close()
    return {"available_slots": slots}

def getOrCreatePatient(name, phone=None, email=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT patient_id FROM patients WHERE name=%s", (name,))
    result = cur.fetchone()
    if result:
        patient_id = result[0]
    else:
        cur.execute(
            "INSERT INTO patients (name, phone, email) VALUES (%s, %s, %s) RETURNING patient_id",
            (name, phone, email)
        )
        patient_id = cur.fetchone()[0]
        conn.commit()
    conn.close()
    return patient_id

def bookAppointment(doctor_name, date, time, patient_name, phone=None, email=None):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT doctor_id FROM doctors WHERE name=%s", (doctor_name,))
    doctor = cur.fetchone()
    if not doctor:
        conn.close()
        return {"status": "error", "message": f"Doctor {doctor_name} not found"}
    doctor_id = doctor[0]

    patient_id = getOrCreatePatient(patient_name, phone, email)

    cur.execute("SELECT is_booked FROM availability WHERE doctor_id=%s AND date=%s AND time=%s",
                (doctor_id, date, time))
    slot = cur.fetchone()
    if not slot:
        conn.close()
        return {"status": "error", "message": "Slot not found"}
    if slot[0]:
        conn.close()
        return {"status": "error", "message": "Slot already booked"}

    cur.execute("UPDATE availability SET is_booked=true WHERE doctor_id=%s AND date=%s AND time=%s",
                (doctor_id, date, time))
    cur.execute("INSERT INTO appointments (patient_id, doctor_id, date, time) VALUES (%s, %s, %s, %s)",
                (patient_id, doctor_id, date, time))
    conn.commit()
    conn.close()
    return {
        "status": "booked",
        "doctor": doctor_name,
        "date": date,
        "time": time,
        "patient": patient_name
    }
