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

def create_indexes():
    '''
    Create indexes in application's PostgreSQL
    database if they do not already exist
    '''
    i1_query = """CREATE INDEX IF NOT EXISTS player_team_index ON Player USING hash (team_id);"""
    i2_query = """CREATE INDEX IF NOT EXISTS home_team_index ON Game USING hash (home_team_id);"""
    i3_query = """CREATE INDEX IF NOT EXISTS away_team_index ON Game USING hash (away_team_id);"""

    conn = connect_database()
    cursor = conn.cursor()

    cursor.execute(i1_query)
    cursor.execute(i2_query)
    cursor.execute(i3_query)

    conn.commit()
    cursor.close()
    conn.close()


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
    (wins, losses) = cursor.fetchone()

    conn.commit()
    cursor.close()
    conn.close()

    return (wins, losses)


def get_team_past_games(team_id):
    '''
    Get a summary of a team's performance in their
    past games (date, opponent, score, w/l)
    '''
    conn = connect_database()
    cursor = conn.cursor()

    games_query = """
    PREPARE get_past_games(int) AS
    SELECT
        g1.date,
        (ateam1.name) AS opponent,
        (CONCAT(g1.home_score, ' - ', g1.away_score)) AS score,
        (CASE WHEN g1.home_score > g1.away_score THEN 'W' ELSE 'L' END) AS wl
    FROM team hteam1
        JOIN game g1 ON g1.home_team_id = hteam1.team_id
        JOIN team ateam1 ON g1.away_team_id = ateam1.team_id
    WHERE hteam1.team_id = $1
    UNION
    SELECT
        g2.date,
        (hteam2.name) AS opponent,
        (CONCAT(g2.away_score, ' - ', g2.home_score)) AS score,
        (CASE WHEN g2.away_score > g2.home_score THEN 'W' ELSE 'L' END) AS wl
    FROM team hteam2
        JOIN game g2 ON g2.home_team_id = hteam2.team_id
        JOIN team ateam2 ON g2.away_team_id = ateam2.team_id
    WHERE ateam2.team_id = $1;
    """

    cursor.execute(games_query)

    cursor.execute("EXECUTE get_past_games(%s)", team_id)
    past_games = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return past_games


def get_team_roster_stats(team_id):
    '''
    Get all the players on a team's roster and
    their average statistics per game
    '''
    conn = connect_database()
    cursor = conn.cursor()

    roster_query = """
    PREPARE get_roster_stats(int) AS
    SELECT
        MAX(CONCAT(p1.first_name, ' ', p1.last_name)) AS player_name,
        ROUND(AVG(s1.points), 1) AS PPG,
        ROUND(AVG(s1.assists), 1) AS APG,
        ROUND(AVG(s1.rebounds), 1) AS RPG,
        ROUND(AVG(s1.blocks), 1) AS BPG,
        ROUND(AVG(s1.steals), 1) AS SPG
    FROM player p1
        LEFT OUTER JOIN stats s1 ON p1.player_id = s1.player_id
    WHERE p1.team_id = $1
    GROUP BY p1.player_id;
    """

    cursor.execute(roster_query)

    cursor.execute("EXECUTE get_roster_stats(%s)", team_id)
    roster = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return roster


def get_team_stats_leaders(team_id):
    '''
    Get the players on a team who have the highest
    average for each per game statistic
    '''
    conn = connect_database()
    cursor = conn.cursor()

    leaders_query = """
    PREPARE get_stats_leaders(int) AS
    SELECT
        'PPG' AS stat_category,
        temp1.player_name
    FROM (
        SELECT
            MAX(CONCAT(p1.first_name, ' ', p1.last_name)) AS player_name,
            ROUND(AVG(s1.points), 1) AS PPG
        FROM player p1
            JOIN stats s1 ON p1.player_id = s1.player_id
        WHERE p1.team_id = $1
        GROUP BY p1.player_id
        ORDER BY PPG DESC
        LIMIT 1
    ) temp1
    UNION
    SELECT
        'APG' AS stat_category,
        temp2.player_name
    FROM (
        SELECT
            MAX(CONCAT(p2.first_name, ' ', p2.last_name)) AS player_name,
            ROUND(AVG(s2.assists), 1) AS APG
        FROM player p2
            JOIN stats s2 ON p2.player_id = s2.player_id
        WHERE p2.team_id = $1
        GROUP BY p2.player_id
        ORDER BY APG DESC
        LIMIT 1
    ) temp2
    UNION
    SELECT
        'RPG' AS stat_category,
        temp3.player_name
    FROM (
        SELECT
            MAX(CONCAT(p3.first_name, ' ', p3.last_name)) AS player_name,
            ROUND(AVG(s3.rebounds), 1) AS RPG
        FROM player p3
            JOIN stats s3 ON p3.player_id = s3.player_id
        WHERE p3.team_id = $1
        GROUP BY p3.player_id
        ORDER BY RPG DESC
        LIMIT 1
    ) temp3
    UNION
    SELECT
        'BPG' AS stat_category,
        temp4.player_name
    FROM (
        SELECT
            MAX(CONCAT(p4.first_name, ' ', p4.last_name)) AS player_name,
            ROUND(AVG(s4.blocks), 1) AS BPG
        FROM player p4
            JOIN stats s4 ON p4.player_id = s4.player_id
        WHERE p4.team_id = $1
        GROUP BY p4.player_id
        ORDER BY BPG DESC
        LIMIT 1
    ) temp4
    UNION
    SELECT
        'SPG' AS stat_category,
        temp5.player_name
    FROM (
        SELECT
            MAX(CONCAT(p5.first_name, ' ', p5.last_name)) AS player_name,
            ROUND(AVG(s5.steals), 1) AS SPG
        FROM player p5
            JOIN stats s5 ON p5.player_id = s5.player_id
        WHERE p5.team_id = $1
        GROUP BY p5.player_id
        ORDER BY SPG DESC
        LIMIT 1
    ) temp5;
    """

    cursor.execute(leaders_query)

    cursor.execute("EXECUTE get_stats_leaders(%s)", team_id)
    leaders = cursor.fetchall()

    conn.commit()
    cursor.close()
    conn.close()

    return leaders