from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

win = 0
loss = 0
mistakes = 0
randnum = 0
not_generated = True

@app.route('/update', methods=['POST'])
def update():
    global win
    global loss
    global mistakes
    response = 0
    if 'quit' in request.json['name']:                   #if player quit
        response = answer(-1)
    elif 'reset' in request.json['name']:                #if player reset scoreboard
        response = answer(-2)
    else:                                        #if player guess incorrectly
        response = answer(int(request.json['num']))
    print('win:',win)
    print('loss:',loss)
    print('mistakes:',mistakes)
    print('response:',response)
    data = {'response':response, 'win':win, 'loss':loss, 'mistakes':mistakes}
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
        else:
            responce = 0
            mistakes += 1
    print(randnum)
    return responce

if __name__ == '__main__':
    app.run(debug=True)