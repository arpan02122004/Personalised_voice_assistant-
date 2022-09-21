from __future__ import print_function

import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyjokes
import PyPDF2
import webbrowser
import os
import random
import datetime
import pickle
import os.path
import subprocess
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.say('Hello Arpan \n What can I do for you today!!! ')
engine.runAndWait()


def talk(text):
    engine.say(text)
    engine.runAndWait()


'''
Authenticate website
'''
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# noinspection PyBroadException
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


def get_event(n, service):
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(now)
    talk(now)
    print("Getting the upcoming", n, " events")
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                          maxResults=10, singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
        talk(f'No Upcoming events in {n} days!!')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        talk(event['summary'] + 'at' + start)


def wiki(command):
    try:
        command = command.replace('what is', '')
    except:
        command = command.replace('who is', '')
    info = wikipedia.summary(command, sentences=5)
    print(info)
    talk(info)
    return info


def note(text):
    date = datetime.datetime.now()
    file_name = str(date).replace(":", '-') + "-note.txt"
    with open(file_name, 'w') as f:
        f.write(text)

    subprocess.Popen(['notepad.exe', file_name])


# noinspection PyBroadException,PyTypeChecker,PyStatementEffect
def run_siri():
    command = take_command()
    print(command)
    try:
        YOUTUBE_MUSIC = ['play music online', 'play music on youtube']
        for phrase in YOUTUBE_MUSIC:
            if phrase in command:
                talk('which youtube video you want me to play on youtube.')
                song = take_command()
                print('starting your video')
                talk('playing your song' + song)
                print('playing')
                pywhatkit.playonyt(song)
        TIME = ['what is time', 'what is the time', 'how much is time', 'time', 'how much is the time']
        for phrase in TIME:
            if phrase in command:
                time = datetime.datetime.now().strftime('%I:%M')
                talk('Current time is ' + time)
        JOKE = ['tell me a joke', 'tell a joke ', 'joke']
        for joke in JOKE:
            if joke in command:
                talk(pyjokes.get_jokes())
        READER = ['get me to pdf reader', 'tell me a story', 'open pdf reader', 'dictate this pdf']
        for phrase in READER:
            try:
                if phrase in command:
                    talk('Arpan, please type the path of the pdf you want to listen')
                    book_path = input('Enter the path here : ')
                    book = open(book_path, 'rb')
                    pdfReader = PyPDF2.PdfFileReader(book)
                    pages = int(pdfReader.numPages)

                    talk("Now type the page number where ypu want me to start reading")
                    pagenumber = int(input('Enter the number of page here from where you want to listen: '))
                    for num in range(pagenumber, pages):
                        page = pdfReader.getPage(int(num))
                        text = page.extractText()
                        talk(text)
            except:
                pages = pdfReader.numPages
                talk('\n' + pages)
                print(pages)
        WISH = ['wish me ', 'wish my friends', 'which my guest', 'wish my relatives', 'wish these people']
        for phrase in WISH:
            if phrase in command:
                hour = int(datetime.datetime.now().hour)
                if 0 <= hour <= 12:
                    talk('Good morning SIR!')

                elif 12 <= hour <= 18:
                    talk("Good Afternoon SIR!")
                else:
                    talk('Good Evening SIR!')
                time = datetime.datetime.now().strftime('%I:%M')
                talk(' and Current time is ' + time)
        WEBSITE = ['go to this website', 'go to this site', 'go to ', 'website']
        for phrase in WEBSITE:
            if phrase in command:
                try:
                    command = command.replce(phrase, '')
                    if 'google.com' in command:
                        try:
                            webbrowser.open_new_tab('www.google.com')
                        except:
                            c = webbrowser.get('chrome')
                            c.open('www.google.com')
                    elif 'facebook.com' in command:
                        try:
                            webbrowser.open_new_tab('www.facebook.com')
                        except:
                            c = webbrowser.get('chrome')
                            c.open('www.facebook.com')
                    elif 'youtube.com' in command:
                        try:
                            webbrowser.open_new_tab('www.youtube.com')
                        except:
                            c = webbrowser.get('chrome')
                            c.open('www.youtube.com')
                    elif 'github.com' in command:
                        try:
                            webbrowser.open_new_tab('www.github.com.com')
                        except:
                            c = webbrowser.get('chrome')
                            c.open('www.github.com')
                    else:
                        print(command)
                        talk('The URL is not inserted in program !!, PLEASE TYPE IN THE URL... ')
                        remaining = input(str('Just type in the remaining url : '))
                        command = command.append(remaining)
                        webbrowser.open(command)
                except:
                    talk('Website is not being recognised, please input the \n url of the website manually! ')
                    websiteURL = input(str('Enter the website url here : '))
                    webbrowser.open(websiteURL)
        EVENT = ['what are the coming events', 'list of events', 'show list of events', 'get list of events',
                 'next events', 'calendar']
        for phrase in EVENT:
            if phrase in command:
                service = googlecalander_authentication()
                talk('Enter the number of events you want to get ')
                n = int(input('Enter the number of event you want to get : '))
                get_event(n, service)
        WIKIPEDIA = ['what is', 'who is', 'which is ', 'search for']
        for phrase in WIKIPEDIA:
            if phrase in command:
                talk('finding')
                print('finding....')
                com = command.replace(phrase, '')
                wiki(com)
        OFFLINE_MUSIC = ['open groove', 'play music offline', 'play offline music']
        for phrase in OFFLINE_MUSIC:
            if phrase in command:
                music_dir = 'H:\\my songs\\Songs'
                songs = os.listdir(music_dir)
                os.startfile(os.path.join(music_dir, songs[random.randint(1, 50)]))
        PHOTOS = ['show me my', ' open my photos', 'open photos folder']
        for phrase in PHOTOS:
            if phrase in command:
                photos_dir = 'F:\\ALL PHOTOS'
                os.startfile(os.path.join(photos_dir))
        PROGRAMS = ['start', 'open']
        for phrase in PROGRAMS:
            if phrase in command:
                try:
                    if 'pycharm' in command:
                        pycharm = 'C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.2.2\\bin\\pycharm64.exe'
                        os.startfile(pycharm)
                    elif 'java editor' in command:
                        java_ide = 'C:\\Program Files\\JetBrains\\IntelliJ IDEA Community Edition 2020.2\\bin\\idea64.exe'
                        os.startfile(java_ide)
                    elif 'visual studio code' in command:
                        visual = 'G:\\Users\\arpan\\Programs\\Microsoft VS Code\\Code.exe'
                        os.startfile(visual)
                    elif 'chrome' in command:
                        chrome = 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
                        os.startfile(chrome)
                    elif 'event manager' in command:
                        event_manager = 'event_manager.py'
                        os.startfile(event_manager)
                except Exception as eas:
                    print('Exception : ', eas)
        NEW_FILE = ['create a new', 'make a note', 'start a new']
        for phrase in NEW_FILE:
            if phrase in command:
                if 'python' in command:
                    date = datetime.datetime.now()
                    file_name = str(date).replace(":", '-') + "-new.py"
                    with open(file_name, 'w') as f:
                        f.write('start writing from here ....\n')

                    thonny = 'C:\\Users\\arpan\\AppData\\Local\\Programs\\Thonny\\thonny.exe'
                    subprocess.Popen(thonny, [file_name])
                if 'note' in command:
                    talk('What do i make note of?')
                    note = take_command()
                    note(note)
                    talk('I have made note of that!')
                if 'html' in command:
                    date = datetime.datetime.now()
                    file_name = str(date).replace(":", '-') + "-new.py"
                    with open(file_name, 'w') as f:
                        f.write('start writing from here ....\n')

                    visual_studio_code = 'G:\\Users\\arpan\\Programs\\Microsoft VS Code\\Code.exe'
                    subprocess.Popen(visual_studio_code, [file_name])
                else:
                    talk('please specify the type of document you want to create!')
                    ask = str(input('Enter the filename here : '))
                    date = datetime.datetime.now()
                    file_name = str(date).replace(":", '-') + ask
                    with open(file_name, 'w') as f:
                        f.write('start writing from here ....\n')
                    talk('now choose the editor you want to open the file with : ')
                    print('1. notepad\n2. pycharm\n3. visual studio code\n4. IntelliJ\n5. Thonny')
                    editor = int(input('Enter the number of your choice here : '))
                    if editor == 1:
                        subprocess.Popen('notepad.exe', [file_name])
                    elif editor == 2:
                        pycharm = 'C:\\Program Files\\JetBrains\\PyCharm Community Edition 2020.2.2\\bin\\pycharm64.exe'
                        subprocess.Popen(pycharm, [file_name])
                    elif editor == 3:
                        visual_studio_code = 'G:\\Users\\arpan\\Programs\\Microsoft VS Code\\Code.exe'
                        subprocess.Popen(visual_studio_code, [file_name])
                    elif editor == 4:
                        java_ide = 'C:\\Program Files\\JetBrains\\IntelliJ IDEA Community Edition 2020.2\\bin\\idea64.exe'
                        subprocess.Popen(java_ide, [file_name])
                    else:
                        thonny = 'C:\\Users\\arpan\\AppData\\Local\\Programs\\Thonny\\thonny.exe'
                        subprocess.Popen(thonny, [file_name])

        NEW_NAME = ['what could be your new name', 'what should be your new name', 'tell me a good new name for you']
        for phrase in NEW_NAME:
            if phrase in command:
                talk(
                    "I don't the answer of these type of questions, give me any name just not these 'Jarvis', 'Alexa', 'Siri', 'google_assistant' because they are not original")
        if 'quit' in command:
            talk('Conform by pressing "quit" you really want to quit')
            try:
                quit = str(input('Enter you answer here : '))
                quit: str = quit.lower()
                if 'quit' == quit:
                    exit()
            except Exception as ases:
                print('Exception : ' + ases)
        elif '' == command:
            talk('You have said nothing... please ask me something what i can do or quit()...')
            print('Ask something else.....')
        else:
            talk("I don't know the answer of this question please ask me anything else")

    except Exception as ea:
        print('Exception : ', ea)
        pass


while True:
    try:
        run_siri()
    except Exception as e:
        print('Exception : ', e)
        pass
