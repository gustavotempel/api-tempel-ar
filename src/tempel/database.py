
import os
import psycopg2


def retrieve_database_config():
    """
    Returns an environment variable corresponding to the database configuration in the following format:
    postgres://{user}:{password}@{hostname}:{port}/{database-name}
    """
    try:
        config = os.environ["DATABASE_URL"]
    except:
        pass
    return config


DB_CONFIG = retrieve_database_config()


def select_query(query, config=DB_CONFIG):
    cursor = None
    try:
        connection = psycopg2.connect(config, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as error:
        print("Error connecting to data base.", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def modify_query(query, config=DB_CONFIG):
    cursor = None
    try:
        connection = psycopg2.connect(config, sslmode="require")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except Exception as error:
        print("Error connecting to data base.", error)
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

