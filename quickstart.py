import datetime
import os.path

from ai import accessAI
from input import getEventInput

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

creds = None
service = None

def setup_authentication():
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  global creds
  if os.path.exists("token.json"):
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())

def get_events(service):
  # Call the Calendar API
  now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
  print("Getting the upcoming 20 events")
  events_result = (
      service.events()
      .list(
          calendarId="primary",
          timeMin=now,
          maxResults=20,
          singleEvents=True,
          orderBy="startTime",
      )
      .execute()
  )
  events = events_result.get("items", [])

  if not events:
    print("No upcoming events found.")
    return

  content = ""
  # Prints the start and name of the next 20 events
  for event in events:
    date_and_time = event["start"].get("dateTime", event["start"].get("date"))
    print(date_and_time, event["summary"])
    summary = event["summary"]
    content = content + " " + date_and_time + " " + summary + "\n"
  
  return content

def main():
  """SmartCalendar"""
  global creds
  content = ""
  
  setup_authentication()

  try:
    service = build("calendar", "v3", credentials=creds)
    content = get_events(service)

    query = "Organize these events:\n"
    aiRequestResult = accessAI(query + "" + content)
    print(aiRequestResult)

  except HttpError as error:
    print(f"An error occurred: {error}")

if __name__ == "__main__":
  main()