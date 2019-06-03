"""This script reads all data from csv into DataFrames,
then builds out a database with those Dataframes"""
import os
import pandas as pd
import time
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
import sys

def main():

    name_dic = csv_to_DataFrame()

    create_db(name_dic)


def create_db(name_dic):

    total_keys  = len(name_dic.keys())

    engine = create_engine("mysql+pymysql://USER:PASSWORD@localhost/DB", echo=False)
    connection = engine.connect()
    metadata = MetaData(engine)

    names =  Table('Names', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(30)))

    metadata.create_all(engine)

    print("Loading DataFrames to Database")

    for progress,key in enumerate(name_dic.keys(),1):

        update_progress(progress/total_keys)

        name_dic[key].to_sql(key, con=engine, if_exists='replace')
        ins = names.insert().values(name=key)
        connection.execute(ins)


    connection.close()

    print("Done Loading Database")


def csv_to_DataFrame():

    name_dic = {}
    header = ['Sex', 'Qty', 'Year']
    print('loading DataFrames...')
    dir = os.listdir("./Year_of_Birth_Data")

    for progress, file in enumerate(dir,1):

        update_progress(progress/len(dir))

        with open("./Year_of_Birth_Data/{}".format(file), 'r') as f_in:
            for line in f_in:
                data = line.split(',')
                key = data[0]
                data[3] = data[3][:-1] #carraige return at the end of each line
                values = data[1:]
                tempdf = pd.DataFrame([values], columns = header)

                if key not in name_dic.keys():
                    name_dic[key] = tempdf
                    #print(name_dic[key])
                else:
                    name_dic[key] = pd.concat([name_dic[key], tempdf], ignore_index = True)

    print("Done loading DataFrames")

    return(name_dic)


def update_progress(progress):
    barLength = 20
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()



if __name__ == "__main__":
    main()
