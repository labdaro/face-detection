import cv2
import face_recognition
img_path ="SectionATest/img_2.jpg"
img = cv2.imread(img_path)
load = face_recognition.face_locations(img)
count= 0
for top, right, bottom, left in load:
                x = left
                y = top
                w = right - x
                h = bottom - y
                crop_ima = img[y:y + h, x:x + w]
                try:
      
                  ENCODE = face_recognition.face_encodings(crop_ima)[0]
                  print(ENCODE)
                  count+=1
                  print(count)
                except:
                      pass



# load1 = face_recognition.load_image_file("SectionATest/Ang Sivhour.jpg")
# en = face_recognition.face_encodings(load1)[0]
# print(en)