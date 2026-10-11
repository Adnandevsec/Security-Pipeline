#Async Alerts - Sends welcome emails upon sign-up or login alerts (can listen to events or be triggered via API).
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI(title="Notification Service")

class Notification(BaseModel):
    recipient: EmailStr
    message: str

@app.get("/healthz")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/notify")
async def send_notification(notification: Notification):
    # Logic to send email/slack notification
    print(f"Sending email to {notification.recipient}: {notification.message}")
    return {"status": "sent", "recipient": notification.recipient}