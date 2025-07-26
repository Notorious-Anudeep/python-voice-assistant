import pyttsx3  # For text to speech conversion
import speech_recognition as sr  # For speech recognition
import wikipedia  # For accessing Wikipedia
import webbrowser  # For opening web pages
import requests  # For fetching weather data
import time  # For getting the current time
import threading  # For the timer

# Initializing the speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Female voice
engine.setProperty('rate', 120)  # Speech rate

# Inactivity timeout (in seconds)
INACTIVITY_TIMEOUT = 120  # 2 minutes

# Greet the user
engine.say("Hi, I am Boomer, your voice assistant. How can I help you?")
engine.runAndWait()


# Function to listen to the user's voice and return the text
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        print("Recognizing...")
        text = r.recognize_google(audio)
        print(f"You said: {text}")
    except sr.UnknownValueError:
        print("Sorry, I could not understand that.")
        text = ""
    return text


# Function to fetch weather information using OpenWeatherMap API
def get_weather(city):
    api_key = "5903e9975d0c693659c746bdeae1edfb"  # Your OpenWeatherMap API key
    base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(base_url)
        data = response.json()

        # Check if the API call was successful
        if data.get("cod") == 200:  # Status code 200 means success
            weather_desc = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            return f"The weather in {city} is {weather_desc} with a temperature of {temperature} degrees Celsius."
        else:
            return f"Sorry, I couldn't find the weather information for {city}. Please try another city."

    except Exception as e:
        return "Sorry, I encountered an error while fetching the weather information."


# Function to respond to the user's query
def respond(text):
    if "hello boomer" in text.lower():
        engine.say("Hello, nice talking to you. How was your day?")
        engine.runAndWait()
        day = listen()
        if "good" in day.lower():
            engine.say("I'm glad to hear that. God made your day.")
        elif "bad" in day.lower():
            engine.say("I'm sorry to hear that. What happened?")
        else:
            engine.say("I hope everything goes well.")
        engine.runAndWait()

    # Current Time feature
    elif "current time" in text.lower():
        current_time = time.strftime("%I:%M %p")
        engine.say(f"The current time is {current_time}")
        engine.runAndWait()

    # Wikipedia feature
    elif "wikipedia" in text.lower():
        engine.say("Searching Wikipedia...")
        engine.runAndWait()
        text = text.replace("wikipedia", "")
        results = wikipedia.summary(text, sentences=2)
        engine.say("According to Wikipedia,")
        engine.say(results)
        engine.runAndWait()

    # Open a Website feature
    elif "open a website" in text.lower():
        engine.say("What website do you want to open?")
        engine.runAndWait()
        website = listen()
        if website:
            webbrowser.open(f"https://{website}")
            engine.say(f"Opening {website}")
            engine.runAndWait()

    # Weather feature
    elif "weather" in text.lower():
        engine.say("Which city would you like the weather for?")
        engine.runAndWait()
        city = listen()
        if city:
            weather_report = get_weather(city)
            engine.say(weather_report)
            engine.runAndWait()

    # YouTube feature
    elif "youtube" in text.lower():
        engine.say("Opening YouTube...")
        engine.runAndWait()
        webbrowser.open("https://www.youtube.com")

    # Reminder/Schedule feature (basic placeholder)
    elif "schedule" in text.lower():
        engine.say("What task do you want to schedule?")
        engine.runAndWait()
        task = listen()
        engine.say("When do you want to schedule it?")
        engine.runAndWait()
        schedule_time = listen()  # Capture the time
        # Logic for scheduling can be implemented later
        engine.say(f"Task {task} scheduled at {schedule_time}.")
        engine.runAndWait()

    # Goodbye feature
    elif "goodbye" in text.lower():
        engine.say("Goodbye, have a nice day.")
        engine.runAndWait()
        exit()

    # Fallback in case the command is not recognized
    else:
        engine.say("Sorry, I did not get that. Please try again.")
        engine.runAndWait()


# Timer to automatically close after inactivity
def inactivity_timer():
    global timer
    timer = threading.Timer(INACTIVITY_TIMEOUT, exit_due_to_inactivity)
    timer.start()


# Function to exit due to inactivity
def exit_due_to_inactivity():
    engine.say("No activity detected for 2 minutes. Goodbye.")
    engine.runAndWait()
    exit()


# Main loop to keep listening and responding until the user says "goodbye"
def main_loop():
    inactivity_timer()  # Start the inactivity timer
    while True:
        text = listen()
        if text:  # If the text is not empty
            timer.cancel()  # Reset the inactivity timer
            respond(text)
            inactivity_timer()  # Restart the timer after each interaction


main_loop()