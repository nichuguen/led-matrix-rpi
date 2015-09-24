from flask import Flask, request, jsonify, url_for, render_template, redirect
import showtext
import os
import signal

#global tuple relating text to its color
color = {'artist': (255, 0, 0), 'album': (130, 52, 0), 'title': (0, 255, 0), 'message': (255, 255, 255)}
app = Flask(__name__)
pid = 0

def change_color(color_tuple, key):
    # color_tuple is a tuple (R,G,B) where RGB are ints
    # key defines which of the three stuffs to change
    global color
    for value in color_tuple:
		if value > 255 or value < 0:
			return
    if key in color.keys():
        color[key] = color_tuple


def update_led(artist, album, title):
    global color, pid
    title_tuple = ("- Titre: "+title+" -", color['title'])
    artist_tuple = ("- Artiste: " + artist + " -", color['artist'])
    album_tuple = ("- Album: "+album + " -", color['album'])
    print(title_tuple)
    list_tuples = [title_tuple, artist_tuple, album_tuple]
    pid = showtext.showOnLEDMatrix(list_tuples, False)

def clear_led():
    global pid
    if pid != 0:
        os.kill(pid, signal.SIGKILL)
        pid = 0
    showtext.clearLEDMatrix()

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        return render_template("home.html")
    elif request.method == 'POST':
		dict_return = {'type': None, 'result': False}
		message_type = request.form.get('type', None)
		if message_type == "song":
			dict_return['type'] = "song"
			artist = request.form.get('artist', None)
			album = request.form.get('album', None)
			title = request.form.get('title', None)
			if artist is not None and album is not None and title is not None:
				clear_led()
				update_led(artist, album, title)
				dict_return['result'] = True
		elif message_type == "stop":
			# clears led
			dict_return['type'] = "stop"
			clear_led()
			dict_return['result'] = True
		elif message_type == "message":
			# display message on led
			global color, pid
			dict_return['type'] = "message"
			message = request.form.get('message', None)
			clear_led()
			if message is not None:
				pid = showtext.showOnLEDMatrix([(message, color['message'])])
				dict_return['result'] = True
		if request.form.get('redirect', None) is None:
			return jsonify(**dict_return)
		else:
			return redirect(url_for("home"))
			
@app.route("/config", methods=['GET', 'POST'])
def config():
	global color
	if request.method == 'GET':
		return render_template("config.html", keys= color.keys() )
	elif request.method == 'POST':
		key = request.form.get('key')
		if key is not None:
			if key in color.keys():
				r = request.form.get('r')
				g = request.form.get('g')
				b = request.form.get('b')
				print((r,g,b))
				r = int(r is not None)*255
				g = int(g is not None)*255
				b = int(b is not None)*255
				print((r,g,b))
				change_color((r, g, b), key)
		return redirect(url_for("config"))
		
if __name__ == "__main__":
	import atexit
	atexit.register(clear_led)
	app.debug = True
	try:
		app.run(host = "0.0.0.0")
	except KeyboardInterrupt:
		clear_led()
		raise
