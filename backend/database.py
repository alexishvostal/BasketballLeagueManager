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


#################################
## Stats Table CRUD Operations ##
#################################

def get_stats_table():
    '''
    Retrieve all rows in the Stats table
    '''
    return Stats.query.all()

def add_player_stats(player_id, game_id, points, assists,
                     rebounds, blocks, steals):
    '''
    Add a player's stats for a game to the Stats table
    '''
    new = Stats(player_id=player_id, game_id=game_id, points=points,
                assists=assists, rebounds=rebounds, blocks=blocks,
                steals=steals)
    session.add(new)
    session.commit()

def edit_player_stats(player_id, game_id, points, assists,
                      rebounds, blocks, steals):
    '''
    Edit a player's stats for a game in the Stats table
    '''
    stat = Stats.query.filter_by(player_id=player_id, game_id=game_id).first()
    stat.points = points
    stat.assists = assists
    stat.rebounds = rebounds
    stat.blocks = blocks
    stat.steals = steals
    session.commit()

def delete_player_stats(player_id, game_id):
    '''
    Delete a player's stats for a game in the Stats table
    '''
    Stats.query.filter_by(player_id=player_id, game_id=game_id).delete()
    session.commit()


#######################
## Testing Functions ##
#######################    

def stats_testing():
    '''
    Function to test CRUD operations for Stats table
    '''
    connect_sqlalchemy()
    add_player_stats(3, 1, 10, 4, 2, 0, 0)
    for stat in get_stats_table():
        print(stat.player_id, stat.game_id, stat.points, stat.assists, 
              stat.rebounds, stat.blocks, stat.steals)
    print("######################################")
    edit_player_stats(3, 1, 5, 5, 5, 5, 5)
    for stat in get_stats_table():
        print(stat.player_id, stat.game_id, stat.points, stat.assists, 
              stat.rebounds, stat.blocks, stat.steals)
    print("######################################")
    delete_player_stats(3, 1)
    for stat in get_stats_table():
        print(stat.player_id, stat.game_id, stat.points, stat.assists, 
              stat.rebounds, stat.blocks, stat.steals)
    print("######################################")

#stats_testing()