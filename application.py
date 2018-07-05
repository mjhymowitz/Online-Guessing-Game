from flask import Flask, render_template, request, jsonify, make_responce,
import random
import os

app = Flask(__name__)

win = 0
loss = 0
mistakes = 0
randnum = 0
not_generated = True
data = {}

@app.route('/update', methods=['POST'])
def update():
    get_score()
    global win
    global loss
    global mistakes
    response = 0
    if 'quit' in request.json['name']:                   #if player quit
        response = answer(-1)
    elif 'reset' in request.json['name']:                #if player reset scoreboard
        response = answer(-2)
    else:                                                #if player guess number
        response = answer(int(request.json['num']))
    data = {'response':response, 'win':win, 'loss':loss, 'mistakes':mistakes}
    set_score()
    return jsonify(data)

@app.route("/",  methods = ['GET'])
def hello():
    return render_template('home.html')
    
def answer(num):
    global not_generated
    global randnum
    global win
    global loss
    global mistakes
    breaker = -1
    reset = -2
    responce = 0 
    if not_generated:
        randnum = random.randint(1,100)
        not_generated = False
    if num == breaker:
        randnum = random.randint(1,100)
        responce = 2
        mistakes = 0
        loss += 1
    elif num == reset:
        win = 0
        loss = 0
        mistakes = 0
        responce = 3
    else:
        if num == randnum:
            responce = 1
            win += 1
            randnum = random.randint(1,100)
        elif num > randnum:
            responce = 0
            mistakes += 1
        else:
            responce = 4
            mistakes += 1
    return responce

def get_score():
    global win
    global loss
    global mistakes
    ip = request.remote_addr
    if ip in data:
        win = data[ip]['win']
        loss = data[ip]['loss']
        mistakes = data[ip]['mistakes']
    else:
        data = {ip:{'win':0,'loss':0,'mistakes':0}}

def set_score():
    data[ip]['win'] = win
    data[ip]['loss'] = loss
    data[ip]['mistakes'] = mistakes

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
