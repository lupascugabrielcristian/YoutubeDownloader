class YoutubeLogger(object):
	def debug(self, msg):
		pass

	def warning(self, msg):
		pass

	def error(self, msg):
		print(msg)


class PlaylistLogger(object):
	def debug(self, msg):
		if "of" in msg:
			print(msg)

	def warning(self, msg):
		print("Warning: " + msg)

	def error(self, msg):
		print(msg)


