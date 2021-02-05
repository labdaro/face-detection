import face_recognition
import os
import psycopg2
import math
import numpy as np

TABLE_NAME = "student_kit" 
try:
    # create the connection into the postgresql 
    connection1 = psycopg2.connect(user = "postgres",
                                  password = "1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "encode_database")

    cursor = connection1.cursor()
       
    load = face_recognition.face_locations("face/User_13.jpg")
    eload = face_recognition.load_image_file(load)
    ENCODE = face_recognition.face_encodings(eload)[0]
    list_name = {}
    query = f'select * from {TABLE_NAME}'
    cursor.execute(query)
    records = cursor.fetchall()
    for encode in records:
        i = 0  
        dist = 0
        for data in range(2,130):
            dist += pow((ENCODE[i] - encode[data]),2)
            i += 1
        result = math.sqrt(dist)
        # res = f"{encode[1]}: {result}"
        list_name[encode[1]] = result
        print(result)
    res = min(list_name, key=list_name.get)
    print(res)
    print(list_name[res])   
    

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection1):
            cursor.close()
            connection1.close()
            print("PostgreSQL connection is closed")
        