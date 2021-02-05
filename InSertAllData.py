import psycopg2
import face_recognition as fr
import os


try:
    connection = psycopg2.connect(user = "postgres",
                                  password = "1234",
                                  host = "127.0.0.1",
                                  port = "5432",
                                  database = "face_recognition_db")

    cursor = connection.cursor()
    TABLE_NAME = "dataset_table"
    COL_NAME = "name"
    COL_ID = "roll_number"

    # create column only ID and NAME 
    def create_table():
       create = f"create table {TABLE_NAME} ({COL_ID} int, {COL_NAME} varchar(100))"
       cursor.execute(create)
       connection.commit()
       return "sucessfully to create table"

    #add 128 column 
    def add_128Col():
        for i in range(1,129):
            COLUMN = "point" + str(i)
            add = f"alter table {TABLE_NAME} add column {COLUMN} float(50)" 
            cursor.execute(add)
            connection.commit()
        return "sucessfully to create 128 column"

    # Insert data into Column Name,Id,point128
    def insert_data():
        path = "Dataset_Image"
        id = 13434
        for user_name in os.listdir(path):
            insert = f"insert into {TABLE_NAME} ({COL_ID},{COL_NAME}) values({id},'{user_name[:-4]}')"
            id +=1
            cursor.execute(insert) 
            connection.commit()      
    
     
            load = fr.load_image_file(path +"/" + user_name)
            ENCODE = fr.face_encodings(load)[0] 
            j=1
            for i in ENCODE:
                COLUMN = "point" + str(j)
                insert1 = f"update {TABLE_NAME} set {COLUMN} = {i} where {COL_NAME} = '{user_name[:-4]}' "             
                cursor.execute(insert1)
                connection.commit()
                j +=1
            print(user_name+" is already encode ")      
        return  "already all"

    

    Table_Create =  create_table()
    print(Table_Create)
    more_column = add_128Col()
    print(more_column)    


    add_data = insert_data()
    print(add_data)

except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
