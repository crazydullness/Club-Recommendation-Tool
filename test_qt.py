import sys
import os
import random
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QComboBox, QDialog, QScrollArea, QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt, QTimer, QUrl
from PyQt5.QtGui import QPixmap, QPalette, QBrush, QFont, QColor, QPainter
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QSoundEffect
import algorithm
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, QAbstractAnimation, QEvent
from PyQt5.QtWidgets import QGraphicsDropShadowEffect
from PyQt5.QtGui import QColor, QPen
import traceback

sys.excepthook = lambda exc_type, exc_value, exc_trace: traceback.print_exception(exc_type, exc_value, exc_trace)
import math
import time
from PyQt5.QtCore import QPoint, QRectF, QPointF
from PyQt5.QtGui import QTransform, QLinearGradient
from PyQt5.QtCore import Qt, QPoint, QRectF, QPointF
from PyQt5.QtGui import QTransform, QLinearGradient


class FlipAnimation(QPropertyAnimation):
    def __init__(self, widget, start_value, end_value):
        super().__init__(widget, b"rotation")
        self.widget = widget
        self.setDuration(500)  # 动画持续时间500毫秒
        self.setStartValue(start_value)
        self.setEndValue(end_value)
        self.setEasingCurve(QEasingCurve.InOutQuad)

    def updateState(self, state):
        if state == QAbstractAnimation.Running:
            self.widget.flipping = True
        else:
            self.widget.flipping = False

    def updateCurrentValue(self, value):
        self.widget.rotation = value
        self.widget.update()


class FlipCard(QWidget):
    def __init__(self, club, theme, parent=None):
        super().__init__(parent)
        self.club = club
        self.theme = theme
        self.rotation = 0
        self.flipping = False
        self.setFixedHeight(150)  # 固定高度
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 设置样式
        self.setStyleSheet(f"""
            background-color: {theme["card_bg"]};
            border-radius: 12px;
            border: 1px solid {theme["button_bg"]};
        """)

        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(10)
        shadow.setXOffset(0)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 50))
        self.setGraphicsEffect(shadow)

        # 安装事件过滤器
        self.installEventFilter(parent)

        # 创建翻转动画
        self.forward_animation = FlipAnimation(self, 0, 180)
        self.backward_animation = FlipAnimation(self, 180, 0)
        self.forward_animation.finished.connect(self.start_backward_flip)

        # 创建定时器用于自动翻转回来
        self.flip_back_timer = QTimer(self)
        self.flip_back_timer.setSingleShot(True)
        self.flip_back_timer.timeout.connect(self.start_backward_flip)

    def start_flip(self):
        # 添加一个标志位来检查是否允许翻转
        if not self.flipping:
            if self.rotation == 0:
                self.forward_animation.start()
                # 设置2秒后自动翻转回来
                self.flip_back_timer.start(2000)
            elif self.rotation == 180:
                # 当旋转到180度时，启动返回动画
                self.backward_animation.start()
                self.flip_back_timer.stop()

    def start_backward_flip(self):
        """启动返回翻转动画"""
        if not self.flipping and self.rotation == 180:
            self.backward_animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.SmoothPixmapTransform)

        # 创建变换矩阵
        transform = QTransform()
        transform.translate(self.width() / 2, self.height() / 2)
        transform.rotate(self.rotation, Qt.YAxis)  # 绕Y轴旋转
        transform.translate(-self.width() / 2, -self.height() / 2)
        painter.setTransform(transform)

        # 根据旋转角度决定绘制正面还是背面
        if self.rotation <= 90:
            self.draw_front(painter)
        else:
            self.draw_back(painter)

        # 绘制侧面高光效果
        if 0 < self.rotation < 180:
            self.draw_side_highlight(painter)

    def draw_front(self, painter):
        # 绘制正面内容
        rect = self.rect()

        # 绘制背景
        painter.fillRect(rect, QColor(self.theme["card_bg"]))

        # 绘制社团名称
        painter.setFont(QFont("微软雅黑", 14, QFont.Bold))
        painter.setPen(QColor(self.theme["text_color"]))
        painter.drawText(rect.adjusted(20, 15, -20, -80), Qt.AlignLeft | Qt.AlignTop, self.club["name"])

        # 绘制社团描述（截取前50字符）
        desc = self.club["desc"][:50] + "..." if len(self.club["desc"]) > 50 else self.club["desc"]
        painter.setFont(QFont("微软雅黑", 10))
        painter.drawText(rect.adjusted(20, 45, -20, -20), Qt.AlignLeft | Qt.AlignTop, desc)

        # 绘制提示文字（悬停翻转）
        painter.setFont(QFont("微软雅黑", 8))
        painter.setPen(QColor(100, 100, 100))
        painter.drawText(rect.adjusted(0, -20, 0, -5), Qt.AlignBottom | Qt.AlignHCenter, "悬停查看详情")

    def draw_back(self, painter):
        # 绘制背面内容
        rect = self.rect()

        # 绘制背景
        painter.fillRect(rect, QColor(self.theme["card_bg"]))

        # 绘制标题
        painter.setFont(QFont("微软雅黑", 14, QFont.Bold))
        painter.setPen(QColor(self.theme["button_bg"]))
        painter.drawText(rect.adjusted(0, 15, 0, -100), Qt.AlignCenter, self.club["name"])

        # 绘制分割线
        painter.setPen(QColor(self.theme["button_bg"]))
        painter.drawLine(20, 50, self.width() - 20, 50)

        # 绘制详细描述
        painter.setFont(QFont("微软雅黑", 10))
        painter.setPen(QColor(self.theme["text_color"]))

        # 自动换行绘制描述
        text_rect = rect.adjusted(20, 60, -20, -30)
        painter.drawText(text_rect, Qt.TextWordWrap, self.club["desc"])

    def draw_side_highlight(self, painter):
        # 绘制侧面高光效果增强3D感
        rect = self.rect()
        gradient = QLinearGradient(0, 0, self.width(), 0)

        if self.rotation < 90:
            # 左侧高光
            gradient.setColorAt(0, QColor(255, 255, 255, 30))
            gradient.setColorAt(0.3, QColor(255, 255, 255, 0))
        else:
            # 右侧高光
            gradient.setColorAt(0.7, QColor(255, 255, 255, 0))
            gradient.setColorAt(1, QColor(255, 255, 255, 30))

        painter.fillRect(rect, gradient)

class NeonLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.glow_size = 10
        self.glow_color = QColor(0, 255, 255)  # 青色
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_glow)
        self.timer.start(50)  # 每50毫秒更新一次
        self.setAttribute(Qt.WA_TranslucentBackground)  # 设置透明背景

    def update_glow(self):
        """创建脉动效果"""
        # 使用正弦函数创建平滑的脉动效果
        self.glow_size = 8 + 2 * abs(math.sin(time.time() * 3))
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)

        rect = self.contentsRect()
        alignment = self.alignment()

        # 绘制霓虹光晕效果
        for i in range(8, 0, -1):
            size_factor = self.glow_size * (i / 8.0)
            alpha = int(40 * (i / 8.0))

            glow_color = QColor(self.glow_color)
            glow_color.setAlpha(alpha)

            pen = QPen(glow_color)
            pen.setWidthF(size_factor)
            painter.setPen(pen)

            # 设置字体 - 稍微放大以增强效果
            font = self.font()
            glow_font = QFont(font)
            glow_font.setPointSizeF(font.pointSizeF() * 1.05)
            painter.setFont(glow_font)

            painter.drawText(rect, alignment, self.text())

        # 绘制主文本
        painter.setPen(QPen(QColor(255, 255, 255)))  # 白色文本
        painter.setFont(self.font())
        painter.drawText(rect, alignment, self.text())

# === 添加这一部分：轮播图组件 ===
class ImageCarouselWidget(QWidget):
    def __init__(self, image_paths, interval=3000, parent=None):
        super().__init__(parent)
        self.image_paths = image_paths
        self.index = 0

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setScaledContents(False)
        self.label.setFixedSize(600, 340)  # ✅ 调整为较小尺寸

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.next_image)
        self.timer.start(interval)

        self.show_image(self.index)

    def show_image(self, index):
        if not self.image_paths:
            return
        pixmap = QPixmap(self.image_paths[index])
        self.label.setPixmap(pixmap.scaled(
            self.label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def next_image(self):
        self.index = (self.index + 1) % len(self.image_paths)
        self.show_image(self.index)


class ParticleWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.particles = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_particles)
        self.timer.start(30)  # 加快更新频率
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # 定义多种颜色
        self.colors = [
            QColor(255, 255, 255, random.randint(100, 200)),  # 白色
            QColor(100, 200, 255, random.randint(100, 200)),  # 浅蓝色
            QColor(255, 100, 200, random.randint(100, 200)),  # 粉色
            QColor(200, 255, 100, random.randint(100, 200))  # 浅绿色
        ]

    def update_particles(self):
        # 添加新粒子（从底部生成）
        if len(self.particles) < 150:  # 增加粒子数量
            self.particles.append({
                'x': random.randint(0, self.width()),
                'y': self.height(),  # 从底部生成
                'dx': random.uniform(-1.5, 1.5),  # 增加水平速度
                'dy': random.uniform(-3.0, -1.5),  # 增加上升速度
                'radius': random.randint(2, 5),  # 增大粒子尺寸
                'color': random.choice(self.colors),  # 随机选择颜色
                'life': random.randint(50, 150),  # 生命周期
                'shape': random.choice(['circle', 'square'])  # 随机形状
            })

        # 更新粒子位置
        for p in self.particles:
            p['x'] += p['dx']
            p['y'] += p['dy']
            p['life'] -= 1  # 生命周期减少

            # 随机轻微摆动
            if random.random() < 0.1:
                p['dx'] += random.uniform(-0.3, 0.3)

        # 移除超出边界或生命周期结束的粒子
        self.particles = [p for p in self.particles
                          if p['y'] > -20 and p['life'] > 0 and
                          p['x'] > -20 and p['x'] < self.width() + 20]

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        for p in self.particles:
            # 根据生命周期调整透明度
            alpha = min(255, p['life'] * 2)
            color = QColor(p['color'])
            color.setAlpha(alpha)
            painter.setBrush(color)
            painter.setPen(Qt.NoPen)

            # 随机绘制圆形或方形
            if p['shape'] == 'circle':
                painter.drawEllipse(int(p['x']), int(p['y']), p['radius'], p['radius'])
            else:
                painter.drawRect(int(p['x']), int(p['y']), p['radius'], p['radius'])


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

        club_desc = club_desc.split('\n')
        desc_label = QLabel(club_desc[0] + "\n\n" + club_desc[1])

        link_label = QLabel('<a href="' + club_desc[2] + '">点击以获得更多详情</a>', self)
        link_label.setOpenExternalLinks(True)
        link_label.setStyleSheet("color: blue; text-decoration: underline;")
        link_label.move(20, 20)
        self.setGeometry(100, 100, 400, 200)

        desc_label.setWordWrap(True)
        layout.addWidget(name_label)
        layout.addWidget(desc_label)
        layout.addWidget(link_label)
        self.setLayout(layout)
        # self.setWindowTitle(f"{club_name} - 详情")
        # self.setFixedSize(400, 300)
        # layout = QVBoxLayout()
        # name_label = QLabel(f"<h2>{club_name}</h2>")
        # desc_label = QLabel(club_desc)
        # desc_label.setWordWrap(True)
        # layout.addWidget(name_label)
        # layout.addWidget(desc_label)
        # self.setLayout(layout)


class ClubRecommendationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("社团推荐系统")

        self.themes = {
            "light": {
                "name": "明亮主题",
                "bg_color": "#f5f5f5",
                "text_color": "#333333",
                "button_bg": "#1E90FF",
                "button_hover": "#4682B4",
                "card_bg": "#ffffff",
                "scroll_bg": "rgba(255, 255, 255, 0.85)"
            },
            "dark": {
                "name": "暗色主题",
                "bg_color": "#2d2d2d",
                "text_color": "#e0e0e0",
                "button_bg": "#3a6ea5",
                "button_hover": "#4a8bd6",
                "card_bg": "#3a3a3a",
                "scroll_bg": "rgba(60, 60, 60, 0.85)"
            },
            "blue": {
                "name": "蓝色主题",
                "bg_color": "#e6f2ff",
                "text_color": "#003366",
                "button_bg": "#0066cc",
                "button_hover": "#0080ff",
                "card_bg": "#cce0ff",
                "scroll_bg": "rgba(204, 224, 255, 0.85)"
            }
        }
        self.current_theme = "light"  # 默认主题

        # 新增动画管理器
        self.animations = {}

        # 自动使用背景图的尺寸
        bg_path = "images/bg.jpg"
        bg_pixmap = QPixmap(bg_path)
        if not bg_pixmap.isNull():
            self.resize(bg_pixmap.size())
        else:
            self.resize(1000, 700)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.history_keywords = []

        self.initUI()
        self.set_background(bg_path)

        self.click_sound = QSoundEffect()
        self.click_sound.setSource(QUrl.fromLocalFile("click.mp3"))
        self.click_sound.setVolume(0.5)

        # 修复音乐播放器初始化
        self.music_player = QMediaPlayer()
        self.music_list = ["bgm1.mp3", "bgm2.mp3", "bgm3.mp3"]
        self.music_player.error.connect(self.handle_music_error)  # 添加错误处理

        self.keyword = {}
        self.display_default_recommendations()

        # 安装事件过滤器
        self.installEventFilter(self)

    def handle_music_error(self):
        """处理音乐播放错误"""
        print("音乐播放错误:", self.music_player.errorString())

    def change_music(self, index):
        """修复后的音乐切换函数"""
        self.click_sound.play()
        if index == 0:
            self.music_player.stop()
        else:
            try:
                # 获取当前音乐文件名
                music_file = self.music_list[index - 1]

                # 构建文件路径
                file_path = os.path.abspath(music_file)

                # 检查文件是否存在
                if not os.path.exists(file_path):
                    print(f"音乐文件不存在: {file_path}")
                    return

                # 创建媒体内容
                url = QUrl.fromLocalFile(file_path)
                media_content = QMediaContent(url)

                # 设置并播放媒体
                self.music_player.setMedia(media_content)
                self.music_player.setVolume(30)
                self.music_player.play()
            except Exception as e:
                print(f"播放音乐出错: {str(e)}")

    def resizeEvent(self, event):
        pass
        #self.particle_widget.setGeometry(0, 0, self.width(), self.height())

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
        grid_layout = QGridLayout()

        # ===== 左上角：轮播图 (0, 0) =====
        carousel_images = [f"carousel/{i}.jpg" for i in range(1, 6) if os.path.exists(f"carousel/{i}.jpg")]
        if not carousel_images:
            print("警告：未找到轮播图图片。请在 carousel/ 目录下放入 1.jpg ~ 5.jpg")
        self.carousel = ImageCarouselWidget(carousel_images)
        grid_layout.addWidget(self.carousel, 0, 0)

        # ===== 右上角：标题 + 搜索栏 (0, 1) =====
        right_top_widget = QWidget()
        right_top_layout = QVBoxLayout()
        right_top_widget.setLayout(right_top_layout)

        # 标题 - 使用霓虹效果
        self.title = NeonLabel("")
        self.title.setFont(QFont("微软雅黑", 28, QFont.Bold))
        self.title.setStyleSheet("background: transparent; margin-top: 10px;")
        self.title.setAlignment(Qt.AlignCenter)
        self.typing_animation("社团推荐系统")
        right_top_layout.addWidget(self.title)

        # ✅ 输入和按钮区域（已加长加高）
        input_layout = QHBoxLayout()
        self.input_box = QLineEdit()
        self.input_box.setPlaceholderText("请输入你的兴趣关键词，例如：编程、音乐、摄影……")
        self.input_box.setMinimumHeight(42)  # 更高一点
        self.input_box.setMinimumWidth(300)  # 更长一点
        self.input_box.setStyleSheet("""
            QLineEdit {
                padding: 10px;
                font-size: 17px;
                border-radius: 10px;
                color: #222222;
            }
        """)
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

        prefer_btn = QPushButton("我的收藏")
        prefer_btn.setCursor(Qt.PointingHandCursor)
        prefer_btn.setStyleSheet(self.button_style())
        prefer_btn.clicked.connect(self.prefer_clubs)
        input_layout.addWidget(prefer_btn)

        right_top_layout.addLayout(input_layout)

        # 说明按钮与音乐选择
        btn_layout = QHBoxLayout()

        about_btn = QPushButton("程序说明")
        about_btn.setCursor(Qt.PointingHandCursor)
        about_btn.setStyleSheet(self.button_style())
        about_btn.clicked.connect(self.show_about)
        btn_layout.addWidget(about_btn)

        clear_prefers_btn = QPushButton("清空收藏夹")
        clear_prefers_btn.setCursor(Qt.PointingHandCursor)
        clear_prefers_btn.setStyleSheet(self.button_style())
        clear_prefers_btn.clicked.connect(algorithm.clear_prefers)
        btn_layout.addWidget(clear_prefers_btn)

        clear_tag_btn = QPushButton("还原tag")
        clear_tag_btn.setCursor(Qt.PointingHandCursor)
        clear_tag_btn.setStyleSheet(self.button_style())
        clear_tag_btn.clicked.connect(algorithm.clear_tag)
        btn_layout.addWidget(clear_tag_btn)
    
        clear_his_btn = QPushButton("清空历史记录")
        clear_his_btn.setCursor(Qt.PointingHandCursor)
        clear_his_btn.setStyleSheet(self.button_style())
        clear_his_btn.clicked.connect(algorithm.clear_his)
        btn_layout.addWidget(clear_his_btn)

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

        right_top_layout.addLayout(btn_layout)

        # 同步右上角区域高度到轮播图高度（如果轮播图是 340 高）
        right_top_widget.setFixedHeight(340)
        grid_layout.addWidget(right_top_widget, 0, 1)

        # ===== 推荐社团区域，跨两列 (1, 0) ~ (1, 1) =====
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
        grid_layout.addWidget(self.scroll_area, 1, 0, 1, 2)

        # 应用最终布局
        self.central_widget.setLayout(grid_layout)

        theme_btn = QPushButton("切换主题")
        theme_btn.setCursor(Qt.PointingHandCursor)
        theme_btn.setStyleSheet(self.button_style())
        theme_btn.clicked.connect(self.toggle_theme)
        btn_layout.addWidget(theme_btn)

    def toggle_theme(self):
        self.click_sound.play()
        theme_keys = list(self.themes.keys())
        current_index = theme_keys.index(self.current_theme)
        next_index = (current_index + 1) % len(theme_keys)
        self.current_theme = theme_keys[next_index]
        self.apply_theme()

    def apply_theme(self):
        theme = self.themes[self.current_theme]

        # 更新全局样式，但不覆盖主窗口背景
        app_style = f"""
            QWidget {{
                color: {theme["text_color"]};
            }}
            QScrollArea {{
                background-color: {theme["scroll_bg"]};
                border-radius: 12px;
            }}
            QLabel {{
                color: {theme["text_color"]};
            }}
        """
        self.setStyleSheet(app_style)

        # 只在明亮主题下显示背景图片，其他主题使用纯色背景
        if self.current_theme == "light":
            self.set_background("images/bg.jpg")  # 使用原始背景图
        else:
            # 使用主题的背景色
            palette = self.palette()
            palette.setColor(QPalette.Window, QColor(theme["bg_color"]))
            self.setPalette(palette)

        # 更新按钮样式
        button_style = f"""
            QPushButton {{
                background-color: {theme["button_bg"]};
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {theme["button_hover"]};
            }}
        """

        # 更新所有按钮
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(button_style)

        # 更新输入框
        input_style = f"""
            QLineEdit {{
                padding: 10px;
                font-size: 17px;
                border-radius: 10px;
                background-color: {theme["card_bg"]};
                color: {theme["text_color"]};
                border: 1px solid {theme["button_bg"]};
            }}
        """
        for input_box in self.findChildren(QLineEdit):
            input_box.setStyleSheet(input_style)

        # 更新下拉框
        combo_style = f"""
            QComboBox {{
                padding: 6px 12px;
                font-size: 14px;
                border-radius: 10px;
                background-color: {theme["card_bg"]};
                color: {theme["text_color"]};
                border: 1px solid {theme["button_bg"]};
            }}
            QComboBox QAbstractItemView {{
                background-color: {theme["card_bg"]};
                selection-background-color: {theme["button_bg"]};
            }}
        """
        for combo in self.findChildren(QComboBox):
            combo.setStyleSheet(combo_style)

        # 更新推荐卡片样式
        card_style = f"""
            background-color: {theme["card_bg"]};
            border-radius: 10px;
        """
        for container in self.result_container.findChildren(QWidget):
            if container != self.result_container:
                container.setStyleSheet(card_style)

        # 更新标题显示当前主题
        self.title.setText(f"社团推荐系统 - {self.themes[self.current_theme]['name']}")

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
            # 直接设置文本，NeonLabel会处理绘制
            self.title.setText(self.current_text)
            self.char_index += 1
        else:
            self.timer.stop()

    def button_style(self):
        theme = self.themes[self.current_theme]
        return f"""
            QPushButton {{
                background-color: {theme["button_bg"]};
                color: white;
                border-radius: 10px;
                padding: 10px 20px;
                font-weight: bold;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: {theme["button_hover"]};
            }}
        """

    def show_about(self):
        self.click_sound.play()
        dlg = AboutDialog()
        dlg.exec_()

    def recommend_clubs(self):
        self.click_sound.play()
        keyword = self.input_box.text().strip().lower()
        recs = self.get_mock_recommendations(keyword)
        self.display_recommendations(recs)

    def prefer_clubs(self):
        def trans(prefers):
            result=[]
            for i in prefers:
                result.append({"name": i[0], "desc": str(i[1]) + "\n更多详情见：\n" + i[2]}) 
            return result       
        algorithm.prefers=algorithm.load_prefers()
        self.display_recommendations(algorithm.prefers)

    def clear_input_and_results(self):
        self.click_sound.play()
        self.input_box.clear()
        self.display_default_recommendations()

    def display_default_recommendations(self):
        default_recs = [
            {"name": "暂无匹配的社团", "desc": "请重新输入你的爱好。"},
        ]
        result = []
        res = algorithm.memory()
        for i in res:
            result.append({"name": i[0], "desc": str(i[2]) + "\n更多详情见：\n" + i[3]})
        if len(result)==0:
            for i in default_recs:
                result.append(i)
        self.display_recommendations(result)

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
        res = algorithm.pinyin_search(keyword)
        for i in res:
            result.append({"name": i[0], "desc": str(i[2]) + "\n更多详情见：\n" + i[3]})
        if len(result)==0:
            for key in clubs:
                if keyword in key:
                    result.extend(clubs[key])
        if len(result)==0:
            all_clubs = sum(clubs.values(), [])
            result = random.sample(all_clubs, min(3, len(all_clubs)))
        return result

    def tag_maintain(self,c,Keyword):
        Keyword=Keyword.text()
        for i in range(120):
            if algorithm.name[i]==c['name']:
                algorithm.tag[i]=algorithm.tag[i]+' '+Keyword
                algorithm.save_tag()

    def show_club_detail(self, club):
        try:
            self.click_sound.play()
            # 停止所有动画
            for anim in list(self.animations.values()):
                if anim and anim.state() == QAbstractAnimation.Running:
                    anim.stop()
            self.animations.clear()

            dlg = ClubDetailDialog(club["name"], club["desc"])
            dlg.exec_()
        except Exception as e:
            print(f"显示详情错误: {str(e)}")

    def safe_show_club_detail(self, club):
        """安全显示社团详情"""
        try:
            # 延迟执行以避免动画冲突
            QTimer.singleShot(100, lambda: self.show_club_detail(club))
        except Exception as e:
            print(f"安全显示详情错误: {str(e)}")

    def eventFilter(self, obj, event):
        """处理悬浮动画的事件过滤器"""
        try:
            # 只处理卡片容器（QWidget类型且标记为animated的对象）
            if not isinstance(obj, QWidget) or not obj.property("animated"):
                return super().eventFilter(obj, event)

            # 处理鼠标进入事件
            if event.type() == QEvent.Enter:
                self.animate_card(obj, True)
                return True

            # 处理鼠标离开事件
            elif event.type() == QEvent.Leave:
                # 对于翻转卡片，离开时不立即翻转回来
                if not isinstance(obj, FlipCard) or obj.rotation == 0:
                    self.animate_card(obj, False)
                return True

            # 处理鼠标点击事件（用于翻转卡片）
            elif event.type() == QEvent.MouseButtonPress and isinstance(obj, FlipCard):
                # 确保卡片处于正确状态后再翻转
                if obj.rotation == 0:
                    obj.start_flip()
                return True

            return super().eventFilter(obj, event)
        except Exception as e:
            print(f"事件过滤器错误: {str(e)}")
            return False

    def animate_card(self, widget, hover):
        """执行卡片动画效果 - 确保能正确放大和缩小"""
        try:
            # 确保对象有效且是卡片容器
            if not widget or not widget.isWidgetType() or not widget.property("animated"):
                return

            # 如果已经有动画在运行，停止它
            if widget in self.animations:
                self.animations[widget].stop()
                del self.animations[widget]

            # 获取当前几何形状
            current_rect = widget.geometry()

            # 计算目标几何形状
            if hover:
                # 放大卡片：在四个方向各扩展10像素（宽高各增加20像素）
                target_rect = current_rect.adjusted(-10, -10, 10, 10)
                # 增强阴影效果
                effect = widget.graphicsEffect()
                if effect and isinstance(effect, QGraphicsDropShadowEffect):
                    effect.setBlurRadius(15)

                # 如果是翻转卡片且处于正面，开始翻转动画
                if isinstance(widget, FlipCard) and widget.rotation == 0:
                    widget.start_flip()
            else:
                # 恢复原始大小
                if hasattr(widget, 'original_geometry'):
                    target_rect = widget.original_geometry
                else:
                    target_rect = current_rect.adjusted(10, 10, -10, -10)  # 安全恢复
                # 恢复阴影效果
                effect = widget.graphicsEffect()
                if effect and isinstance(effect, QGraphicsDropShadowEffect):
                    effect.setBlurRadius(8)

                # 如果是翻转卡片且处于背面，启动返回动画
                if isinstance(widget, FlipCard) and widget.rotation == 180:
                    widget.start_flip()

            # 创建新动画
            animation = QPropertyAnimation(widget, b"geometry")
            animation.setDuration(200)  # 稍微延长动画时间
            animation.setEasingCurve(QEasingCurve.OutBack)  # 使用更有弹性的曲线
            animation.setStartValue(current_rect)
            animation.setEndValue(target_rect)

            # 存储并启动动画
            self.animations[widget] = animation
            animation.finished.connect(lambda: self._cleanup_animation(widget))
            animation.start(QAbstractAnimation.DeleteWhenStopped)

            # 存储原始几何形状供恢复使用
            if hover and not hasattr(widget, 'original_geometry'):
                widget.original_geometry = current_rect

        except Exception as e:
            print(f"动画错误: {str(e)}")

    def display_recommendations(self, recs):
        """显示推荐结果（带悬浮动画和3D翻转）"""
        # 清空旧内容（包括动画引用）
        for i in reversed(range(self.result_layout.count())):
            widget = self.result_layout.itemAt(i).widget()
            if widget:
                # 清理关联的动画
                if widget in self.animations:
                    self.animations[widget].stop()
                    del self.animations[widget]
                widget.deleteLater()

        # 获取当前主题
        theme = self.themes[self.current_theme]

        for club in recs:
            # 创建主容器
            container = QWidget()
            container.setProperty("animated", False)  # 容器本身不应用动画
            container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

            # 设置容器布局
            container_layout = QVBoxLayout()
            container_layout.setContentsMargins(5, 5, 5, 15)  # 增加底部边距
            container.setLayout(container_layout)

            # 创建翻转卡片 - 确保初始状态正确
            flip_card = FlipCard(club, theme, self)
            flip_card.rotation = 0  # 明确设置旋转角度为0（正面）
            flip_card.setProperty("animated", True)  # 卡片应用动画
            container_layout.addWidget(flip_card)

            # 创建按钮区域
            button_container = QWidget()
            button_layout = QHBoxLayout()
            button_layout.setContentsMargins(0, 10, 0, 0)
            button_container.setLayout(button_layout)

            # 详情按钮
            detail_btn = QPushButton("详情")
            detail_btn.setCursor(Qt.PointingHandCursor)
            detail_btn.setFixedSize(80, 36)
            detail_btn.setStyleSheet(self.button_style())
            from functools import partial
            detail_btn.clicked.connect(partial(self.safe_show_club_detail, club))
            button_layout.addWidget(detail_btn)

            # 收藏按钮
            algorithm.prefers=algorithm.load_prefers()
            if club not in algorithm.prefers:
                prefer_btn = QPushButton("☆")
                prefer_btn.setCursor(Qt.PointingHandCursor)
                prefer_btn.setFixedSize(80, 36)
                prefer_btn.setStyleSheet(self.button_style())
                prefer_btn.clicked.connect(lambda checked, c=club: algorithm.save_prefers1(c))
                button_layout.addWidget(prefer_btn)
            else:
                prefer_btn = QPushButton("★")
                prefer_btn.setCursor(Qt.PointingHandCursor)
                prefer_btn.setFixedSize(80, 36)
                prefer_btn.setStyleSheet(self.button_style())
                prefer_btn.clicked.connect(lambda checked, c=club: algorithm.save_prefers2(c))
                button_layout.addWidget(prefer_btn)

            # tag维护按钮
            tag_btn = QPushButton("tag维护")
            tag_btn.setCursor(Qt.PointingHandCursor)
            tag_btn.setFixedSize(110, 36)
            tag_btn.setStyleSheet(self.button_style())
            button_layout.addWidget(tag_btn)

            # 输入框
            input_box1 = QLineEdit()
            input_box1.setPlaceholderText("请输入关键词")
            input_box1.setMinimumHeight(36)
            input_box1.setMinimumWidth(80)
            input_box1.setStyleSheet(f"""
                QLineEdit {{
                    padding: 8px;
                    font-size: 14px;
                    border-radius: 8px;
                    background-color: {theme["card_bg"]};
                    color: {theme["text_color"]};
                    border: 1px solid {theme["button_bg"]};
                }}
            """)
            button_layout.addWidget(input_box1)
            tag_btn.clicked.connect(lambda checked, c=club, k=input_box1: self.tag_maintain(c, k))

            container_layout.addWidget(button_container)

            self.result_layout.addWidget(container)

        self.result_layout.addStretch(1)


    def _cleanup_animation(self, widget):
        """动画完成后的清理"""
        if widget in self.animations:
            del self.animations[widget]


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ClubRecommendationApp()
    window.show()
    sys.exit(app.exec_())
