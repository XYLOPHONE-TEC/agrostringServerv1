import requests
from django.conf import settings

def send_sms_africastalking(phone_number, message):
    url = "https://api.sandbox.africastalking.com/version1/messaging/bulk"
    
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "apiKey": settings.AFRICASTALKING_API_KEY,
    }

    payload = {
        "username": settings.AFRICASTALKING_USERNAME,
        "message": message,
        "senderId": settings.AFRICASTALKING_SENDER_ID,
        "phoneNumbers": [phone_number],  # must be a list
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        print("SMS response:", data)  # Log for now
        return data
    except Exception as e:
        print("SMS send error:", e)
        return None
