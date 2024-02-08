import os

def getSecrets():
    secrets = {
        'MONGO_HOST':f"{os.environ.get('mongodb_host')}/?retryWrites=true&w=majority",
        'MONGO_DB_NAME':'ccpa2',
        'GOOGLE_CLIENT_ID': os.environ.get('ccpa_google_client_id'),
        'GOOGLE_CLIENT_SECRET':os.environ.get('ccpa_google_client_secret'),
        'GOOGLE_DISCOVERY_URL':"https://accounts.google.com/.well-known/openid-configuration",
        'MY_EMAIL_ADDRESS':os.environ.get('my_email_address'),
        'SPOTIFY_CLIENT_ID':os.environ.get('spotify_client_id'),
        'SPOTIFY_CLIENT_SECRET':os.environ.get('spotify_client_secret'),
        }
    return secrets