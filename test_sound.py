import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl, QTimer

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("MP3音效测试")
window.resize(300, 100)
window.show()

player = QMediaPlayer()
player.setMedia(QMediaContent(QUrl.fromLocalFile("click.mp3")))  # 确认你的路径对哦
player.setVolume(90)  # 音量90%

def play_sound():
    player.play()

QTimer.singleShot(500, play_sound)  # 延迟0.5秒播放，保证窗口先弹出来

sys.exit(app.exec_())
