import smtplib
import msal
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import base64
import logging
import json


# Email details
TO_EMAIL = "steve@yopmail.com"  # recipient
SUBJECT = "Test Email from Azure AD OAuth"
BODY = "This is a test email sent using Azure AD OAuth and SMTP in python"


# Load conf file with the sensitive stuff
with open("conf.json", "r") as file:
    conf = json.load(file)

# retrieve Azure AD App registration details from config file
CLIENT_ID = conf["clientId"]  # Application (client) ID from Azure AD
CLIENT_SECRET = conf["clientSecret"]  # Client secret from Azure AD
TENANT_ID = conf["tenantId"]  # Tenant ID from Azure AD
AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"

# SMTP details (Exchange Online SMTP)
FROM_EMAIL = conf["fromEmail"]
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587


# Step 1: Get the OAuth token using MSAL (Microsoft Authentication Library)
def get_oauth_token():
    app = msal.ConfidentialClientApplication(
        CLIENT_ID, authority=AUTHORITY, client_credential=CLIENT_SECRET
    )

    # Request the OAuth token
    result = app.acquire_token_for_client(
        scopes=["https://outlook.office365.com/.default"]
    )

    if "access_token" in result:
        return result["access_token"]
    else:
        raise Exception(f"Could not obtain token: {result.get('error_description')}")


# Function to perform OAuth2 SMTP authentication
def oauth2_login(smtp_server, smtp_port, access_token, from_email):
    auth_string = f"user={from_email}\x01auth=Bearer {access_token}\x01\x01"
    auth_string = base64.b64encode(auth_string.encode("utf-8")).decode("utf-8")

    # Create SMTP connection
    server = smtplib.SMTP(smtp_server, smtp_port)
    # server.set_debuglevel(1)
    server.starttls()  # Secure the connection

    server.ehlo()  # !!! this is what smtp server from ms expects, otherwise 503

    response = server.docmd(
        "AUTH", f"XOAUTH2 {auth_string}"
    )  # Use XOAUTH2 authentication

    logging.info(response)

    return server


# Function to send email using OAuth2 with SMTP
def send_email_via_smtp(oauth_token, from_email, to_email, subject, body):
    # Create the email message
    message = MIMEMultipart()
    message["From"] = from_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Authenticate and send email
        server = oauth2_login(SMTP_SERVER, SMTP_PORT, oauth_token, from_email)
        server.sendmail(from_email, to_email, message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")
    finally:
        server.quit()


# Main function
def main():
    # Authenticate using OAuth token
    oauth_token = get_oauth_token()

    if oauth_token:
        send_email_via_smtp(oauth_token, FROM_EMAIL, TO_EMAIL, SUBJECT, BODY)


if __name__ == "__main__":
    main()
