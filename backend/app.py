import database as db
from flask import Flask, request, jsonify
from datetime import time, datetime

app = Flask(__name__)

# Connect to database
db.connect_sqlalchemy()

#######################
## Stats routes      ##
#######################

@app.route('/stats/get_stats', methods=['GET'])
def stats_data():
    stats = db.get_stats_table()
    stats_list = [
        {
            "player_id": stat.player_id,
            "game_id": stat.game_id,
            "points": stat.points,
            "assists": stat.assists,
            "rebounds": stat.rebounds,
            "blocks": stat.blocks,
            "steals": stat.steals
        }
        for stat in stats
    ]
    return jsonify(stats_list)

@app.route('/stats/add_stats', methods=['POST'])
def add_stats():
    data = request.get_json()
    db.add_player_stats(
        data['player_id'],
        data['game_id'],
        data['points'],
        data['assists'],
        data['rebounds'],
        data['blocks'],
        data['steals']
    )
    return jsonify({"message": "Stats added successfully"}), 200

@app.route('/stats/edit_stats', methods=['PUT'])
def edit_stats():
    data = request.get_json()
    db.edit_player_stats(
        data['player_id'],
        data['game_id'],
        data['points'],
        data['assists'],
        data['rebounds'],
        data['blocks'],
        data['steals']
    )
    return jsonify({"message": "Stats edited successfully"}), 200

@app.route('/stats/delete_stats', methods=['DELETE'])
def delete_stats():
    data = request.get_json()
    db.delete_player_stats(
        data['player_id'],
        data['game_id']
    )
    return jsonify({"message": "Stats deleted successfully"}), 200


#######################
## Player routes     ##
#######################

@app.route('/player/get_players', methods=['GET'])
def player_data():
    players = db.get_player_table()
    players_list = [
        {
            "player_id": player.player_id,
            "team_id": player.team_id,
            "first_name": player.first_name,
            "last_name": player.last_name,
            "position": player.position,
            "jersey_number": player.jersey_number
        }
        for player in players
    ]
    return jsonify(players_list)


#######################
## Game routes       ##
#######################

@app.route('/game/get_games', methods=['GET'])
def game_data():
    games = db.get_game_table()
    games_list = [
        {
            "game_id": game.game_id,
            "date": (game.date).strftime("%m/%d/%y"),
            "time": (game.time).strftime("%H:%M:%S"),
            "location": game.location,
            "home_team_id": game.home_team_id,
            "home_score": game.home_score,
            "away_team_id": game.away_team_id,
            "away_score": game.away_score
        }
        for game in games
    ]
    return jsonify(games_list)

#######################
## Team routes       ##
#######################
@app.route('/team/get_teams', methods=['GET'])
def team_data():
    teams = db.get_team_table()
    teams_list = [
        {
            "team_id": team.team_id,
            "name": team.name,
            "coach": team.coach
        }
        for team in teams
    ]
    return jsonify(teams_list)

#######################
## Report routes     ##
#######################
@app.route('/report/get_record', methods=['GET'])
def get_record():
    team_id = request.args.get('team_id')
    (wins, losses) = db.get_team_record(team_id)
    record = {
        'wins': wins,
        'losses': losses
    }
    return jsonify(record)

@app.route('/report/get_roster', methods=['GET'])
def get_roster():
    team_id = request.args.get('team_id')
    players = db.get_team_roster_stats(team_id)
    roster_list = [
        {
            'player_name': player_name,
            'ppg': ppg,
            'apg': apg,
            'rpg': rpg,
            'bpg': bpg,
            'spg': spg
        } for (player_name, ppg, apg, rpg, bpg, spg) in players
    ]
    return jsonify(roster_list)


# Main function - connect to DB and start app
if __name__ == "__main__":
    db.connect_sqlalchemy()
    app.run(debug=True, host="localhost", port=5000)