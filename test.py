import psycopg2
import face_recognition
import math
import os
import pika
import json
import numpy as np
try:
    # creddentail = pika.PlainCredentials('test', '123456')
    # connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='localhost', port=5672, virtual_host='/', credentials=creddentail))
    # channel = connection.channel()
    # #Information about the queue
    # channel.queue_declare(queue='sectiona', durable=True)
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sectiona', durable=True)


    connection1 = psycopg2.connect(user = "postgres",
                                  password = "1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "newdataset")

    cursor = connection1.cursor()
    TABLE_NAME = "testing"
    COL_NAME = "name"
    attendence=[]
    
    def callback(ch, method,properties, body):
        print('Waiting.....')
        print(f"{body}")
        #recieveData = json.loads(body)
        # print(recieveData)
        # #convert to numpy array
        # numpyArray =np.array(recieveData)
        # convertString = numpyArray.tostring()
        # ENCODE = np.fromstring(convertString, dtype=float)
        # print(ENCODE)
        # print(type(ENCODE))
        # query = f'select * from {TABLE_NAME}'
        # cursor.execute(query)
        # records = cursor.fetchall()
        # for encode in records:
        #     i = 0  
        #     dist = 0
        #     for data in range(2,130):
        #         dist += pow((ENCODE[i] - encode[data]),2)
        #         i += 1
        #     result = math.sqrt(dist)
        #     if result <0.435:
        #         print(result)
        #         attendence.append(encode[1])
        # channel.stop_consuming()
        print("----------------------------------------------------------")
    
        print(attendence)
        ch.basic_ack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='sectiona', on_message_callback=callback)
    channel.start_consuming()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection1):
            cursor.close()
            connection1.close()
            print("PostgreSQL connection is closed")
