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

    states = csv_to_DataFrame()

    upload(states)


def upload(state_dic):

    total_states = len(state_dic.keys())

    connection, metadata, engine = connect()

    db_tables = set(metadata.tables.keys())

    print("Loading DataFrames to Database Tables")

    for progress, k in enumerate(state_dic.keys(), 1):
        if k in db_tables:
            update_progress(progress/total_states)
            continue
        try:
            state_dic[k].to_sql(k, con=engine, if_exists='replace')
        except exc.SQLAlchemyError as e:
            print("****Couldn't insert {0} table. Investigate!****".format(k))

        update_progress(progress/total_states)
        state_dic[k] = ''

    print("Done uploading state DataFrames to the Database")


def csv_to_DataFrame():
    header = ['Sex', 'Year', 'Name', 'Qty']
    print('loading DataFrames...')
    directory = os.listdir("./Names_By_State")
    states_dic = {}

    for progress, file in enumerate(directory, 1):
        update_progress(progress / len(directory))

        with open("./Names_By_State/{}".format(file), 'r') as f_in:
            for line in f_in:
                try:
                    data = line.split(',')
                    key = data[0]
                    data[2] = int(data[2])#year
                    data[4] = int(data[4][:-1])#qty
                    tempdf = pd.DataFrame([data[1:]], columns=header)
                    
                except ValueError as e:
                    print("Error creating DF.... Investigate")

                if key not in states_dic.keys():
                    states_dic[key] = tempdf
                else:
                    states_dic[key] = pd.concat([states_dic[key], tempdf], ignore_index=True)

    print("Done loading DataFrames")

    return (states_dic)



if __name__ == "__main__":
    main()
