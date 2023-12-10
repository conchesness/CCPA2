import os

def getSecrets():
    secrets = {
        'MONGO_HOST':f"{os.environ.get('mongodb_host')}/ccpa?retryWrites=true&w=majority",
        'MONGO_DB_NAME':'ccpa2',
        'GOOGLE_CLIENT_ID': os.environ.get('ccpa2_google_client_id'),
        'GOOGLE_CLIENT_SECRET':os.environ.get('ccpa2_google_client_secret'),
        'GOOGLE_DISCOVERY_URL':"https://accounts.google.com/.well-known/openid-configuration",
        'MY_EMAIL_ADDRESS':os.environ.get('my_email_address')
        }
    return secrets


    #        'MONGO_HOST':'mongodb+srv://admin:bu11d0gz@cluster0.8m0v1.mongodb.net',
