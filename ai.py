import pyttsx3 as p
import speech_recognition as sr



engine=p.init()
rate=engine.getProperty('rate')
engine.setProperty('rate',180)
voices=engine.getProperty('voices')
engine.setProperty('voice',voices[1].id)
print(voices)
engine.say("hello world. my name is boomer iam your voice assistant")
engine.runAndWait()

r=sr.Recognizer()