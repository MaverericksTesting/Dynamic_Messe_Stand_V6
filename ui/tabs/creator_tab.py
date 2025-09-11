#!/usr/bin/env python3
"""
Creator Tab für die Bertrandt GUI
3-Spalten Drag & Drop Editor für Demo-Folien
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
from PIL import Image, ImageTk
from core.theme import theme_manager
from core.logger import logger
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.components.slide_widget import SlideWidget
from datetime import datetime

class CreatorTabQt(QWidget):
    slide_changed = pyqtSignal(int, dict)  # Сигнал про зміну слайду
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_slide = 1
        self.total_slides = 10
        self.slides = {}
        self.setup_ui()
        self.setup_slides()
        
    def setup_ui(self):
        """Налаштування інтерфейсу Creator табу"""
        self.main_layout = QHBoxLayout(self)
        self.main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Ліва панель - список слайдів
        self.setup_slides_list()
        
        # Права панель - редактор слайдів
        self.setup_editor()
        
    def setup_slides_list(self):
        """Налаштування списку слайдів"""
        self.slides_panel = QWidget()
        self.slides_panel.setMaximumWidth(300)
        self.slides_panel.setStyleSheet("""
            QWidget {
                background: #333333;
                border-right: 1px solid #555555;
            }
        """)
        
        slides_layout = QVBoxLayout(self.slides_panel)
        
        # Заголовок панелі
        header_label = QLabel("Demo-Folien")
        header_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                background: #404040;
            }
        """)
        slides_layout.addWidget(header_label)
        
        # Підзаголовок
        sub_header = QLabel("Klicken zum Bearbeiten")
        sub_header.setStyleSheet("""
            QLabel {
                color: #CCCCCC;
                font-size: 12px;
                padding: 5px 10px;
            }
        """)
        slides_layout.addWidget(sub_header)
        
        # Список слайдів
        self.slides_list = QListWidget()
        self.slides_list.setStyleSheet("""
            QListWidget {
                background: #333333;
                border: none;
                outline: none;
            }
            QListWidget::item {
                color: white;
                padding: 12px 10px;
                border-bottom: 1px solid #444444;
                background: #333333;
            }
            QListWidget::item:selected {
                background: #0078d4;
                color: white;
            }
            QListWidget::item:hover {
                background: #404040;
            }
        """)
        
        # Додаємо елементи списку
        for i in range(1, self.total_slides + 1):
            item_text = f"Folie {i}\n{self.get_slide_title(i)}"
            item = QListWidgetItem(item_text)
            item.setData(Qt.UserRole, i)
            self.slides_list.addItem(item)
            
        self.slides_list.currentRowChanged.connect(self.on_slide_selected)
        slides_layout.addWidget(self.slides_list)
        
        self.main_layout.addWidget(self.slides_panel)
        
    def setup_editor(self):
        """Налаштування редактора слайдів"""
        self.editor_panel = QWidget()
        editor_layout = QVBoxLayout(self.editor_panel)
        
        # Заголовок редактора
        self.editor_header = QLabel("IO-Folie 1: BumbleB - Das automatisierte Shuttle")
        self.editor_header.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 15px;
                background: #404040;
                border-bottom: 2px solid #0078d4;
            }
        """)
        editor_layout.addWidget(self.editor_header)
        
        # Навігаційні кнопки
        nav_widget = QWidget()
        nav_layout = QHBoxLayout(nav_widget)
        
        self.back_btn = QPushButton("◀ Zurück")
        self.back_btn.clicked.connect(self.prev_slide)
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        self.forward_btn = QPushButton("Weiter ▶")
        self.forward_btn.clicked.connect(self.next_slide)
        
        # Стилі для навігаційних кнопок
        btn_style = """
            QPushButton {
                background: #0078d4;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #106ebe;
            }
            QPushButton:disabled {
                background: #666666;
                color: #999999;
            }
        """
        self.back_btn.setStyleSheet(btn_style)
        self.forward_btn.setStyleSheet(btn_style)
        
        nav_layout.addWidget(self.back_btn)
        nav_layout.addItem(spacer)
        nav_layout.addWidget(self.forward_btn)
        
        editor_layout.addWidget(nav_widget)
        
        # Контейнер для слайдів
        self.editor_container = QStackedWidget()
        editor_layout.addWidget(self.editor_container)
        
        # Кнопки дій
        self.setup_action_buttons(editor_layout)
        
        self.main_layout.addWidget(self.editor_panel)
        
    def setup_action_buttons(self, layout):
        """Налаштування кнопок дій"""
        actions_widget = QWidget()
        actions_layout = QHBoxLayout(actions_widget)
        
        # Кнопка збереження
        self.save_btn = QPushButton("💾 Speichern")
        self.save_btn.clicked.connect(self.save_current_slide)
        
        # Кнопка попереднього перегляду
        self.preview_btn = QPushButton("👁 Vorschau")
        self.preview_btn.clicked.connect(self.preview_slide)
        
        # Стилі для кнопок дій
        action_btn_style = """
            QPushButton {
                background: #28a745;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
                margin: 5px;
            }
            QPushButton:hover {
                background: #218838;
            }
        """
        
        self.save_btn.setStyleSheet(action_btn_style)
        self.preview_btn.setStyleSheet(action_btn_style.replace('#28a745', '#17a2b8').replace('#218838', '#138496'))
        
        actions_layout.addWidget(self.save_btn)
        actions_layout.addWidget(self.preview_btn)
        actions_layout.addStretch()
        
        layout.addWidget(actions_widget)
        
    def setup_slides(self):
        """Створення всіх слайдів для редагування"""
        for slide_id in range(1, self.total_slides + 1):
            slide_widget = SlideWidget(slide_id, mode='creator', parent=self)
            slide_widget.content_changed.connect(
                lambda data, sid=slide_id: self.on_slide_content_changed(sid, data)
            )
            self.slides[slide_id] = slide_widget
            self.editor_container.addWidget(slide_widget)
            
        # Показуємо перший слайд
        self.show_slide(1)
        self.slides_list.setCurrentRow(0)
        
    def get_slide_title(self, slide_id):
        """Отримання заголовка слайду"""
        titles = {
            1: "BumbleB - Das automa...",
            2: "BumbleB - Wie die Hu...", 
            3: "Einsatzgebiete und...",
            4: "Sicherheitssysteme...",
            5: "Nachhaltigkeit & U..."
        }
        return titles.get(slide_id, f"Slide {slide_id}")
        
    def show_slide(self, slide_id):
        """Показати слайд для редагування"""
        if slide_id in self.slides:
            self.current_slide = slide_id
            self.editor_container.setCurrentWidget(self.slides[slide_id])
            self.editor_header.setText(f"IO-Folie {slide_id}: {self.get_slide_title(slide_id)}")
            
            # Оновлюємо стан кнопок
            self.back_btn.setEnabled(slide_id > 1)
            self.forward_btn.setEnabled(slide_id < self.total_slides)
            
    def on_slide_selected(self, row):
        """Обробка вибору слайду зі списку"""
        if row >= 0:
            slide_id = row + 1  # Перетворення індексу в ID слайду
            self.show_slide(slide_id)
            
    def on_slide_content_changed(self, slide_id, data):
        """Обробка зміни вмісту слайду"""
        self.slide_changed.emit(slide_id, data)
        
    def prev_slide(self):
        """Перехід до попереднього слайду"""
        if self.current_slide > 1:
            self.show_slide(self.current_slide - 1)
            self.slides_list.setCurrentRow(self.current_slide - 1)
            
    def next_slide(self):
        """Перехід до наступного слайду"""
        if self.current_slide < self.total_slides:
            self.show_slide(self.current_slide + 1)
            self.slides_list.setCurrentRow(self.current_slide - 1)
            
    def save_current_slide(self):
        """Збереження поточного слайду"""
        if self.current_slide in self.slides:
            # Логіка збереження
            print(f"Saving slide {self.current_slide}")
            
    def preview_slide(self):
        """Попередній перегляд слайду"""
        if self.current_slide in self.slides:
            # Логіка попереднього перегляду
            print(f"Previewing slide {self.current_slide}")


class CreatorTab:
    """3-Spalten Creator-Tab für Demo-Folien Bearbeitung"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.visible = False
        self.current_edit_slide = 1
        self.current_slide = None
        self.auto_save_timer_id = None
        
        # Drag & Drop Variablen
        self.drag_data = {'element_type': None, 'widget': None}
        self.slide_width = 1920
        self.slide_height = 1080
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        self.create_creator_content()
        
        self.schedule_auto_save()
        
    def schedule_auto_save(self):
        """Планує автоматичне збереження через 1 секунду"""
        if self.auto_save_timer_id:
            self.main_window.root.after_cancel(self.auto_save_timer_id)
        self.auto_save_timer_id = self.main_window.root.after(1000, self.auto_save_presentation)

    def auto_save_presentation(self):
        """Автоматично зберігає презентацію щосекундно"""
        try:
            self.save_current_slide_content()
            # Планує наступне збереження
            self.schedule_auto_save()
        except Exception as e:
            logger.error(f"Fehler beim Auto-Speichern: {e}")
            self.schedule_auto_save()  # Продовжуємо спроби
        
    def create_creator_content(self):
        """Erstellt den 3-Spalten Creator-Tab"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Haupt-Container
        self.container = tk.Frame(self.parent, bg=colors['background_primary'])
        
        # Header-Toolbar (oben)
        self.create_header_toolbar()
        
        # 3-Spalten-Layout
        content_frame = tk.Frame(self.container, bg=colors['background_primary'])
        content_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Grid-Layout für 3 Spalten
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=0, minsize=250)  # Folien-Übersicht (links)
        content_frame.grid_columnconfigure(1, weight=1, minsize=800)  # Editor (mitte)
        content_frame.grid_columnconfigure(2, weight=0, minsize=300)  # Tool-Box (rechts)
        
        # Spalte 1: Folien-Übersicht (links)
        self.create_slides_overview_panel(content_frame)
        
        # Spalte 2: Haupt-Editor (mitte)
        self.create_main_editor_panel(content_frame)
        
        # Spalte 3: Tool-Box (rechts)
        self.create_toolbox_panel(content_frame)
        
        # Status-Leiste (unten)
        self.create_status_bar()
    
    def create_header_toolbar(self):
        """Erstellt die Header-Toolbar"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Header-Frame (15% höher)
        header_frame = tk.Frame(
            self.container,
            bg=colors['background_secondary'],
            relief='flat',
            bd=0,
            height=80  # Von 70 auf 80 (ca. 15% höher)
        )
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Titel
        title_frame = tk.Frame(header_frame, bg=colors['background_secondary'])
        title_frame.pack(side='left', fill='y', padx=(15, 30))
        
        title_label = tk.Label(
            title_frame,
            text="🎨 Slide Creator",
            font=fonts['title'],
            fg=colors['accent_primary'],
            bg=colors['background_secondary']
        )
        title_label.pack(anchor='w', pady=(15, 0))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Drag & Drop Editor",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        subtitle_label.pack(anchor='w')
        
        # Aktionen
        actions_frame = tk.Frame(header_frame, bg=colors['background_secondary'])
        actions_frame.pack(side='left', fill='y', padx=20)
        
        # Speichern
        save_btn = tk.Button(
            actions_frame,
            text="💾 Speichern",
            font=fonts['button'],
            bg=colors['accent_primary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.save_current_slide_content
        )
        save_btn.pack(side='left', padx=(0, 10), pady=15)
        
        # Vorschau
        preview_btn = tk.Button(
            actions_frame,
            text="👁 Vorschau",
            font=fonts['button'],
            bg=colors['accent_secondary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=10,
            cursor='hand2',
            command=self.preview_slide
        )
        preview_btn.pack(side='left', padx=(0, 10), pady=15)
        
        # Slide-Navigation
        nav_frame = tk.Frame(header_frame, bg=colors['background_secondary'])
        nav_frame.pack(side='right', fill='y', padx=(20, 15))
        
        # Slide-Zähler
        self.slide_counter = tk.Label(
            nav_frame,
            text="Demo-Folie 1 von 10",
            font=fonts['subtitle'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        self.slide_counter.pack(pady=(20, 5))
        
        # Navigation-Buttons
        nav_buttons = tk.Frame(nav_frame, bg=colors['background_secondary'])
        nav_buttons.pack()
        
        prev_btn = tk.Button(
            nav_buttons,
            text="◀ Zurück",
            font=fonts['button'],
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.previous_slide
        )
        prev_btn.pack(side='left', padx=(0, 5))
        
        next_btn = tk.Button(
            nav_buttons,
            text="Weiter ▶",
            font=fonts['button'],
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            padx=15,
            pady=5,
            cursor='hand2',
            command=self.next_slide
        )
        next_btn.pack(side='left', padx=(5, 0))
    
    def create_slides_overview_panel(self, parent):
        """Erstellt die Folien-Übersicht (links) - Demo-Folien"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Panel Frame
        panel_frame = tk.Frame(
            parent,
            bg=colors['background_secondary'],
            relief='solid',
            bd=1,
            width=250
        )
        panel_frame.grid(row=0, column=0, sticky='nsew', padx=(0, 5))
        panel_frame.grid_propagate(False)
        
        # Header
        header_frame = tk.Frame(panel_frame, bg=colors['background_secondary'])
        header_frame.pack(fill='x', padx=15, pady=(15, 10))
        
        header_label = tk.Label(
            header_frame,
            text="📋 Demo-Folien",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        header_label.pack(anchor='w')
        
        # Info-Label
        info_label = tk.Label(
            header_frame,
            text="Klicken zum Bearbeiten",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        info_label.pack(anchor='w', pady=(5, 0))
        
        # Scrollable Thumbnail List
        canvas = tk.Canvas(panel_frame, bg=colors['background_secondary'], highlightthickness=0)
        scrollbar = tk.Scrollbar(panel_frame, orient="vertical", command=canvas.yview)
        self.thumbnail_frame = tk.Frame(canvas, bg=colors['background_secondary'])
        
        self.thumbnail_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.thumbnail_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(15, 0), pady=(0, 15))
        scrollbar.pack(side="right", fill="y", pady=(0, 15))
        
        # Thumbnails erstellen
        self.create_slide_thumbnails()
    
    def create_slide_thumbnails(self):
        """Erstellt Slide-Thumbnails aus den Demo-Folien"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        self.thumbnail_buttons = {}
        
        # Content-Manager verwenden (Demo-Folien)
        from models.content import content_manager
        slides = content_manager.get_all_slides()
        
        if not slides:
            logger.warning("Keine Demo-Folien gefunden")
            return
        
        for slide_id, slide in slides.items():
            try:
                # Thumbnail-Container
                thumb_container = tk.Frame(
                    self.thumbnail_frame,
                    bg=colors['background_secondary']
                )
                thumb_container.pack(fill='x', padx=5, pady=3)
                
                # Thumbnail-Button
                is_active = slide_id == self.current_edit_slide
                bg_color = colors['accent_primary'] if is_active else colors['background_tertiary']
                
                title = slide.title
                display_title = title[:18] + "..." if len(title) > 18 else title
                
                thumb_btn = tk.Button(
                    thumb_container,
                    text=f"Folie {slide_id}\n{display_title}",
                    font=fonts['body'],
                    bg=bg_color,
                    fg='white' if is_active else colors['text_primary'],
                    relief='flat',
                    bd=0,
                    width=20,
                    height=3,
                    cursor='hand2',
                    command=lambda sid=slide_id: self.load_slide_to_editor(sid),
                    justify='left'
                )
                thumb_btn.pack(fill='x', ipady=5)
                
                self.thumbnail_buttons[slide_id] = thumb_btn
                
            except Exception as e:
                logger.error(f"Fehler beim Erstellen von Thumbnail für Slide {slide_id}: {e}")
    
    def create_main_editor_panel(self, parent):
        """Erstellt den Haupt-Editor (mitte) - immer weiße Canvas"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Editor Frame
        editor_frame = tk.Frame(
            parent,
            bg=colors['background_secondary'],
            relief='solid',
            bd=1
        )
        editor_frame.grid(row=0, column=1, sticky='nsew', padx=5)
        
        # Header
        header_frame = tk.Frame(editor_frame, bg=colors['background_secondary'])
        header_frame.pack(fill='x', padx=20, pady=(15, 10))
        
        # Slide-Info
        self.slide_info_label = tk.Label(
            header_frame,
            text="Demo-Folie 1: Wählen Sie eine Folie zum Bearbeiten",
            font=fonts['display'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        self.slide_info_label.pack(anchor='w')
        
        # Canvas für Drag & Drop Editor - volle Breite und Höhe
        canvas_frame = tk.Frame(editor_frame, bg=colors['background_secondary'])
        canvas_frame.pack(fill='both', expand=True, padx=10, pady=(10, 10))
        
        # Canvas Container - nutzt kompletten verfügbaren Platz
        canvas_container = tk.Frame(canvas_frame, bg=colors['background_secondary'])
        canvas_container.pack(fill='both', expand=True)
        
        # Slide Canvas erstellen - mit dunklerem Hintergrund für besseren Kontrast
        self.slide_canvas = tk.Canvas(
            canvas_container,
            bg='#E8E8E8',  # Etwas dunkler für besseren Kontrast zur weißen Folie
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.slide_canvas.pack(fill='both', expand=True)
        
        # Canvas-Größe überwachen und Folie entsprechend skalieren
        self.slide_canvas.bind('<Configure>', self.on_canvas_resize)
        
        # Initiale Drop-Zone erstellen (unsichtbar)
        self.create_slide_content()
        
        # Canvas Drop-Events
        self.setup_canvas_drop_events()
    
    def create_slide_content(self):
        """Erstellt Drop-Zone und initialen Slide-Rahmen"""
        # Unsichtbare Drop-Zone für Drop-Erkennung
        self.dropzone_rect = self.slide_canvas.create_rectangle(
            0, 0, self.slide_width, self.slide_height,
            outline='',  # Unsichtbar
            width=0,
            fill='',
            tags='dropzone'
        )
        
        # Initialen Slide-Rahmen hinzufügen
        self.slide_canvas.after(100, self.add_slide_frame)
    
    def on_canvas_resize(self, event):
        """Optimale Skalierung - Folie komplett sichtbar mit mehr Rand"""
        canvas_width = event.width
        canvas_height = event.height
        
        # Minimale Größe sicherstellen
        if canvas_width < 100 or canvas_height < 100:
            return
        
        # Mehr Rand für bessere Sichtbarkeit (80px statt 40px)
        margin = 80
        
        # Skalierungsfaktor berechnen - Folie komplett sichtbar
        scale_x = (canvas_width - margin) / self.slide_width
        scale_y = (canvas_height - margin) / self.slide_height
        
        # Kleineren Faktor verwenden, damit komplette Folie sichtbar bleibt
        self.scale_factor = min(scale_x, scale_y)
        
        # Minimale und maximale Skalierung sicherstellen
        if self.scale_factor < 0.15:  # Etwas größer als vorher
            self.scale_factor = 0.15
        elif self.scale_factor > 1.0:  # Nicht größer als Original
            self.scale_factor = 1.0
        
        # Neue skalierte Dimensionen
        scaled_width = self.slide_width * self.scale_factor
        scaled_height = self.slide_height * self.scale_factor
        
        # Canvas-Inhalt perfekt zentrieren
        self.offset_x = (canvas_width - scaled_width) / 2
        self.offset_y = (canvas_height - scaled_height) / 2
        
        # Sicherstellen, dass die Folie nicht außerhalb des Canvas ist
        if self.offset_x < 20:
            self.offset_x = 20
        if self.offset_y < 20:
            self.offset_y = 20
        
        # Drop-Zone exakt auf Foliengröße setzen
        self.slide_canvas.coords(
            self.dropzone_rect,
            self.offset_x, self.offset_y,
            self.offset_x + scaled_width, self.offset_y + scaled_height
        )
        
        # Slide-Rahmen für bessere Sichtbarkeit hinzufügen
        self.add_slide_frame()
        
        # Debug-Info für optimale Skalierung
        logger.debug(f"Canvas: {canvas_width}x{canvas_height}, "
                    f"Slide: {self.slide_width}x{self.slide_height}, "
                    f"Scale: {self.scale_factor:.3f}, "
                    f"Scaled: {scaled_width:.0f}x{scaled_height:.0f}, "
                    f"Offset: ({self.offset_x:.0f}, {self.offset_y:.0f})")
        
        # Alle bestehenden Elemente neu skalieren
        self.rescale_existing_elements()
    
    def add_slide_frame(self):
        """Fügt einen sichtbaren Rahmen um die Folie hinzu - HINTERGRUND-LAYER"""
        # Entferne alten Rahmen
        self.slide_canvas.delete('slide_background_frame')
        self.slide_canvas.delete('slide_background_shadow')
        self.slide_canvas.delete('slide_background_main')
        
        # Skalierte Dimensionen
        scaled_width = self.slide_width * self.scale_factor
        scaled_height = self.slide_height * self.scale_factor
        
        # Rahmen um die Folie - HINTERGRUND-LAYER
        self.slide_canvas.create_rectangle(
            self.offset_x - 2, self.offset_y - 2,
            self.offset_x + scaled_width + 2, self.offset_y + scaled_height + 2,
            outline='#333333',
            width=2,
            tags='slide_background_frame'
        )
        
        # Schatten-Effekt für bessere Sichtbarkeit - HINTERGRUND-LAYER
        shadow_offset = 5
        self.slide_canvas.create_rectangle(
            self.offset_x + shadow_offset, self.offset_y + shadow_offset,
            self.offset_x + scaled_width + shadow_offset, self.offset_y + scale
