"""This script is specifically meant for connecting to the database and passing
 back the connection and the MetaData """

from sqlalchemy import create_engine, MetaData


def connect():
    """connects to db and returns connection, MetaData """
    engine = create_engine("mysql+pymysql://admindrm:7259988Aa!!263Dy530aW?@localhost/US_Names",
        echo=False)

    connection = engine.connect()
    metadata = MetaData(engine)
    # metadata.reflect(engine)

    return(connection, metadata, engine)



if __name__ == "__main__":
    main()

