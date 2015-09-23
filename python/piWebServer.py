from flask import Flask, request, jsonify
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
    showtext.clearLEDMatrix()

@app.route("/", methods=['GET', 'POST'])
def serv():
    dict_return = {'type': None, 'result': False}
    if request.method == 'GET':
        return "<h1>NATHING TO SEE HERE BUT IT WERKS</h1>"
    elif request.method == 'POST':
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
            clear_led()
            dict_return['type'] = "stop"
            dict_return['result'] = True
        elif message_type == "message":
            # display message on led
            global color, pid
            message = request.form.get('message', None)
            clear_led()
            pid = showtext.showOnLEDMatrix(message, color['message'])
            dict_return['type'] = "message"
            dict_return['result'] = True
        return jsonify(**dict_return)


if __name__ == "__main__":
    app.debug = True
    app.run(host = "0.0.0.0")
