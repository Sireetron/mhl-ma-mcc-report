from impala.dbapi import connect
from dotenv import load_dotenv
import os
import pandas as pd
import sqlalchemy
import utils
load_dotenv()


def split_dataframe(df, chunk_size = 1000): 
    chunks = list()
    num_chunks = len(df) // chunk_size + 1
    for i in range(num_chunks):
        chunks.append(df[i*chunk_size:(i+1)*chunk_size])
    return chunks

class impala_instance:
    def __init__(self,user = os.environ.get('impala_user'),password = '') -> None:
        self.user=user
        self.password=password
    def connect(self):
        conn = connect(
            host=os.environ.get('impala_host'),
            port=os.environ.get('impala_port')
        )
        self.con,self.cur = conn,conn.cursor(self.user)
        print('Impala connected')
        return self.con,self.cur

    def close_connection(self):
        self.con.close()
        print('Impala disconnected')

    def create_table(self,dataframe,database,table):
        CREATE_STATEMENT = utils.guess_schema(dataframe,database,table)
        CREATE_STATEMENT= CREATE_STATEMENT.replace('CREATE TABLE','CREATE TABLE IF NOT EXISTS')
        CREATE_STATEMENT = CREATE_STATEMENT.replace('`','')

        print(CREATE_STATEMENT)
        self.cur.execute(CREATE_STATEMENT)

    def insert_chunk(self,dataframe,database,table,chuck_size=1000):
        chunks = split_dataframe(dataframe,chuck_size)
        print(len(dataframe),'records found,','split into',len(chunks),'chunks')
        counter = 0
        for chunk in chunks:
            tuples = [tuple(x) for x in chunk.to_numpy()]
            combined_data = tuple(tuples)
            query_buffer = ''
            for x in combined_data:
                query_buffer = query_buffer + str(x)
            # print(query_buffer)
            query_buffer = query_buffer.replace(')(', '),(')  # .replace('\'','')
            INSERT_STATEMENT_q = 'INSERT INTO '+database +'.'+table+' VALUES ' + query_buffer + ';'
            self.cur.execute(INSERT_STATEMENT_q)
            counter = counter+len(chunk)
            print(len(chunk),'rows inserted',counter*100//len(dataframe),'%')
    


if __name__ == '__main__':
    # DATABASE_NAME = 'default'
    # TABLE_NAME = 'rainfall24h'
    # df=pd.read_csv('test/data/rain_Df.csv')
    DATABASE_NAME = 'l1_diw'
    TABLE_NAME = 'factory'
    df=pd.read_csv('./diw/all_factory.csv',sep='|')
    df = df.astype(str)
    # print(df)
    imp = impala_instance()
    imp.connect()
    imp.create_table(df,DATABASE_NAME,TABLE_NAME)
    imp.insert_chunk(df,DATABASE_NAME,TABLE_NAME,10000)
    imp.close_connection()

