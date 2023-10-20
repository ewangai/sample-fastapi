from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

#SQLALCHEMY_DATABASE_URL = "postgresql://<username>:<password>@<ip address>/<hostname>/<databse_name>"
#SQLALCHEMY_DATABASE_URL = "postgresql://postgres:Johanna12.@localhost/fastapi"
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'
#Issue exposing username and password.


engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Dependency Function
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


#while True:
#    try:
#        #conn = psycopg2.connect(host, database ,user, password, ReadDictCursor for column names )
#        conn = psycopg2.connect(host='localhost', database='fastapi' ,user='postgres', password='Johanna12.', cursor_factory=RealDictCursor)
#        cursor = conn.cursor() # DB object
#        print("Database connection was successful")
#        break
#    except Exception as error:
#        print("Connecting to database failed")
#        print("Error", error)
#        time.sleep(2)
#
