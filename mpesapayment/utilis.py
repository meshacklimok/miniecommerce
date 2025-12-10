import base64
import datetime
import requests
from requests.auth import HTTPBasicAuth
from django.conf import settings
from django.utils import timezone

def get_mpesa_token():
    url = f"{settings.MPESA_BASE_URL}/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(
        url,
        auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET)
    )
    response.raise_for_status()
    return response.json().get("access_token")

def get_timestamp():
    return timezone.now().strftime("%Y%m%d%H%M%S")

def generate_password(shortcode, passkey, timestamp):
    data = f"{shortcode}{passkey}{timestamp}"
    return base64.b64encode(data.encode()).decode()
