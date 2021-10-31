import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime

path = 'ImagesAttendance'
images = []
classNames = []
mylist = os.listdir(path)
for cls in mylist:
    curImg = cv2.imread((f'{path}/{cls}'))
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)

def findencoding(images):
    encodelist =[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodelist.append(encode)
    return encodelist

def markattendance(name):
    with open('Attendance.csv','r+') as f:
        mydatalist = f.readline()
        namelist = []
        # print(mydatalist)
        for line in mydatalist:
            entry = line.split(',')
            namelist.append(entry[0])
        if name not in namelist:
            now = datetime.now()
            dtstring = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtstring}')



encodelistknown = findencoding(images)
print('Encoding Complete')

cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    imgS = cv2.resize(img,(0,0),None,0.25,0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facescurframe = face_recognition.face_locations(imgS)
    encodecurframe = face_recognition.face_encodings(imgS,facescurframe)

    for encodeface,faceloc in zip(encodecurframe,facescurframe):
        matches = face_recognition.compare_faces(encodelistknown,encodeface)
        facedis = face_recognition.face_distance(encodelistknown,encodeface)
        #print(facedis)
        matcheindex = np.argmin(facedis)

        if matches[matcheindex]:
            name = classNames[matcheindex].upper()
            #print(name)
            y1,x2,y2,x1 = faceloc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            markattendance(name)


    cv2.imshow('Webcam',img)
    cv2.waitKey(1)

# faceLoc = face_recognition.face_locations(imgElon)[0]
# encodeElon = face_recognition.face_encodings(imgElon)[0]
# cv2.rectangle(imgElon,(faceLoc[3],faceLoc[0]),(faceLoc[1],faceLoc[2]),(255,0,255),2)
#
# faceLocTest = face_recognition.face_locations(imgTest)[0]
# encodeTest = face_recognition.face_encodings(imgTest)[0]
# cv2.rectangle(imgTest,(faceLocTest[3],faceLocTest[0]),(faceLocTest[1],faceLocTest[2]),(255,0,255),2)
#
# results = face_recognition.compare_faces([encodeElon],encodeTest)
# faceDis = face_recognition.face_distance([encodeElon],encodeTest)