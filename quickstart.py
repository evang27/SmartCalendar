import datetime
import os.path
import json

from ai import accessAI
from input import getEventInput

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar"]

def setup_authentication():
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  creds = None
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
  return creds

def get_events(service, amount):
  # Call the Calendar API
  now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
  print("Getting the upcoming " + str(amount) + " events")
  events_result = (
      service.events()
      .list(
          calendarId="primary",
          timeMin=now,
          maxResults=amount,
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
  for event in events:
    date_and_time = event["start"].get("dateTime", event["start"].get("date"))
    print(date_and_time, event["summary"])
    summary = event["summary"]
    content = content + " " + date_and_time + " " + summary + "\n"
  
  return content

def main():
  """SmartCalendar"""
  creds = setup_authentication()

  try:
    service = build("calendar", "v3", credentials=creds)

    content = get_events(service, 50)

    input = getEventInput()

    # event = {
    #   'summary': 'Google I/O 2015',
    #   'location': '800 Howard St., San Francisco, CA 94103',
    #   'description': 'A chance to hear more about Google\'s developer products.',
    #   'start': {
    #     'dateTime': '2024-09-10T09:00:00-04:00',
    #     'timeZone': 'America/New_York',
    #   },
    #   'end': {
    #     'dateTime': '2024-09-10T17:00:00-04:00',
    #     'timeZone': 'America/New_York',
    #   },
    #   'recurrence': [
    #     'RRULE:FREQ=DAILY;COUNT=2'
    #   ],
    #   'reminders': {
    #     'useDefault': False,
    #     'overrides': [
    #       {'method': 'popup', 'minutes': 10},
    #     ],
    #   },
    # }

    query = "It is currently: " + str(datetime.datetime.now()) + ".\nThe following is a list of the user's upcoming events:\n" + content + " Now, the following is a description of the event the user wants to add:\n" + input + "Create the json object for an upcoming event somewhere in the user's schedule that matches their description. Always try to have a minimum of 15 minutes between events where nothing is scheduled."
    aiRequestResult = accessAI(query)
  
    if (aiRequestResult[:7] == '```json'):
      aiRequestResult = aiRequestResult[8:]
      print("stripped json beginning")

    if (aiRequestResult[-3:] == '```'):
      aiRequestResult = aiRequestResult[:-4]
      print("stripped json ending")

    print(aiRequestResult)
    event = json.loads(aiRequestResult)
    event = service.events().insert(calendarId='primary', body=event).execute()
    print('Event created: %s' % (event.get('htmlLink')))

  except HttpError as error:
    print(f"An error occurred: {error}")

if __name__ == "__main__":
  main()