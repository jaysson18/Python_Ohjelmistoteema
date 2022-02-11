from flask import Flask, request
import mysql.connector
import config
from game import Game
from airport import Airport
import json

app = Flask(__name__)

# Tietokantayhteys
config.conn = mysql.connector.connect(
         host='127.0.0.1',
         port= 3306,
         database='lento',
         user='lentopassi',
         password='piLo_t5AD'
         )

def fly(id,dest):
    game = Game(id)
    game.set_location(Airport(dest))
    game.location.getWeather()
    game.location.find_nearby_airports()
    json_data = json.dumps(game, default=lambda o: o.__dict__, indent=4)
    return json_data


# http://127.0.0.1:5000/flyto?game=123&dest=HEL
@app.route('/flyto')
def flyto():
    args = request.args
    id = args.get("game")
    dest = args.get("dest")
    json_data = fly(id, dest)
    return json_data


# http://127.0.0.1:5000/newgame?player=Vesa&loc=RVN
@app.route('/newgame')
def newgame():
    args = request.args
    player = args.get("player")
    loc = args.get("loc")
    #reply = main.new_game(player, loc)
    game = Game(0, player, loc)
    json_data = fly(game.id, loc)
    return json_data
    #return reply



if __name__ == '__main__':
    app.run(use_reloader=True, host='127.0.0.1', port=5000)