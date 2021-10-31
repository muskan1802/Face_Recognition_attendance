import cv2
import numpy as np
import face_recognition
import os

path = 'ImagesAttendance'
images = []
classNames = []
mylist = os.listdir(path)
for cls in mylist:
    curImg = cv2.imread((f'{path}/{cls}'))
    images.append(curImg)
    classNames.append(os.path.splitext(cls)[0])
print(classNames)



# imgElon = face_recognition.load_image_file('ImagesBasic/elonmusk.jpg')
# imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)
# imgTest = face_recognition.load_image_file('ImagesBasic/elonmusktest.jpg')
# imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)