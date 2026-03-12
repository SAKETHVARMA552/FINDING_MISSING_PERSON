import cv2
import numpy as np
import base64

def compare_faces(uploaded_file, persons):

    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img1 = cv2.imdecode(file_bytes, 1)
    img1 = cv2.resize(img1, (200,200))

    for person in persons:

        if person["image_data"]:

            img_bytes = base64.b64decode(person["image_data"])
            img_array = np.frombuffer(img_bytes, np.uint8)

            img2 = cv2.imdecode(img_array, 1)
            img2 = cv2.resize(img2, (200,200))

            diff = cv2.absdiff(img1, img2)

            score = np.mean(diff)

            if score < 60:   # lower = more similar
                return person

    return None