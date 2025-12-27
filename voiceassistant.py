import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
import pyjokes
from openai import OpenAI

client = OpenAI(api_key="secuirty reason i cant give you if you want then generate in you laptoop")

engine = pyttsx3.init()
engine.setProperty('rate', 165)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        command = command.lower()
        print("You:", command)
        return command
    except:
        speak("Sorry, I did not understand")
        return ""

def ai_chat(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a friendly smart voice assistant"},
                {"role": "user", "content": question}
            ]
        )
        return response.choices[0].message.content
    except:
        return "Sorry, my AI service is temporarily unavailable."

def run_assistant():
    speak("listen, what you have to do today")

    while True:
        command = take_command()

        if command == "":
            continue

        if "time" in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak("The current time is " + current_time)

        elif "date" in command:
            current_date = datetime.datetime.now().strftime('%d %B %Y')
            speak("Today's date is " + current_date)

        elif "wikipedia" in command:
            speak("Searching Wikipedia")
            query = command.replace("wikipedia", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except:
                speak("Sorry, I could not find this on Wikipedia")

        elif "play" in command:
            song = command.replace("play", "")
            speak("Playing " + song)
            pywhatkit.playonyt(song)

        elif "search" in command:
            query = command.replace("search", "")
            speak("Searching Google")
            pywhatkit.search(query)

        elif "open google" in command:
            speak("Opening Google")
            webbrowser.open("https://google.com")

        elif "open youtube" in command:
            speak("Opening YouTube")
            webbrowser.open("https://youtube.com")

        elif "joke" in command or "make me laugh" in command:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "exit" in command or "stop" in command or "quit" in command:
            speak("Goodbye, have a nice day")
            break

        else:
            speak("Let me think")
            answer = ai_chat(command)
            speak(answer)

run_assistant()
