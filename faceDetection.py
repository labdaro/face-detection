import pika
import json
import os
import face_recognition

credentail = pika.PlainCredentials('face-recognition', 'face123')
connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='192.168.0.226', port=5672, virtual_host='/', credentials=credentail))
channel = connection.channel()
channel.queue_declare(queue='testings', durable=True)
# connection = pika.BlockingConnection(
#     pika.ConnectionParameters(host='localhost', port=5672))
# channel = connection.channel()
# channel.queue_declare(queue='show_queue', durable=True)
count = 0
for image in  os.listdir("test_image"):
    X_img = face_recognition.load_image_file("test_image/"+image)
    X_face_locations = face_recognition.face_locations(X_img)
    faces_encode = face_recognition.face_encodings(X_img, known_face_locations=X_face_locations)[0]
    res = faces_encode.tolist()
    channel.basic_publish(
        exchange='',
        routing_key='testings',
        body=json.dumps(res),
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    print('sent...')
print('Data is already sent to Queue....')
connection.close()