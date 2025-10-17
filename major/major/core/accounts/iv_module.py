import threading
import time
import random  # remove when sensors are used
from django.utils import timezone
from .models import IVBag


# Threshold for low IV alert
THRESHOLD = 20  # 20%

# Flag to toggle between demo (dummy values) and real sensor
USE_DEMO = True


# Function to get IV level
def get_iv_level(patient_id):
    """
    Returns current IV bag level for a patient.
    In demo mode: returns dummy decreasing value.
    In real sensor mode: replace this function to read sensor.
    # Function to get IV level (dummy for demo / placeholder for real sensor)
# def get_iv_level(patient_id):

     iv_bag, created = IVBag.objects.get_or_create(patient_id=patient_id)
     
     if USE_DEMO:
         # Simulate draining
         if iv_bag.level is None or iv_bag.level <= 0:
             iv_bag.level = 100  # reset full bag for demo
         else:
             iv_bag.level -= random.randint(5, 15)  # decrease randomly
     else:
         # TODO: Replace with sensor reading code
         # Example: iv_bag.level = read_sensor(patient_id)
         pass
 
     iv_bag.last_updated = timezone.now()
     iv_bag.save()
     return iv_bag.level

    """
    iv_bag, created = IVBag.objects.get_or_create(patient_id=patient_id)
    
    if USE_DEMO:
        # Simulate draining
        if iv_bag.level is None or iv_bag.level <= 0:
            iv_bag.level = 100  # reset full bag for demo       
        else:
            iv_bag.level -= random.randint(5, 15)  # decrease randomly
    else:
        # TODO: Replace with sensor reading code
        # Example: iv_bag.level = read_sensor(patient_id)
        pass

    iv_bag.last_updated = timezone.now()
    iv_bag.save()
    return iv_bag.level

# Check and trigger alert
def check_iv_alert(patient_id):
    iv_bag = IVBag.objects.get(patient_id=patient_id)
    if iv_bag.level <= THRESHOLD:
        # Here you can trigger alert (console print, beep, SMS)
        print(f"⚠ ALERT: IV bag low for {iv_bag.patient.name} - {iv_bag.level}%")

# Background thread to simulate IV updates
def run_iv_simulation():
    while True:
        for iv_bag in IVBag.objects.all():
            get_iv_level(iv_bag.patient.id)
            check_iv_alert(iv_bag.patient.id)
        time.sleep(5)  # update every second

# Start the simulation thread when server starts
threading.Thread(target=run_iv_simulation, daemon=True).start()
