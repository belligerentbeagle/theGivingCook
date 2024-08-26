import os.path
import streamlit as st
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage

class EmailSender:
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly",
              'https://www.googleapis.com/auth/gmail.send',
              'https://www.googleapis.com/auth/gmail.modify']

    def __init__(self):
        self.creds = None

    def authenticate_user(self):
        if os.path.exists("./config/token.json"):
            self.creds = Credentials.from_authorized_user_file("./config/token.json", self.SCOPES)

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "./config/credentials.json", self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            with open("./config/token.json", "w") as token:
                token.write(self.creds.to_json())

    def test_api(self):
        """Shows basic usage of the Gmail API. Lists the user's Gmail labels."""
        self.authenticate_user()

        try:
            service = build("gmail", "v1", credentials=self.creds)
            results = service.users().labels().list(userId="me").execute()
            labels = results.get("labels", [])

            if not labels:
                print("No labels found.")
                return
            print("Labels:")
            for label in labels:
                print(label["name"])

        except HttpError as error:
            print(f"An error occurred: {error}")

    def send_message(self, recipient_email="", subject="", body=""):
        """Create and send an email message"""
        self.authenticate_user()

        try:
            service = build("gmail", "v1", credentials=self.creds)
            message = EmailMessage()

            message.set_content(body)
            message["To"] = recipient_email
            message["From"] = "gduser2@workspacesamples.dev"
            message["Subject"] = subject
            
            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
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

        return send_message

    def email_sender(self, email, subject, body):
        self.test_api()
        self.send_message(email, subject, body)

# Usage:
# if __name__ == "__main__":
#     sender = EmailSender()
#     sender.email_sender("recipient@example.com", "Test Subject", "Test Body")