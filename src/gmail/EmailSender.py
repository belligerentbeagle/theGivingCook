import os.path
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",'https://www.googleapis.com/auth/gmail.send','https://www.googleapis.com/auth/gmail.modify']

def test_api():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  creds = authenticate_user()

  try:
    # Call the Gmail API
    service = build("gmail", "v1", credentials=creds)
    results = service.users().labels().list(userId="me").execute()
    labels = results.get("labels", [])

    if not labels:
      print("No labels found.")
      return
    print("Labels:")
    for label in labels:
      print(label["name"])

  except HttpError as error:
    # TODO(developer) - Handle errors from gmail API.
    print(f"An error occurred: {error}")

def authenticate_user():
  creds = None

  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("./config/token.json"):
    creds = Credentials.from_authorized_user_file("./config/token.json", SCOPES)

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
        "./config/credentials.json", SCOPES
    )
      creds = flow.run_local_server(port=0)

  # Save the credentials for the next run
    with open("./config/token.json", "w") as token:
      token.write(creds.to_json())
  return creds


def send_message(recipientEmail="", subject="", body=""):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  # creds, _ = google.auth.default()
  creds = authenticate_user()

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content(body)

    message["To"] = recipientEmail
    message["From"] = "gduser2@workspacesamples.dev"
    message["Subject"] = subject
    
    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')

  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None

  st.write("Email sent successfully!: ", send_message)
  return send_message

# def emailSender():
#   test_api()
#   message_sent = send_message("mahc081203@gmail.com")

# if __name__ == "__main__":
#     emailSender()