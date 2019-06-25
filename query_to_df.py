import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
from connector import connect

def query():
"""query() takes in the selections for Name and Sex as imput and queries the Database.
   Returns the result of the query stored as a dataframe """
    connection, metadata, engine = connect()

    #Take in a name an sex as input, will change to take input from Django
    name = input("What Name Would You Like To Query: ")
    sex = input("What Sex Would You Like To Query [M/F]: ")

    #check if name exist in db
    if not engine.dialect.has_table(engine, name):
        print("{0} does not exist in the dataset".format(name))
    else:
        print("{0} exists in the dataset".format(name))
        query = "Select * from {0} where {0}.Sex in ('{1}') order by {0}.Year".format(name, sex)
        df = pd.read_sql(query, connection)

    return(df)


if __name__ == '__main__':
    main()

