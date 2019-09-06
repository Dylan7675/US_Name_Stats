"""This script is specifically meant for connecting to the database and passing
 back the connection and the MetaData """

from sqlalchemy import create_engine, MetaData
import os


def connect():
    """connects to db and returns connection, MetaData """
    user = os.environ['NAME_STAT_USER']
    password = os.environ['NAME_STAT_PASS']
    engine = create_engine(f"mysql+pymysql://{user}:{password}@localhost/US_Names", echo=False)

    connection = engine.connect()
    metadata = MetaData(engine)

    return(connection, metadata, engine)


if __name__ == "__main__":
    main()

