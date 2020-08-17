"""This script reads all data from csv into DataFrames,
then builds out a database with those Dataframes"""
import os
import pandas as pd
import time
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import exc
import sys
from connector import connect
from progress_bar import update_progress

def main():

    name_dic = csv_to_DataFrame()

    upload(name_dic)


def upload(name_dic):

    year_list = [i for i in range(1880,2018)]

    total_keys = len(name_dic.keys())
    total_years = len(year_list)

    connection, metadata, engine = connect()

    db_tables = set(metadata.tables.keys())

    if "Names" in db_tables:
        print("Names Table already exists")
        name_table = Table('Names', metadata)

    else:
        name_table =  Table('Names', metadata,
            Column('id', Integer, primary_key=True),
            Column('name', String(30)))

    if "Years" in db_tables:
        print("Years Table already exists")
        year_table = Table('Years', metadata)

    else:
        year_table =  Table('Years', metadata,
            Column('id', Integer, primary_key=True),
            Column('year', Integer))

    try:
        metadata.create_all(engine)

    except exc.SQLAlchemyError as e:
        print("Tables already existed")

    print("Loading DataFrames to Database Tables")

    for progress,k in enumerate(name_dic.keys(), 1):

        if k in db_tables:
            update_progress(progress/total_keys)
            continue

        try:
            name_dic[k].to_sql(k, con=engine, if_exists='replace')
        except exc.SQLAlchemyError as e:
            print("****Couldn't insert {0} table. Investigate!****".format(k))

        ins = name_table.insert().values(name=k)
        connection.execute(ins)

        update_progress(progress/total_keys)
        name_dic[k] = ''

    print("Loading Years to Year table")

    for progress, y in enumerate(year_list, 1):

        ins = year_table.insert().values(year=y)
        connection.execute(ins)
        update_progress(progress/total_years)

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
                try:
                    data = line.split(',')
                    key = data[0]
                    data[2] = int(data[2])
                    data[3] = int(data[3][:-1]) #carraige return at the end of each line
                    values = data[1:]
                    tempdf = pd.DataFrame([values], columns = header)
                except ValueError as e:
                    continue #offsetting for the header of every file, throws value error converting text to int

                if key not in name_dic.keys():
                    name_dic[key] = tempdf
                else:
                    name_dic[key] = pd.concat([name_dic[key], tempdf], ignore_index = True)

    print("Done loading DataFrames")

    return(name_dic)


if __name__ == "__main__":
    main()
