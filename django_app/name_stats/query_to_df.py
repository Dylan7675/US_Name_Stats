import sqlalchemy
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
from connector import connect

def query(name, sex):
    """query() takes in the selections for Name and Sex as input and queries the Database. Returns the result of the query stored as a dataframe, and the Name that was queried"""
    connection, metadata, engine = connect()

    #check if name exist in db
    if not engine.dialect.has_table(engine, name):
        raise ValueError("{} not found in DB".format(name))
    else:
        query_db = "Select * from {0} where {0}.Sex in ('{1}') order by {0}.Year".format(name, sex)
        df = pd.read_sql(query_db, connection)

    query_vals = dict([('name',name), ('sex',sex)])

    return(df, query_vals)


if __name__ == '__main__':
    main()


