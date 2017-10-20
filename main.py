from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets

import sys
import os

import sys


class MediaItem(QtMultimedia.QMediaContent):
    def __init__(self, filename, start=0, stop=0, intermission=None):
        base = "/Volumes/HardDrive/Users/mark/Movies/CinemaCo/"
        url = QtCore.QUrl.fromLocalFile(base + filename + ".mp4")
        super(MediaItem, self).__init__(url)

        self.start = start
        self.stop = stop
        self.intermission = intermission
        self._intermission_due = False

    def prepare_play(self):
        if self.intermission is not None:
            self._intermission_due = True
        else:
            self._intermission_due = False

    def start_pos_ms(self):
        return self.start*1000

    def stop_pos_ms(self):
        return self.stop*1000

    def intermission_pos_ms(self):
        return self.intermission*1000

    def start_intermission(self, player):
        self._intermission_due = False
        print('intermission')
        player.pause()
        timer = QtCore.QTimer()
        timer.singleShot(5000, player.play)

    def intermission_due(self):
        return self._intermission_due

    def position_changed(self, position, player):
        print(position)
        if position < self.start_pos_ms():
            player.setPosition(self.start_pos_ms())
        if position > self.stop_pos_ms() > 0:
            player.playlist().next()
        if self.intermission_due() and position > self.intermission_pos_ms() > 0:
            self.start_intermission(player)

class Playlist(QtMultimedia.QMediaPlaylist):
    def __init__(self):
        self.media = []
        self.__start_pos_cache = None
        super(Playlist, self).__init__()
        self.currentIndexChanged.connect(self.current_media_index_changed)

    def add_media(self, media : QtMultimedia.QMediaContent):
        self.addMedia(media)
        self.media.append(media)

    def current_media_index_changed(self, index):
        self.media[index].prepare_play()

    def currentMedia(self):
        return self.media[self.currentIndex()]

class VideoPlayer(QVideoWidget):
    def __init__(self, parent=None):
        super(VideoPlayer, self).__init__(parent)

        # get player
        self.player = QtMultimedia.QMediaPlayer(self)
        self.player.setVideoOutput(self)

        self.player.positionChanged.connect(self.position_changed)
        #self.player.mediaStatusChanged.connect(self.position_changed)

        self.playlist = None

        #self.resize(300, 300)
        self.move(0, 0)

    def play(self, playlist):
        self.playlist = playlist
        self.playlist.setCurrentIndex(1)
        self.player.setPlaylist(self.playlist)
        self.player.play()

    # tell media that the position has changed
    def position_changed(self, position):
        media = self.current_media()
        if media is not None:
            media.position_changed(position, self.player)

    def current_media(self):
        if self.playlist is not None:
            return self.playlist.currentMedia()
        return None

    def fade_out(self, duration=5000):
        return self.fade(duration=duration, startval=1.0, endval=0.0)

    def fade_in(self, duration=5000):
        return self.fade(duration=duration, startval=0.0, endval=1.0)

    def fade(self, duration=0, startval=1.0, endval=0.0):
        self.animation = QtCore.QPropertyAnimation(self.opacityEffect, b"opacity",self)
        self.animation.setDuration(duration)
        self.animation.setStartValue(startval)
        self.animation.setEndValue(endval)
        self.animation.setEasingCurve(QtCore.QEasingCurve.OutBack)
        self.animation.start(QtCore.QPropertyAnimation.DeleteWhenStopped)
        self.animation.finished.connect(self.next)

    def bp(self):
        pass

app = QApplication(sys.argv)

w = VideoPlayer()
if True:
    w.setFullScreen(True)
    screen = app.screens()[1]
    w.windowHandle().setScreen(screen)
    w.setGeometry(screen.geometry())
w.show()

p = Playlist()
#media = MediaItem("trailer_alien", stop=3)
#p.add_media(media)

media = MediaItem("main_feature", start=10, intermission=12.5)
p.add_media(media)

media = MediaItem("trailer_gotg", stop=3)
p.add_media(media)

w.play(p)

timer = QtCore.QTimer()
timer.singleShot(1000, w.bp)


# fade
#eff = QtGui.QGraphicsOpacityEffect(w)
#
#a=QtGui.QPropertyAnimation(eff,"opacity")
#w.connect(a, a.finished,this,SLOT(hideThisWidget()));

sys.exit(app.exec_())
