# Connect to Database and define operations
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine, insert
from sqlalchemy.orm import sessionmaker, scoped_session
from models import *
from sample_data.teams import sample_teams
from sample_data.players import sample_players
from sample_data.games import sample_games
from sample_data.stats import sample_stats


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
    '''
    Connect SQLAlchemy to application's PostgreSQL database and
    create tables if they do not already exist.
    '''
    engine = sqlalchemy.create_engine(db_uri, echo=False)

    global session
    session = scoped_session(sessionmaker(bind=engine))
    
    global Base
    Base.query = session.query_property()
    Base.metadata.create_all(bind=engine)

def initialize_tables():
    '''
    Populate database with example instance
    '''
    connect_sqlalchemy()
    # Add Teams
    teams_to_insert = insert(Team).values(sample_teams)
    session.execute(teams_to_insert)
    session.commit()
    # Add Players
    players_to_insert = insert(Player).values(sample_players)
    session.execute(players_to_insert)
    session.commit()
    # Add Games
    games_to_insert = insert(Game).values(sample_games)
    session.execute(games_to_insert)
    session.commit()
    # Add Stats
    stats_to_insert = insert(Stats).values(sample_stats)
    session.execute(stats_to_insert)
    session.commit()

#initialize_tables()