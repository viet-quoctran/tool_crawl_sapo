import os
import urllib.parse as up
import psycopg2

def connect_to_database():
    try:
        up.uses_netloc.append("postgres")
        url = up.urlparse("postgres://tofzkkbb:nytl6GEmWB2oKM7CEicSbLjWZqrFcCDC@rain.db.elephantsql.com/tofzkkbb")
        conn = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        print("Connect database successfuly")
        return conn
    except Exception as e:
        print("Error connect database", e)
        return None

conn = connect_to_database()
