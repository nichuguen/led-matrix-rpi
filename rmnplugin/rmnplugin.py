from gi.repository import GObject, RB, Peas


class RmnPlugin (GObject.Object, Peas.Activatable):
	object = GObject.property(type=GObject.Object)

	def __init__(self):
		super(RmnPlugin, self).__init__()

	def do_activate(self):
		print("Loading RMNPLlugin")
		self.shell = self.object
		self.shell_player = self.shell.props.shell_player
		self.id_playing_song_changed = self.shell_player.connect("playing-song-changed", self.playing_song_changed)
		self.id_playing_changed = self.shell_player.connect("playing-changed", self.playing_changed)
		pass

	def do_deactivate(self):
		self.shell_player.disconnect(self.id_playing_song_changed)
		self.shell_player.disconnect(self.id_playing_changed)
		pass

	def playing_song_changed(self, shell, entry):
		print("Song changed")
		print( RmnPlugin.get_song_info(None, entry))
	
	def playing_changed(self, shell, playing):
		if not playing:
			#todo
			pass
		
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

