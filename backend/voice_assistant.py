import speech_recognition as sr
import pyttsx3

# ==============================
# SPEAK ENGINE
# ==============================

engine = pyttsx3.init()

engine.setProperty(
    'rate',
    170
)

# ==============================
# SPEAK FUNCTION
# ==============================

def speak(text):

    print("AI:", text)

    engine.say(text)

    engine.runAndWait()

# ==============================
# LISTEN FUNCTION
# ==============================

def listen():

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:

        print("Listening...")

        recognizer.adjust_for_ambient_noise(source)

        audio = recognizer.listen(source)

    try:

        text = recognizer.recognize_google(audio)

        print("You:", text)

        return text.lower()

    except:

        return ""

# ==============================
# AI RESPONSE
# ==============================

def get_response(message):

    if "fever" in message:

        return """
You may have fever.
Drink water and take proper rest.
"""

    elif "headache" in message:

        return """
Take proper rest and drink water.
"""

    elif "cold" in message:

        return """
Drink warm water and avoid cold drinks.
"""

    else:

        return """
Please explain symptoms clearly.
"""

# ==============================
# MAIN
# ==============================

speak("MediCall AI Assistant Started")

while True:

    user_message = listen()

    if user_message == "":
        continue

    if "stop" in user_message:
        speak("Goodbye")
        break

    response = get_response(
        user_message
    )

    speak(response)