from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import speech_recognition as sr
import pyttsx3
import pytz
import subprocess

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.say('Hello Arpan \n What can I do for you today!!! ')
engine.runAndWait()


def talk(call):
    engine.say(call)
    engine.runAndWait()


def take_command():
    try:
        with sr.Microphone() as source:
            print('Listening....')
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if 'siri' in command:
                command = command.replace('siri', "")
                talk(command)
    except:
        talk('Speak Again You said nothing and I am waiting!')
        pass
    return command


# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
          "december"]
DAYS = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]


def googlecalander_authentication():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service


# noinspection PyTypeChecker
def event_manager(day, service):
    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        talk('No event on that day')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        start_time = str(start.split('T')[1].split('-')[0])
        if not int(start_time.split(':')[0]) <= 12:
            start_time = start_time + 'am'
        else:
            start_time = str(int(start_time.split(":")[0]) - 12) + start_time.split(':')[1]
            start_time = start_time + 'pm'
        talk(event['summary' + 'at' + start_time])


def get_event(n, service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    now2 = str(datetime.datetime.utcnow().isoformat() + 'Z')

    talk(now2)
    print(now)
    print('Getting the upcoming', {n}, 'events')
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=n, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        talk('No upcoming Events')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        talk(event['summary'] + 'at' + start)


def get_date(text):
    text = text.lower()
    today = datetime.date.today()

    if text.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year
    for word in text.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass
    if month < today.month and month != -1:
        year = year + 1
    if day < today.day and month == -1 and day != -1:
        month = month + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if text.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None
    return datetime.date(month=month, day=day, year=year)
def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":",'-') + "-note.txt"
    with open(file_name, 'w') as f:
        f.write(text)

    subprocess.Popen(['notepad.exe', file_name])

service = googlecalander_authentication()
print('start')

while True:
    print('Listning...')
    command = take_command()
    Wake = 'siri'

    if command.count(Wake) > 0:
        talk('I am ready')
        text = command
        if 'calculate' in text:
            n = int(take_command())
            get_event(n, service)
        CALANDER_STRS = ['what do i have', 'do i have plans', 'am i busy', 'what is']
        for phrase in CALANDER_STRS:
            if phrase in text:
                date = get_date(text)
                if date:
                    event_manager(date, service)
                else:
                    talk("I don't under stand")
        NOTE_STRS = ['make a note', 'write this down', 'remember this']
        for phrase in NOTE_STRS:
            if phrase in NOTE_STRS:
                talk('What do i make note of?')
                note = take_command()
                note(note)
                talk('I have made note of that!')