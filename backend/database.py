# Connect to Database and define operations
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import *

#########################
## Connect to Database ##
#########################
load_dotenv(dotenv_path='C:/Users/Lexie/BasketballLeagueManager/.env')
db_uri = os.getenv("DB_URI")
if db_uri is None:
    raise Exception("DB_URI is not defined in the .env file")
# connection global variable
session = None

def connect_sqlalchemy():
    engine = sqlalchemy.create_engine(db_uri, echo=False)

    global session
    session = scoped_session(sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=engine))
    
    global Base
    Base.query = session.query_property()
    Base.metadata.create_all(bind=engine)

connect_sqlalchemy()