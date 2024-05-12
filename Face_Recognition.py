import glob
import os
from time import time
import cv2
from cvzone.FaceDetectionModule import FaceDetector
import face_recognition
import numpy as np
import logging
import serial

class SimpleFacerec:
    def __init__(self):
        self.known_face_encodings = []
        self.known_face_names = []

        # Resize frame for a faster speed
        self.frame_resizing = 0.25
        self.ser = serial.Serial('COM3', 9600)  # Change 'COM1' to the port connected to Arduino
        logging.basicConfig(level=logging.INFO)

    def load_encoding_images(self, images_path):
        images_path = glob.glob(os.path.join(images_path, "*.*"))
        logging.info("{} encoding images found.".format(len(images_path)))

        for img_path in images_path:
            img = cv2.imread(img_path)
            rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            basename = os.path.basename(img_path)
            (filename, ext) = os.path.splitext(basename)
            encodings = face_recognition.face_encodings(rgb_img)

            if len(encodings) > 0:
                img_encoding = encodings[0]
                self.known_face_encodings.append(img_encoding)
                self.known_face_names.append(filename)
            else:
                logging.warning("No faces found in {}. Skipping this image.".format(img_path))

        logging.info("Encoding images loaded")

    def detect_known_faces(self, frame):
        small_frame = cv2.resize(frame, (0, 0), fx=self.frame_resizing, fy=self.frame_resizing)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
            name = "Unknown"
            face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index] and score >= confidence :
                name = self.known_face_names[best_match_index]
                if blurValue < blurThreshold:
                    # Write '1' to serial if a valid face with confidence above or equal 0.8 is detected
                    self.ser.write(b'0')
                elif blurValue >= blurThreshold:
                    self.ser.write(b'1')
            else:
                # Write '0' to serial if no valid face or confidence below 0.8 is detected
                self.ser.write(b'0')

            face_names.append(name)

        # Convert to numpy array to adjust coordinates with frame resizing quickly
        face_locations = np.array(face_locations)
        face_locations = face_locations / self.frame_resizing
        return face_locations.astype(int), face_names, face_encodings

outputFolderPath = 'Dataset/DataCollect'
confidence = 0.8
save = True
blurThreshold = 100  # Larger is more focus


offsetPercentageW = 10
offsetPercentageH = 20
floatingPoint = 6

# Create the output folder if it doesn't exist
if not os.path.exists(outputFolderPath):
    os.makedirs(outputFolderPath)

cap = cv2.VideoCapture(0)
detector = FaceDetector()
sfr = SimpleFacerec()
sfr.load_encoding_images("images/")

while True:
    success, img = cap.read()
    imgOut = img.copy()
    img, bboxs = detector.findFaces(img, draw=False)

    listBlur = []  # True False values indicating if the faces are blur or not
    listInfo = []
    if bboxs:
        for bbox in bboxs:
            x, y, w, h = bbox["bbox"]
            score = bbox["score"][0]

            if score > confidence:
                offsetW = (offsetPercentageW / 100) * w
                x = int(x - offsetW)
                w = int(w + offsetW * 2)
                offsetH = (offsetPercentageH / 100) * h
                y = int(y - offsetH * 3)
                h = int(h + offsetH * 3.5)

                if x < 0: x = 0
                if y < 0: y = 0
                if w < 0: w = 0
                if h < 0: h = 0

                imgFace = img[y:y + h, x:x + w]
                blurValue = int(cv2.Laplacian(imgFace, cv2.CV_64F).var())
                if blurValue > blurThreshold:
                    listBlur.append("Real") #Real person
                else:
                    listBlur.append("Fake") #Fake person

                ih, iw, _ = img.shape
                xc, yc = x + w / 2, y + h / 2

                xcn, ycn = round(xc / iw, floatingPoint), round(yc / ih, floatingPoint)
                wn, hn = round(w / iw, floatingPoint), round(h / ih, floatingPoint)

                if xcn > 1: xcn = 1
                if ycn > 1: ycn = 1
                if wn > 1: wn = 1
                if hn > 1: hn = 1

                listInfo.append(f" {xcn} {ycn} {wn} {hn}\n")

                # Recognize known faces
                face_locations, face_names, _ = sfr.detect_known_faces(img[y:y + h, x:x + w])

                for (face_loc, name) in zip(face_locations, face_names):
                    y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
                    cv2.rectangle(imgOut, (x, y, w, h), (255, 0, 0), 3)  # Change the rectangle color to blue
                    cv2.rectangle(imgOut, (x, y - 30), (x + 410, y), (255, 0, 0),
                                  -1)  # Blue rectangle for text background
                    cv2.putText(imgOut, f'Score: {int(score * 100)}% Blur:{blurValue} Class:{listBlur} Name:{name}', (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1,
                                cv2.LINE_AA)


        if save:
            if all(listBlur) and listBlur != []:
                timeNow = time()
                timeNow = str(timeNow).split('.')
                timeNow = timeNow[0] + timeNow[1]
                cv2.imwrite(f"{outputFolderPath}/{timeNow}.jpg", img)
                for info in listInfo:
                    f = open(f"{outputFolderPath}/{timeNow}.txt", 'a')
                    f.write(info)
                    f.close()

    cv2.imshow("Image", imgOut)
    key = cv2.waitKey(1)
    if key == ord('q'):  # Quit if 'q' is pressed
        break

cap.release()
cv2.destroyAllWindows()