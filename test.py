import requests
import pyttsx3 as p
import speech_recognition as sr
import time
from datetime import date


"""url = "http://api.weatherapi.com/v1/current.json?key=9d1a06cf296748bba91154256201606&q=77494"
response = requests.get(url)

get_response = response.json()


print(get_response)

init = p.init()
init.setProperty('rate', 150)
init.setProperty("volume", 0.8)
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
init.setProperty("voice", voice_id)
init.say("pulling up weather conditions")
init.say("the conditions are")
init.say(str(get_response["current"]["condition"]["text"]))
init.say(str(get_response["current"]["humidity"]))
init.say("Percent humidity")
init.say("The current temperature is")
init.say(str(get_response["current"]["temp_f"]))
init.say("degrees Fahrenheit")
init.say("Feels like")
init.say(str(get_response["current"]["feelslike_f"]))
init.say("degrees Fahrenheit")
init.say("The UV index is")
init.say(get_response["current"]["uv"])
init.say("UV safety index")
init.say("0 to 2 is Low Danger")
init.say("3 to 5 is Moderate Danger")
init.say("6 to 7 is High Danger")
init.say("8 to 10 is Very High Danger")
init.say("11 or more is Extreme Danger Danger DO NOT GO OUT SIDE")"""


class Time:

    def systemTime(self):
        t = time.localtime()
        currentTime = time.strftime("%I:%M %p", t)
        engine = p.init()
        engine.setProperty('rate', 150)
        engine.setProperty("volume", 0.8)
        voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        engine.setProperty("voice", voice_id)
        engine.say("The current time is " + str(currentTime))
        engine.runAndWait()


class Weather:
    def __init__(self):
        self.url = "http://api.weatherapi.com/v1/current.json?key=9d1a06cf296748bba91154256201606&q=77494"

    def weather(self):
        response = requests.get(self.url)

        get_response = response.json()
        init = p.init()
        init.setProperty('rate', 130)
        init.setProperty("volume", 0.8)
        voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        init.setProperty("voice", voice_id)
        init.say("pulling up weather conditions")
        init.say("the conditions are")
        init.say(str(get_response["current"]["condition"]["text"]))
        init.say(str(get_response["current"]["humidity"]))
        init.say("Percent humidity")
        init.say("The current temperature is")
        init.say(str(get_response["current"]["temp_f"]))
        init.say("degrees Fahrenheit")
        init.say("Feels like")
        init.say(str(get_response["current"]["feelslike_f"]))
        init.say("degrees Fahrenheit")
        init.say("The UV index is")
        init.say(get_response["current"]["uv"])
        init.say("UV safety index")
        init.say("0 to 2 is Low Danger")
        init.say("3 to 5 is Moderate Danger")
        init.say("6 to 7 is High Danger")
        init.say("8 to 10 is Very High Danger")
        init.say("11 or more is Extreme Danger Danger DO NOT GO OUT SIDE")
        init.runAndWait()


class Voice:
    def __init__(self):
        self.recon1 = sr.Recognizer()
        self.recon2 = sr.Recognizer()
        self.recon3 = sr.Recognizer()
        self.voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
        self.rate = 130
        self.volume = 0.8

    def voice_Hello(self):
        try:
            with sr.Microphone() as source1:
                human_audio1 = self.recon1.listen(source1)
                recognized_audio1 = self.recon1.recognize_google(human_audio1)
                if recognized_audio1 == "Archer Hello" or "Archer" or "Hello Archer":
                    talk = p.init()
                    talk.setProperty('rate', self.rate)
                    talk.setProperty("volume", self.volume)
                    talk.setProperty("voice", self.voice_id)
                    talk.say("hello kayden what can i do for you")
                    talk.runAndWait()
                    print(recognized_audio1)
        except sr.UnknownValueError as e:
            print(e)

    def voice_weather(self):
        with sr.Microphone() as source2:
            human_audio2 = self.recon2.listen(source2)
            recognized_audio2 = self.recon2.recognize_google(human_audio2)
            if recognized_audio2 == "weather" or "What's the weather" or "What's The Weather like":
                w = Weather()
                w.weather()
                print(recognized_audio2)

    def voice_time(self):
        with sr.Microphone() as source3:
            human_audio3 = self.recon3.listen(source3)
            recognized_audio3 = self.recon3.recognize_google(human_audio3)
            if recognized_audio3 == "time" or "What's the time" or "System Time":
                t = Time()
                t.systemTime()
                print(recognized_audio3)

    def archer_quit(self):
        init = p.init()
        init.setProperty("rate", self.rate)
        init.setProperty("volume", self.volume)
        init.setProperty("voice", self.voice_id)
        init.say("Shutting Down")
        init.runAndWait()


url = "http://api.weatherapi.com/v1/current.json?key=9d1a06cf296748bba91154256201606&q=78873"
url_air = "http://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=77494&distance=35&API_KEY=1069D93A-9C50-44C5-B70D-F10624F40038"

response = requests.get(url=url_air)

get_response = response.json()

print(get_response[:])

