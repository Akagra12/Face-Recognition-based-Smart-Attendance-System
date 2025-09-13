import os
import pickle
import numpy as np
import cv2
import face_recognition
import cvzone
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
# from firebase_admin import storage
import numpy as np
from datetime import datetime


# ---------------- FIREBASE DATABASE SETUP ----------------

cred = credentials.Certificate("faceattendance-7493e-firebase-adminsdk-fbsvc-918b07cdfc.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendance-7493e-default-rtdb.firebaseio.com/"})
# { 'databaseURL': "", 
# 'storageBucket': "" })
# bucket = storage.bucket()


# ---------------- WEBCAM SETTINGS ----------------

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)


# ---------------- BACKGROUND AND MODE IMAGES ----------------

# ...existing code...
imgBackground = cv2.imread('Files/Resources/background.png')
# Importing the mode images into a list

folderModePath = 'Files/Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))


# ---------------- ENCODINGS FILE (LOCAL) ----------------

# load encoding
print("Loading encoding file...")
file =open('EncodeFile.p','rb')
encodeListKnownWithIds=pickle.load(file)
file.close()
encodeListKnown, studentIds=encodeListKnownWithIds
print(studentIds)
print("Encode file loaded")


# ---------------- VARIABLES ----------------

modeType = 0
counter = 0
# It is used to control the timing and
# state of attendance processing after a face is detected.
# You increment it in your main loop to manage 
# how long student info is displayed and when to reset or change modes.

id = -1
imgStudent = []

# ---------------- MAIN LOOP ----------------

while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Find faces in current frame
    faceCurFrame = face_recognition.face_locations(imgS)
    # 👉 Purpose: Find where faces are inside the image.
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)
    # For each face, it generates a 128-dimensional vector (list of 128 floating-point numbers).
    # {Step 1: “Where is the face?” (coordinates).
    # Step 2: “What does this face look like in numbers?” (128-d vector).}
    
    
        # Place webcam feed onto background template

    imgBackground[162:162 + 480, 55:55 + 640] = img
    imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]



    # Loop through all faces detected

    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
                matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
                #  checks if the current face matches any known faces by comparing encodings. It returns a list of True/False
                #             matches = Yes/No result for each known person.
    
                faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
                # faceDis = How close the detected face is to each known person (smaller = better).
                
                # print("matches", matches)
                # print("faceDis", faceDis)
                
                
                matchIndex = np.argmin(faceDis)
                # print("Match Index", matchIndex)
    
                if matches[matchIndex]:
                    # print("Known Face Detected")
                    # print(studentIds[matchIndex])
                                    # If match found
    
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentIds[matchIndex]
                    
                    if(counter == 0):
                        
                        # cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        # cv2.imshow("Face Attendance", imgBackground)
                        # cv2.waitKey(1)
                        
                        
                        counter = 1# Start processing
                        modeType = 1   # Switch to "loading" mode
                        
                        
                # If student detected
    
        if(counter!=0):
            if(counter ==1):
                # Get the Data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
# Ge    t the image from local Images folder instead of Firebase Storage
                # imgPath = f'Images/{id}.png'
                # imgStudent = cv2.imread(imgPath)
                imgPathPng = f'Files/Images/{id}.png'
                imgPathJpeg = f'Files/Images/{id}.jpeg'
                imgStudent = None
                
                if os.path.exists(imgPathPng):
                    imgStudent = cv2.imread(imgPathPng)
                    print("image found")
                elif os.path.exists(imgPathJpeg):
                    imgStudent = cv2.imread(imgPathJpeg)
                    imgStudent = cv2.resize(imgStudent, (216, 216))
    
                else:
                    print(f"Image not found: {imgPathPng} or {imgPathJpeg}")
                    imgStudent = np.zeros((216, 216, 3), dtype=np.uint8)  # fallback blank image
            
                # Update data of attendance
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'],
                                                    "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
                print(secondsElapsed)
    
                if secondsElapsed > 30:
                    # 30 seconds have passed  
                        ref = db.reference(f'Students/{id}')
                        studentInfo['total_attendance'] += 1
                        ref.child('total_attendance').set(studentInfo['total_attendance'])
                        ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                        modeType = 3
                        counter = 0
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    
            
            if modeType != 3:
        
                if 10 < counter < 20:
                        modeType = 2
    
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    
                if counter <= 10:
                        cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(id), (1006, 493),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                        cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                        cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
    
                        (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                        offset = (414 - w) // 2
                        cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                                    cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)
    
                        imgBackground[175:175 + 216, 909:909 + 216] = imgStudent
    
                counter += 1    
            
            
                if counter >= 20:
                        counter = 0
                        modeType = 0
                        studentInfo = []
                        imgStudent = []
                        imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
        
                
    cv2.imshow("web", img)
    cv2.imshow("Background", imgBackground)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    cv2.waitKey(1)