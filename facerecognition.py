import cv2
import face_recognition as fr
videoCapture = cv2.VideoCapture(0)

try:
    # Load owner image and encode it (outside the loop)
    image = fr.load_image_file("C:\\Users\\erens\\Downloads\\reference.jpg")
    ownerEncode = [fr.face_encodings(image)[0]]
except FileNotFoundError:
    print("Error: Reference image not found!")
    exit()

while True:
    res, frame = videoCapture.read()
    cv2.imshow('Kamera', frame)
    

    # Find all face locations in the frame
    frameEncodings = fr.face_encodings(frame)
    for frame in frameEncodings:
        matchCheck = fr.compare_faces(ownerEncode, frame)
        if matchCheck[0]:
            print("Found")
            cv2.putText(frame, "Eren Sirin", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
            continue

        else:
            print("yok")    
            cv2.putText(frame, "Taninamadi!", (20, 450), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
videoCapture.release()
cv2.destroyAllWindows()