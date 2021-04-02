import os
import pandas as pd
from dotenv import load_dotenv
import psycopg2
from psycopg2.extensions import AsIs
load_dotenv()


def create_table(cur):
    query = '''CREATE TABLE IF NOT EXISTS LOAN
      (Id INT PRIMARY KEY     NOT NULL,
      Grade            TEXT    NOT NULL,
      Defaulter           INT     NOT NULL,
      Amount           INT     NOT NULL,
      Interest         REAL     NOT NULL,
      Years            INT     NOT NULL,
      Ownership        TEXT     NOT NULL,
      Income           REAL     NOT NULL,
      Age              INT     NOT NULL)'''
    cur.execute(query)

def insert_row(cur,id,vec):
    defaulter,amount,interest,grade,years,ownership,income,age = vec
    insert_query = """INSERT INTO LOAN (Id,Defaulter,Amount,Interest,Grade,Years,Ownership,Income,Age) 
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    cur.execute(insert_query,(id,defaulter,amount,interest,grade,years,ownership,income,age))

def insert_data(data):
    for id,values in data.iterrows():
        print(values.values)
        insert_row(cur,id,values.values)

#Connection
def psql_connection(database_name, user_name, password, host_name):
    try:
        conn = psycopg2.connect(database=database_name, user=user_name, password=password, host=host_name, port="5432")
        print("Connection Established")
    except ConnectionError:
        print("Error in DB connection")


if __name__ == '__main__':
    database_name = os.getenv('DB_NAME')
    user_name = os.getenv('DB_USER')
    password = os.getenv('DB_KEY')
    host_name = os.getenv('DB_URL')
    conn = psql_connection(database_name, user_name, password, host_name)
    cur = conn.cursor()
    create_table(cur)

    file_name = os.getenv('FILE_NAME')
    data = pd.read_csv(file_name)
    insert_data(data)
    #cur.execute("DROP TABLE LOAN")

    conn.commit()
    conn.close()
