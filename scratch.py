
print(os.environ['VLC_PLUGIN_PATH'])

app = QtWidgets.QApplication(sys.argv)

app.setApplicationName('Cinema Video Player')

url = QtCore.QUrl.fromLocalFile('/Volumes/HardDrive/Users/mark/Movies/MDG_0769.MOV')
content = QtMultimedia.QMediaContent(url)
player = QtMultimedia.QMediaPlayer()
player.setMedia(content)

player.stateChanged.connect( app.quit )

videoWidget = QtMultimediaWidgets.QVideoWidget()
player.setVideoOutput(videoWidget);
videoWidget.show()
player.play()
app.exec()