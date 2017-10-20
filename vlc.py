class MediaPlayerWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super(MediaPlayerWidget, self).__init__(parent)
        self.resize(700, 700)
        self.instance = vlc.Instance('--no-audio', '--fullscreen')
        if self.instance is None:
            raise EnvironmentError
        else:
            self.player = self.instance.media_player_new()
            self.player.set_nsobject(self.winId())

    def volume(self):
        return self.instance.audio_get_volume()

    def play_media(self,url):
        self.media = i.media_new(url)
        self.player.set_media(self.media)
        self.player.play()

    def url(self):
        return self.media.get_murl()

vlcWidget = MediaPlayerWidget()
vlcWidget.show()

vlcWidget.play('file:///Volumes/HardDrive/Users/mark/Movies/MDG_0769.MOV')