import struct
import time
import webbrowser
from playsound import playsound
import eel
import os
import requests
from dotenv import load_dotenv
import pyaudio
from engine.config import ASSISTANT_NAME
import pywhatkit as kit
from engine.db import conn, cursor
from engine.helpers import extract_yt_term
from engine.speech import speak
import pvporcupine

load_dotenv()

@eel.expose 
def playAssistantSound():
    music_dir = "www/assets/audio/start_sound.mp3"
    playsound(music_dir)


def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower().strip()  # Normalize query

    if query:
        try:
            # Search sys_command (for apps)
            cursor.execute('SELECT path FROM sys_command WHERE name = %s', (query,))
            results = cursor.fetchall()

            if results:
                speak("Opening " + query)
                os.startfile(results[0][0])
                return
            
            # Search web_command (for websites)
            cursor.execute('SELECT url FROM web_command WHERE name = %s', (query,))
            results = cursor.fetchall()

            if results:
                speak("Opening " + query)
                webbrowser.open(results[0][0])
                return

            speak("Sorry, I couldn't find that application or website.")
        
        except Exception as e:
            speak("Something went wrong.")
            print(f"[ERROR - openCommand]: {str(e)}")

    else:
        speak("Not Found.")



def PlayYoutube(query):
    try:
        search_term = extract_yt_term(query)
        if not search_term:
            raise ValueError("Invalid YouTube search term format.")
        
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)

    except Exception as e:
        speak("Sorry! I do not understand what you are talking about.")
        print(f"[ERROR - PlayYoutube]: {str(e)}")


def hotword():
    porcupine= None
    paud=None
    audio_stream=None
    try:

        porcupine=pvporcupine.create(keywords=["jarvis","alexa"])
        paud=pyaudio.PyAudio()
        audio_stream= paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True, frames_per_buffer=porcupine.frame_length)
        while True:
            keyword=audio_stream.read(porcupine.frame_length)
            keyword=struct.unpack_from("h"*porcupine.frame_length,keyword)

            keyword_index=porcupine.process(keyword)
            if keyword_index>=0:
                print("hotword detected")

                import pyautogui as autogui
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()



