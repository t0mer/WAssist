import os
import os.path
from loguru import logger
from datetime import datetime, timedelta, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build

# If modifying these scopes, make sure to grant appropriate permissions in the Google Cloud Console.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
CREDENTIALS_PATH = os.getenv("CAL_CREDS")
CALENDAR_ID = os.getenv("CALENDAR_ID")

class GoogleCal():
    

    def get_events(self):
        self.events = ""
        try:
            # Create a service account credentials object
            creds = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)

            # Build the Google Calendar API service
            service = build('calendar', 'v3', credentials=creds)

            # Call the Calendar API
            now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            logger.info('Getting the upcoming 10 events')
            events_result = service.events().list(calendarId=CALENDAR_ID, timeMin=now, maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])
            current_time = datetime.now(timezone.utc)
            future_time = current_time + timedelta(hours=24)
            if not events:
                logger.warning('No upcoming events found.')
                return 'No upcoming events found.'

            # Prints the start and name of the next 10 events
            for event in events:
                start = event['start'].get('dateTime', event['start'].get('date'))
                event_datetime = datetime.fromisoformat(start)
                if event_datetime < future_time:
                    self.events = self.events + "*" + event['summary'] + "*\n" + datetime.fromisoformat(start).strftime("%d/%m/%Y %H:%M") + "\n"
            return self.events


        except Exception as e:
            logger.error('An error occurred: %s' % str(e))
            return("aw snap something went wrong")

print(GoogleCal().get_events())