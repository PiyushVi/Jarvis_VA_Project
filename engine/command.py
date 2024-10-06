import pyttsx3
import speech_recognition as sr
import eel
import time



def speak(text):
    engine = pyttsx3.init('sapi5')
    voices = engine.getProperty('voices')
    
    # Use the first voice (you can change this to voices[1] for a different voice)
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 174)
    
    # Commenting out print(voices) so it doesn't output the list
    # print(voices)  

    engine.say(text)
    engine.runAndWait()

@eel.expose
def takecommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print('listening...')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10, 6)

    try:
        print('recognizing...')
        
        # Using Google API for speech recognition
        query = r.recognize_google(audio, language="en-in")
        print(f"user said: {query}")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return ""

    return query.lower()

# Get spoken input and speak it back
text = takecommand()
if text:
    speak(text)
else:
    speak("I couldn't understand what you said.")

@eel.expose
def allCommands(message=1):

    if message == 1:
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
    try:

        if "open" in query:
            from engine.features import openCommand
            openCommand(query)
        elif "on youtube" in query:
            from engine.features import PlayYoutube
            PlayYoutube(query)
        
        elif "send message" in query or "phone call" in query or "video call" in query:
            from engine.features import findContact, whatsApp, makeCall, sendMessage
            contact_no, name = findContact(query)
            if(contact_no != 0):
                speak("Which mode you want to use whatsapp or mobile")
                preferance = takecommand()
                print(preferance)

                if "mobile" in preferance:
                    if "send message" in query or "send sms" in query: 
                        speak("what message to send")
                        message = takecommand()
                        sendMessage(message, contact_no, name)
                    elif "phone call" in query:
                        makeCall(name, contact_no)
                    else:
                        speak("please try again")
                elif "whatsapp" in preferance:
                    message = ""
                    if "send message" in query:
                        message = 'message'
                        speak("what message to send")
                        query = takecommand()
                                        
                    elif "phone call" in query:
                        message = 'call'
                    else:
                        message = 'video call'
                                        
                    whatsApp(contact_no, query, message, name)

        else:
            from engine.features import chatBot
            chatBot(query)
    except:
        print("error")