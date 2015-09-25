from gi.repository import GObject, RB, Peas
from dispatcher import Dispatcher

class RmnPlugin (GObject.Object, Peas.Activatable):
	object = GObject.property(type=GObject.Object)
	last_song = None

	def __init__(self):
		super(RmnPlugin, self).__init__()

	'''
	virtual fonction called when the plugin is activated
	'''
	def do_activate(self):
		print("Loading RMNPLlugin")
		self.shell = self.object
		self.shell_player = self.shell.props.shell_player
		self.id_playing_song_changed = self.shell_player.connect("playing-song-changed", self.playing_song_changed)
		self.id_playing_changed = self.shell_player.connect("playing-changed", self.playing_changed)
		pass

	''' 
	virtual function called when the plugin is deactivated
	'''
	def do_deactivate(self):
		Dispatcher.send_stop()
		self.shell_player.disconnect(self.id_playing_song_changed)
		self.shell_player.disconnect(self.id_playing_changed)
		pass

	'''
	callback for ShellPlayer's playing-song-changed
	'''
	def playing_song_changed(self, shell, entry):
		print("Song changed")

		song = RmnPlugin.get_song_info(None, entry)
		print( song )
		#Dispatcher.send_song(song)
		self.last_song = song
				
	'''
	callback for ShellPlayer's playing-changed (started/stopped)
	'''
	def playing_changed(self, shell, playing):
		print("playing changed")
		if not playing:
			Dispatcher.send_stop()
		else:
			if self.last_song is not None:
				Dispatcher.send_song(self.last_song)
		
	@staticmethod
	def get_song_info(db, entry):
		# we don't want the PROP_MEDIA_TYPE, as it doesn't contain mimetype
		# of the audio file itself
		song = {
			"album": entry.get_string(RB.RhythmDBPropType.ALBUM),
			"artist": entry.get_string(RB.RhythmDBPropType.ARTIST),
			"title":  entry.get_string(RB.RhythmDBPropType.TITLE),
			"location": entry.get_playback_uri(),
		}
		return song

