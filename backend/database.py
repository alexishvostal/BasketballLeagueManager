# Connect to Database and define operations
import os
from dotenv import load_dotenv
import psycopg2
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
database = os.getenv("DATABASE")
user = os.getenv("USER")
password = os.getenv("PASSWORD")
host = os.getenv("HOST")
port = os.getenv("PORT")
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


def connect_database():
    '''
    Connect to application's PostgreSQL database
    '''
    conn = psycopg2.connect(
        database=database,
        user=user,
        password=password,
        host=host,
        port=port
    )
    return conn


def initialize_tables():
    '''
    Populate database with example instance
    '''
    connect_sqlalchemy()
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


##########################
## Team Table Functions ##
##########################
def get_team_table():
    '''
    Retrieve all rows in the Team table
    '''
    session = scoped_session(sessionmaker(bind=engine))
    teams = session.query(Team).all()
    session.close()
    return teams


######################
## Report Functions ##
######################
def get_team_record(team_id):
    '''
    Get a team's win-loss record from their previous games
    '''
    conn = connect_database()
    cursor = conn.cursor()

    record_query = """
    PREPARE get_record (int) AS
    SELECT 
        (tbl.num_home_wins + tbl.num_away_wins) AS wins,
        (tbl.num_home_losses + tbl.num_away_losses) AS losses
    FROM (
        SELECT
            (
                SELECT COUNT(*) 
                FROM game g1 
                WHERE g1.home_team_id = team.team_id AND 
                    g1.home_score > g1.away_score
            ) AS num_home_wins,
            (
                SELECT COUNT(*) 
                FROM game g2
                WHERE g2.away_team_id = team.team_id AND 
                    g2.away_score > g2.home_score
            ) AS num_away_wins,
            (
                SELECT COUNT(*) 
                FROM game g3
                WHERE g3.home_team_id = team.team_id AND 
                    g3.home_score < g3.away_score
            ) AS num_home_losses,
            (
                SELECT COUNT(*) 
                FROM game g4
                WHERE g4.away_team_id = team.team_id AND 
                    g4.away_score < g4.home_score
            ) AS num_away_losses
        FROM team
        WHERE team.team_id = $1
    ) tbl;
    """
    cursor.execute(record_query)

    cursor.execute("EXECUTE get_record(%s)", team_id)
    row = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return row