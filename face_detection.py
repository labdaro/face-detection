import cv2
import time
import json
import pika
import numpy as np
import sys
import face_recognition
import os

def publish_data():
    credentail = pika.PlainCredentials('face-recognition', 'face123')
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='192.168.0.226', port=5672, virtual_host='/', credentials=credentail))
    channel = connection.channel()
    channel.queue_declare(queue='sorry', durable=True)
    # load = face_recognition.load_image_file('images/img_6.jpg')
    # encode = face_recognition.face_encodings(load)[0]
    
    cap = cv2.VideoCapture(0)
    # cap = cv2.VideoCapture("rtsp://admin:face$can@10.2.7.250/live") 
    while True:
        success,img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        # imgS = cv2.cvtColor(img,cv2.COLOR_BGR2RGB) 
        faceCurFrame = face_recognition.face_locations(imgS)
        encodingCurFrame = face_recognition.face_encodings(imgS,faceCurFrame)
        s = time.time()
        for encodeFace,faceLoc in zip(encodingCurFrame,faceCurFrame): 
            res = encodeFace.tolist()
            y1,x2,y2,x1 = faceLoc
            y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4 
            cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
            cv2.putText(img,'face',(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
            channel.basic_publish(
                exchange='',
                routing_key='sorry',
                body= json.dumps(res),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
            print('Send already')
            cv2.imshow('WebCam',img)
            cv2.waitKey(1)
        es = time.time() - s
        print("%f" %es)
        
    connection.close()


# def encode_face():
#     list_encode = []
#     for i in os.listdir('Images'):
#         img_path = "Images/" + i
#         img = face_recognition.load_image_file(img_path)
#         encoding = face_recognition.face_encodings(img)[0]
#         print(type(encoding))
#         # list_encode.append(encoding)
#         publish_data(encoding)
    # print(list_encode)
    # print(type(list_encode))
    # publish_data(list_encode)

def cropFace(number):
    """
    Function to crop face in image
    :param number: number of image
    :return: number of user
    """

    # numer of user in image
    number_user = 1

    # get image from file one by one
    for i in range(1, number):
        print(">>", i)

        args_image = 'image/img_' + str(i) + '.jpg'

        # read image
        image = cv2.imread(args_image)

        # if image is not a file move to next
        if image is None:
            print("Could not read input image")
            continue

        # start time of detection
        start = time.time()

        # apply face detection (cnn)
        try:

            faces_cnn = face_recognition.face_locations(image)

            end = time.time()
            print("CNN : ", format(end - start, '.2f'))
            # loop over detected faces
            for top, right, bottom, left in faces_cnn:
                x = left
                y = top
                w = right - x
                h = bottom - y

                # side of Face for cropping
                crop_ima = image[y:y + h, x:x + w]
                # save image face
                cv2.imwrite("face_128D/User_" + str(number_user) + '.jpg', crop_ima)
                # count next number of face
                number_user = number_user + 1

        except Exception as e:
            print ("pass")

    return number_user


# Start program
if __name__ == "__main__":
    publish_data()

    # Capture video from    
    # camera = cv2.VideoCapture("rtsp://keen_danei:keen123!@#@10.0.17.25/live")  # change base on system
    # camera = cv2.VideoCapture("rtsp://keen_danei:keen123!@#@10.0.17.42/live")

    # camera = cv2.VideoCapture(0)

    # # set count = 1 to count image save in image file
    # count = 1
    # time.sleep(5)
    

    # # save frame from Camera
    # while True:

    #     # read frame from camera
    #     return_value, image_frame = camera.read()

    #     # Save frame Camera in left side of frame IP Camera
    #     # cv2.imwrite("image/img_" + str(count) + ".jpg", image_frame[400:1440, 200:1500])  # Change base on Frame side
    #     # Count as new image
    #     # count = count + 1
    #     # Save frame Camera in right side of frame IP Camera
    #     # cv2.imwrite("image/img_" + str(count) + ".jpg", image_frame[400:1440, 1200:2560])  # Change base on Frame side

    #     cv2.imwrite("images/img_" + str(count) + ".jpg", image_frame)
    #     time.sleep(1)
    #     count = count + 1

    #     # number of image you want from frame EX: 10 image equal 20 + 1 = 21 (Both side)
    #     if count == 10:
    #         break

    # # Stop video
    # camera.release()
    # # Close all started windows
    # cv2.destroyAllWindows()

    # print("Finish Save frame from Camera.")
    # time.sleep(5)

    # print("Start crop Face in image.")
    # # Function call crop
    # user_id = cropFace(count)  # number of user that can crop Face to return
    # time.sleep(5)

    # encode 128-d from image crop of user.
    # encode_face()
