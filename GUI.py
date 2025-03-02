from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QStackedWidget,
                           QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFrame,
                           QLabel, QSizePolicy, QSpacerItem)
from PyQt5.QtGui import QIcon, QPainter, QColor, QTextCharFormat, QFont, QPixmap, QTextBlockFormat, QMovie, QPalette
from PyQt5.QtCore import Qt, QSize, QTimer, QDateTime, QTimeZone, QByteArray
from dotenv import dotenv_values
import sys
import os

# Constants and configurations
env_vars = dotenv_values(".env")
AssistantName = env_vars.get("AssistantName", "Jarvis")
current_dir = os.getcwd()
old_chat_message = ""
TempDirPath = os.path.join(current_dir, "Frontend", "Files")
GraphicsDir = os.path.join(current_dir, "Frontend", "Graphics")

# Ensure directories exist
os.makedirs(TempDirPath, exist_ok=True)

# Initialize files if they don't exist
def init_files():
    files = {
        'Mic.data': 'False',
        'Status.data': 'Initializing...',
        'Responses.data': ''
    }
    for filename, default_content in files.items():
        filepath = os.path.join(TempDirPath, filename)
        if not os.path.exists(filepath):
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(default_content)

init_files()

def SetMicrophoneStatus(Command):
    with open(os.path.join(TempDirPath, 'Mic.data'), "w", encoding='utf-8') as file:
        file.write(Command)

def GetMicrophoneStatus():
    with open(os.path.join(TempDirPath, 'Mic.data'), "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def SetAssistantStatus(Status):
    with open(os.path.join(TempDirPath, 'Status.data'), "w", encoding='utf-8') as file:
        file.write(Status)

def GetAssistantStatus():
    with open(os.path.join(TempDirPath, 'Status.data'), "r", encoding='utf-8') as file:
        Status = file.read()
    return Status

def ShowTextToScreen(Text):
    with open(os.path.join(TempDirPath, 'Responses.data'), "w", encoding='utf-8') as file:
        file.write(Text)

def AnswerModifier(text):
    return f"Modified Answer: {text}"

def QueryModifier(query):
    return f"Modified Query: {query}"

def getGraphicsDirPath(Filename):
    Path = os.path.join(GraphicsDir, Filename)
    return Path

# Update the getSystemInfo function to match the desired format
def getCurrentTimeFormatted():
    pakistan_timezone = QTimeZone(QByteArray(b"Asia/Karachi"))
    current_time = QDateTime.currentDateTime().toTimeZone(pakistan_timezone)
    return current_time.toString("yyyy-MM-dd HH:mm:ss")

def getCurrentUser():
    return os.getenv('USERNAME', 'HusainCoder')

def getSystemInfo():
    current_time = getCurrentTimeFormatted()
    user_login = getCurrentUser()
    return f"Current Date and Time : {current_time}\nCurrent User's Login: {user_login}\n"

# Update the ChatSection class to ensure proper display
class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)

        # System Info Display with updated format
        self.system_info = QLabel()
        self.system_info.setStyleSheet("""
            QLabel {
                color: #7a7a7a;
                font-size: 14px;
                background-color: black;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        self.updateSystemInfo()
        layout.addWidget(self.system_info)

        # Chat area
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setMinimumHeight(400)
        self.chat_text_edit.setStyleSheet("""
            QTextEdit {
                background-color: black;
                border-radius: 15px;
                padding: 15px;
                color: white;
            }
        """)
        layout.addWidget(self.chat_text_edit)

        # Bottom section with GIF and status
        bottom_layout = QHBoxLayout()

        # Jarvis GIF
        self.gif_label = QLabel()
        self.gif_label.setStyleSheet("background: transparent;")
        movie = QMovie(getGraphicsDirPath('Jarvis.gif'))
        movie.setScaledSize(QSize(110, 110))
        self.gif_label.setMovie(movie)
        movie.start()

        # Status label
        self.translating_label = QLabel("Listening...")
        self.translating_label.setStyleSheet("""
            QLabel {
                color: #7a7a7a;
                font-size: 16px;
                padding: 5px 15px;
                background-color: black;
                border-radius: 10px;
            }
        """)

        bottom_layout.addStretch()
        bottom_layout.addWidget(self.translating_label)
        bottom_layout.addWidget(self.gif_label)
        layout.addLayout(bottom_layout)

        # Set up timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSystemInfo)
        self.timer.timeout.connect(self.loadMessages)
        self.timer.timeout.connect(self.SpeechRecogText)
        self.timer.start(1000)

    def updateSystemInfo(self):
        self.system_info.setText(getSystemInfo())

    def loadMessages(self):
        global old_chat_message
        try:
            with open(os.path.join(TempDirPath, 'Responses.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                if messages and messages != old_chat_message:
                    self.addMessage(messages)
                    old_chat_message = messages
        except Exception as e:
            print(f"Error loading messages: {e}")

    def SpeechRecogText(self):
        try:
            with open(os.path.join(TempDirPath, 'Status.data'), "r", encoding='utf-8') as file:
                messages = file.read()
                self.translating_label.setText(messages)
        except Exception as e:
            print(f"Error updating status: {e}")

    def addMessage(self, message):
        current_time = getCurrentTimeFormatted()
        formatted_message = f"[{current_time}] {message}\n"
        self.chat_text_edit.append(formatted_message)
        self.chat_text_edit.verticalScrollBar().setValue(
            self.chat_text_edit.verticalScrollBar().maximum()
        )

# Update the InitialScreen class to match the format
class InitialScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(20)

        # System Info Display with updated format
        self.system_info = QLabel()
        self.system_info.setStyleSheet("""
            QLabel {
                color: #7a7a7a;
                font-size: 14px;
                background-color: black;
                padding: 10px;
                border-radius: 5px;
            }
        """)
        self.updateSystemInfo()
        layout.addWidget(self.system_info, alignment=Qt.AlignCenter)

        # Jarvis GIF
        self.gif_label = QLabel()
        movie = QMovie(getGraphicsDirPath('Jarvis.gif'))
        movie.setScaledSize(QSize(400, 400))  # Updated size to 400x400
        self.gif_label.setMovie(movie)
        movie.start()
        layout.addWidget(self.gif_label, alignment=Qt.AlignCenter)

        # Welcome text
        welcome_label = QLabel(f"Welcome to {AssistantName}")
        welcome_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 32px;
                font-weight: bold;
            }
        """)
        layout.addWidget(welcome_label, alignment=Qt.AlignCenter)

        # Status text
        self.status_label = QLabel("Initializing systems...")
        self.status_label.setStyleSheet("""
            QLabel {
                color: #7a7a7a;
                font-size: 18px;
            }
        """)
        layout.addWidget(self.status_label, alignment=Qt.AlignCenter)

        # Add a vertical spacer item before the mic button
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Microphone button
        self.mic_button = QPushButton()
        self.mic_button.setIcon(QIcon(getGraphicsDirPath('Mic_on.png')))
        self.mic_button.setIconSize(QSize(60, 60))
        self.mic_button.setFixedSize(80, 80)
        self.mic_button.setStyleSheet("""
            QPushButton {
                background-color: #2d2d2d;
                border-radius: 40px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
            }
        """)
        self.mic_button.clicked.connect(self.toggleMic)
        layout.addWidget(self.mic_button, alignment=Qt.AlignCenter)

        # Add another vertical spacer to push it further if needed
        layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Fixed))

        self.setLayout(layout)

        # Timer for updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateSystemInfo)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(1000)

        self.mic_active = True

    def updateSystemInfo(self):
        self.system_info.setText(getSystemInfo())

    def toggleMic(self):
        self.mic_active = not self.mic_active
        icon_name = 'Mic_on.png' if self.mic_active else 'Mic_off.png'
        self.mic_button.setIcon(QIcon(getGraphicsDirPath(icon_name)))
        SetMicrophoneStatus("False" if self.mic_active else "True")

    def updateStatus(self):
        try:
            with open(os.path.join(TempDirPath, 'Status.data'), "r", encoding='utf-8') as file:
                status = file.read()
                self.status_label.setText(status)
        except Exception as e:
            print(f"Error updating status: {e}")

class CustomTopBar(QWidget):
    def __init__(self, parent, stacked_widget):
        super().__init__(parent)
        self.parent = parent
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)

        # Title
        title_label = QLabel(f"{AssistantName} AI")
        title_label.setStyleSheet("""
            font-size: 18px; 
            font-weight: bold; 
            color: white;
            background-color: black;  /* Set background to black */
            padding: 5px;          /* Add some padding for better appearance */
        """)

        # Navigation buttons
        self.home_btn = self.createNavButton("Home", "Home.png")
        self.chat_btn = self.createNavButton("Chat", "Chat.png")

        # Window control buttons
        minimize_btn = self.createControlButton("─")
        maximize_btn = self.createControlButton("□")
        close_btn = self.createControlButton("×")

        minimize_btn.clicked.connect(self.parent.showMinimized)
        maximize_btn.clicked.connect(self.toggleMaximize)
        close_btn.clicked.connect(self.parent.close)

        layout.addWidget(title_label)
        layout.addStretch(1)
        layout.addWidget(self.home_btn)
        layout.addWidget(self.chat_btn)
        layout.addStretch(1)
        layout.addWidget(minimize_btn)
        layout.addWidget(maximize_btn)
        layout.addWidget(close_btn)

        self.setFixedHeight(50)
        self.setStyleSheet("background-color: #2d2d2d;")

    def createNavButton(self, text, icon_name):
        btn = QPushButton(text)
        btn.setIcon(QIcon(getGraphicsDirPath(icon_name)))
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                padding: 8px 15px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #3d3d3d;
                border-radius: 5px;
            }
        """)
        if text == "Home":
            btn.clicked.connect(self.showHome)
        else:
            btn.clicked.connect(self.showChat)
        return btn

    def createControlButton(self, text):
        btn = QPushButton(text)
        btn.setFixedSize(30, 30)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                color: white;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #ff4444;
            }
        """)
        return btn

    def showHome(self):
        self.stacked_widget.setCurrentIndex(0)

    def showChat(self):
        self.stacked_widget.setCurrentIndex(1)

    def toggleMaximize(self):
        if self.parent.isMaximized():
            self.parent.showNormal()
        else:
            self.parent.showMaximized()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.dragPos = event.globalPos() - self.parent.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            self.parent.move(event.globalPos() - self.dragPos)
            event.accept()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Main container
        main_container = QWidget()
        main_container.setStyleSheet("""
            QWidget {
                background-color: black;
                color: white;
            }
        """)

        main_layout = QVBoxLayout(main_container)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Stacked widget for multiple screens
        self.stacked_widget = QStackedWidget()
        self.initial_screen = InitialScreen()
        self.chat_screen = ChatSection()

        self.stacked_widget.addWidget(self.initial_screen)
        self.stacked_widget.addWidget(self.chat_screen)

        # Custom title bar
        self.title_bar = CustomTopBar(self, self.stacked_widget)
        main_layout.addWidget(self.title_bar)
        main_layout.addWidget(self.stacked_widget)

        self.setCentralWidget(main_container)
        self.setMinimumSize(800, 600)
        self.showMaximized()

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MainWindow()  # Fixed: Changed 'Main' to 'MainWindow'
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()