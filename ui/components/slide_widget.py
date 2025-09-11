from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from core.style_manager import StyleManager

class SlideWidget(QWidget):
    """
    Уніфікований віджет слайду для Demo і Creator режимів
    """
    content_changed = pyqtSignal(dict)
    
    def __init__(self, slide_id, mode='demo', parent=None):
        super().__init__(parent)
        self.slide_id = slide_id
        self.mode = mode  # 'demo' або 'creator'
        self.style_manager = StyleManager()
        self.content_elements = {}
        
        self.setup_ui()
        self.load_content()
        
    def setup_ui(self):
        """Налаштування інтерфейсу"""
        self.setObjectName(f"slide_{self.slide_id}")
        
        # Головний layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.main_layout.setSpacing(15)
        
        # Контейнер для контенту
        self.content_container = QFrame()
        self.content_container.setObjectName("contentContainer")
        self.content_container.setStyleSheet("""
            QFrame#contentContainer {
                background: #2b2b2b;
                border: 1px solid #404040;
                border-radius: 8px;
            }
        """)
        
        self.content_layout = QVBoxLayout(self.content_container)
        self.content_layout.setContentsMargins(20, 20, 20, 20)
        self.content_layout.setSpacing(10)
        
        # Заголовок слайду
        self.setup_title()
        
        # Контент слайду
        self.setup_content()
        
        self.main_layout.addWidget(self.content_container)
        
        # Застосовуємо стилі
        self.apply_styles()
        
    def setup_title(self):
        """Налаштування заголовка"""
        if self.mode == 'creator':
            self.title_edit = QLineEdit()
            self.title_edit.setProperty('elementType', 'slide_title')
            self.title_edit.setPlaceholderText("Введіть заголовок слайду...")
            self.title_edit.textChanged.connect(self.on_content_changed)
            self.content_layout.addWidget(self.title_edit)
            self.content_elements['title'] = self.title_edit
        else:
            self.title_label = QLabel()
            self.title_label.setProperty('elementType', 'slide_title')
            self.title_label.setAlignment(Qt.AlignCenter)
            self.title_label.setWordWrap(True)
            self.content_layout.addWidget(self.title_label)
            self.content_elements['title'] = self.title_label
            
    def setup_content(self):
        """Налаштування контенту"""
        if self.mode == 'creator':
            self.content_edit = QTextEdit()
            self.content_edit.setProperty('elementType', 'slide_content')
            self.content_edit.setPlaceholderText("Введіть текст слайду...")
            self.content_edit.textChanged.connect(self.on_content_changed)
            self.content_layout.addWidget(self.content_edit)
            self.content_elements['content'] = self.content_edit
        else:
            self.content_label = QLabel()
            self.content_label.setProperty('elementType', 'slide_content')
            self.content_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
            self.content_label.setWordWrap(True)
            self.content_layout.addWidget(self.content_label)
            self.content_elements['content'] = self.content_label
            
    def apply_styles(self):
        """Застосування стилів до елементів"""
        # Стилі для заголовка
        title_style = self.style_manager.get_style_sheet('slide_title')
        self.content_elements['title'].setStyleSheet(title_style)
        
        # Стилі для контенту
        content_style = self.style_manager.get_style_sheet('slide_content')
        self.content_elements['content'].setStyleSheet(content_style)
        
        # Встановлення мінімальних розмірів
        self.content_elements['title'].setMinimumHeight(50)
        self.content_elements['content'].setMinimumHeight(200)
        
    def load_content(self):
        """Завантаження збереженого контенту"""
        content_data = self.style_manager.load_slide_content(self.slide_id)
        
        if content_data:
            # Завантажуємо заголовок
            title_text = content_data.get('title', '')
            if self.mode == 'creator':
                self.title_edit.setText(title_text)
            else:
                self.title_label.setText(title_text)
                
            # Завантажуємо контент
            content_text = content_data.get('content', '')
            if self.mode == 'creator':
                self.content_edit.setPlainText(content_text)
            else:
                self.content_label.setText(content_text)
        else:
            # Встановлюємо контент за замовчуванням
            self.set_default_content()
            
    def set_default_content(self):
        """Встановлення контенту за замовчуванням"""
        default_titles = {
            1: "BumbleB - Das automatisierte Shuttle",
            2: "BumbleB - Wie die Hummel fährt",
            3: "Einsatzgebiete und Vorteile",
            4: "Sicherheitssysteme",
            5: "Nachhaltigkeit & Umwelt"
        }
        
        default_content = {
            1: "Schonmal ein automatisiert Shuttle gesehen, das aussieht wie eine Hummel?\n\nShuttle fährt los von Bushaltestelle an Bahnhof...",
            2: "Wie die Hummel ihre Flügel nutzt, so nutzt unser BumbleB innovative Technologie...",
            3: "Vielseitige Einsatzmöglichkeiten in urbanen Gebieten...",
            4: "Moderne Sicherheitssysteme gewährleisten maximale Sicherheit...",
            5: "Nachhaltiger Transport für eine grüne Zukunft..."
        }
        
        title = default_titles.get(self.slide_id, f"Slide {self.slide_id}")
        content = default_content.get(self.slide_id, f"Content für Slide {self.slide_id}")
        
        if self.mode == 'creator':
            self.title_edit.setText(title)
            self.content_edit.setPlainText(content)
        else:
            self.title_label.setText(title)
            self.content_label.setText(content)
            
    def on_content_changed(self):
        """Обробка змін контенту"""
        if self.mode == 'creator':
            content_data = {
                'title': self.title_edit.text(),
                'content': self.content_edit.toPlainText(),
                'timestamp': QDateTime.currentDateTime().toString()
            }
            
            # Зберігаємо зміни
            self.style_manager.save_slide_content(self.slide_id, content_data)
            
            # Сигналізуємо про зміни
            self.content_changed.emit(content_data)
            
    def get_content_data(self):
        """Отримання даних контенту"""
        if self.mode == 'creator':
            return {
                'title': self.title_edit.text(),
                'content': self.content_edit.toPlainText()
            }
        else:
            return {
                'title': self.title_label.text(),
                'content': self.content_label.text()
            }
            
    def update_content(self, content_data):
        """Оновлення контенту слайду"""
        if 'title' in content_data:
            if self.mode == 'creator':
                self.title_edit.setText(content_data['title'])
            else:
                self.title_label.setText(content_data['title'])
                
        if 'content' in content_data:
            if self.mode == 'creator':
                self.content_edit.setPlainText(content_data['content'])
            else:
                self.content_label.setText(content_data['content'])
