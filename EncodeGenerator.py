import cv2
import face_recognition
import pickle
import os
import numpy as np
# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import db
# from firebase_admin import  storage

# cred = credentials.Certificate("serviceAccountKey.json")
# firebase_admin.initialize_app(cred, {
#     'databaseURL': "",
#     'storageBucket': ""
# })


# Importing student images
folderPath = 'Files\Images'
pathList = os.listdir(folderPath)
print(pathList)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    studentIds.append(os.path.splitext(path)[0])

    # fileName = f'{folderPath}/{path}'
    # bucket = storage.bucket()
    # blob = bucket.blob(fileName)
    # blob.upload_from_filename(fileName)


    # print(path) text(path)[0])
print(studentIds)


def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        
        if img is None:
            print("⚠️ Image not loaded properly, skipping...")
            continue
        else:
            print ("yes")
            
            
        print(img.dtype, img.shape)
        img = np.ascontiguousarray(img)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # opencv use BGR and face recog use RGB
        
        
        encodes = face_recognition.face_encodings(img)
        
        if len(encodes) > 0:
            encodeList.append(encodes[0])  # take first face encoding
        else:
            print("⚠️ No face found in image, skipping...")
    return encodeList


print("Encoding Started ...")
encodeListKnown = findEncodings(imgList)
encodeListKnownWithIds = [encodeListKnown, studentIds]
print("Encoding Complete")

file = open("EncodeFile.p", 'wb')
pickle.dump(encodeListKnownWithIds, file)
file.close()
print("File Saved")