import speech_recognition as sr
import pyttsx3
import time
# Initialize the recognizer
r = sr.Recognizer()


# Function to convert text to speech
def SpeakText(command):
    # Initialize the engine
    engine = pyttsx3.init()
    engine.say(command)
    engine.runAndWait()


def set_password():
    # Speak the prompt to set the password
    SpeakText("Please speak your password to set it.")
    start_time = time.time()  

    # Exception handling to handle exceptions at the runtime
    while True:
        if time.time() - start_time > 10:  # 10 saniyeden fazla bekletmiyoruz
            SpeakText("Timeout. Please try again later.")
            return None

        try:
            # use the microphone as source for input.
            with sr.Microphone() as source:
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source, duration=0.2)

                # listens for the user's input
                audio = r.listen(source)

                # Using google to recognize audio
                password = r.recognize_google(audio)
                password = password.lower()

                # Speak confirmation
                SpeakText("Your password is set successfully.")
                return password

        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")


def verify_password(password):
    attempts = 3
    while attempts > 0:
        # Speak the prompt to enter the password
        SpeakText("Please speak your password to verify.")
        try:
            # use the microphone as source for input.
            with sr.Microphone() as source:
                # wait for a second to let the recognizer
                # adjust the energy threshold based on
                # the surrounding noise level
                r.adjust_for_ambient_noise(source, duration=0.2)

                # listens for the user's input
                audio = r.listen(source)

                # Using google to recognize audio
                entered_password = r.recognize_google(audio)
                entered_password = entered_password.lower()

                # Verify the entered password
                if entered_password == password:
                    SpeakText("Correct.")
                    return True
                else:
                    SpeakText("False.")
                    attempts -= 1
                    SpeakText(f"You have {attempts} attempts left.")
                    # Beep sound for wrong attempt
                    
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))

        except sr.UnknownValueError:
            print("unknown error occurred")
            SpeakText("False.")
            attempts -= 1
            SpeakText(f"You have {attempts} attempts left.")
            # Beep sound for wrong attempt
           

    return False


def main():
    # Set password
    password = set_password()
    if password is None:
        return 

    # Verify password
    result = verify_password(password)
    if result:
        print("Access granted.")
        SpeakText("Access granted.")
    else:
        print("Access denied.")
        SpeakText("Access denied.")


if __name__ == "__main__":
    main()
