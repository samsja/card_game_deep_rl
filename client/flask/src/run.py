from flask import Flask, render_template
from handler import get_path_card
import requests as r

import os

api_host = os.getenv("API_HOST","localhost:8888")
my_host = os.getenv("MY_HOST","localhost:8000")



app = Flask(__name__,
            static_url_path='',
            static_folder='web/static',
            template_folder='web/templates')


@app.route('/')
def home():
    return render_template('home.html',
                            my_host = my_host, 
                            api_host=api_host,
                            colors = ["SPADE","CLUB","HEART","DIAMOND"]
                        
                                
                            )



@app.route('/play/<player_index>')
def play(player_index):


    try :
        hand = r.get(f"http://{api_host}/hands/{player_index}")
    except r.exceptions.HTTPError as errh:
        return f"Http Error:{errh}",500
    except r.exceptions.ConnectionError as errc:
        return f"Error Connecting:{errc}",500
    except r.exceptions.Timeout as errt:
        return f"Timeout Error:{errt}",500
    except r.exceptions.RequestException as err:
        return f"OOps: Something Else {err}",500


    Cards = []
    for card in hand.json():
        Cards.append(get_path_card(hand.json()[card]))


    try :
        trick = r.get(f"http://{api_host}/current_trick")
    except r.exceptions.HTTPError as errh:
        return f"Http Error:{errh}",500
    except r.exceptions.ConnectionError as errc:
        return f"Error Connecting:{errc}",500
    except r.exceptions.Timeout as errt:
        return f"Timeout Error:{errt}",500
    except r.exceptions.RequestException as err:
        return f"OOps: Something Else {err}",500



    trick_cards= ["" for i in range(4)]
    for key in trick.json().keys():
        card_played = trick.json()[key]
        player = card_played["player"]
        card = card_played["card"]
        trick_cards[player]=get_path_card(card)


    trick_str=[str((i-int(player_index))%4) for i in range(4)]

    return render_template("hand.html",
                            Cards = Cards,
                            len_card=len(Cards),
                            trick = trick_cards,
                            len_trick=len(trick_cards),
                            trick_str=trick_str,
                            player=player_index,
                            bets_available = ["pass","coinche"] + [str(80 + 10*i) for i in range(9)] + ["250","270","500"],
                            colors = ["SPADE","CLUB","HEART","DIAMOND"],
                            api_host = api_host,
                            my_host = my_host
                           )


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
