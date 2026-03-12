import cv2
import numpy as np

def detect_face(uploaded_file):

    file_bytes = np.asarray(bytearray(uploaded_file.read()),dtype=np.uint8)

    img = cv2.imdecode(file_bytes,1)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    faces = face_cascade.detectMultiScale(gray,1.3,5)

    return len(faces) > 0