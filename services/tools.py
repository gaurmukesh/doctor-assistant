TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "getDoctorsBySpecialty",
            "description": "Find doctors at the clinic by their specialty",
            "parameters": {
                "type": "object",
                "properties": {
                    "specialty": {"type": "string"}
                },
                "required": ["specialty"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "getDoctorAvailability",
            "description": "Check doctor availability for a given date/time",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"},
                    "date": {"type": "string"},
                    "time": {"type": "string"}
                },
                "required": ["doctor_name", "date", "time"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "getAvailableSlots",
            "description": "Get all available time slots for a doctor on a given date",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"},
                    "date": {"type": "string"}
                },
                "required": ["doctor_name", "date"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "bookAppointment",
            "description": "Book an appointment with a doctor",
            "parameters": {
                "type": "object",
                "properties": {
                    "doctor_name": {"type": "string"},
                    "date": {"type": "string"},
                    "time": {"type": "string"},
                    "patient_name": {"type": "string"},
                    "phone": {"type": "string"},
                    "email": {"type": "string"}
                },
                "required": ["doctor_name", "date", "time", "patient_name"]
            }
        }
    }
]
