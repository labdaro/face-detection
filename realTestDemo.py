# create a connection to RabbitMQ and PostgreSQL
# create a table for commitlog in PostgreSQL

#  create table logs(
# 	student_name varchar(20),
# 	sudent_id int,
# 	date date,
# 	time time,
	# attendance varchar(20)
)

import psycopg2
import face_recognition
import math
import os
import pika
import json
import datetime
import numpy as np 
try:
    #Create the connection into the Rabbitmq
    creddentail = pika.PlainCredentials('lyhov', '123456')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='10.1.33.186', port=5672, virtual_host='/', credentials=creddentail))
    channel = connection.channel()
    channel.queue_declare(queue='abc', durable=True)
    

    # Demo the local 
    # connection = pika.BlockingConnection(
    # pika.ConnectionParameters(host='localhost'))
    # channel = connection.channel() 
    # channel.queue_declare(queue='face_recognition_queue', durable=True)

    # create the connection into the postgresql 
    connection1 = psycopg2.connect(user = "postgres",
                                  password = "1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "face_recognition_db")

    cursor = connection1.cursor()

    #Dataset from the database
    TABLE_NAME = "dataset_table"
    name_buffer = set()
    list_name  = dict()
    result = []
    
    #for log table to store the present student 
    TABLE_ATTENDENCE = "logs"
    COL_NAME = "student_name"
    COL_ID = "student_id"
    COL_DATE = "date"
    COL_TIME = "time"
    COL_ATTENDANCE = "attendance"

   

    def callback(ch, method,properties, body):
        #Get the current time 
        dateTimeObj = datetime.datetime.now()
        date = dateTimeObj.strftime("%A-%d-%B-%Y")
        time = dateTimeObj.strftime("%I:%M %p")  
        try:
            #Recieve the data from queue and convert into the numpy
            recieveData = json.loads(body)
            numpyArray =np.array(recieveData)
            convertString = numpyArray.tostring()
            ENCODE = np.fromstring(convertString, dtype=float)
        #Compare the encode data with data in database
            query = f'select * from {TABLE_NAME}'
            cursor.execute(query)
            records = cursor.fetchall()
            for encode in records:
                i = 0  
                dist = 0
                #checking for one people face
                for data in range(2,130):
                    dist += pow((ENCODE[i] - encode[data]),2)
                    i += 1
                result = math.sqrt(dist)
                if result < 0.50:
                    print(encode[1]+ " is matching face")
                # else:
                #     print("Have no Matching.... ")
            #     list_name[encode[1]] = dist
            #     print(dist)
            # minDistance = min(list_name, key=list_name.get) #caculate the low distance function
            # name_buffer.add(minDistance)
            # result.append(list_name[minDistance])
            # print(name_buffer)
            # print(result)
                
                # if result < 0.445:
                #     name_present.append(encode[1])
                #     checking = f"insert into {TABLE_ATTENDENCE} ({COL_ID},{COL_NAME},{COL_DATE},{COL_TIME},{COL_ATTENDANCE}) values({encode[0]},'{encode[1]}','{date}','{time}','Present')"
                #     cursor.execute(checking) 
                #     connection1.commit()
                # print(name_present)



            #     list_name[encode[1]] = result
            # minDistance = min(list_name, key=list_name.get) #caculate the low distance function

            #if list_name[minDistance] < 0.44:
            # print(minDistance)
            # print(list_name[minDistance])
            # name_buffer.add(minDistance)
                
            # dataResult = f"select {COL_ID},name from {TABLE_NAME} where name ='{minDistance}' "
            # cursor.execute(dataResult)
            # record1 = cursor.fetchall()
            # print("==========+++++++=+")
            # print(record1)
            # for check in record1:
            #     checking = f"insert into {TABLE_ATTENDENCE} ({COL_ID},{COL_NAME},{COL_DATE},{COL_TIME},{COL_ATTENDANCE}) values({check[0]},'{check[1]}','{date}','{time}','Present')"
            #     cursor.execute(checking) 
            #     connection1.commit()
                

                
                
                        
            
            # channel.stop_consuming()
            print("----------------------------------------------------------")
            # print(LIST_NAME_PRESENT)     
                                         

        except Exception as e: 
            print(e)
            
        finally:
            ch.basic_ack(delivery_tag=method.delivery_tag)



    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='face_recognition_queue', on_message_callback=callback)
    channel.start_consuming()

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection1):
            cursor.close()
            connection1.close()
            print("PostgreSQL connection is closed")


    









