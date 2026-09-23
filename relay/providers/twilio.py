import os
import urllib.parse

from relay.http import request_json
from relay.text import chunk_text


def send(message: str) -> None:
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID", "").strip()
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN", "").strip()
    from_number = os.environ.get("TWILIO_FROM", "").strip()
    to_number = os.environ.get("TWILIO_TO", "").strip()
    messaging_service_sid = os.environ.get("TWILIO_MESSAGING_SERVICE_SID", "").strip()

    if not account_sid or not auth_token or not to_number:
        raise RuntimeError(
            "Twilio requires TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN and TWILIO_TO"
        )
    if not from_number and not messaging_service_sid:
        raise RuntimeError("Twilio requires TWILIO_FROM or TWILIO_MESSAGING_SERVICE_SID")

    sid = urllib.parse.quote(account_sid, safe="")
    url = f"https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json"
    for chunk in chunk_text(message, 1500):
        form = {"To": to_number, "Body": chunk}
        if messaging_service_sid:
            form["MessagingServiceSid"] = messaging_service_sid
        else:
            form["From"] = from_number
        _, result = request_json(
            "POST", url, form_body=form, basic_auth=(account_sid, auth_token)
        )
        if not result.get("sid"):
            raise RuntimeError(
                f"Twilio rejected request: {result.get('message', 'missing message sid')}"
            )
