import cv2
import face_recognition as fr
import pyttsx3
import time
import speech_recognition as sr
import serial

# Initialize the recognizer
r = sr.Recognizer()

# Initialize the engine for text-to-speech
engine = pyttsx3.init()

# Arduino connection
arduino = serial.Serial('COM8', 9600)  # COMX kısmını bağlı olduğunuz seri port numarasıyla değiştirin
faceCheck = 0

# Function to convert text to speech
def speak_text(command):
    engine.say(command)
    engine.runAndWait()

# Function to set password via speech recognition
def set_voice_password():
    speak_text("Please speak your password to set it.")
    while True:
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.01)
                audio = r.listen(source)
                voice_password = r.recognize_google(audio)
                voice_password = voice_password.lower()
                speak_text("Your password is set successfully.")
                return voice_password
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")

# Function to verify password via speech recognition
def voice_recognition(voice_password):
    attempts = 3
    while attempts > 0:
        speak_text("Please speak your password to verify.")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.2)
                audio = r.listen(source)
                entered_password = r.recognize_google(audio)
                entered_password = entered_password.lower()
                if entered_password == voice_password:
                    speak_text("Correct.")
                    speak_text("Access Granted.")
                    return True
                else:
                    speak_text("False.")
                    attempts -= 1
                    speak_text(f"You have {attempts} attempts left.")
        except sr.RequestError as e:
            print("Could not request results; {0}".format(e))
        except sr.UnknownValueError:
            print("unknown error occurred")
            speak_text("False.")
            attempts -= 1
            speak_text(f"You have {attempts} attempts left.")
    if attempts == 0:
        speak_text("Access Denied !!!")
        speak_text("Please enter your password on keypad.")
        return False
    return False

# Function to perform face recognition
def face_recognition():
    speak_text("Please wait for face recognition to complete. It will take 10 seconds.")
    arduino.write(b'2')
    start_time = time.time()
    owner_image = fr.load_image_file("C:\\Users\\erens\\Downloads\\reference.jpg")
    owner_encode = [fr.face_encodings(owner_image)[0]]

    video_capture = cv2.VideoCapture(0)
    while time.time() - start_time < 10:
        ret, frame = video_capture.read()
        frame_encodings = fr.face_encodings(frame)
        for frame_encoding in frame_encodings:
            match_check = fr.compare_faces(owner_encode, frame_encoding)
            if match_check[0]:
                speak_text("Face recognized.")
                arduino.write(b'1')
                speak_text("Welcome! Access granted.")
                video_capture.release()
                cv2.destroyAllWindows()
                return True
        cv2.imshow('Face Recognition', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    speak_text("Face not recognized.")
    video_capture.release()
    cv2.destroyAllWindows()
    return False

def main():
    while True:
        faceCheck = arduino.readline()
        faceCheck = int(faceCheck.decode().strip())
        if faceCheck == 1:
            break
    if faceCheck == 1:
        voice_password = set_voice_password()
        if voice_password is None:
            return 

        # Verify password
        password_verification_result = False
        while not password_verification_result:
            face_recognition_result = face_recognition()
            if face_recognition_result:
                arduino.write(b'1')
                return
            else:
                voice_check = voice_recognition(voice_password)
                if voice_check:
                    arduino.write(b'1')  # Send data to Arduino if voice recognition is successful
                    return
                else:
                    arduino.write(b'0')  # Send data to Arduino if both face and voice recognition fail
                    return
if __name__ == "__main__":
    main()
