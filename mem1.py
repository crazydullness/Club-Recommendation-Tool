import sys
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QComboBox, QDialog, QScrollArea, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QColor, QPainter
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect


class ParticleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(50)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

    def update_particles(self):
        if len(self.particles) < 100:
            self.particles.append({
                'x': random.randint(0, self.width()),
                'y': random.randint(0, self.height()),
                'dx': random.uniform(-0.5, 0.5),
                'dy': random.uniform(-1.0, -0.5),
                'radius': random.randint(1, 3),
                'color': QColor(255, 255, 255, random.randint(80, 180))
            })
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
        self.particles = [p for p in self.particles if p['y'] > -10]
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        for p in self.particles:
            painter.setBrush(p['color'])
            painter.setPen(Qt.NoPen)
            painter.drawEllipse(int(p['x']), int(p['y']), p['radius'], p['radius'])


class AboutDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("关于本程序")
        self.setFixedSize(400, 250)
        layout = QVBoxLayout()
        label = QLabel("这是一个炫酷的社团推荐系统🎉\n\n"
                       "你只需输入兴趣关键词，如“编程”“摄影”或“音乐”，\n"
                       "系统会根据内容推荐相应社团，并展示他们的简介和动态。\n\n"
                       "还有音效、音乐选择、粒子背景等酷炫功能，祝你使用愉快！")
        label.setWordWrap(True)
        layout.addWidget(label)
        self.setLayout(layout)


class ClubDetailDialog(QDialog):
    def __init__(self, club_name, club_desc):
        super().__init__()
        self.setWindowTitle(f"{club_name} - 详情")
        self.setFixedSize(400, 300)
        layout = QVBoxLayout()
        name_label = QLabel(f"<h2>{club_name}</h2>")
        desc_label = QLabel(club_desc)
        desc_label.setWordWrap(True)
        layout.addWidget(name_label)
        layout.addWidget(desc_label)
        self.setLayout(layout)


class ClubRecommendationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("社团推荐系统")
        self.resize(1000, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.history_keywords = []

        self.initUI()
        self.set_background("images/bg.jpg")

        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("click.mp3"))
        self.click_sound.setVolume(0.5)

        self.music_player = QMediaPlayer()
        self.music_list = ["kikujirou.mp3", "wedding.mp3", "alley.mp3"]

        self.particle_widget = ParticleWidget(self.central_widget)
        self.particle_widget.setGeometry(0, 0, self.width(), self.height())
        self.particle_widget.lower()

        self.display_default_recommendations()

    def resizeEvent(self, event):
        self.particle_widget.setGeometry(0, 0, self.width(), self.height())

    def set_background(self, path):
        pixmap = QPixmap(path)
        if not pixmap.isNull():
            palette = QPalette()
            palette.setBrush(QPalette.Window, QBrush(pixmap.scaled(
                self.size(), Qt.IgnoreAspectRatio, Qt.SmoothTransformation)))
            self.setPalette(palette)
        else:
            print("背景图加载失败")

    def initUI(self):
        main_layout = QVBoxLayout()

        self.title = QLabel("")
        self.title.setFont(QFont("微软雅黑", 28, QFont.Bold))
        self.title.setStyleSheet("color: #222222; margin-top: 20px;")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)
        self.typing_animation("社团推荐系统")

        input_layout = QHBoxLayout()

        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("请输入你的兴趣关键词，例如：编程、音乐、摄影……")
        self.input_box.setStyleSheet("padding: 10px; font-size: 16px; border-radius: 10px; color: #222222;")
        input_layout.addWidget(self.input_box)

        recommend_btn = QPushButton("推荐社团")
        recommend_btn.setCursor(Qt.PointingHandCursor)
        recommend_btn.setStyleSheet(self.button_style())
        recommend_btn.clicked.connect(self.recommend_clubs)
        input_layout.addWidget(recommend_btn)

        clear_btn = QPushButton("清空输入")
        clear_btn.setCursor(Qt.PointingHandCursor)
        clear_btn.setStyleSheet(self.button_style())
        clear_btn.clicked.connect(self.clear_input_and_results)
        input_layout.addWidget(clear_btn)

        main_layout.addLayout(input_layout)

        # 改为用QScrollArea包裹，方便结果太多时滚动
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.result_container = QWidget()
        self.result_layout = QVBoxLayout()
        self.result_layout.setContentsMargins(10, 10, 10, 10)
        self.result_layout.setSpacing(10)
        self.result_container.setLayout(self.result_layout)
        self.scroll_area.setWidget(self.result_container)

        self.scroll_area.setStyleSheet("""
            background-color: rgba(255, 255, 255, 0.85);
            border-radius: 12px;
        """)

        main_layout.addWidget(self.scroll_area, stretch=1)

        btn_layout = QHBoxLayout()

        about_btn = QPushButton("程序说明")
        about_btn.setCursor(Qt.PointingHandCursor)
        about_btn.setStyleSheet(self.button_style())
        about_btn.clicked.connect(self.show_about)
        btn_layout.addWidget(about_btn)

        self.music_combo = QComboBox()
        self.music_combo.addItems(["无音乐", "菊次郎的夏天", "梦中的婚礼", "青石巷"])
        self.music_combo.currentIndexChanged.connect(self.change_music)
        self.music_combo.setStyleSheet("""
            QComboBox {
                padding: 6px 12px;
                font-size: 14px;
                border-radius: 10px;
                color: #222222;
            }
            QComboBox QAbstractItemView {
                selection-background-color: #1E90FF;
            }
        """)
        btn_layout.addWidget(self.music_combo)

        main_layout.addLayout(btn_layout)

        self.central_widget.setLayout(main_layout)

    def typing_animation(self, text):
        self.current_text = ""
        self.full_text = text
        self.char_index = 0
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_title)
        self.timer.start(100)

    def update_title(self):
        if self.char_index < len(self.full_text):
            self.current_text += self.full_text[self.char_index]
            self.title.setText(self.current_text)
            self.char_index += 1
        else:
            self.timer.stop()

    def button_style(self):
        return """
            QPushButton {
                background-color: #1E90FF;
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #4682B4;
            }
        """

    def show_about(self):
        self.click_sound.play()
        dlg = AboutDialog()
        dlg.exec_()

    def change_music(self, index):
        self.click_sound.play()
        if index == 0:
            self.music_player.stop()
        else:
            music_file = self.music_list[index - 1]
            url = QUrl.fromLocalFile(os.path.abspath(music_file))
            self.music_player.setMedia(QMediaContent(url))
            self.music_player.setVolume(30)
            self.music_player.play()

    def recommend_clubs(self):
        self.click_sound.play()
        keyword = self.input_box.text().strip().lower()
        recs = self.get_mock_recommendations(keyword)
        self.display_recommendations(recs)

    def clear_input_and_results(self):
        self.click_sound.play()
        self.input_box.clear()
        self.display_default_recommendations()

    def display_default_recommendations(self):
        default_recs = [
            {"name": "AI协会", "desc": "专注人工智能技术交流与实践，定期举办讲座和项目开发。"},
            {"name": "摄影社", "desc": "分享摄影技巧，组织户外拍摄活动，提升拍摄水平。"},
            {"name": "音乐社团", "desc": "聚集音乐爱好者，举办音乐会和乐器演奏交流。"},
            {"name": "编程俱乐部", "desc": "学习各种编程语言，参加编程比赛与团队项目。"},
            {"name": "篮球协会", "desc": "组织篮球训练与比赛，增强身体素质和团队协作。"}
        ]
        self.display_recommendations(default_recs)

    def get_mock_recommendations(self, keyword):
        clubs = {
            "ai": [
                {"name": "AI协会", "desc": "人工智能技术交流与项目实践。"},
                {"name": "机器人社", "desc": "机器人设计与竞赛。"}
            ],
            "编程": [
                {"name": "编程俱乐部", "desc": "各种编程语言学习与竞赛。"},
                {"name": "算法研习社", "desc": "算法和数据结构深度学习。"}
            ],
            "摄影": [
                {"name": "摄影社", "desc": "摄影技巧分享与外拍活动。"},
                {"name": "影视制作社", "desc": "视频拍摄与剪辑。"}
            ],
            "音乐": [
                {"name": "音乐社团", "desc": "音乐演奏与交流。"},
                {"name": "合唱团", "desc": "声乐训练与合唱表演。"}
            ],
            "篮球": [
                {"name": "篮球协会", "desc": "篮球训练与比赛。"},
                {"name": "体育社", "desc": "多种体育活动组织。"}
            ]
        }
        result = []
        for key in clubs:
            if keyword in key:
                result.extend(clubs[key])
        if not result:
            all_clubs = sum(clubs.values(), [])
            result = random.sample(all_clubs, min(3, len(all_clubs)))
        return result

    def display_recommendations(self, recs):
        # 先清空旧的布局内容
        for i in reversed(range(self.result_layout.count())):
            widget_to_remove = self.result_layout.itemAt(i).widget()
            if widget_to_remove:
                widget_to_remove.deleteLater()

        for club in recs:
            container = QWidget()
            container_layout = QHBoxLayout()
            container_layout.setContentsMargins(10, 10, 10, 10)
            container_layout.setSpacing(15)
            container.setLayout(container_layout)
            container.setStyleSheet("""
                background-color: #f0f0f0;
                border-radius: 10px;
            """)

            text_label = QLabel(f"<b>{club['name']}</b><br>{club['desc']}")
            text_label.setWordWrap(True)
            text_label.setFont(QFont("微软雅黑", 14))
            container_layout.addWidget(text_label, stretch=1)

            detail_btn = QPushButton("详情")
            detail_btn.setCursor(Qt.PointingHandCursor)
            detail_btn.setFixedSize(80, 40)
            detail_btn.setStyleSheet(self.button_style())
            container_layout.addWidget(detail_btn)

            # 这里用lambda绑定带参数的槽函数，避免late binding问题
            detail_btn.clicked.connect(lambda checked, c=club: self.show_club_detail(c))

            self.result_layout.addWidget(container)

        self.result_layout.addStretch(1)

    def show_club_detail(self, club):
        self.click_sound.play()
        dlg = ClubDetailDialog(club["name"], club["desc"])
        dlg.exec_()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClubRecommendationApp()
    window.show()
    sys.exit(app.exec_())
