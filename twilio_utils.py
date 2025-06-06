import os
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

# Twilio setup
account_sid = "AC9995db683a0351c6527e93ee7a4f3b82"
auth_token = "a352936033b4fa24d8d032fbb963f092"

if not account_sid or not auth_token:
    raise Exception("Twilio credentials not found. Set them in .env (locally) or Streamlit Secrets (in cloud).")
    
client = Client(account_sid, auth_token)

def fetch_call_logs(limit=20):
    calls = client.calls.list(limit=limit)
    call_data = []

    for call in calls:
        call_data.append({
            "caller": call.from_formatted,
            "phone": call.to_formatted,
            "timestamp": call.start_time.strftime("%Y-%m-%d %H:%M:%S") if call.start_time else "",
            "duration": f"{int(call.duration)//60:02}:{int(call.duration)%60:02}" if call.duration else "00:00",
            "status": call.status.capitalize()
        })

    return call_data

def fetch_call_recordings(limit=10):
    recordings = client.recordings.list(limit=limit)
    rec_data = []

    for rec in recordings:
        # Get related call for context
        call = client.calls(rec.call_sid).fetch()
        rec_data.append({
            "caller": call.from_formatted,
            "date": rec.date_created.strftime("%Y-%m-%d"),
            "duration": f"{int(rec.duration)//60:02}:{int(rec.duration)%60:02}" if rec.duration else "00:00",
            "url": f"https://api.twilio.com{rec.uri.replace('.json', '.mp3')}"
        })

    return rec_data


