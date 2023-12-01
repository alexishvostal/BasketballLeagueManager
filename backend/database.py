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


#####################################
## Connect and Initialize Database ##
#####################################

load_dotenv(dotenv_path='C:/Users/Lexie/BasketballLeagueManager/.env')
db_uri = os.getenv("DB_URI")
if db_uri is None:
    raise Exception("DB_URI is not defined in the .env file")

def connect_sqlalchemy():
    '''
    Connect SQLAlchemy to application's PostgreSQL database and
    create tables if they do not already exist.
    '''
    global engine
    engine = sqlalchemy.create_engine(db_uri, echo=False)
    
    global Base
    Base.metadata.create_all(bind=engine)

def initialize_tables():
    '''
    Populate database with example instance
    '''
    session = scoped_session(sessionmaker(bind=engine))

    # Add Teams
    teams_to_insert = insert(Team).values(sample_teams)
    session.execute(teams_to_insert)
    # Add Players
    players_to_insert = insert(Player).values(sample_players)
    session.execute(players_to_insert)
    # Add Games
    games_to_insert = insert(Game).values(sample_games)
    session.execute(games_to_insert)
    # Add Stats
    stats_to_insert = insert(Stats).values(sample_stats)
    session.execute(stats_to_insert)

    session.commit()
    session.close()


#################################
## Stats Table CRUD Operations ##
#################################

def get_stats_table():
    '''
    Retrieve all rows in the Stats table
    '''
    session = scoped_session(sessionmaker(bind=engine))
    stats = session.query(Stats).all()
    session.close()
    return stats

def add_player_stats(player_id, game_id, points, assists,
                     rebounds, blocks, steals):
    '''
    Add a player's stats for a game to the Stats table
    '''
    session = scoped_session(sessionmaker(bind=engine))
    new = Stats(player_id=player_id, game_id=game_id, points=points,
                assists=assists, rebounds=rebounds, blocks=blocks,
                steals=steals)
    session.add(new)
    session.commit()
    session.close()

def edit_player_stats(player_id, game_id, points, assists,
                      rebounds, blocks, steals):
    '''
    Edit a player's stats for a game in the Stats table
    '''
    session = scoped_session(sessionmaker(bind=engine))
    stat = session.query(Stats).filter_by(player_id=player_id, game_id=game_id).first()
    stat.points = points
    stat.assists = assists
    stat.rebounds = rebounds
    stat.blocks = blocks
    stat.steals = steals
    session.commit()
    session.close()

def delete_player_stats(player_id, game_id):
    '''
    Delete a player's stats for a game in the Stats table
    '''
    session = scoped_session(sessionmaker(bind=engine))
    session.query(Stats).filter_by(player_id=player_id, game_id=game_id).delete()
    session.commit()
    session.close()


############################
## Player Table Functions ##
############################

def get_player_table():
    '''
    Retrieve all rows in the Player table
    '''
    session = scoped_session(sessionmaker(bind=engine))
    players = session.query(Player).all()
    session.close()
    return players

##########################
## Game Table Functions ##
##########################
def get_game_table():
    '''
    Retrieve all rows in the Game table
    '''
    session = scoped_session(sessionmaker(bind=engine))
    games = session.query(Game).all()
    session.close()
    return games