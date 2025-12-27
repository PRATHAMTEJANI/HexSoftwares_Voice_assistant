import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import webbrowser
import pyjokes
from openai import OpenAI

client = OpenAI(api_key="YOUR_API_KEY_HERE")

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
        command = recognizer.recognize_google(audio, language="en-IN")
        command = command.lower()
        print("You:", command)
        return command
    except:
        speak("माफ़ कीजिए, मैं समझ नहीं पाया")
        return ""

def ai_chat(question):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a smart bilingual voice assistant. Reply in the same language as the user (Hindi or English)."
                },
                {
                    "role": "user",
                    "content": question
                }
            ]
        )
        return response.choices[0].message.content
    except:
        return "अभी मेरी AI सेवा उपलब्ध नहीं है"

def run_assistant():
    speak("नमस्ते, मैं आपका स्मार्ट वॉइस असिस्टेंट हूँ")

    while True:
        command = take_command()

        if command == "":
            continue

        if "time" in command or "समय" in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            speak("अभी का समय है " + current_time)

        elif "date" in command or "तारीख" in command:
            current_date = datetime.datetime.now().strftime('%d %B %Y')
            speak("आज की तारीख है " + current_date)

        elif "wikipedia" in command or "विकिपीडिया" in command:
            speak("विकिपीडिया पर खोज रहा हूँ")
            query = command.replace("wikipedia", "").replace("विकिपीडिया", "")
            try:
                result = wikipedia.summary(query, sentences=2)
                speak(result)
            except:
                speak("माफ़ कीजिए, जानकारी नहीं मिली")

        elif "play" in command or "चलाओ" in command or "प्ले" in command:
            song = command.replace("play", "").replace("चलाओ", "").replace("प्ले", "")
            speak(song + " चला रहा हूँ")
            pywhatkit.playonyt(song)

        elif "search" in command or "खोजो" in command:
            query = command.replace("search", "").replace("खोजो", "")
            speak("गूगल पर खोज रहा हूँ")
            pywhatkit.search(query)

        elif "open google" in command or "गूगल खोलो" in command:
            speak("गूगल खोल रहा हूँ")
            webbrowser.open("https://google.com")

        elif "open youtube" in command or "यूट्यूब खोलो" in command:
            speak("यूट्यूब खोल रहा हूँ")
            webbrowser.open("https://youtube.com")

        elif "joke" in command or "मजाक" in command or "हंसाओ" in command:
            joke = pyjokes.get_joke()
            speak(joke)

        elif "exit" in command or "stop" in command or "quit" in command or "बंद" in command:
            speak("अलविदा, आपका दिन शुभ हो")
            break

        else:
            speak("सोचने दीजिए")
            answer = ai_chat(command)
            speak(answer)

run_assistant()
