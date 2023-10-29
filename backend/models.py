# Specify Database Models / Schema
import sqlalchemy
from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Team(Base):
    __tablename__='team'

    team_id = Column(Integer, primary_key=True)
    name = Column(String(50))
    coach = Column(String(30))

class Player(Base):
    __tablename__='player'

    player_id = Column(Integer, primary_key=True)
    team_id = Column(Integer, ForeignKey('team.team_id'))
    first_name = Column(String(30))
    last_name = Column(String(30))
    position = Column(String(3))
    jersey_number = Column(Integer)

class Game(Base):
    __tablename__='game'

    game_id = Column(Integer, primary_key=True)
    date = Column(Date)
    time = Column(Time)
    location = Column(String(100))
    home_team_id = Column(Integer, ForeignKey('team.team_id'))
    home_score = Column(Integer)
    away_team_id = Column(Integer, ForeignKey('team.team_id'))
    away_score = Column(Integer)

class Stats(Base):
    __tablename__='stats'

    player_id = Column(Integer, ForeignKey('player.player_id'), primary_key=True)
    game_id = Column(Integer, ForeignKey('game.game_id'), primary_key=True)
    points = Column(Integer)
    assists = Column(Integer)
    rebounds = Column(Integer)
    blocks = Column(Integer)
    steals = Column(Integer)