from langchain.tools import tool
from services.db import getDoctorsBySpecialty, getDoctorAvailability, getAvailableSlots, bookAppointment as _bookAppointment

# Wrap DB functions as LangChain tools
#                                                                                                                                                                                                             
@tool
def check_specialty(specialty: str) -> dict:                                                                                                                                                              
    """Find doctors at the clinic by their medical specialty."""
    return getDoctorsBySpecialty(specialty)                                                                                                                                                               
   
@tool                                                                                                                                                                                                     
def check_slot(doctor_name: str, date: str, time: str) -> dict:
    """Check if a specific time slot is available for a doctor."""                                                                                                                                        
    return getDoctorAvailability(doctor_name, date, time)
                                                                                                                                                                                                            
@tool           
def get_slots(doctor_name: str, date: str) -> dict:                                                                                                                                                       
    """Get all available time slots for a doctor on a given date."""
    return getAvailableSlots(doctor_name, date)                                                                                                                                                           
   
@tool                                                                                                                                                                                                     
def book_appointment(doctor_name: str, date: str, time: str, patient_name: str, phone: str = None, email: str = None) -> dict:
    """Book an appointment for a patient with a doctor."""                                                                                                                                                
    return _bookAppointment(doctor_name, date, time, patient_name, phone, email)