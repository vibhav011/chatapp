from flask import Flask, render_template
from flask_socketio import SocketIO

chatrooms = []

app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

@app.route('/')
def join():
	return render_template('join.html')

@app.route('/chatroom')
def chatroom():
	return render_template('chatroom.html')

@socketio.on('create request')
def check_aval(msg, methods = ['GET', 'POST']):
	aval = 1
	for room in chatrooms :
		if room[0] == msg['roomname'] :
			aval = 0

	if aval == 1 :
		chatrooms.append([msg['roomname'], msg['id'], 1])

	socketio.emit(msg['id'], str(aval))

@socketio.on('join request')
def check_room(msg, methods = ['GET', 'POST']):
	found = 0
	for room in chatrooms :
		if room[1] == msg['roomcode'] :
			found = 1
			room[2] += 1

	socketio.emit(msg['id'], str(found))

@socketio.on('send message')
def forward_message(msg, methods = ['GET', 'POST']):
	socketio.emit(msg['rcode'], {'user' : msg['user'], 'message' : msg['message']})

@socketio.on('send info')
def send_info(rc) :
	for room in chatrooms :
		if room[1] == rc :
			socketio.emit('get info ' + str(rc), {'roomname' : room[0], 'active' : room[2]})
			break

if __name__ == '__main__':
	socketio.run(app, debug=True)