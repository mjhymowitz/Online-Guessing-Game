from flask import Flask, render_template, request, jsonify, session
import random
import os

app = Flask(__name__)
app.secret_key = 'super secret key'

not_generated = True

@app.route('/update', methods=['POST'])
def update():
    response = 0
    session_start()
    if 'quit' in request.json['name']:                   #if player quit
        response = answer(-1)
    elif 'reset' in request.json['name']:                #if player reset scoreboard
        response = answer(-2)
    else:                                                #if player guess number
        response = answer(int(request.json['num']))
    data = {'response':response, 'win':session['win'], 'loss':session['loss'], 'mistakes':session['mistakes']}
    return jsonify(data)

@app.route("/",  methods = ['GET'])
def hello():
    return render_template('home.html')
    
def answer(num):
    global not_generated
    breaker = -1
    reset = -2
    responce = 0 
    if not_generated:
        session['randnum'] = random.randint(1,100)
        not_generated = False
    if num == breaker:
        session['randnum'] = random.randint(1,100)
        responce = 2
        session['mistakes'] = 0
        session['loss'] += 1
    elif num == reset:
        session['win'] = 0
        session['loss'] = 0
        session['mistakes'] = 0
        responce = 3
    else:
        if num == session['randnum']:
            responce = 1
            session['win'] += 1
            session['randnum'] = random.randint(1,100)
        elif num > session['randnum']:
            responce = 0
            session['mistakes'] += 1
        else:
            responce = 4
            if 'mistakes' in session:
                session['mistakes'] += 1
            else:
                session['mistakes'] = 1
    return responce

def session_start():
    # if not 'randnum' in session:
    if 'mistakes' not in session:
        session['win'] = 0
        session['loss'] = 0
        session['mistakes'] = 0
        session['randnum'] = 0

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

