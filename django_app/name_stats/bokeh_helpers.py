from collections import OrderedDict
import pandas as pd
from connector import connect
import sqlalchemy
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.sql import select
import os


class Connection:

    connection, metadata, engine = connect()

    conn_vars = dict(
        connection=connection,
        metadata=metadata,
        engine=engine
    )

def build_matrix(years, states, state_name_dfs):
    """Input: Year List, State List, DF from build_df
       Output: Returns an OrderedDict of qty's per state by year"""

    qty_by_state = list()
    matrix = OrderedDict()
    for year in years:

        if year not in matrix.keys():
            matrix[str(year)] = []
        for state in states:
            if year in state_name_dfs[state]['Year'].tolist():
                tempdf = state_name_dfs[state].query(f'Year == {year}')
                qty_by_state.append(tempdf['Qty'].tolist()[0])
            else:
                qty_by_state.append(0)

        matrix[str(year)] = qty_by_state
        qty_by_state = []

    return matrix


def build_state_name_df(name, sex):
    """Input: Name and Sex to be queried
       Output: returns an Ordered dict of dataframes arranged by state
       This function Queries the database and builds state dataframes with
       data regarding the Name and Sex input"""

    conn_vars = Connection.conn_vars
    states = [file.split('.')[0] for file in os.listdir('./Names_By_State')]
    name_by_state = OrderedDict()

    for state in states:
        # check if state exist in db
        if not conn_vars['engine'].dialect.has_table(conn_vars['engine'], state):
            raise ValueError(f"{state} not found in DB")
        else:
            query_db = f"Select * from `{state}` where " \
                       f"Name='{name}' AND " \
                       f"Sex='{sex}' " \
                       f"Order by Year"
            temp_df = pd.read_sql(query_db, conn_vars['connection'])

        if state not in name_by_state.keys():
            name_by_state[state] = temp_df

    return name_by_state


def query_popularity(name, sex):
    """query() takes in the selections for Name and Sex as input and queries the Database.
    Returns the result of the query stored as a dataframe."""
    conn_vars = Connection.conn_vars

    #check if name exist in db
    try:
        if not conn_vars['engine'].dialect.has_table(conn_vars['engine'], name):
            raise ValueError(f"{name} not found in DB")
        else:
            query_db = f"Select * from {name} where Sex='{sex}' order by {name}.Year"
            df = pd.read_sql(query_db, conn_vars['connection'])
            if df.empty:
                null_data = [[0, 0, 0, 0], [0, 0, 0, 0]]
                df = pd.DataFrame(null_data, columns=['index', 'Sex', 'Qty', 'Year'])
    except sqlalchemy.exc.ProgrammingError:
        null_data = [[0, 0, 0, 0], [0, 0, 0, 0]]
        df = pd.DataFrame(null_data, columns=['index', 'Sex', 'Qty', 'Year'])

    return df

def check_tables(name):

    conn_vars = Connection.conn_vars
    if not conn_vars['engine'].dialect.has_table(conn_vars['engine'], name):
        raise ValueError(f"{name} not found in DB")

    return


if __name__ == "__main__":
    main()