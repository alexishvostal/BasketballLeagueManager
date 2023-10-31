import database as db
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to database
db.connect_sqlalchemy()

#@app.route('/')
#def root():
#    return "This is the API for BasketballLeagueManager"

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

# Main function - connect to DB and start app
if __name__ == "__main__":
    db.connect_sqlalchemy()
    app.run(debug=True, host="localhost", port=5000)