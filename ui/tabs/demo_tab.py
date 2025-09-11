#!/usr/bin/env python3
"""
Demo Tab für Dynamic Messe Stand V4
Automatische Präsentations-Steuerung
"""

import tkinter as tk
from tkinter import ttk
from core.theme import theme_manager, THEME_VARS, _mix
from core.logger import logger
from services.demo import demo_service
from models.content import content_manager
from ui.components.slide_renderer import SlideRenderer
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from ui.components.slide_widget import SlideWidget

class DemoTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_slide = 1
        self.total_slides = 10
        self.slides = {}
        self.setup_ui()
        self.setup_slides()
        
    def setup_ui(self):
        """Налаштування інтерфейсу Demo табу"""
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        
        # Контейнер для слайдів
        self.slides_container = QStackedWidget()
        self.slides_container.setObjectName("slidesContainer")
        
        # Контролери навігації
        self.setup_navigation()
        
        self.layout.addWidget(self.slides_container)
        self.layout.addWidget(self.nav_container)
        
    def setup_slides(self):
        """Створення всіх слайдів"""
        for slide_id in range(1, self.total_slides + 1):
            slide_widget = SlideWidget(slide_id, mode='demo', parent=self)
            self.slides[slide_id] = slide_widget
            self.slides_container.addWidget(slide_widget)
            
        # Показуємо перший слайд
        self.show_slide(1)
        
    def setup_navigation(self):
        """Налаштування навігації"""
        self.nav_container = QWidget()
        self.nav_layout = QHBoxLayout(self.nav_container)
        
        # Кнопка "Назад"
        self.prev_btn = QPushButton("◀ Zurück")
        self.prev_btn.clicked.connect(self.prev_slide)
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background: #404040;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #505050;
            }
        """)
        
        # Spacer
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Індикатор слайдів
        self.slide_indicator = QLabel("1/10")
        self.slide_indicator.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 14px;
                font-weight: bold;
                padding: 10px;
            }
        """)
        
        # Spacer
        spacer2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        
        # Кнопка "Далі"
        self.next_btn = QPushButton("Weiter ▶")
        self.next_btn.clicked.connect(self.next_slide)
        self.next_btn.setStyleSheet(self.prev_btn.styleSheet())
        
        self.nav_layout.addWidget(self.prev_btn)
        self.nav_layout.addItem(spacer)
        self.nav_layout.addWidget(self.slide_indicator)
        self.nav_layout.addItem(spacer2)
        self.nav_layout.addWidget(self.next_btn)
        
    def show_slide(self, slide_id):
        """Показати конкретний слайд"""
        if slide_id in self.slides:
            self.current_slide = slide_id
            self.slides_container.setCurrentWidget(self.slides[slide_id])
            self.slide_indicator.setText(f"{slide_id}/{self.total_slides}")
            
            # Оновлюємо стан кнопок
            self.prev_btn.setEnabled(slide_id > 1)
            self.next_btn.setEnabled(slide_id < self.total_slides)
            
    def next_slide(self):
        """Перехід до наступного слайду"""
        if self.current_slide < self.total_slides:
            self.show_slide(self.current_slide + 1)
            
    def prev_slide(self):
        """Перехід до попереднього слайду"""
        if self.current_slide > 1:
            self.show_slide(self.current_slide - 1)
            
    def refresh_slides(self):
        """Оновлення всіх слайдів (викликається при змінах у Creator)"""
        for slide_id, slide_widget in self.slides.items():
            slide_widget.load_content()
            
class DemoTab:
    """Demo-Tab für automatische Präsentationen"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.visible = False
        
        self.create_demo_content()
        
        # Demo-Service Callback registrieren
        demo_service.add_callback(self.on_slide_changed)
    
    def create_demo_content(self):
        """Erstellt den Demo-Tab - Bertrandt Dark Theme Style"""
        # Haupt-Container - Bertrandt Style
        self.container = tk.Frame(self.parent, bg=THEME_VARS["bg"])
        
        # Hauptarbeitsbereich mit Bertrandt Design
        main_workspace = tk.Frame(self.container, bg=THEME_VARS["bg"])
        main_workspace.pack(fill='both', expand=True, padx=THEME_VARS["pad"]*2, pady=THEME_VARS["pad"]*2)
        
        # Layout: Slide-Panel (links) + Folien-Anzeige (rechts) - KEIN Demo-Player mehr
        main_workspace.grid_columnconfigure(1, weight=4)  # Folien-Anzeige bekommt noch mehr Platz
        main_workspace.grid_rowconfigure(0, weight=1)
        
        # Slide-Thumbnail Panel (links)
        self.create_demo_slide_panel(main_workspace)
        
        # Haupt-Folien-Anzeige mit Steuerung (rechts)
        self.create_slide_display_with_controls(main_workspace)
        
        # Status-Leiste (unten)
        self.create_demo_status_bar()
        
        # Jetzt erst die erste Slide laden (nach vollständiger Initialisierung)
        self.update_slide_display(1)
    
    def create_demo_ribbon(self):
        """Erstellt die Demo-Ribbon-Toolbar"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Ribbon-Container - kompakter für 24" Screen
        ribbon_frame = tk.Frame(
            self.container,
            bg=colors['background_secondary'],
            relief='flat',
            bd=0,
            height=90
        )
        ribbon_frame.pack(fill='x', padx=10, pady=(10, 8))
        ribbon_frame.pack_propagate(False)
        
        # Titel-Bereich
        title_frame = tk.Frame(ribbon_frame, bg=colors['background_secondary'])
        title_frame.pack(side='left', fill='y', padx=(25, 40))
        
        title_label = tk.Label(
            title_frame,
            text="▶ BumbleB Demo Player",
            font=fonts['display'],
            fg=colors['accent_primary'],
            bg=colors['background_secondary']
        )
        title_label.pack(anchor='w', pady=(20, 5))
        
        subtitle_label = tk.Label(
            title_frame,
            text="Automatische Präsentations-Steuerung",
            font=fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        subtitle_label.pack(anchor='w')
        
        # Separator
        separator = tk.Frame(ribbon_frame, bg=colors['border_medium'], width=1)
        separator.pack(side='left', fill='y', padx=10, pady=10)
        
        # Demo-Steuerung
        demo_frame = tk.Frame(ribbon_frame, bg=colors['background_secondary'])
        demo_frame.pack(side='left', fill='y', padx=10)
        
        # Start/Stop Button (prominent)
        self.start_stop_btn = tk.Button(
            demo_frame,
            text="▶️\nDemo Starten",
            font=fonts['large_button'],
            bg=colors['accent_primary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=25,
            pady=15,
            cursor='hand2',
            command=self.toggle_demo,
            width=12,
            height=3
        )
        self.start_stop_btn.pack(side='left', padx=(0, 15), pady=15)
        
        # Pause Button
        self.pause_btn = tk.Button(
            demo_frame,
            text="⏸️\nPause",
            font=fonts['large_button'],
            bg=colors['accent_warning'],
            fg='white',
            relief='flat',
            bd=0,
            padx=25,
            pady=15,
            cursor='hand2',
            command=self.pause_demo,
            width=12,
            height=3
        )
        self.pause_btn.pack(side='left', padx=10, pady=15)
        
        # Separator
        separator2 = tk.Frame(ribbon_frame, bg=colors['border_medium'], width=1)
        separator2.pack(side='left', fill='y', padx=10, pady=10)
        
        # Slide-Navigation
        nav_frame = tk.Frame(ribbon_frame, bg=colors['background_secondary'])
        nav_frame.pack(side='left', fill='y', padx=10)
        
        nav_label = tk.Label(
            nav_frame,
            text="Navigation:",
            font=fonts['subtitle'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        nav_label.pack(anchor='w', pady=(25, 5))
        
        nav_buttons = tk.Frame(nav_frame, bg=colors['background_secondary'])
        nav_buttons.pack(pady=(10, 0))
        
        prev_btn = tk.Button(
            nav_buttons,
            text="◀◀",
            font=fonts['large_button'],
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            padx=15,
            pady=10,
            cursor='hand2',
            command=demo_service.previous_slide,
            width=4,
            height=2
        )
        prev_btn.pack(side='left', padx=(0, 10))
        
        self.slide_counter = tk.Label(
            nav_buttons,
            text="1/10",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        self.slide_counter.pack(side='left', padx=15)
        
        next_btn = tk.Button(
            nav_buttons,
            text="▶▶",
            font=fonts['large_button'],
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            padx=15,
            pady=10,
            cursor='hand2',
            command=demo_service.next_slide,
            width=4,
            height=2
        )
        next_btn.pack(side='left', padx=(10, 0))
        
        # Separator
        separator3 = tk.Frame(ribbon_frame, bg=colors['border_medium'], width=1)
        separator3.pack(side='left', fill='y', padx=10, pady=10)
        
        # Einstellungen
        settings_frame = tk.Frame(ribbon_frame, bg=colors['background_secondary'])
        settings_frame.pack(side='left', fill='y', padx=10)
        
        settings_label = tk.Label(
            settings_frame,
            text="Einstellungen:",
            font=fonts['subtitle'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        settings_label.pack(anchor='w', pady=(25, 5))
        
        # Slide-Dauer
        duration_frame = tk.Frame(settings_frame, bg=colors['background_secondary'])
        duration_frame.pack(pady=(5, 0))
        
        tk.Label(
            duration_frame,
            text="Dauer:",
            font=fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        ).pack(side='left')
        
        self.duration_var = tk.StringVar(value="5")
        duration_entry = tk.Entry(
            duration_frame,
            textvariable=self.duration_var,
            font=fonts['body'],
            width=5,
            justify='center'
        )
        duration_entry.pack(side='left', padx=(5, 2))
        duration_entry.bind('<Return>', self.update_duration)
        
        tk.Label(
            duration_frame,
            text="s",
            font=fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        ).pack(side='left')
    
    def create_demo_slide_panel(self, parent):
        """Erstellt das Demo-Slide-Panel (links) - Bertrandt Dark Theme Style"""
        # Slide-Panel Frame - Bertrandt Style
        panel_frame = tk.Frame(
            parent,
            bg=THEME_VARS["panel"],
            relief='flat',
            bd=1,
            highlightbackground=THEME_VARS["elev_outline"],
            highlightthickness=1,
            width=320
        )
        panel_frame.grid(row=0, column=0, sticky='nsew', padx=(0, THEME_VARS["pad"]))
        panel_frame.grid_propagate(False)
        
        # Panel-Header mit Theme-System
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        header_frame = tk.Frame(panel_frame, bg=colors['background_secondary'])
        header_frame.pack(fill='x', padx=spacing['xl'], pady=(spacing['xl'], spacing['lg']))
        
        header_label = tk.Label(
            header_frame,
            text="▤ BumbleB Story",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        header_label.pack(anchor='w')
        
        info_label = tk.Label(
            header_frame,
            text="10 Folien verfügbar",
            font=fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        info_label.pack(anchor='w', pady=(spacing['xxs'], 0))
        
        # Scrollable Thumbnail-Liste
        canvas = tk.Canvas(
            panel_frame,
            bg=colors['background_secondary'],
            highlightthickness=0
        )
        scrollbar = tk.Scrollbar(panel_frame, orient="vertical", command=canvas.yview)
        self.demo_thumbnail_frame = tk.Frame(canvas, bg=colors['background_secondary'])
        
        self.demo_thumbnail_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.demo_thumbnail_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=(spacing['md'], 0), pady=(0, spacing['md']))
        scrollbar.pack(side="right", fill="y", pady=(0, spacing['md']))
        
        # Demo-Thumbnails erstellen
        self.create_demo_thumbnails()
    
    def create_demo_thumbnails(self):
        """Erstellt Demo-Slide-Thumbnails mit Theme-System"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        slides = content_manager.get_all_slides()
        self.demo_thumbnail_buttons = {}
        
        for i, (slide_id, slide) in enumerate(slides.items()):
            # Thumbnail-Container
            thumb_container = tk.Frame(
                self.demo_thumbnail_frame,
                bg=colors['background_secondary']
            )
            thumb_container.pack(fill='x', padx=spacing['xs'], pady=spacing['xxs'])
            
            # Thumbnail-Button
            is_active = slide_id == demo_service.current_slide
            bg_color = colors['accent_secondary'] if is_active else colors['background_tertiary']
            
            thumb_btn = tk.Button(
                thumb_container,
                text=f"{slide_id}\n{slide.title[:20]}...",
                font=fonts['body'],
                bg=bg_color,
                fg='white' if is_active else colors['text_primary'],
                relief='flat',
                bd=0,
                width=25,
                height=4,
                cursor='hand2',
                command=lambda sid=slide_id: demo_service.goto_slide(sid),
                justify='left'
            )
            thumb_btn.pack(fill='x', ipady=spacing['xxs'])
            
            self.demo_thumbnail_buttons[slide_id] = thumb_btn
    
    def create_slide_display_with_controls(self, parent):
        """Erstellt die Haupt-Folien-Anzeige mit integrierten Steuerungsbuttons"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        # Slide-Display Frame
        display_frame = tk.Frame(
            parent,
            bg=colors['background_secondary'],
            relief='flat',
            bd=0
        )
        display_frame.grid(row=0, column=1, sticky='nsew', padx=spacing['sm'])
        
        # Display-Header mit Theme-Spacing
        header_frame = tk.Frame(display_frame, bg=colors['background_secondary'])
        header_frame.pack(fill='x', padx=spacing['lg'], pady=(spacing['lg'], spacing['md']))
        
        # Aktuelle Slide-Info
        self.current_slide_info = tk.Label(
            header_frame,
            text="Folie 1: BumbleB - Das automatisierte Shuttle",
            font=fonts['display'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        self.current_slide_info.pack(anchor='w', pady=(0, spacing['sm']))
        
        # Slide-Status mit integriertem Play/Pause Button
        status_frame = tk.Frame(header_frame, bg=colors['background_secondary'])
        status_frame.pack(anchor='w')
        
        # Play/Pause Button direkt in der Folien-Ansicht
        self.play_pause_btn = tk.Button(
            status_frame,
            text="▶ Demo Starten",
            font=fonts['large_button'],
            bg=colors['accent_primary'],
            fg='white',
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2',
            command=self.toggle_demo,
            width=12,
            height=1
        )
        self.play_pause_btn.pack(side='left', padx=(0, 20))
        
        self.demo_status_indicator = tk.Label(
            status_frame,
            text="◼ Gestoppt",
            font=fonts['title'],
            fg=colors['accent_tertiary'],
            bg=colors['background_secondary']
        )
        self.demo_status_indicator.pack(side='left')
        
        self.time_remaining = tk.Label(
            status_frame,
            text="",
            font=fonts['title'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        self.time_remaining.pack(side='left', padx=(spacing['lg'], 0))
        
        # Slide-Content-Bereich (wie PowerPoint Slide-Ansicht) mit Theme-Spacing
        content_container = tk.Frame(display_frame, bg=colors['background_secondary'])
        content_container.pack(fill='both', expand=True, padx=spacing['lg'], pady=(0, spacing['md']))
        
        # Slide-Rahmen mit modernem Glass-Design
        self.slide_frame = tk.Frame(
            content_container,
            bg=colors['glass_bg'],  # Glass-Effekt für Slide-Anzeige
            relief='flat',
            bd=0,
            highlightbackground=colors['glass_border'],
            highlightthickness=2  # Dickerer Border für schöneren Effekt
        )
        self.slide_frame.pack(fill='both', expand=True, padx=spacing['lg'], pady=spacing['lg'])  # Mehr Abstand
        
        # Slide-Inhalt
        self.create_slide_content_view()
        
        # Steuerungsbuttons unter der Folien-Anzeige
        self.create_control_buttons(display_frame)
    
    def create_slide_content_view(self):
        """Erstellt die Canvas-basierte Slide-Anzeige (wie im Creator)"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        # Clear existing content
        for widget in self.slide_frame.winfo_children():
            widget.destroy()
        
        # Canvas für 1:1 Darstellung wie im Creator
        canvas_container = tk.Frame(self.slide_frame, bg=colors['background_secondary'])
        canvas_container.pack(fill='both', expand=True, padx=spacing['lg'], pady=spacing['lg'])
        
        # Slide-Canvas erstellen (moderner Stil)
        self.demo_slide_canvas = tk.Canvas(
            canvas_container,
            bg='#E8E8E8',  # Konsistent mit Creator
            relief='flat',
            bd=0,
            highlightthickness=0
        )
        self.demo_slide_canvas.pack(fill='both', expand=True)
        
        # Canvas-Größe überwachen und Folie entsprechend skalieren
        self.demo_slide_canvas.bind('<Configure>', self.on_demo_canvas_resize)
        
        # Slide-Dimensionen (identisch zum Creator)
        self.demo_slide_width = 1920
        self.demo_slide_height = 1080
        self.demo_scale_factor = 1.0
        self.demo_offset_x = 0
        self.demo_offset_y = 0
        
        # Info-Bereich (unten)
        info_frame = tk.Frame(self.slide_frame, bg=colors['background_tertiary'])
        info_frame.pack(fill='x', side='bottom')
        
        self.slide_info_display = tk.Label(
            info_frame,
            text="Slide-Vorschau - Creator-Layout wird 1:1 angezeigt",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary']
        )
        self.slide_info_display.pack(side='left', padx=spacing['sm'], pady=spacing['xxs'])
    
    def on_demo_canvas_resize(self, event):
        """Optimale Skalierung für Demo-Canvas (identisch zum Creator)"""
        canvas_width = event.width
        canvas_height = event.height
        
        # Minimale Größe sicherstellen
        if canvas_width < 100 or canvas_height < 100:
            return
        
        # Skalierungsfaktor berechnen - Folie komplett sichtbar
        scale_x = (canvas_width - 40) / self.demo_slide_width
        scale_y = (canvas_height - 40) / self.demo_slide_height
        
        # Kleineren Faktor verwenden, damit komplette Folie sichtbar bleibt
        self.demo_scale_factor = min(scale_x, scale_y)
        
        # Minimale Skalierung sicherstellen
        if self.demo_scale_factor < 0.1:
            self.demo_scale_factor = 0.1
        
        # Neue skalierte Dimensionen
        scaled_width = self.demo_slide_width * self.demo_scale_factor
        scaled_height = self.demo_slide_height * self.demo_scale_factor
        
        # Canvas-Inhalt perfekt zentrieren
        self.demo_offset_x = (canvas_width - scaled_width) / 2
        self.demo_offset_y = (canvas_height - scaled_height) / 2
        
        # Alle bestehenden Elemente neu skalieren
        self.rescale_demo_elements()
    
    def rescale_demo_elements(self):
        """Skaliert alle Demo-Canvas-Elemente bei Größenänderungen"""
        try:
            # Alle Canvas-Items durchgehen
            for item in self.demo_slide_canvas.find_all():
                tags = self.demo_slide_canvas.gettags(item)
                
                # Canvas-Widgets (Text, Bilder, etc.) neu positionieren
                item_type = self.demo_slide_canvas.type(item)
                if item_type == 'window':
                    coords = self.demo_slide_canvas.coords(item)
                    if len(coords) >= 2:
                        # Relative Position aus Tags holen (falls gespeichert)
                        rel_x = float(tags[1]) if len(tags) > 1 and tags[1].replace('.', '').replace('-', '').isdigit() else 0
                        rel_y = float(tags[2]) if len(tags) > 2 and tags[2].replace('.', '').replace('-', '').isdigit() else 0
                        
                        # Neue absolute Position berechnen
                        new_x = self.demo_offset_x + (rel_x * self.demo_scale_factor)
                        new_y = self.demo_offset_y + (rel_y * self.demo_scale_factor)
                        
                        # Widget neu positionieren
                        self.demo_slide_canvas.coords(item, new_x, new_y)
                
                # Canvas-Formen skalieren
                elif item_type in ['oval', 'rectangle', 'line', 'text']:
                    coords = self.demo_slide_canvas.coords(item)
                    if len(coords) >= 2:
                        # Relative Koordinaten aus Tags holen
                        if len(tags) >= 3:
                            try:
                                rel_coords = [float(tag) for tag in tags[1:] if tag.replace('.', '').replace('-', '').isdigit()]
                                if len(rel_coords) >= 2:
                                    # Neue absolute Koordinaten
                                    new_coords = []
                                    for i in range(0, len(rel_coords), 2):
                                        if i+1 < len(rel_coords):
                                            new_x = self.demo_offset_x + (rel_coords[i] * self.demo_scale_factor)
                                            new_y = self.demo_offset_y + (rel_coords[i+1] * self.demo_scale_factor)
                                            new_coords.extend([new_x, new_y])
                                    
                                    if new_coords:
                                        self.demo_slide_canvas.coords(item, *new_coords)
                            except ValueError:
                                pass  # Tags enthalten keine Koordinaten
            
        except Exception as e:
            logger.error(f"Fehler beim Neu-Skalieren der Demo-Elemente: {e}")
    
    def create_control_buttons(self, parent):
        """Erstellt die Steuerungsbuttons unter der Folien-Anzeige"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        # Control-Container mit Theme-Spacing
        control_frame = tk.Frame(parent, bg=colors['background_secondary'])
        control_frame.pack(fill='x', padx=spacing['lg'], pady=(0, spacing['lg']))
        
        # Button-Container zentriert
        button_container = tk.Frame(control_frame, bg=colors['background_secondary'])
        button_container.pack(anchor='center')
        
        # Zurück Button mit modernem Glass-Design
        prev_btn = tk.Button(
            button_container,
            text="◀◀ Zurück",
            font=fonts['large_button'],
            bg=colors['glass_bg'],  # Glass-Effekt
            fg=colors['text_primary'],
            relief='flat',
            bd=2,
            highlightbackground=colors['glass_border'],
            highlightthickness=1,
            padx=spacing['xl'],      # Größere Buttons
            pady=spacing['lg'],      # Mehr Padding
            cursor='hand2',
            command=demo_service.previous_slide,
            width=14,               # Breitere Buttons
            height=2
        )
        prev_btn.pack(side='left', padx=(0, spacing['lg']))  # Mehr Abstand zwischen Buttons
        
        # Weiter Button mit modernem Glass-Design
        next_btn = tk.Button(
            button_container,
            text="▶▶ Weiter",
            font=fonts['large_button'],
            bg=colors['glass_bg'],  # Glass-Effekt
            fg=colors['text_primary'],
            relief='flat',
            bd=2,
            highlightbackground=colors['glass_border'],
            highlightthickness=1,
            padx=spacing['xl'],      # Größere Buttons
            pady=spacing['lg'],      # Mehr Padding
            cursor='hand2',
            command=demo_service.next_slide,
            width=14,               # Breitere Buttons
            height=2
        )
        next_btn.pack(side='left', padx=(spacing['lg'], 0))  # Mehr Abstand zwischen Buttons
        
        # Slide-Zähler unter den Buttons mit Theme-Spacing
        self.slide_counter = tk.Label(
            control_frame,
            text="1/10",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        self.slide_counter.pack(anchor='center', pady=(spacing['sm'], 0))
    
    
    def create_demo_status_bar(self):
        """Erstellt die Demo-Status-Leiste (unten) mit Theme-System"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        components = theme_manager.get_components()
        
        # Status-Bar mit Theme-System
        toolbar_style = components['toolbar']
        status_frame = tk.Frame(
            self.container,
            bg=colors['background_tertiary'],
            height=toolbar_style['height'] * 0.7  # Etwas niedriger als Header
        )
        status_frame.pack(fill='x', padx=spacing['md'], pady=(0, spacing['md']))
        status_frame.pack_propagate(False)
        
        # Status-Text mit Theme-Spacing
        self.status_text = tk.Label(
            status_frame,
            text="Demo bereit - BumbleB Story mit 10 Folien geladen",
            font=fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary']
        )
        self.status_text.pack(side='left', padx=spacing['md'], pady=spacing['sm'])
        
        # Hardware-Status (rechts) mit Theme-Spacing
        self.hardware_status = tk.Label(
            status_frame,
            text="Hardware: Prüfe...",
            font=fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary']
        )
        self.hardware_status.pack(side='right', padx=spacing['md'], pady=spacing['sm'])
    
    def update_slide_display(self, slide_id):
        """Aktualisiert die Slide-Anzeige mit 1:1 Creator-Layout"""
        slide = content_manager.get_slide(slide_id)
        
        if slide:
            # Titel aktualisieren (falls vorhanden)
            if hasattr(self, 'current_slide_info'):
                self.current_slide_info.configure(text=f"Folie {slide_id}: {slide.title}")
            
            # Canvas-basierte Anzeige aktualisieren
            if hasattr(self, 'demo_slide_canvas'):
                self.render_slide_canvas(slide)
            
            # Info aktualisieren
            if hasattr(self, 'slide_info_display'):
                canvas_elements = slide.config_data.get('canvas_elements', [])
                self.slide_info_display.configure(
                    text=f"Folie {slide_id}: {slide.title} - {len(canvas_elements)} Elemente"
                )
            
            # Slide-Zähler aktualisieren (falls vorhanden)
            if hasattr(self, 'slide_counter'):
                total_slides = content_manager.get_slide_count()
                self.slide_counter.configure(text=f"{slide_id}/{total_slides}")
            
            # Thumbnail-Auswahl aktualisieren (falls vorhanden)
            if hasattr(self, 'demo_thumbnail_buttons'):
                self.update_demo_thumbnail_selection(slide_id)

    def render_slide_canvas(self, slide):
        """Rendert die Slide mit IDENTISCHEM Layout wie im Creator"""
        try:
            # Canvas leeren
            self.demo_slide_canvas.delete('all')
            
            # EXAKT DASSELBE Rendering wie im Creator verwenden
            self.render_creator_style_slide(slide)
            logger.debug(f"Demo: Slide {slide.slide_id} im Creator-Stil gerendert")
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern der Slide: {e}")
            self.render_fallback_text_display(slide)
    
    def render_creator_style_slide(self, slide):
        """Rendert Slide EXAKT wie im Creator - identisches Aussehen"""
        # SCHRITT 1: Slide-Hintergrund rendern (IDENTISCH zum Creator)
        self.render_identical_slide_background()
        
        # SCHRITT 2: Canvas-Elemente aus config_data rendern (falls vorhanden)
        config_data = getattr(slide, 'config_data', {})
        canvas_elements = config_data.get('canvas_elements', [])
        
        if canvas_elements:
            # Gespeicherte Canvas-Elemente rendern (READ-ONLY)
            for element_data in canvas_elements:
                self.render_readonly_canvas_element(element_data)
        else:
            # Fallback: Text direkt auf Folie (aber im Creator-Stil)
            self.render_text_in_creator_style(slide)
        
        # SCHRITT 3: Z-Order korrigieren
        self.fix_content_z_order()
    
    def render_identical_slide_background(self):
        """Rendert IDENTISCHEN Slide-Hintergrund wie im Creator"""
        # Skalierte Dimensionen berechnen (IDENTISCH zum Creator)
        scaled_width = self.demo_slide_width * self.demo_scale_factor
        scaled_height = self.demo_slide_height * self.demo_scale_factor
        shadow_offset = max(8, int(12 * self.demo_scale_factor))  # Creator verwendet 12
        
        # Schatten-Effekt (IDENTISCH) - HINTERGRUND-LAYER
        self.demo_slide_canvas.create_rectangle(
            self.demo_offset_x + shadow_offset, 
            self.demo_offset_y + shadow_offset,
            self.demo_offset_x + scaled_width + shadow_offset, 
            self.demo_offset_y + scaled_height + shadow_offset,
            fill='#CCCCCC',  # IDENTISCHE Farbe wie Creator
            outline='',
            tags='slide_background_shadow'
        )
        
        # Hauptbereich (weiß) mit IDENTISCHEM Rahmen - HINTERGRUND-LAYER
        self.demo_slide_canvas.create_rectangle(
            self.demo_offset_x, self.demo_offset_y,
            self.demo_offset_x + scaled_width, self.demo_offset_y + scaled_height,
            fill='#FFFFFF',  # IDENTISCHE Farbe
            outline='#666666',  # IDENTISCHE Rahmenfarbe
            width=max(1, int(2 * self.demo_scale_factor)),
            tags='slide_background_main'
        )
        
        # Rahmen für bessere Sichtbarkeit (IDENTISCH zum Creator)
        self.demo_slide_canvas.create_rectangle(
            self.demo_offset_x - 2, self.demo_offset_y - 2,
            self.demo_offset_x + scaled_width + 2, self.demo_offset_y + scaled_height + 2,
            outline='#333333',  # IDENTISCHE Farbe wie Creator
            width=2,
            tags='slide_background_frame'
        )
    
    def render_readonly_canvas_element(self, element_data):
        """Rendert Canvas-Element READONLY aber IDENTISCH zum Creator"""
        try:
            element_type = element_data.get('type')
            coords = element_data.get('coords', [])
            
            if not coords or len(coords) < 2:
                return
            
            # Koordinaten skalieren (IDENTISCH zum Creator)
            scaled_coords = []
            for i in range(0, len(coords), 2):
                if i+1 < len(coords):
                    x = self.demo_offset_x + (coords[i] * self.demo_scale_factor)
                    y = self.demo_offset_y + (coords[i+1] * self.demo_scale_factor)
                    scaled_coords.extend([x, y])
            
            # Widget-Elemente als READONLY Labels rendern
            if element_type == 'window':
                self.render_readonly_widget_element(element_data, scaled_coords[0], scaled_coords[1])
            
            # Canvas-Elemente IDENTISCH rendern
            elif element_type in ['text', 'rectangle', 'oval', 'line']:
                self.render_identical_canvas_shape(element_type, element_data, scaled_coords)
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern des readonly Canvas-Elements: {e}")
    
    def render_readonly_widget_element(self, element_data, x, y):
        """Rendert Widget-Elements als READ-ONLY aber IDENTISCH aussehend - VOLLSTÄNDIGE METHODE"""
        try:
            widget_type = element_data.get('widget_type', 'Label')
            
            if widget_type == 'Text':
                # Text-Widget als READ-ONLY Text-Widget (IDENTISCHES Aussehen)
                text = element_data.get('text', 'Text')
                font = element_data.get('font', 'Arial 12')
                bg = element_data.get('bg', 'white')
                fg = element_data.get('fg', 'black')
                width = element_data.get('width', 20)
                height = element_data.get('height', 1)
                
                # IDENTISCHES Text-Widget erstellen
                text_widget = tk.Text(
                    self.demo_slide_canvas,
                    width=width,
                    height=height,
                    font=font,
                    bg=bg,
                    fg=fg,
                    relief='flat',  # IDENTISCH zum Creator
                    bd=1,           # IDENTISCH zum Creator
                    wrap='word',
                    state='normal'  # Temporär für Insert
                )
                text_widget.insert('1.0', text)
                text_widget.configure(state='disabled')  # READ-ONLY für Demo
                
                self.demo_slide_canvas.create_window(x, y, window=text_widget, anchor='nw', tags='slide_content')
                logger.debug(f"Demo: Text-Widget erstellt (READ-ONLY): '{text[:30]}...'")
            
            elif widget_type == 'Label':
                # Label-Widget IDENTISCH rendern
                text = element_data.get('text', 'Label')
                font = element_data.get('font', 'Arial 12')
                bg = element_data.get('bg', 'white')
                fg = element_data.get('fg', 'black')
                
                label_widget = tk.Label(
                    self.demo_slide_canvas,
                    text=text,
                    font=font,
                    bg=bg,
                    fg=fg,
                    relief='flat'  # IDENTISCH zum Creator
                )
                
                self.demo_slide_canvas.create_window(x, y, window=label_widget, anchor='nw', tags='slide_content')
                logger.debug(f"Demo: Label-Widget erstellt: '{text}'")
            
            elif widget_type == 'Frame':
                # Frame-Widget als READ-ONLY Container
                bg = element_data.get('bg', 'lightgray')
                width = element_data.get('width', 100)
                height = element_data.get('height', 50)
                relief = element_data.get('relief', 'flat')
                bd = element_data.get('bd', 1)
                
                frame_widget = tk.Frame(
                    self.demo_slide_canvas,
                    bg=bg,
                    width=width,
                    height=height,
                    relief=relief,
                    bd=bd
                )
                frame_widget.pack_propagate(False)
                
                # Child-Widgets als READ-ONLY rendern (falls vorhanden)
                children = element_data.get('children', [])
                for child_data in children:
                    self.render_readonly_child_widget(frame_widget, child_data)
                
                self.demo_slide_canvas.create_window(x, y, window=frame_widget, anchor='nw', tags='slide_content')
                logger.debug(f"Demo: Frame-Widget erstellt mit {len(children)} Kindern")
            
            else:
                # Unbekannter Widget-Typ: Als Label mit Info rendern
                fallback_label = tk.Label(
                    self.demo_slide_canvas,
                    text=f"[{widget_type}]",
                    font=('Arial', 10),
                    bg='#EEEEEE',
                    fg='#666666',
                    relief='flat'
                )
                
                self.demo_slide_canvas.create_window(x, y, window=fallback_label, anchor='nw', tags='slide_content')
                logger.debug(f"Demo: Fallback-Widget für unbekannten Typ: {widget_type}")
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern des readonly Widget-Elements: {e}")
            # Fallback: Einfaches Label mit Fehler-Info
            try:
                error_label = tk.Label(
                    self.demo_slide_canvas,
                    text="[Element-Fehler]",
                    font=('Arial', 10),
                    bg='#FFEEEE',
                    fg='#CC0000',
                    relief='flat'
                )
                self.demo_slide_canvas.create_window(x, y, window=error_label, anchor='nw', tags='slide_content')
            except:
                pass  # Selbst Fallback-Widget konnte nicht erstellt werden
    
    def render_readonly_child_widget(self, parent_frame, child_data):
        """Rendert Child-Widgets in einem Frame als READ-ONLY"""
        try:
            widget_type = child_data.get('widget_type', 'Label')
            
            if widget_type == 'Label':
                text = child_data.get('text', 'Child Label')
                font = child_data.get('font', 'Arial 10')
                bg = child_data.get('bg', parent_frame.cget('bg'))
                fg = child_data.get('fg', 'black')
                
                child_label = tk.Label(
                    parent_frame,
                    text=text,
                    font=font,
                    bg=bg,
                    fg=fg
                )
                child_label.pack(expand=True)
                
            elif widget_type == 'Text':
                # Child-Text als READ-ONLY
                text = child_data.get('text', 'Child Text')
                font = child_data.get('font', 'Arial 10')
                bg = child_data.get('bg', 'white')
                fg = child_data.get('fg', 'black')
                width = child_data.get('width', 15)
                height = child_data.get('height', 1)
                
                child_text = tk.Text(
                    parent_frame,
                    width=width,
                    height=height,
                    font=font,
                    bg=bg,
                    fg=fg,
                    state='normal'
                )
                child_text.insert('1.0', text)
                child_text.configure(state='disabled')  # READ-ONLY
                child_text.pack(expand=True)
            
            else:
                # Unbekannter Child-Typ
                fallback_child = tk.Label(
                    parent_frame,
                    text=f"[{widget_type}]",
                    font=('Arial', 8),
                    bg='#F0F0F0',
                    fg='#888888'
                )
                fallback_child.pack(expand=True)
                
        except Exception as e:
            logger.error(f"Fehler beim Rendern des Child-Widgets: {e}")
    
    def render_identical_canvas_shape(self, element_type, element_data, scaled_coords):
        """Rendert Canvas-Formen IDENTISCH zum Creator"""
        try:
            if element_type == 'text' and len(scaled_coords) >= 2:
                text = element_data.get('text', 'Text')
                font = element_data.get('font', 'Arial 12')
                fill = element_data.get('fill', 'black')
                
                self.demo_slide_canvas.create_text(
                    scaled_coords[0], scaled_coords[1],
                    text=text,
                    font=font,
                    fill=fill,
                    tags='slide_content'
                )
            
            elif element_type == 'rectangle' and len(scaled_coords) >= 4:
                fill = element_data.get('fill', '')
                outline = element_data.get('outline', 'black')
                width = element_data.get('width', 1)
                
                self.demo_slide_canvas.create_rectangle(
                    scaled_coords[0], scaled_coords[1],
                    scaled_coords[2], scaled_coords[3],
                    fill=fill,
                    outline=outline,
                    width=width,
                    tags='slide_content'
                )
            
            elif element_type == 'oval' and len(scaled_coords) >= 4:
                fill = element_data.get('fill', '')
                outline = element_data.get('outline', 'black')
                width = element_data.get('width', 1)
                
                self.demo_slide_canvas.create_oval(
                    scaled_coords[0], scaled_coords[1],
                    scaled_coords[2], scaled_coords[3],
                    fill=fill,
                    outline=outline,
                    width=width,
                    tags='slide_content'
                )
            
            elif element_type == 'line' and len(scaled_coords) >= 4:
                fill = element_data.get('fill', 'black')
                width = element_data.get('width', 1)
                
                self.demo_slide_canvas.create_line(
                    scaled_coords[0], scaled_coords[1],
                    scaled_coords[2], scaled_coords[3],
                    fill=fill,
                    width=width,
                    tags='slide_content'
                )
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern der identischen Canvas-Shape: {e}")
    
    def render_text_in_creator_style(self, slide):
        """Rendert Text im IDENTISCHEN Creator-Stil (Fallback)"""
        # IDENTISCHE Positionierung wie im Creator
        title_x = self.demo_offset_x + (80 * self.demo_scale_factor)  # IDENTISCH
        title_y = self.demo_offset_y + (60 * self.demo_scale_factor)   # IDENTISCH
        
        # Titel mit IDENTISCHEM Styling
        self.demo_slide_canvas.create_text(
            title_x,
            title_y,
            text=slide.title,
            font=('Segoe UI', int(28 * self.demo_scale_factor), 'bold'),  # IDENTISCHE Schrift
            fill='#1E88E5',  # IDENTISCHE Farbe
            anchor='nw',
            width=int((self.demo_slide_width - 200) * self.demo_scale_factor),
            tags='slide_content'
        )
        
        # Content mit IDENTISCHEM Styling
        content_y = title_y + (120 * self.demo_scale_factor)  # IDENTISCHER Abstand
        content_lines = slide.content.split('\n')
        
        for i, line in enumerate(content_lines[:8]):
            if line.strip():
                self.demo_slide_canvas.create_text(
                    title_x,
                    content_y + (i * 35 * self.demo_scale_factor),  # IDENTISCHER Zeilenabstand
                    text=f"• {line.strip()}",
                    font=('Segoe UI', int(16 * self.demo_scale_factor)),  # IDENTISCHE Schrift
                    fill='#2C3E50',  # IDENTISCHE Farbe
                    anchor='nw',
                    width=int((self.demo_slide_width - 200) * self.demo_scale_factor),
                    tags='slide_content'
                )
        
        # Branding IDENTISCH zum Creator
        self.add_identical_branding_on_slide(slide)
    
    def add_identical_branding_on_slide(self, slide):
        """Fügt IDENTISCHES Branding wie im Creator hinzu"""
        # IDENTISCHE Positionierung und Styling wie Creator
        brand_x = self.demo_offset_x + (self.demo_slide_width - 250) * self.demo_scale_factor
        brand_y = self.demo_offset_y + (self.demo_slide_height - 120) * self.demo_scale_factor
        
        self.demo_slide_canvas.create_text(
            brand_x,
            brand_y,
            text="BERTRANDT",
            font=('Segoe UI', int(20 * self.demo_scale_factor), 'bold'),  # IDENTISCH
            fill='#003366',  # IDENTISCH
            anchor='se',
            tags='slide_content'
        )
        
        # Folien-Nummer IDENTISCH
        number_x = self.demo_offset_x + (80 * self.demo_scale_factor)
        number_y = self.demo_offset_y + (self.demo_slide_height - 120) * self.demo_scale_factor
        
        self.demo_slide_canvas.create_text(
            number_x,
            number_y,
            text=f"Folie {slide.slide_id}",
            font=('Segoe UI', int(16 * self.demo_scale_factor)),  # IDENTISCH
            fill='#666666',  # IDENTISCH
            anchor='sw',
            tags='slide_content'
        )
    
    def load_presentation_data(self, presentation_data):
        """Lädt Präsentationsdaten (für initialen Load)"""
        try:
            slides = presentation_data.get('presentation', {}).get('slides', [])
            if slides:
                logger.info(f"Demo: {len(slides)} Slides zum Laden erhalten")
                # Optional: Zur ersten Slide wechseln
                if len(slides) > 0:
                    first_slide_id = slides[0].get('id', 1)
                    self.update_slide_display(first_slide_id)
        except Exception as e:
            logger.error(f"Fehler beim Laden der Präsentationsdaten im Demo: {e}")
    
    def fix_content_z_order(self):
        """Korrigiert die Z-Order - bringt alle Content-Elemente nach vorne"""
        try:
            # Alle Canvas-Items mit slide_content Tag nach vorne bringen
            content_items = self.demo_slide_canvas.find_withtag('slide_content')
            for item in content_items:
                self.demo_slide_canvas.tag_raise(item)
            
            # Alle Window-Items (Widgets) nach vorne bringen
            all_items = self.demo_slide_canvas.find_all()
            for item in all_items:
                item_type = self.demo_slide_canvas.type(item)
                if item_type == 'window':
                    self.demo_slide_canvas.tag_raise(item)
            
            logger.debug("Z-Order korrigiert - Content-Elemente sind jetzt über dem Hintergrund")
            
        except Exception as e:
            logger.error(f"Fehler beim Korrigieren der Z-Order: {e}")
    
    def render_demo_slide_background(self):
        """Rendert den modernen Slide-Hintergrund für Demo"""
        # Skalierte Dimensionen berechnen
        scaled_width = self.demo_slide_width * self.demo_scale_factor
        scaled_height = self.demo_slide_height * self.demo_scale_factor
        shadow_offset = max(6, int(8 * self.demo_scale_factor))
        
        # Moderner Schatten-Effekt (weicher) - HINTERGRUND-LAYER
        self.demo_slide_canvas.create_rectangle(
            self.demo_offset_x + shadow_offset, 
            self.demo_offset_y + shadow_offset,
            self.demo_offset_x + scaled_width + shadow_offset, 
            self.demo_offset_y + scaled_height + shadow_offset,
            fill='#CCCCCC',
            outline='',
            tags='slide_background_shadow'
        )
        
        # Hauptbereich (weiß) mit modernem Rahmen - HINTERGRUND-LAYER
        self.demo_slide_canvas.create_rectangle(
            self.demo_offset_x, self.demo_offset_y,
            self.demo_offset_x + scaled_width, self.demo_offset_y + scaled_height,
            fill='#FFFFFF',
            outline='#666666',
            width=max(1, int(2 * self.demo_scale_factor)),
            tags='slide_background_main'
        )
        
        # Demo-spezifischer Akzent-Rahmen (Bertrandt Blau) - HINTERGRUND-LAYER
        self.demo_slide_canvas.create_rectangle(
            self.demo_offset_x - 2, self.demo_offset_y - 2,
            self.demo_offset_x + scaled_width + 2, self.demo_offset_y + scaled_height + 2,
            fill='',
            outline='#1E88E5',  # Bertrandt Blau
            width=max(2, int(3 * self.demo_scale_factor)),
            tags='slide_background_border'
        )
        
        # Demo-Status-Indikator (kleiner Punkt oben links) - HINTERGRUND-LAYER
        indicator_size = max(8, int(12 * self.demo_scale_factor))
        self.demo_slide_canvas.create_oval(
            self.demo_offset_x + 20, self.demo_offset_y + 20,
            self.demo_offset_x + 20 + indicator_size, self.demo_offset_y + 20 + indicator_size,
            fill='#FF6600',  # Bertrandt Orange
            outline='#FF6600',
            tags='slide_background_indicator'
        )
    
    def render_canvas_element(self, element_data):
        """Rendert ein einzelnes Canvas-Element"""
        try:
            element_type = element_data.get('type')
            coords = element_data.get('coords', [])
            
            if not coords or len(coords) < 2:
                return
            
            # Koordinaten skalieren und positionieren
            scaled_coords = []
            for i in range(0, len(coords), 2):
                if i+1 < len(coords):
                    x = self.demo_offset_x + (coords[i] * self.demo_scale_factor)
                    y = self.demo_offset_y + (coords[i+1] * self.demo_scale_factor)
                    scaled_coords.extend([x, y])
            
            # Tags für Skalierung speichern
            tags = ['element'] + [str(coord) for coord in coords]
            
            # Element-spezifisches Rendering
            if element_type == 'window':
                self.render_widget_element(element_data, scaled_coords[0], scaled_coords[1])
            
            elif element_type == 'text':
                # Text-Element
                text = element_data.get('text', 'Text')
                font = element_data.get('font', 'Arial 12')
                fill = element_data.get('fill', 'black')
                
                self.demo_slide_canvas.create_text(
                    scaled_coords[0], scaled_coords[1],
                    text=text,
                    font=font,
                    fill=fill,
                    tags=tags
                )
            
            elif element_type == 'rectangle':
                # Rechteck
                if len(scaled_coords) >= 4:
                    fill = element_data.get('fill', '')
                    outline = element_data.get('outline', 'black')
                    width = element_data.get('width', 1)
                    
                    self.demo_slide_canvas.create_rectangle(
                        scaled_coords[0], scaled_coords[1],
                        scaled_coords[2], scaled_coords[3],
                        fill=fill,
                        outline=outline,
                        width=width,
                        tags=tags
                    )
            
            elif element_type == 'oval':
                # Kreis/Oval
                if len(scaled_coords) >= 4:
                    fill = element_data.get('fill', '')
                    outline = element_data.get('outline', 'black')
                    width = element_data.get('width', 1)
                    
                    self.demo_slide_canvas.create_oval(
                        scaled_coords[0], scaled_coords[1],
                        scaled_coords[2], scaled_coords[3],
                        fill=fill,
                        outline=outline,
                        width=width,
                        tags=tags
                    )
            
            elif element_type == 'line':
                # Linie
                if len(scaled_coords) >= 4:
                    fill = element_data.get('fill', 'black')
                    width = element_data.get('width', 1)
                    
                    self.demo_slide_canvas.create_line(
                        scaled_coords[0], scaled_coords[1],
                        scaled_coords[2], scaled_coords[3],
                        fill=fill,
                        width=width,
                        tags=tags
                    )
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern des Canvas-Elements: {e}")
    
    def render_widget_element(self, element_data, x, y):
        """Rendert ein Widget-Element (Text, Label, Frame, etc.)"""
        try:
            widget_type = element_data.get('widget_type', 'Label')
            
            if widget_type == 'Text':
                # Text-Widget als Label darstellen
                text = element_data.get('text', 'Text')
                font = element_data.get('font', 'Arial 12')
                bg = element_data.get('bg', 'white')
                fg = element_data.get('fg', 'black')
                width = element_data.get('width', 20)
                height = element_data.get('height', 1)
                
                # Skalierte Größe
                scaled_width = int(width * self.demo_scale_factor * 8)  # Approximation
                scaled_height = int(height * self.demo_scale_factor * 20)  # Approximation
                
                text_widget = tk.Text(
                    self.demo_slide_canvas,
                    width=width,
                    height=height,
                    font=font,
                    bg=bg,
                    fg=fg,
                    relief='flat',
                    bd=1,
                    wrap='word'
                )
                text_widget.insert('1.0', text)
                text_widget.configure(state='disabled')  # Read-only in Demo
                
                self.demo_slide_canvas.create_window(x, y, window=text_widget, anchor='nw')
            
            elif widget_type == 'Label':
                # Label-Widget
                text = element_data.get('text', 'Label')
                font = element_data.get('font', 'Arial 12')
                bg = element_data.get('bg', 'white')
                fg = element_data.get('fg', 'black')
                
                label_widget = tk.Label(
                    self.demo_slide_canvas,
                    text=text,
                    font=font,
                    bg=bg,
                    fg=fg,
                    relief='flat'
                )
                
                self.demo_slide_canvas.create_window(x, y, window=label_widget, anchor='nw')
            
            elif widget_type == 'Frame':
                # Frame-Widget
                bg = element_data.get('bg', 'lightgray')
                width = element_data.get('width', 100)
                height = element_data.get('height', 50)
                relief = element_data.get('relief', 'flat')
                bd = element_data.get('bd', 1)
                
                frame_widget = tk.Frame(
                    self.demo_slide_canvas,
                    bg=bg,
                    width=width,
                    height=height,
                    relief=relief,
                    bd=bd
                )
                frame_widget.pack_propagate(False)
                
                # Child-Widgets rendern (falls vorhanden)
                children = element_data.get('children', [])
                for child_data in children:
                    self.render_child_widget(frame_widget, child_data)
                
                self.demo_slide_canvas.create_window(x, y, window=frame_widget, anchor='nw')
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern des Widget-Elements: {e}")
    
    def render_child_widget(self, parent, child_data):
        """Rendert Child-Widgets in einem Frame"""
        try:
            widget_type = child_data.get('widget_type', 'Label')
            
            if widget_type == 'Label':
                text = child_data.get('text', 'Child Label')
                font = child_data.get('font', 'Arial 10')
                bg = child_data.get('bg', parent.cget('bg'))
                fg = child_data.get('fg', 'black')
                
                child_label = tk.Label(
                    parent,
                    text=text,
                    font=font,
                    bg=bg,
                    fg=fg
                )
                child_label.pack(expand=True)
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern des Child-Widgets: {e}")
    
    def render_fallback_text_display(self, slide):
        """Moderne Text-Anzeige als Fallback - mit Hintergrund"""
        # Erst den Slide-Hintergrund rendern
        self.render_demo_slide_background()
        
        # Dann den Inhalt rendern
        self.render_fallback_text_content_only(slide)
    
    def render_fallback_text_content_only(self, slide):
        """Rendert Text direkt AUF der weißen Folie (nicht in separaten Containern)"""
        # Titel direkt auf der Folie (innerhalb der Slide-Grenzen)
        title_x = self.demo_offset_x + (100 * self.demo_scale_factor)  # Links mit Abstand
        title_y = self.demo_offset_y + (80 * self.demo_scale_factor)   # Oben mit Abstand
        
        # Titel mit Bertrandt-Styling direkt auf der Folie
        self.demo_slide_canvas.create_text(
            title_x,
            title_y,
            text=slide.title,
            font=('Segoe UI', int(32 * self.demo_scale_factor), 'bold'),
            fill='#1E88E5',  # Bertrandt Blau
            anchor='nw',
            width=int((self.demo_slide_width - 200) * self.demo_scale_factor),
            tags='slide_content'
        )
        
        # Untertitel-Linie direkt auf der Folie
        line_y = title_y + (60 * self.demo_scale_factor)
        self.demo_slide_canvas.create_line(
            title_x,
            line_y,
            self.demo_offset_x + (self.demo_slide_width - 100) * self.demo_scale_factor,
            line_y,
            fill='#FF6600',  # Bertrandt Orange
            width=int(4 * self.demo_scale_factor),
            tags='slide_content'
        )
        
        # Content direkt auf der Folie
        content_y = line_y + (40 * self.demo_scale_factor)
        content_lines = slide.content.split('\n')
        
        for i, line in enumerate(content_lines[:8]):  # Mehr Zeilen möglich
            if line.strip():
                self.demo_slide_canvas.create_text(
                    title_x,
                    content_y + (i * 40 * self.demo_scale_factor),
                    text=f"• {line.strip()}",
                    font=('Segoe UI', int(18 * self.demo_scale_factor)),
                    fill='#2C3E50',
                    anchor='nw',
                    width=int((self.demo_slide_width - 200) * self.demo_scale_factor),
                    tags='slide_content'
                )
        
        # Bertrandt-Branding direkt auf der Folie (unten)
        self.add_demo_modern_branding_on_slide(slide)
    
    def add_demo_modern_branding_on_slide(self, slide):
        """Fügt Bertrandt-Branding direkt AUF die Folie (innerhalb der Slide-Grenzen)"""
        # Bertrandt-Logo/Text (unten rechts, AUF der Folie)
        brand_x = self.demo_offset_x + (self.demo_slide_width - 200) * self.demo_scale_factor
        brand_y = self.demo_offset_y + (self.demo_slide_height - 80) * self.demo_scale_factor
        
        self.demo_slide_canvas.create_text(
            brand_x,
            brand_y,
            text="BERTRANDT",
            font=('Segoe UI', int(16 * self.demo_scale_factor), 'bold'),
            fill='#003366',
            anchor='se',
            tags='slide_content'
        )
        
        # Folien-Nummer (unten links, AUF der Folie)
        number_x = self.demo_offset_x + (100 * self.demo_scale_factor)
        number_y = self.demo_offset_y + (self.demo_slide_height - 80) * self.demo_scale_factor
        
        self.demo_slide_canvas.create_text(
            number_x,
            number_y,
            text=f"Folie {slide.slide_id}",
            font=('Segoe UI', int(14 * self.demo_scale_factor)),
            fill='#666666',
            anchor='sw',
            tags='slide_content'
        )
    
    def add_demo_modern_branding(self, slide):
        """Fügt modernes Bertrandt-Branding zur Demo-Ansicht hinzu (über dem Slide)"""
        # Bertrandt-Logo/Text (unten rechts, über dem Slide)
        brand_x = self.demo_offset_x + (self.demo_slide_width - 120) * self.demo_scale_factor
        brand_y = self.demo_offset_y + (self.demo_slide_height - 80) * self.demo_scale_factor
        
        self.demo_slide_canvas.create_text(
            brand_x,
            brand_y,
            text="BERTRANDT",
            font=('Segoe UI', int(12 * self.demo_scale_factor), 'bold'),
            fill='#003366',
            anchor='se',
            tags='slide_content'  # Über dem Slide
        )
        
        # Folien-Nummer (unten links, über dem Slide)
        number_x = self.demo_offset_x + (120 * self.demo_scale_factor)
        number_y = self.demo_offset_y + (self.demo_slide_height - 80) * self.demo_scale_factor
        
        self.demo_slide_canvas.create_text(
            number_x,
            number_y,
            text=f"Folie {slide.slide_id}",
            font=('Segoe UI', int(10 * self.demo_scale_factor)),
            fill='#666666',
            anchor='sw',
            tags='slide_content'  # Über dem Slide
        )
        
        # Demo-Indikator (oben rechts, über dem Slide)
        demo_x = self.demo_offset_x + (self.demo_slide_width - 120) * self.demo_scale_factor
        demo_y = self.demo_offset_y + (80 * self.demo_scale_factor)
        
        self.demo_slide_canvas.create_text(
            demo_x,
            demo_y,
            text="▶ DEMO",
            font=('Segoe UI', int(11 * self.demo_scale_factor), 'bold'),
            fill='#FF6600',  # Bertrandt Orange
            anchor='ne',
            tags='slide_content'  # Über dem Slide
        )
    
    def update_demo_thumbnail_selection(self, slide_id):
        """Aktualisiert die Demo-Thumbnail-Auswahl"""
        colors = theme_manager.get_colors()
        
        for sid, btn in self.demo_thumbnail_buttons.items():
            if sid == slide_id:
                btn.configure(bg=colors['accent_secondary'], fg='white')
            else:
                btn.configure(bg=colors['background_tertiary'], fg=colors['text_primary'])
    
    def create_control_panel(self):
        """Erstellt das Steuerungs-Panel"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Control Panel Frame
        control_frame = ttk.Frame(self.container, style='Card.TFrame')
        control_frame.pack(fill='x', padx=40, pady=(0, 20))
        
        # Titel
        control_title = tk.Label(
            control_frame,
            text="🎮 Steuerung",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_tertiary']
        )
        control_title.pack(pady=(15, 10))
        
        # Button-Container
        button_frame = tk.Frame(control_frame, bg=colors['background_tertiary'])
        button_frame.pack(pady=(0, 15))
        
        # Start/Stop Button
        self.start_stop_btn = tk.Button(
            button_frame,
            text="▶️ Demo Starten",
            font=fonts['button'],
            bg=colors['accent_primary'],
            fg='white',
            padx=20,
            pady=10,
            command=self.toggle_demo
        )
        self.start_stop_btn.pack(side='left', padx=5)
        
        # Vorherige Slide
        prev_btn = tk.Button(
            button_frame,
            text="⏮️ Zurück",
            font=fonts['button'],
            bg=colors['background_hover'],
            fg=colors['text_primary'],
            padx=15,
            pady=10,
            command=demo_service.previous_slide
        )
        prev_btn.pack(side='left', padx=5)
        
        # Nächste Slide
        next_btn = tk.Button(
            button_frame,
            text="⏭️ Weiter",
            font=fonts['button'],
            bg=colors['background_hover'],
            fg=colors['text_primary'],
            padx=15,
            pady=10,
            command=demo_service.next_slide
        )
        next_btn.pack(side='left', padx=5)
        
        # Einstellungen
        settings_frame = tk.Frame(control_frame, bg=colors['background_tertiary'])
        settings_frame.pack(pady=(10, 15))
        
        # Slide-Dauer
        duration_label = tk.Label(
            settings_frame,
            text="Slide-Dauer (Sekunden):",
            font=fonts['label'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary']
        )
        duration_label.pack(side='left', padx=(0, 10))
        
        self.duration_var = tk.StringVar(value="5")
        duration_entry = tk.Entry(
            settings_frame,
            textvariable=self.duration_var,
            font=fonts['body'],
            width=5
        )
        duration_entry.pack(side='left', padx=(0, 10))
        duration_entry.bind('<Return>', self.update_duration)
        
        # Loop-Modus
        self.loop_var = tk.BooleanVar(value=True)
        loop_check = tk.Checkbutton(
            settings_frame,
            text="Endlos-Schleife",
            variable=self.loop_var,
            font=fonts['label'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary'],
            command=self.update_loop_mode
        )
        loop_check.pack(side='left', padx=(20, 0))
    
    def create_status_display(self):
        """Erstellt die Status-Anzeige"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Status Frame
        status_frame = ttk.Frame(self.container, style='Card.TFrame')
        status_frame.pack(fill='x', padx=40, pady=(0, 20))
        
        # Titel
        status_title = tk.Label(
            status_frame,
            text="📊 Status",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_tertiary']
        )
        status_title.pack(pady=(15, 10))
        
        # Status-Grid
        status_grid = tk.Frame(status_frame, bg=colors['background_tertiary'])
        status_grid.pack(pady=(0, 15))
        
        # Aktueller Status
        self.status_label = tk.Label(
            status_grid,
            text="Status: ⏹️ Gestoppt",
            font=fonts['body'],
            fg=colors['text_primary'],
            bg=colors['background_tertiary']
        )
        self.status_label.grid(row=0, column=0, sticky='w', padx=20, pady=5)
        
        # Aktuelle Slide
        self.slide_label = tk.Label(
            status_grid,
            text="Slide: - / -",
            font=fonts['body'],
            fg=colors['text_primary'],
            bg=colors['background_tertiary']
        )
        self.slide_label.grid(row=0, column=1, sticky='w', padx=20, pady=5)
        
        # Verbleibende Zeit
        self.time_label = tk.Label(
            status_grid,
            text="Zeit: --:--",
            font=fonts['body'],
            fg=colors['text_primary'],
            bg=colors['background_tertiary']
        )
        self.time_label.grid(row=1, column=0, sticky='w', padx=20, pady=5)
        
        # Gesamte Slides
        total_slides = content_manager.get_slide_count()
        self.total_label = tk.Label(
            status_grid,
            text=f"Gesamt: {total_slides} Slides",
            font=fonts['body'],
            fg=colors['text_primary'],
            bg=colors['background_tertiary']
        )
        self.total_label.grid(row=1, column=1, sticky='w', padx=20, pady=5)
    
    def create_slide_preview(self):
        """Erstellt die Slide-Vorschau"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Preview Frame
        preview_frame = ttk.Frame(self.container, style='Card.TFrame')
        preview_frame.pack(fill='both', expand=True, padx=40, pady=(0, 20))
        
        # Titel
        preview_title = tk.Label(
            preview_frame,
            text="👁️ Aktuelle Slide",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_tertiary']
        )
        preview_title.pack(pady=(15, 10))
        
        # Preview-Container
        self.preview_container = tk.Frame(
            preview_frame,
            bg=colors['background_secondary'],
            relief='solid',
            bd=1
        )
        self.preview_container.pack(fill='both', expand=True, padx=20, pady=(0, 15))
        
        # Placeholder
        self.preview_label = tk.Label(
            self.preview_container,
            text="Keine Slide ausgewählt",
            font=fonts['subtitle'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        self.preview_label.pack(expand=True)
    
    def toggle_demo(self):
        """Startet/Stoppt die Demo"""
        if demo_service.running:
            demo_service.stop_demo()
            self.play_pause_btn.configure(text="▶ Demo Starten", bg=theme_manager.get_colors()['accent_primary'])
            self.demo_status_indicator.configure(text="⏹️ Gestoppt", fg=theme_manager.get_colors()['accent_tertiary'])
            self.time_remaining.configure(text="")
        else:
            # Standard-Werte für Demo
            demo_service.set_slide_duration(5)  # 5 Sekunden pro Slide
            demo_service.set_loop_mode(True)    # Endlos-Schleife
            demo_service.start_demo()
            self.play_pause_btn.configure(text="⏸ Demo Stoppen", bg=theme_manager.get_colors()['accent_warning'])
            self.demo_status_indicator.configure(text="▶️ Läuft", fg=theme_manager.get_colors()['accent_primary'])
        
        self.update_status_display()
    
    
    def on_slide_changed(self, slide_id):
        """Callback für Slide-Wechsel"""
        self.update_slide_display(slide_id)
        self.update_status_display()
        
        # Hardware-Status aktualisieren
        from models.hardware import hardware_manager
        connected_devices = sum(1 for status in hardware_manager.get_status_summary().values() if status == "connected")
        self.hardware_status.configure(text=f"Hardware: {connected_devices} Geräte verbunden")
    
    def update_status_display(self):
        """Aktualisiert die Status-Anzeige"""
        status = demo_service.get_status()
        
        # Slide-Zähler aktualisieren
        if hasattr(self, 'slide_counter'):
            self.slide_counter.configure(text=f"{status['current_slide']}/10")
        
        # Status-Text aktualisieren
        if hasattr(self, 'status_text'):
            if status['running']:
                self.status_text.configure(text=f"Demo läuft - Folie {status['current_slide']} von 10")
            else:
                self.status_text.configure(text="Demo bereit - BumbleB Story mit 10 Folien geladen")
    
    def update_slide_preview(self, slide_id):
        """Aktualisiert die Slide-Vorschau"""
        slide = content_manager.get_slide(slide_id)
        
        if slide:
            preview_text = f"Slide {slide_id}: {slide.title}\n\n{slide.content[:100]}..."
        else:
            preview_text = f"Slide {slide_id}\nKein Inhalt verfügbar"
        
        self.preview_label.configure(text=preview_text)
    
    def refresh_theme(self):
        """Aktualisiert das Theme für den Demo-Tab"""
        from core.theme import THEME_VARS, theme_manager
        
        # Neue Farben holen
        colors = theme_manager.get_colors()
        
        # Container-Hintergrund aktualisieren
        if hasattr(self, 'container'):
            try:
                if hasattr(self.container, 'configure') and 'bg' in self.container.configure():
                    self.container.configure(bg=THEME_VARS["bg"])
            except:
                pass
        
        # Alle Widgets mit theme-aware Farben aktualisieren
        self._update_all_widget_colors(self.container, colors)
        
        logger.debug("Demo-Tab Theme aktualisiert")
    
    def _update_all_widget_colors(self, widget, colors):
        """Aktualisiert alle Widget-Farben rekursiv basierend auf dem aktuellen Theme"""
        try:
            widget_class = widget.winfo_class()
            
            # Frame-Widgets
            if isinstance(widget, tk.Frame) and not isinstance(widget, ttk.Frame):
                # Bestimme die richtige Hintergrundfarbe basierend auf dem Widget-Kontext
                if hasattr(widget, '_bg_type'):
                    bg_key = widget._bg_type
                else:
                    # Standard-Hintergrund
                    bg_key = 'background_secondary'
                
                widget.configure(bg=colors.get(bg_key, colors['background_secondary']))
            
            # Label-Widgets
            elif isinstance(widget, tk.Label):
                widget.configure(
                    bg=colors['background_secondary'],
                    fg=colors['text_primary']
                )
            
            # Button-Widgets
            elif isinstance(widget, tk.Button):
                # Prüfe ob es ein spezieller Button ist
                button_text = widget.cget('text')
                if any(keyword in button_text.lower() for keyword in ['start', 'play', '▶']):
                    widget.configure(bg=colors['accent_primary'], fg=colors['text_on_accent'])
                elif any(keyword in button_text.lower() for keyword in ['stop', 'pause', '⏸']):
                    widget.configure(bg=colors['accent_warning'], fg=colors['text_on_accent'])
                else:
                    widget.configure(bg=colors['background_hover'], fg=colors['text_primary'])
            
            # Text-Widgets
            elif isinstance(widget, tk.Text):
                widget.configure(
                    bg=colors['background_secondary'],
                    fg=colors['text_primary'],
                    insertbackground=colors['text_primary']
                )
            
            # Scrollbar-Widgets
            elif isinstance(widget, tk.Scrollbar):
                widget.configure(bg=colors['background_tertiary'])
            
            # Canvas-Widgets
            elif isinstance(widget, tk.Canvas):
                widget.configure(bg=colors['background_secondary'])
            
            # Rekursiv alle Child-Widgets durchgehen
            for child in widget.winfo_children():
                self._update_all_widget_colors(child, colors)
                
        except Exception as e:
            # Ignoriere Fehler bei Widgets die keine Farb-Optionen haben
            pass
    
    def _update_frame_backgrounds(self, widget, bg_color):
        """Hilfsfunktion: Aktualisiert Hintergründe aller Frame-Widgets rekursiv"""
        try:
            # Nur tk.Frame unterstützt bg-Option, ttk.Frame nicht
            if isinstance(widget, tk.Frame) and not isinstance(widget, ttk.Frame):
                widget.configure(bg=bg_color)
            
            # Alle Child-Widgets durchgehen
            for child in widget.winfo_children():
                self._update_frame_backgrounds(child, bg_color)
        except Exception as e:
            # Ignoriere Fehler bei Widgets die keine bg-Option haben
            pass
    
    def show(self):
        """Zeigt den Tab"""
        if not self.visible:
            self.container.pack(fill='both', expand=True)
            self.visible = True
            self.update_status_display()
            logger.debug("Demo-Tab angezeigt")
    
    def hide(self):
        """Versteckt den Tab"""
        if self.visible:
            self.container.pack_forget()
            self.visible = False
            logger.debug("Demo-Tab versteckt")
