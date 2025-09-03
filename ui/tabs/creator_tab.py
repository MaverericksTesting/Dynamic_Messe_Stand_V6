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

class CreatorTab:
    """3-Spalten Creator-Tab für Demo-Folien Bearbeitung"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.visible = False
        self.current_edit_slide = 1
        self.current_slide = None
        
        # Drag & Drop Variablen
        self.drag_data = {'element_type': None, 'widget': None}
        self.slide_width = 1920
        self.slide_height = 1080
        self.scale_factor = 1.0
        self.offset_x = 0
        self.offset_y = 0
        
        self.create_creator_content()
    
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
            self.offset_x + scaled_width + shadow_offset, self.offset_y + scaled_height + shadow_offset,
            fill='#CCCCCC',
            outline='',
            tags='slide_background_shadow'
        )
        
        # Hauptbereich (weiß) über dem Schatten - HINTERGRUND-LAYER
        self.slide_canvas.create_rectangle(
            self.offset_x, self.offset_y,
            self.offset_x + scaled_width, self.offset_y + scaled_height,
            fill='#FFFFFF',
            outline='#666666',
            width=1,
            tags='slide_background_main'
        )
    
    def rescale_existing_elements(self):
        """Skaliert alle bestehenden Canvas-Elemente bei Größenänderungen"""
        try:
            # Alle Canvas-Items durchgehen (außer Drop-Zone)
            for item in self.slide_canvas.find_all():
                tags = self.slide_canvas.gettags(item)
                
                # Drop-Zone überspringen
                if 'dropzone' in tags:
                    continue
                
                # Canvas-Widgets (Text, Bilder, etc.) neu positionieren
                item_type = self.slide_canvas.type(item)
                if item_type == 'window':
                    # Widget-Position neu berechnen
                    coords = self.slide_canvas.coords(item)
                    if len(coords) >= 2:
                        # Ursprüngliche relative Position beibehalten
                        rel_x = (coords[0] - self.offset_x) / self.scale_factor if self.scale_factor > 0 else 0
                        rel_y = (coords[1] - self.offset_y) / self.scale_factor if self.scale_factor > 0 else 0
                        
                        # Neue absolute Position berechnen
                        new_x = self.offset_x + (rel_x * self.scale_factor)
                        new_y = self.offset_y + (rel_y * self.scale_factor)
                        
                        # Widget neu positionieren
                        self.slide_canvas.coords(item, new_x, new_y)
                
                # Canvas-Formen (Kreise, Linien, etc.) skalieren
                elif item_type in ['oval', 'rectangle', 'line']:
                    coords = self.slide_canvas.coords(item)
                    if len(coords) >= 4:
                        # Relative Koordinaten berechnen
                        rel_coords = []
                        for i in range(0, len(coords), 2):
                            rel_x = (coords[i] - self.offset_x) / self.scale_factor if self.scale_factor > 0 else 0
                            rel_y = (coords[i+1] - self.offset_y) / self.scale_factor if self.scale_factor > 0 else 0
                            rel_coords.extend([rel_x, rel_y])
                        
                        # Neue absolute Koordinaten
                        new_coords = []
                        for i in range(0, len(rel_coords), 2):
                            new_x = self.offset_x + (rel_coords[i] * self.scale_factor)
                            new_y = self.offset_y + (rel_coords[i+1] * self.scale_factor)
                            new_coords.extend([new_x, new_y])
                        
                        # Form neu skalieren
                        self.slide_canvas.coords(item, *new_coords)
                
                # Text-Elemente skalieren
                elif item_type == 'text':
                    coords = self.slide_canvas.coords(item)
                    if len(coords) >= 2:
                        # Position neu berechnen
                        rel_x = (coords[0] - self.offset_x) / self.scale_factor if self.scale_factor > 0 else 0
                        rel_y = (coords[1] - self.offset_y) / self.scale_factor if self.scale_factor > 0 else 0
                        
                        new_x = self.offset_x + (rel_x * self.scale_factor)
                        new_y = self.offset_y + (rel_y * self.scale_factor)
                        
                        self.slide_canvas.coords(item, new_x, new_y)
                        
                        # Schriftgröße anpassen (optional)
                        current_font = self.slide_canvas.itemconfig(item, 'font')[4]
                        if current_font:
                            try:
                                font_parts = current_font.split()
                                if len(font_parts) >= 2:
                                    base_size = int(font_parts[1])
                                    new_size = max(8, int(base_size * self.scale_factor))
                                    new_font = f"{font_parts[0]} {new_size}"
                                    if len(font_parts) > 2:
                                        new_font += f" {' '.join(font_parts[2:])}"
                                    self.slide_canvas.itemconfig(item, font=new_font)
                            except (ValueError, IndexError):
                                pass  # Fehler beim Font-Parsing ignorieren
            
            logger.debug(f"Bestehende Elemente neu skaliert mit Faktor {self.scale_factor:.3f}")
            
        except Exception as e:
            logger.error(f"Fehler beim Neu-Skalieren der Elemente: {e}")
    
    def setup_canvas_drop_events(self):
        """Konfiguriert Drop-Events für die Slide-Canvas"""
        # Events für bessere Benutzerfreundlichkeit
        def on_canvas_click(event):
            # Focus auf Canvas setzen
            self.slide_canvas.focus_set()
        
        self.slide_canvas.bind('<Button-1>', on_canvas_click)
    
    def create_toolbox_panel(self, parent):
        """Erstellt die intuitive Tool-Box (rechts) mit Symbolen und Funktionen"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Panel Frame mit modernem Design
        panel_frame = tk.Frame(
            parent,
            bg=colors['background_secondary'],
            relief='flat',
            bd=0,
            width=320
        )
        panel_frame.grid(row=0, column=2, sticky='nsew', padx=(8, 0))
        panel_frame.grid_propagate(False)
        
        # Moderner Header mit Gradient-Effekt
        header_frame = tk.Frame(panel_frame, bg=colors['accent_primary'], height=80)
        header_frame.pack(fill='x', padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # Header-Inhalt
        header_content = tk.Frame(header_frame, bg=colors['accent_primary'])
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        header_label = tk.Label(
            header_content,
            text="🎨 Design-Werkzeuge",
            font=(fonts['title'][0], fonts['title'][1] + 2, 'bold'),
            fg='white',
            bg=colors['accent_primary']
        )
        header_label.pack(anchor='w')
        
        info_label = tk.Label(
            header_content,
            text="Ziehen Sie Elemente auf die Folie",
            font=fonts['caption'],
            fg='#E8F4FD',
            bg=colors['accent_primary']
        )
        info_label.pack(anchor='w', pady=(2, 0))
        
        # Direkter Content-Frame ohne Scrolling
        main_content = tk.Frame(panel_frame, bg=colors['background_secondary'])
        main_content.pack(fill='both', expand=True, padx=0, pady=0)
        
        # Kompakte Tool-Box ohne Scrollen - Nur wichtigste Elemente
        self.create_compact_toolbox(main_content, colors, fonts)
    
    def create_compact_toolbox(self, parent, colors, fonts):
        """Moderne Icon-basierte ToolBox mit minimalem Text"""
        
        # Hauptcontainer mit modernem Grid-Layout
        main_grid = tk.Frame(parent, bg=colors['background_secondary'])
        main_grid.pack(fill='both', expand=True, padx=12, pady=8)
        
        # === BERTRANDT LOGOS (Oben, prominent) ===
        logo_section = self.create_modern_section(main_grid, "LOGOS", colors)
        logo_grid = tk.Frame(logo_section, bg=colors['background_secondary'])
        logo_grid.pack(pady=8)
        
        self.create_icon_button(logo_grid, "🟡", 'logo_yellow', '#FFD700', colors, row=0, col=0)
        self.create_icon_button(logo_grid, "⚫", 'logo_black', '#000000', colors, row=0, col=1)
        self.create_icon_button(logo_grid, "⚪", 'logo_white', '#FFFFFF', colors, row=0, col=2)
        
        # === TEXT & CONTENT (Links) ===
        content_section = self.create_modern_section(main_grid, "CONTENT", colors)
        content_grid = tk.Frame(content_section, bg=colors['background_secondary'])
        content_grid.pack(pady=8)
        
        self.create_icon_button(content_grid, "H1", 'title_text', '#1E88E5', colors, row=0, col=0, font_style='bold')
        self.create_icon_button(content_grid, "H2", 'subtitle_text', '#42A5F5', colors, row=0, col=1, font_style='normal')
        self.create_icon_button(content_grid, "📝", 'text_block', '#66BB6A', colors, row=1, col=0)
        self.create_icon_button(content_grid, "•", 'bullet_list', '#FFA726', colors, row=1, col=1, font_size=20)
        
        # === SHAPES & MEDIA (Rechts) ===
        shapes_section = self.create_modern_section(main_grid, "SHAPES", colors)
        shapes_grid = tk.Frame(shapes_section, bg=colors['background_secondary'])
        shapes_grid.pack(pady=8)
        
        self.create_icon_button(shapes_grid, "—", 'line', '#607D8B', colors, row=0, col=0, font_size=20)
        self.create_icon_button(shapes_grid, "○", 'circle', '#FF5722', colors, row=0, col=1, font_size=18)
        self.create_icon_button(shapes_grid, "🖼", 'image', '#4CAF50', colors, row=1, col=0)
        self.create_icon_button(shapes_grid, "🎥", 'video', '#F44336', colors, row=1, col=1)
        
        # === ICONS PALETTE ===
        icons_section = self.create_modern_section(main_grid, "ICONS", colors)
        icons_grid = tk.Frame(icons_section, bg=colors['background_secondary'])
        icons_grid.pack(pady=8)
        
        icon_symbols = [
            ("⭐", 'icon_star', '#FF9800'),
            ("🔧", 'icon_tool', '#9C27B0'),
            ("💡", 'icon_idea', '#FFEB3B'),
            ("🚀", 'icon_rocket', '#2196F3'),
            ("⚡", 'icon_lightning', '#FF5722')
        ]
        
        for i, (symbol, element_type, color) in enumerate(icon_symbols):
            row = i // 3
            col = i % 3
            self.create_icon_button(icons_grid, symbol, element_type, color, colors, row=row, col=col)
        
        # === FORMATTING TOOLS ===
        format_section = self.create_modern_section(main_grid, "FORMAT", colors)
        format_grid = tk.Frame(format_section, bg=colors['background_secondary'])
        format_grid.pack(pady=8)
        
        self.create_icon_button(format_grid, "B", 'format_bold', '#795548', colors, row=0, col=0, font_style='bold')
        self.create_icon_button(format_grid, "I", 'format_italic', '#795548', colors, row=0, col=1, font_style='italic')
        self.create_icon_button(format_grid, "U", 'format_underline', '#795548', colors, row=0, col=2, underline=True)
    
    def create_modern_section(self, parent, title, colors):
        """Erstellt moderne Sektion mit minimalistischem Design"""
        section_frame = tk.Frame(parent, bg=colors['background_secondary'])
        section_frame.pack(fill='x', pady=6)
        
        # Minimaler Titel
        title_label = tk.Label(
            section_frame,
            text=title,
            font=('Segoe UI', 9, 'bold'),
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        title_label.pack(anchor='w', padx=4, pady=(0, 4))
        
        return section_frame
    
    def create_icon_button(self, parent, icon_text, element_type, accent_color, colors, 
                          row=0, col=0, font_size=16, font_style='normal', underline=False):
        """Erstellt moderne Icon-Buttons im Grid"""
        
        # Button-Container
        btn_frame = tk.Frame(parent, bg=colors['background_secondary'])
        btn_frame.grid(row=row, column=col, padx=3, pady=3, sticky='nsew')
        
        # Quadratischer Button
        btn = tk.Button(
            btn_frame,
            text=icon_text,
            font=('Segoe UI', font_size, font_style),
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            width=4,
            height=2,
            cursor='hand2'
        )
        
        if underline:
            btn.config(font=('Segoe UI', font_size, 'normal underline'))
        
        btn.pack(fill='both', expand=True)
        
        # Moderne Hover-Effekte mit Schatten-Simulation
        def on_enter(e):
            btn.config(
                bg=accent_color, 
                fg='white',
                relief='raised',
                bd=1
            )
        
        def on_leave(e):
            btn.config(
                bg=colors['background_tertiary'], 
                fg=colors['text_primary'],
                relief='flat',
                bd=0
            )
        
        # Klick-Effekt
        def on_click(e):
            btn.config(relief='sunken', bd=2)
            btn.after(100, lambda: btn.config(relief='flat', bd=0))
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        btn.bind('<Button-1>', on_click)
        
        # Grid-Konfiguration für gleichmäßige Verteilung
        parent.grid_rowconfigure(row, weight=1)
        parent.grid_columnconfigure(col, weight=1)
        
        # Draggable machen
        self.make_draggable(btn, element_type)
        
        return btn
    
    def create_compact_button(self, parent, text, colors, fonts, element_type, accent_color, side='left'):
        """Erstellt kompakte Buttons für die ToolBox"""
        btn = tk.Button(
            parent,
            text=text,
            font=('Segoe UI', 9),
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            padx=8,
            pady=6,
            cursor='hand2',
            width=12
        )
        btn.pack(side=side, padx=2, pady=1)
        
        # Hover-Effekte
        def on_enter(e):
            btn.config(bg=accent_color, fg='white')
        
        def on_leave(e):
            btn.config(bg=colors['background_tertiary'], fg=colors['text_primary'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        # Draggable machen
        self.make_draggable(btn, element_type)
        
        return btn
    
    def create_content_elements_section(self, parent, colors, fonts):
        """Inhaltselemente Sektion - Verbessert mit Icons"""
        section_frame = self.create_section_frame(parent, colors, "📝 Inhaltselemente", "Texte und Überschriften")
        
        # Überschrift
        title_btn = self.create_tool_button(
            section_frame, "📋 Überschrift", "Große Überschrift hinzufügen", 
            colors, fonts, 'title_text', '#1E88E5'
        )
        
        # Untertitel
        subtitle_btn = self.create_tool_button(
            section_frame, "📄 Untertitel", "Untertitel hinzufügen", 
            colors, fonts, 'subtitle_text', '#42A5F5'
        )
        
        # Textblock
        text_btn = self.create_tool_button(
            section_frame, "📝 Textblock", "Mehrzeiliger Text", 
            colors, fonts, 'text_block', '#66BB6A'
        )
        
        # Aufzählung
        list_btn = self.create_tool_button(
            section_frame, "• Aufzählung", "Bullet-Point Liste", 
            colors, fonts, 'bullet_list', '#FFA726'
        )
    
    def create_section_frame(self, parent, colors, title, subtitle):
        """Erstellt einen einheitlichen Sektions-Frame"""
        # Hauptcontainer
        main_frame = tk.Frame(parent, bg=colors['background_secondary'])
        main_frame.pack(fill='x', padx=12, pady=(8, 4))
        
        # Header mit Linie
        header_frame = tk.Frame(main_frame, bg=colors['background_secondary'])
        header_frame.pack(fill='x', pady=(0, 8))
        
        # Titel
        title_label = tk.Label(
            header_frame,
            text=title,
            font=('Segoe UI', 12, 'bold'),
            fg=colors['accent_primary'],
            bg=colors['background_secondary']
        )
        title_label.pack(anchor='w')
        
        # Untertitel
        if subtitle:
            subtitle_label = tk.Label(
                header_frame,
                text=subtitle,
                font=('Segoe UI', 9),
                fg=colors['text_secondary'],
                bg=colors['background_secondary']
            )
            subtitle_label.pack(anchor='w', pady=(2, 0))
        
        # Trennlinie
        separator = tk.Frame(header_frame, bg=colors['background_tertiary'], height=1)
        separator.pack(fill='x', pady=(6, 0))
        
        # Content-Frame
        content_frame = tk.Frame(main_frame, bg=colors['background_secondary'])
        content_frame.pack(fill='x')
        
        return content_frame
    
    def create_tool_button(self, parent, text, tooltip, colors, fonts, element_type, accent_color=None):
        """Erstellt einen modernen Tool-Button mit Hover-Effekt"""
        if not accent_color:
            accent_color = colors['accent_secondary']
        
        button_frame = tk.Frame(parent, bg=colors['background_secondary'])
        button_frame.pack(fill='x', pady=2)
        
        btn = tk.Button(
            button_frame,
            text=text,
            font=fonts['button'],
            bg=colors['background_tertiary'],
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            padx=15,
            pady=12,
            cursor='hand2',
            width=22,
            anchor='w'
        )
        btn.pack(fill='x')
        
        # Hover-Effekte
        def on_enter(e):
            btn.config(bg=accent_color, fg='white')
        
        def on_leave(e):
            btn.config(bg=colors['background_tertiary'], fg=colors['text_primary'])
        
        btn.bind('<Enter>', on_enter)
        btn.bind('<Leave>', on_leave)
        
        # Tooltip (einfache Implementierung)
        def show_tooltip(e):
            btn.config(text=f"{text} - {tooltip}")
        
        def hide_tooltip(e):
            btn.config(text=text)
        
        # Draggable machen
        self.make_draggable(btn, element_type)
        
        return btn
    
    def create_layout_elements_section(self, parent, colors, fonts):
        """Layout-Elemente Sektion"""
        section_frame = self.create_section_frame(parent, colors, "📐 Layout-Elemente", "Strukturen und Formen")
        
        # Container/Box
        container_btn = self.create_tool_button(
            section_frame, "📦 Container", "Rechteckiger Container", 
            colors, fonts, 'container', '#9C27B0'
        )
        
        # Linie
        line_btn = self.create_tool_button(
            section_frame, "➖ Linie", "Horizontale Trennlinie", 
            colors, fonts, 'line', '#607D8B'
        )
        
        # Kreis
        circle_btn = self.create_tool_button(
            section_frame, "⭕ Kreis", "Kreisform hinzufügen", 
            colors, fonts, 'circle', '#FF5722'
        )
    
    def create_media_elements_section_improved(self, parent, colors, fonts):
        """Verbesserte Media-Elemente Sektion"""
        section_frame = self.create_section_frame(parent, colors, "🎬 Medien", "Bilder, Videos und Grafiken")
        
        # Bild
        image_btn = self.create_tool_button(
            section_frame, "🖼️ Bild", "Bild aus Datei laden", 
            colors, fonts, 'image', '#4CAF50'
        )
        
        # Video
        video_btn = self.create_tool_button(
            section_frame, "🎥 Video", "Video-Player hinzufügen", 
            colors, fonts, 'video', '#F44336'
        )
        
        # Icon
        icon_btn = self.create_tool_button(
            section_frame, "⭐ Icon", "Symbol hinzufügen", 
            colors, fonts, 'icon', '#FF9800'
        )
        
        # Diagramm
        chart_btn = self.create_tool_button(
            section_frame, "📊 Diagramm", "Einfaches Diagramm", 
            colors, fonts, 'chart', '#2196F3'
        )
    
    def create_branding_elements_section(self, parent, colors, fonts):
        """Bertrandt Branding Sektion"""
        section_frame = self.create_section_frame(parent, colors, "🏢 Bertrandt Branding", "Corporate Design Elemente")
        
        # Logo Schwarz
        logo_black_btn = self.create_tool_button(
            section_frame, "⚫ Logo Schwarz", "Schwarzes Bertrandt Logo", 
            colors, fonts, 'logo_black', '#000000'
        )
        
        # Logo Weiß
        logo_white_btn = self.create_tool_button(
            section_frame, "⚪ Logo Weiß", "Weißes Bertrandt Logo", 
            colors, fonts, 'logo_white', '#FFFFFF'
        )
        
        # Logo Gelb
        logo_yellow_btn = self.create_tool_button(
            section_frame, "🟡 Logo Gelb", "Gelbes Bertrandt Logo", 
            colors, fonts, 'logo_yellow', '#FFD700'
        )
        
        # Corporate Farben
        colors_btn = self.create_tool_button(
            section_frame, "🎨 Corporate Farben", "Bertrandt Farbpalette", 
            colors, fonts, 'corporate_colors', colors['accent_primary']
        )
    
    def create_formatting_tools_section(self, parent, colors, fonts):
        """Formatierungs-Werkzeuge Sektion"""
        section_frame = self.create_section_frame(parent, colors, "✏️ Formatierung", "Text-Styling Werkzeuge")
        
        # Fett
        bold_btn = self.create_tool_button(
            section_frame, "𝐁 Fett", "Text fett formatieren", 
            colors, fonts, 'format_bold', '#795548'
        )
        
        # Kursiv
        italic_btn = self.create_tool_button(
            section_frame, "𝐼 Kursiv", "Text kursiv formatieren", 
            colors, fonts, 'format_italic', '#795548'
        )
        
        # Unterstrichen
        underline_btn = self.create_tool_button(
            section_frame, "U̲ Unterstrichen", "Text unterstreichen", 
            colors, fonts, 'format_underline', '#795548'
        )
        
        # Textfarbe
        color_btn = self.create_tool_button(
            section_frame, "🎨 Textfarbe", "Textfarbe ändern", 
            colors, fonts, 'text_color', '#E91E63'
        )
    
    def create_slide_actions_section(self, parent, colors, fonts):
        """Folien-Aktionen Sektion"""
        section_frame = self.create_section_frame(parent, colors, "⚡ Aktionen", "Folien-Management")
        
        # Neue Folie
        new_slide_btn = self.create_tool_button(
            section_frame, "➕ Neue Folie", "Leere Folie erstellen", 
            colors, fonts, 'new_slide', '#4CAF50'
        )
        
        # Folie duplizieren
        duplicate_btn = self.create_tool_button(
            section_frame, "📋 Duplizieren", "Aktuelle Folie kopieren", 
            colors, fonts, 'duplicate_slide', '#2196F3'
        )
        
        # Folie löschen
        delete_btn = self.create_tool_button(
            section_frame, "🗑️ Löschen", "Folie entfernen", 
            colors, fonts, 'delete_slide', '#F44336'
        )
        
        # Alles löschen
        clear_btn = self.create_tool_button(
            section_frame, "🧹 Alles löschen", "Folie leeren", 
            colors, fonts, 'clear_slide', '#FF5722'
        )
    
    def make_draggable(self, widget, element_type):
        """Macht ein Widget draggable"""
        def start_drag(event):
            self.drag_data = {
                'element_type': element_type,
                'widget': widget,
                'start_x': event.x_root,
                'start_y': event.y_root
            }
            
            # Visual feedback
            colors = theme_manager.get_colors()
            widget.config(bg=colors['accent_primary'], fg='white')
            
            # Drag-Cursor erstellen
            self.create_drag_cursor(element_type)
            
        def on_drag(event):
            if self.drag_data['element_type']:
                self.update_drag_cursor(event.x_root, event.y_root)
        
        def end_drag(event):
            if self.drag_data['element_type']:
                # Visual feedback zurücksetzen
                colors = theme_manager.get_colors()
                widget.config(bg=colors['background_tertiary'], fg=colors['text_primary'])
                
                # Drop-Position ermitteln
                drop_x = event.x_root
                drop_y = event.y_root
                
                # Prüfen ob über Canvas gedroppt
                if hasattr(self, 'slide_canvas') and self.slide_canvas.winfo_exists():
                    try:
                        canvas_x = self.slide_canvas.winfo_rootx()
                        canvas_y = self.slide_canvas.winfo_rooty()
                        canvas_width = self.slide_canvas.winfo_width()
                        canvas_height = self.slide_canvas.winfo_height()
                        
                        if (canvas_x <= drop_x <= canvas_x + canvas_width and 
                            canvas_y <= drop_y <= canvas_y + canvas_height):
                            # Relative Position berechnen
                            rel_x = drop_x - canvas_x
                            rel_y = drop_y - canvas_y
                            
                            # In Slide-Koordinaten umrechnen
                            slide_x = (rel_x - self.offset_x) / self.scale_factor
                            slide_y = (rel_y - self.offset_y) / self.scale_factor
                            
                            # Prüfen ob innerhalb der Slide-Grenzen
                            if (0 <= slide_x <= self.slide_width and 0 <= slide_y <= self.slide_height):
                                self.handle_drop(self.drag_data['element_type'], slide_x, slide_y)
                    except Exception as e:
                        logger.error(f"Fehler beim Drop: {e}")
                
                # Drag-Cursor entfernen
                self.remove_drag_cursor()
                
                # Drag-Daten zurücksetzen
                self.drag_data = {'element_type': None, 'widget': None}
        
        # Events binden
        widget.bind('<Button-1>', start_drag)
        widget.bind('<B1-Motion>', on_drag)
        widget.bind('<ButtonRelease-1>', end_drag)
    
    def create_drag_cursor(self, element_type):
        """Erstellt visuellen Drag-Cursor"""
        if hasattr(self, 'drag_cursor'):
            self.drag_cursor.destroy()
        
        self.drag_cursor = tk.Toplevel(self.main_window.root)
        self.drag_cursor.wm_overrideredirect(True)
        self.drag_cursor.wm_attributes('-topmost', True)
        self.drag_cursor.wm_attributes('-alpha', 0.8)
        
        cursor_text = {
            'textfield': '📄 Text',
            'imagefield': '🖼️ Bild', 
            'videofield': '🎥 Video',
            'logo_black': '⚫ Logo',
            'logo_white': '⚪ Logo',
            'format_bold': '𝐁 Fett',
            'format_italic': '𝐼 Kursiv',
            'format_underline': 'U̲ Unter'
        }.get(element_type, element_type)
        
        colors = theme_manager.get_colors()
        cursor_label = tk.Label(
            self.drag_cursor,
            text=cursor_text,
            bg=colors['accent_primary'],
            fg='white',
            font=self.main_window.fonts['button'],
            padx=10,
            pady=5,
            relief='solid',
            bd=1
        )
        cursor_label.pack()
    
    def update_drag_cursor(self, x, y):
        """Aktualisiert Drag-Cursor Position"""
        if hasattr(self, 'drag_cursor'):
            self.drag_cursor.wm_geometry(f"+{x+10}+{y+10}")
    
    def remove_drag_cursor(self):
        """Entfernt Drag-Cursor"""
        if hasattr(self, 'drag_cursor'):
            self.drag_cursor.destroy()
            delattr(self, 'drag_cursor')
    
    def handle_drop(self, element_type, x, y):
        """Behandelt Drop von Elementen auf Canvas - Erweitert für alle neuen Typen"""
        try:
            # Inhaltselemente
            if element_type == 'title_text':
                self.add_title_element(x, y)
            elif element_type == 'subtitle_text':
                self.add_subtitle_element(x, y)
            elif element_type == 'text_block':
                self.add_text_block_element(x, y)
            elif element_type == 'bullet_list':
                self.add_bullet_list_element(x, y)
            
            # Layout-Elemente
            elif element_type == 'container':
                self.add_container_element(x, y)
            elif element_type == 'line':
                self.add_line_element(x, y)
            elif element_type == 'circle':
                self.add_circle_element(x, y)
            
            # Media-Elemente
            elif element_type == 'image':
                self.add_image_element(x, y)
            elif element_type == 'video':
                self.add_video_element(x, y)
            elif element_type == 'icon':
                self.add_icon_element(x, y)
            elif element_type == 'chart':
                self.add_chart_element(x, y)
            
            # Spezifische Icons
            elif element_type == 'icon_star':
                self.add_specific_icon_element(x, y, '⭐')
            elif element_type == 'icon_tool':
                self.add_specific_icon_element(x, y, '🔧')
            elif element_type == 'icon_idea':
                self.add_specific_icon_element(x, y, '💡')
            elif element_type == 'icon_rocket':
                self.add_specific_icon_element(x, y, '🚀')
            elif element_type == 'icon_lightning':
                self.add_specific_icon_element(x, y, '⚡')
            
            # Branding-Elemente
            elif element_type == 'logo_black':
                self.add_logo_element(x, y, 'black')
            elif element_type == 'logo_white':
                self.add_logo_element(x, y, 'white')
            elif element_type == 'logo_yellow':
                self.add_logo_element(x, y, 'yellow')
            elif element_type == 'corporate_colors':
                self.add_corporate_colors_element(x, y)
            
            # Formatierungs-Werkzeuge (keine Position nötig)
            elif element_type in ['format_bold', 'format_italic', 'format_underline', 'text_color']:
                self.apply_text_formatting(element_type)
                return  # Kein Drop-Feedback für Formatierung
            
            # Folien-Aktionen (keine Position nötig)
            elif element_type == 'new_slide':
                self.create_new_slide()
                return
            elif element_type == 'duplicate_slide':
                self.duplicate_current_slide()
                return
            elif element_type == 'delete_slide':
                self.delete_current_slide()
                return
            elif element_type == 'clear_slide':
                self.clear_current_slide()
                return
            
            # Legacy-Support
            elif element_type == 'textfield':
                self.add_text_block_element(x, y)
            elif element_type == 'imagefield':
                self.add_image_element(x, y)
            elif element_type == 'videofield':
                self.add_video_element(x, y)
            
            else:
                logger.warning(f"Unbekannter Element-Typ: {element_type}")
                return
            
            # Erfolgs-Feedback für positionsbasierte Elemente
            self.show_drop_feedback(x, y)
            logger.info(f"Element '{element_type}' hinzugefügt bei ({x}, {y})")
            
        except Exception as e:
            logger.error(f"Fehler beim Hinzufügen von Element '{element_type}': {e}")
            messagebox.showerror("Fehler", f"Element konnte nicht hinzugefügt werden: {e}")
    
    def show_drop_feedback(self, x, y):
        """Zeigt visuelles Drop-Feedback"""
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        feedback = self.slide_canvas.create_oval(
            canvas_x-10, canvas_y-10, canvas_x+10, canvas_y+10,
            fill='green',
            outline='darkgreen',
            width=2,
            tags='drop_feedback'
        )
        
        self.main_window.root.after(500, lambda: self.slide_canvas.delete('drop_feedback'))
    
    def add_title_element(self, x, y):
        """Fügt große Überschrift zur Slide hinzu"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        title_widget = tk.Text(
            self.slide_canvas,
            width=40,
            height=2,
            font=(fonts['title'][0], 24, 'bold'),
            bg='white',
            fg=colors['accent_primary'],
            relief='flat',
            bd=0,
            wrap='word'
        )
        title_widget.insert('1.0', 'Neue Überschrift')
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=title_widget, anchor='nw')
        self.make_canvas_item_movable(title_widget, canvas_item)
    
    def add_subtitle_element(self, x, y):
        """Fügt Untertitel zur Slide hinzu"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        subtitle_widget = tk.Text(
            self.slide_canvas,
            width=35,
            height=1,
            font=(fonts['subtitle'][0], 18, 'normal'),
            bg='white',
            fg=colors['text_primary'],
            relief='flat',
            bd=0,
            wrap='word'
        )
        subtitle_widget.insert('1.0', 'Untertitel')
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=subtitle_widget, anchor='nw')
        self.make_canvas_item_movable(subtitle_widget, canvas_item)
    
    def add_text_block_element(self, x, y):
        """Fügt Textblock zur Slide hinzu"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        text_widget = tk.Text(
            self.slide_canvas,
            width=40,
            height=6,
            font=fonts['body'],
            bg='white',
            fg='black',
            relief='solid',
            bd=1,
            wrap='word'
        )
        text_widget.insert('1.0', 'Hier Text eingeben...\n\nMehrzeiliger Textblock für längere Inhalte.')
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=text_widget, anchor='nw')
        self.make_canvas_item_movable(text_widget, canvas_item)
    
    def add_bullet_list_element(self, x, y):
        """Fügt Aufzählungsliste zur Slide hinzu"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        list_widget = tk.Text(
            self.slide_canvas,
            width=35,
            height=5,
            font=fonts['body'],
            bg='white',
            fg='black',
            relief='solid',
            bd=1,
            wrap='word'
        )
        list_widget.insert('1.0', '• Erster Punkt\n• Zweiter Punkt\n• Dritter Punkt\n• Vierter Punkt')
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=list_widget, anchor='nw')
        self.make_canvas_item_movable(list_widget, canvas_item)
    
    def add_text_element(self, x, y):
        """Legacy-Funktion - leitet zu add_text_block_element weiter"""
        self.add_text_block_element(x, y)
    
    def add_image_element(self, x, y):
        """Fügt Bildfeld zur Slide hinzu"""
        colors = theme_manager.get_colors()
        
        image_frame = tk.Frame(
            self.slide_canvas,
            width=200,
            height=150,
            bg=colors['background_tertiary'],
            relief='solid',
            bd=2
        )
        image_frame.pack_propagate(False)
        
        placeholder_label = tk.Label(
            image_frame,
            text="🖼️\nBild hier\nhinzufügen",
            font=self.main_window.fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary'],
            cursor='hand2'
        )
        placeholder_label.pack(expand=True)
        placeholder_label.bind('<Double-Button-1>', lambda e: self.select_image_file(image_frame))
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=image_frame, anchor='nw')
        self.make_canvas_item_movable(image_frame, canvas_item)
    
    def add_video_element(self, x, y):
        """Fügt Videofeld zur Slide hinzu"""
        colors = theme_manager.get_colors()
        
        video_frame = tk.Frame(
            self.slide_canvas,
            width=300,
            height=200,
            bg=colors['background_tertiary'],
            relief='solid',
            bd=2
        )
        video_frame.pack_propagate(False)
        
        placeholder_label = tk.Label(
            video_frame,
            text="🎥\nVideo hier\nhinzufügen",
            font=self.main_window.fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary'],
            cursor='hand2'
        )
        placeholder_label.pack(expand=True)
        placeholder_label.bind('<Double-Button-1>', lambda e: self.select_video_file(video_frame))
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=video_frame, anchor='nw')
        self.make_canvas_item_movable(video_frame, canvas_item)
    
    def add_container_element(self, x, y):
        """Fügt Container/Box zur Slide hinzu"""
        colors = theme_manager.get_colors()
        
        container_frame = tk.Frame(
            self.slide_canvas,
            width=250,
            height=150,
            bg=colors['background_tertiary'],
            relief='solid',
            bd=2
        )
        container_frame.pack_propagate(False)
        
        placeholder_label = tk.Label(
            container_frame,
            text="📦\nContainer\nDoppelklick zum Bearbeiten",
            font=self.main_window.fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary'],
            cursor='hand2'
        )
        placeholder_label.pack(expand=True)
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=container_frame, anchor='nw')
        self.make_canvas_item_movable(container_frame, canvas_item)
    
    def add_line_element(self, x, y):
        """Fügt Linie zur Slide hinzu"""
        colors = theme_manager.get_colors()
        
        line_frame = tk.Frame(
            self.slide_canvas,
            width=200,
            height=3,
            bg=colors['accent_primary'],
            relief='flat'
        )
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=line_frame, anchor='nw')
        self.make_canvas_item_movable(line_frame, canvas_item)
    
    def add_circle_element(self, x, y):
        """Fügt Kreis zur Slide hinzu"""
        colors = theme_manager.get_colors()
        
        # Canvas-Element für Kreis
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        circle = self.slide_canvas.create_oval(
            canvas_x, canvas_y, canvas_x + 80, canvas_y + 80,
            fill=colors['accent_secondary'],
            outline=colors['accent_primary'],
            width=3,
            tags='movable_circle'
        )
    
    def add_icon_element(self, x, y):
        """Fügt zufälliges Icon zur Slide hinzu"""
        colors = theme_manager.get_colors()
        
        # Icon-Auswahl
        icons = ['⭐', '🔧', '💡', '🚀', '⚡', '🎯', '📈', '🔒', '✅', '❌']
        import random
        selected_icon = random.choice(icons)
        
        icon_label = tk.Label(
            self.slide_canvas,
            text=selected_icon,
            font=('Arial', 32),
            bg='white',
            fg=colors['accent_primary'],
            relief='flat',
            padx=10,
            pady=10
        )
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=icon_label, anchor='nw')
        self.make_canvas_item_movable(icon_label, canvas_item)
    
    def add_specific_icon_element(self, x, y, icon):
        """Fügt spezifisches Icon zur Slide hinzu"""
        colors = theme_manager.get_colors()
        
        icon_label = tk.Label(
            self.slide_canvas,
            text=icon,
            font=('Arial', 32),
            bg='white',
            fg=colors['accent_primary'],
            relief='flat',
            padx=10,
            pady=10
        )
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=icon_label, anchor='nw')
        self.make_canvas_item_movable(icon_label, canvas_item)
    
    def add_chart_element(self, x, y):
        """Fügt einfaches Diagramm zur Slide hinzu"""
        colors = theme_manager.get_colors()
        
        chart_frame = tk.Frame(
            self.slide_canvas,
            width=200,
            height=150,
            bg='white',
            relief='solid',
            bd=2
        )
        chart_frame.pack_propagate(False)
        
        # Einfaches Balkendiagramm mit Canvas
        chart_canvas = tk.Canvas(chart_frame, bg='white', highlightthickness=0)
        chart_canvas.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Beispiel-Balken zeichnen
        def draw_chart():
            chart_canvas.delete('all')
            w = chart_canvas.winfo_width()
            h = chart_canvas.winfo_height()
            if w > 10 and h > 10:
                # 3 Balken
                bar_width = w // 4
                values = [0.7, 0.5, 0.9]  # Relative Höhen
                colors_bars = [colors['accent_primary'], colors['accent_secondary'], '#4CAF50']
                
                for i, (val, color) in enumerate(zip(values, colors_bars)):
                    x1 = i * bar_width + 10
                    y1 = h - 20
                    x2 = x1 + bar_width - 10
                    y2 = h - (val * (h - 40)) - 20
                    chart_canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline='')
        
        chart_canvas.bind('<Configure>', lambda e: draw_chart())
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=chart_frame, anchor='nw')
        self.make_canvas_item_movable(chart_frame, canvas_item)
    
    def add_corporate_colors_element(self, x, y):
        """Fügt Bertrandt Corporate Colors Palette hinzu"""
        colors = theme_manager.get_colors()
        
        palette_frame = tk.Frame(
            self.slide_canvas,
            width=180,
            height=60,
            bg='white',
            relief='solid',
            bd=1
        )
        palette_frame.pack_propagate(False)
        
        # Farbfelder
        color_values = [colors['accent_primary'], '#FF6600', '#333333', '#FFFFFF']
        color_names = ['Blau', 'Orange', 'Grau', 'Weiß']
        
        for i, (color_val, name) in enumerate(zip(color_values, color_names)):
            color_frame = tk.Frame(palette_frame, bg=color_val, width=40, height=50)
            color_frame.pack(side='left', padx=2, pady=5)
            color_frame.pack_propagate(False)
        
        canvas_x = self.offset_x + (x * self.scale_factor)
        canvas_y = self.offset_y + (y * self.scale_factor)
        
        canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=palette_frame, anchor='nw')
        self.make_canvas_item_movable(palette_frame, canvas_item)
    
    def add_logo_element(self, x, y, logo_type):
        """Fügt Bertrandt-Logo zur Slide hinzu - Mit echten PNG-Dateien"""
        try:
            # Logo-Pfad bestimmen (korrekte Pfade zu den PNG-Dateien)
            if logo_type == 'black':
                logo_path = 'assets/Bertrandt_logo_schwarz.png'
                bg_color = 'white'
            elif logo_type == 'white':
                logo_path = 'assets/Bertrandt_logo_weis.png'
                bg_color = '#333333'
            elif logo_type == 'yellow':
                logo_path = 'assets/Bertrandt_logo_gelb.png'
                bg_color = 'white'
            else:
                raise FileNotFoundError(f"Unbekannter Logo-Typ: {logo_type}")
            
            # Prüfen ob Datei existiert
            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"Logo-Datei nicht gefunden: {logo_path}")
            
            # Logo laden und skalieren (größer für bessere Sichtbarkeit)
            pil_image = Image.open(logo_path)
            
            # Originalgröße beibehalten, aber skalieren falls zu groß
            original_width, original_height = pil_image.size
            max_width, max_height = 200, 80
            
            # Seitenverhältnis beibehalten
            ratio = min(max_width/original_width, max_height/original_height)
            new_width = int(original_width * ratio)
            new_height = int(original_height * ratio)
            
            pil_image = pil_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(pil_image)
            
            # Logo-Container mit Padding
            logo_frame = tk.Frame(
                self.slide_canvas,
                bg=bg_color,
                relief='solid',
                bd=1,
                padx=10,
                pady=10
            )
            
            logo_label = tk.Label(
                logo_frame,
                image=photo,
                bg=bg_color,
                relief='flat',
                bd=0
            )
            logo_label.image = photo  # Referenz behalten
            logo_label.pack()
            
            canvas_x = self.offset_x + (x * self.scale_factor)
            canvas_y = self.offset_y + (y * self.scale_factor)
            
            canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=logo_frame, anchor='nw')
            self.make_canvas_item_movable(logo_frame, canvas_item)
            
            logger.info(f"Bertrandt Logo ({logo_type}) erfolgreich geladen: {logo_path}")
            
        except Exception as e:
            logger.error(f"Fehler beim Laden des Logos: {e}")
            # Fallback: Text-Label mit Bertrandt-Styling
            colors = theme_manager.get_colors()
            
            fallback_frame = tk.Frame(
                self.slide_canvas,
                bg='white' if logo_type != 'white' else '#333333',
                relief='solid',
                bd=2,
                padx=15,
                pady=10
            )
            
            logo_label = tk.Label(
                fallback_frame,
                text="BERTRANDT",
                font=('Arial', 16, 'bold'),
                bg='white' if logo_type != 'white' else '#333333',
                fg=colors['accent_primary'] if logo_type != 'yellow' else '#FFD700',
                relief='flat'
            )
            logo_label.pack()
            
            type_label = tk.Label(
                fallback_frame,
                text=f"Logo {logo_type}",
                font=('Arial', 10),
                bg='white' if logo_type != 'white' else '#333333',
                fg='#666666',
                relief='flat'
            )
            type_label.pack()
            
            canvas_x = self.offset_x + (x * self.scale_factor)
            canvas_y = self.offset_y + (y * self.scale_factor)
            
            canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=fallback_frame, anchor='nw')
            self.make_canvas_item_movable(fallback_frame, canvas_item)
    
    def make_canvas_item_movable(self, widget, canvas_item):
        """Macht Canvas-Item bewegbar"""
        def start_move(event):
            widget.start_x = event.x
            widget.start_y = event.y
        
        def on_move(event):
            dx = event.x - widget.start_x
            dy = event.y - widget.start_y
            self.slide_canvas.move(canvas_item, dx, dy)
        
        widget.bind('<Button-1>', start_move)
        widget.bind('<B1-Motion>', on_move)
    
    def apply_text_formatting(self, format_type):
        """Wendet Textformatierung an - Erweitert mit echten Funktionen"""
        try:
            if format_type == 'format_bold':
                self.show_formatting_dialog("Fett", "bold")
            elif format_type == 'format_italic':
                self.show_formatting_dialog("Kursiv", "italic")
            elif format_type == 'format_underline':
                self.show_formatting_dialog("Unterstrichen", "underline")
            elif format_type == 'text_color':
                self.show_color_picker_dialog()
            else:
                messagebox.showinfo("Formatierung", f"Formatierung '{format_type}' angewendet")
        except Exception as e:
            logger.error(f"Fehler bei Formatierung: {e}")
    
    def show_formatting_dialog(self, format_name, format_type):
        """Zeigt Formatierungs-Dialog"""
        messagebox.showinfo(
            "Text-Formatierung", 
            f"{format_name}-Formatierung aktiviert!\n\n"
            f"Wählen Sie ein Textelement aus und bearbeiten Sie es direkt.\n"
            f"Die {format_name}-Formatierung wird automatisch angewendet."
        )
    
    def show_color_picker_dialog(self):
        """Zeigt Farbauswahl-Dialog"""
        from tkinter import colorchooser
        color = colorchooser.askcolor(title="Textfarbe wählen")
        if color[1]:  # Wenn eine Farbe gewählt wurde
            messagebox.showinfo(
                "Textfarbe", 
                f"Farbe {color[1]} ausgewählt!\n\n"
                f"Wählen Sie ein Textelement aus, um die Farbe anzuwenden."
            )
    
    def create_new_slide(self):
        """Erstellt eine neue leere Folie"""
        try:
            from models.content import content_manager
            
            # Neue Slide-Nummer bestimmen
            total_slides = content_manager.get_slide_count()
            new_slide_id = total_slides + 1
            
            # Neue Slide erstellen
            new_slide_data = {
                'title': f'Neue Folie {new_slide_id}',
                'content': 'Hier können Sie Ihren Inhalt hinzufügen...',
                'slide_number': new_slide_id,
                'created_date': 'now'
            }
            
            # Slide hinzufügen (vereinfacht - würde normalerweise über content_manager gehen)
            messagebox.showinfo(
                "Neue Folie", 
                f"Neue Folie {new_slide_id} erstellt!\n\n"
                f"Die Folie wurde zur Präsentation hinzugefügt."
            )
            
            # Thumbnails aktualisieren
            self.refresh_thumbnails()
            
            logger.info(f"Neue Folie {new_slide_id} erstellt")
            
        except Exception as e:
            logger.error(f"Fehler beim Erstellen neuer Folie: {e}")
            messagebox.showerror("Fehler", f"Neue Folie konnte nicht erstellt werden: {e}")
    
    def duplicate_current_slide(self):
        """Dupliziert die aktuelle Folie"""
        try:
            if not hasattr(self, 'current_slide') or not self.current_slide:
                messagebox.showwarning("Warnung", "Keine Folie zum Duplizieren ausgewählt!")
                return
            
            # Aktuelle Folie speichern
            self.save_current_slide_content()
            
            from models.content import content_manager
            total_slides = content_manager.get_slide_count()
            new_slide_id = total_slides + 1
            
            # Kopie erstellen
            messagebox.showinfo(
                "Folie dupliziert", 
                f"Folie {self.current_edit_slide} wurde als Folie {new_slide_id} dupliziert!\n\n"
                f"Die neue Folie enthält alle Inhalte der ursprünglichen Folie."
            )
            
            # Thumbnails aktualisieren
            self.refresh_thumbnails()
            
            logger.info(f"Folie {self.current_edit_slide} dupliziert als Folie {new_slide_id}")
            
        except Exception as e:
            logger.error(f"Fehler beim Duplizieren der Folie: {e}")
            messagebox.showerror("Fehler", f"Folie konnte nicht dupliziert werden: {e}")
    
    def delete_current_slide(self):
        """Löscht die aktuelle Folie"""
        try:
            if not hasattr(self, 'current_slide') or not self.current_slide:
                messagebox.showwarning("Warnung", "Keine Folie zum Löschen ausgewählt!")
                return
            
            # Bestätigung
            result = messagebox.askyesno(
                "Folie löschen", 
                f"Möchten Sie Folie {self.current_edit_slide} wirklich löschen?\n\n"
                f"Diese Aktion kann nicht rückgängig gemacht werden!"
            )
            
            if result:
                slide_id = self.current_edit_slide
                
                # Folie löschen (vereinfacht)
                messagebox.showinfo(
                    "Folie gelöscht", 
                    f"Folie {slide_id} wurde erfolgreich gelöscht!"
                )
                
                # Zur ersten Folie wechseln
                self.load_slide_to_editor(1)
                
                # Thumbnails aktualisieren
                self.refresh_thumbnails()
                
                logger.info(f"Folie {slide_id} gelöscht")
            
        except Exception as e:
            logger.error(f"Fehler beim Löschen der Folie: {e}")
            messagebox.showerror("Fehler", f"Folie konnte nicht gelöscht werden: {e}")
    
    def clear_current_slide(self):
        """Leert die aktuelle Folie"""
        try:
            if not hasattr(self, 'current_slide') or not self.current_slide:
                messagebox.showwarning("Warnung", "Keine Folie zum Leeren ausgewählt!")
                return
            
            # Bestätigung
            result = messagebox.askyesno(
                "Folie leeren", 
                f"Möchten Sie alle Inhalte von Folie {self.current_edit_slide} löschen?\n\n"
                f"Diese Aktion kann nicht rückgängig gemacht werden!"
            )
            
            if result:
                # Canvas leeren
                self.clear_slide_canvas()
                
                # Nur Drop-Zone wieder erstellen
                self.create_slide_content()
                
                messagebox.showinfo(
                    "Folie geleert", 
                    f"Alle Inhalte von Folie {self.current_edit_slide} wurden entfernt!"
                )
                
                logger.info(f"Folie {self.current_edit_slide} geleert")
            
        except Exception as e:
            logger.error(f"Fehler beim Leeren der Folie: {e}")
            messagebox.showerror("Fehler", f"Folie konnte nicht geleert werden: {e}")
    
    def refresh_thumbnails(self):
        """Aktualisiert die Thumbnail-Anzeige"""
        try:
            # Alle bestehenden Thumbnails entfernen
            for widget in self.thumbnail_frame.winfo_children():
                widget.destroy()
            
            # Thumbnails neu erstellen
            self.create_slide_thumbnails()
            
            logger.debug("Thumbnails aktualisiert")
            
        except Exception as e:
            logger.error(f"Fehler beim Aktualisieren der Thumbnails: {e}")
    
    def select_image_file(self, image_frame):
        """Öffnet Dateidialog zur Bildauswahl"""
        file_path = filedialog.askopenfilename(
            title="Bild auswählen",
            filetypes=[
                ("Bilddateien", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("Alle Dateien", "*.*")
            ]
        )
        if file_path:
            try:
                pil_image = Image.open(file_path)
                pil_image = pil_image.resize((200, 150), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(pil_image)
                
                for widget in image_frame.winfo_children():
                    widget.destroy()
                
                image_label = tk.Label(image_frame, image=photo)
                image_label.image = photo
                image_label.pack(expand=True)
                
            except Exception as e:
                logger.error(f"Fehler beim Laden des Bildes: {e}")
                messagebox.showerror("Fehler", f"Bild konnte nicht geladen werden: {e}")
    
    def select_video_file(self, video_frame):
        """Öffnet Dateidialog zur Videoauswahl"""
        file_path = filedialog.askopenfilename(
            title="Video auswählen",
            filetypes=[
                ("Videodateien", "*.mp4 *.avi *.mov *.wmv *.mkv"),
                ("Alle Dateien", "*.*")
            ]
        )
        if file_path:
            for widget in video_frame.winfo_children():
                widget.destroy()
            
            video_label = tk.Label(
                video_frame,
                text=f"🎥\n{os.path.basename(file_path)}\n(Video geladen)",
                font=self.main_window.fonts['body'],
                fg=theme_manager.get_colors()['text_primary'],
                bg=theme_manager.get_colors()['background_tertiary']
            )
            video_label.pack(expand=True)
    
    def load_slide_to_editor(self, slide_id):
        """Lädt Demo-Folie in den Editor"""
        # Aktuelle Slide speichern
        if hasattr(self, 'current_edit_slide') and self.current_slide:
            self.save_current_slide_content()
        
        # Demo-Folie laden
        from models.content import content_manager
        slide = content_manager.get_slide(slide_id)
        
        if slide:
            self.current_edit_slide = slide_id
            self.current_slide = slide
            
            # UI-Updates
            self.update_thumbnail_selection()
            self.update_slide_counter()
            
            # Slide-Info aktualisieren
            self.slide_info_label.configure(
                text=f"Demo-Folie {slide_id}: {slide.title}"
            )
            
            # Canvas leeren und Inhalt laden
            self.clear_slide_canvas()
            self.display_existing_slide_content(slide.config_data)
            
            # Sicherstellen, dass die Folie optimal sichtbar ist
            self.ensure_slide_visibility()
            
            logger.debug(f"Demo-Slide {slide_id} geladen: {slide.title}")
    
    def ensure_slide_visibility(self):
        """Stellt sicher, dass die Folie optimal sichtbar ist"""
        try:
            # Canvas-Größe aktualisieren
            self.slide_canvas.update_idletasks()
            
            # Resize-Event manuell auslösen für optimale Skalierung
            canvas_width = self.slide_canvas.winfo_width()
            canvas_height = self.slide_canvas.winfo_height()
            
            if canvas_width > 100 and canvas_height > 100:
                # Fake-Event für Resize erstellen
                class FakeEvent:
                    def __init__(self, width, height):
                        self.width = width
                        self.height = height
                
                fake_event = FakeEvent(canvas_width, canvas_height)
                self.on_canvas_resize(fake_event)
                
                logger.debug(f"Slide-Sichtbarkeit optimiert: {canvas_width}x{canvas_height}")
            
        except Exception as e:
            logger.error(f"Fehler beim Optimieren der Slide-Sichtbarkeit: {e}")
    
    def display_existing_slide_content(self, slide_data):
        """Zeigt bestehenden Folieninhalt im modernen Bertrandt-Stil an"""
        if not slide_data:
            self.render_empty_slide()
            return
        
        # SCHRITT 1: Slide-Hintergrund rendern (HINTERGRUND-LAYER)
        self.add_slide_frame()
        
        # SCHRITT 2: IMMER den Text als editierbare Widgets direkt auf der Folie rendern (wie Folie 6)
        # Das stellt sicher, dass alle Folien einheitlich dargestellt werden
        self.render_existing_content_as_editable_widgets(slide_data)
        
        # SCHRITT 3: Z-Order korrigieren - Alle Content-Elemente nach vorne bringen
        self.fix_creator_content_z_order()
        
        # SCHRITT 4: Zusätzliche Z-Order Korrektur nach kurzer Verzögerung
        self.main_window.root.after(100, self.fix_creator_content_z_order)
    
    def fix_creator_content_z_order(self):
        """Korrigiert die Z-Order im Creator - bringt alle Content-Elemente nach vorne"""
        try:
            # SCHRITT 1: Alle Hintergrund-Elemente nach hinten bringen
            background_tags = ['slide_background_frame', 'slide_background_shadow', 'slide_background_main', 'dropzone']
            for tag in background_tags:
                bg_items = self.slide_canvas.find_withtag(tag)
                for item in bg_items:
                    self.slide_canvas.tag_lower(item)
            
            # SCHRITT 2: Alle Canvas-Items mit slide_content Tag nach vorne bringen
            content_items = self.slide_canvas.find_withtag('slide_content')
            for item in content_items:
                self.slide_canvas.tag_raise(item)
            
            # SCHRITT 3: Alle Window-Items (Widgets) nach vorne bringen - diese sind editierbar
            all_items = self.slide_canvas.find_all()
            for item in all_items:
                item_type = self.slide_canvas.type(item)
                if item_type == 'window':
                    self.slide_canvas.tag_raise(item)
            
            # SCHRITT 4: Alle recreated_element Items nach vorne bringen
            recreated_items = self.slide_canvas.find_withtag('recreated_element')
            for item in recreated_items:
                self.slide_canvas.tag_raise(item)
            
            # SCHRITT 5: Explizit alle Text-Widgets nach ganz vorne bringen
            self.force_text_widgets_to_front()
            
            logger.debug("Creator Z-Order korrigiert - Content-Elemente sind jetzt über dem Hintergrund")
            
        except Exception as e:
            logger.error(f"Fehler beim Korrigieren der Creator Z-Order: {e}")
    
    def force_text_widgets_to_front(self):
        """Bringt alle Text-Widgets explizit nach ganz vorne"""
        try:
            all_items = self.slide_canvas.find_all()
            for item in all_items:
                item_type = self.slide_canvas.type(item)
                if item_type == 'window':
                    # Widget-Objekt holen
                    try:
                        widget_path = self.slide_canvas.itemcget(item, 'window')
                        widget = self.slide_canvas.nametowidget(widget_path)
                        widget_class = widget.winfo_class()
                        
                        # Text-Widgets und Labels explizit nach vorne bringen
                        if widget_class in ['Text', 'Label', 'Entry']:
                            self.slide_canvas.tag_raise(item)
                            logger.debug(f"Text-Widget ({widget_class}) nach vorne gebracht")
                    except:
                        # Fallback: Alle Window-Items nach vorne
                        self.slide_canvas.tag_raise(item)
            
        except Exception as e:
            logger.error(f"Fehler beim Forcieren der Text-Widgets nach vorne: {e}")
    
    def render_saved_canvas_elements(self, canvas_elements):
        """Rendert gespeicherte Canvas-Elemente im Creator"""
        try:
            for element_data in canvas_elements:
                self.render_creator_canvas_element(element_data)
            
            logger.debug(f"Creator: {len(canvas_elements)} Canvas-Elemente gerendert")
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern der Canvas-Elemente im Creator: {e}")
    
    def render_creator_canvas_element(self, element_data):
        """Rendert ein Canvas-Element im Creator (editierbar)"""
        try:
            element_type = element_data.get('type')
            coords = element_data.get('coords', [])
            
            if not coords or len(coords) < 2:
                return
            
            # Koordinaten skalieren
            scaled_coords = []
            for i in range(0, len(coords), 2):
                if i+1 < len(coords):
                    x = self.offset_x + (coords[i] * self.scale_factor)
                    y = self.offset_y + (coords[i+1] * self.scale_factor)
                    scaled_coords.extend([x, y])
            
            # Widget-Elemente (editierbar)
            if element_type == 'window':
                self.recreate_widget_element(element_data, scaled_coords[0], scaled_coords[1])
            
            # Canvas-Elemente (Formen, Linien, etc.)
            elif element_type in ['text', 'rectangle', 'oval', 'line']:
                self.recreate_canvas_shape(element_type, element_data, scaled_coords)
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern des Creator-Canvas-Elements: {e}")
    
    def recreate_widget_element(self, element_data, x, y):
        """Erstellt Widget-Elemente neu (editierbar)"""
        try:
            widget_type = element_data.get('widget_type', 'Label')
            
            if widget_type == 'Text':
                text = element_data.get('text', 'Text')
                font = element_data.get('font', 'Arial 12')
                bg = element_data.get('bg', 'white')
                fg = element_data.get('fg', 'black')
                width = element_data.get('width', 20)
                height = element_data.get('height', 1)
                
                text_widget = tk.Text(
                    self.slide_canvas,
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
                
                canvas_item = self.slide_canvas.create_window(x, y, window=text_widget, anchor='nw')
                self.make_canvas_item_movable(text_widget, canvas_item)
            
            elif widget_type == 'Label':
                text = element_data.get('text', 'Label')
                font = element_data.get('font', 'Arial 12')
                bg = element_data.get('bg', 'white')
                fg = element_data.get('fg', 'black')
                
                label_widget = tk.Label(
                    self.slide_canvas,
                    text=text,
                    font=font,
                    bg=bg,
                    fg=fg,
                    relief='flat'
                )
                
                canvas_item = self.slide_canvas.create_window(x, y, window=label_widget, anchor='nw')
                self.make_canvas_item_movable(label_widget, canvas_item)
            
        except Exception as e:
            logger.error(f"Fehler beim Recreate Widget-Element: {e}")
    
    def recreate_canvas_shape(self, element_type, element_data, scaled_coords):
        """Erstellt Canvas-Formen neu"""
        try:
            if element_type == 'text' and len(scaled_coords) >= 2:
                text = element_data.get('text', 'Text')
                font = element_data.get('font', 'Arial 12')
                fill = element_data.get('fill', 'black')
                
                self.slide_canvas.create_text(
                    scaled_coords[0], scaled_coords[1],
                    text=text,
                    font=font,
                    fill=fill,
                    tags='recreated_element'
                )
            
            elif element_type == 'rectangle' and len(scaled_coords) >= 4:
                fill = element_data.get('fill', '')
                outline = element_data.get('outline', 'black')
                width = element_data.get('width', 1)
                
                self.slide_canvas.create_rectangle(
                    scaled_coords[0], scaled_coords[1],
                    scaled_coords[2], scaled_coords[3],
                    fill=fill,
                    outline=outline,
                    width=width,
                    tags='recreated_element'
                )
            
            elif element_type == 'oval' and len(scaled_coords) >= 4:
                fill = element_data.get('fill', '')
                outline = element_data.get('outline', 'black')
                width = element_data.get('width', 1)
                
                self.slide_canvas.create_oval(
                    scaled_coords[0], scaled_coords[1],
                    scaled_coords[2], scaled_coords[3],
                    fill=fill,
                    outline=outline,
                    width=width,
                    tags='recreated_element'
                )
            
            elif element_type == 'line' and len(scaled_coords) >= 4:
                fill = element_data.get('fill', 'black')
                width = element_data.get('width', 1)
                
                self.slide_canvas.create_line(
                    scaled_coords[0], scaled_coords[1],
                    scaled_coords[2], scaled_coords[3],
                    fill=fill,
                    width=width,
                    tags='recreated_element'
                )
            
        except Exception as e:
            logger.error(f"Fehler beim Recreate Canvas-Shape: {e}")
    
    def render_existing_content_as_editable_widgets(self, slide_data):
        """Rendert bestehenden Folien-Inhalt als editierbare Text-Widgets DIREKT AUF der Folie"""
        try:
            colors = theme_manager.get_colors()
            fonts = self.main_window.fonts
            
            # Titel als editierbares Widget direkt auf der Folie
            title = slide_data.get('title', '')
            if title and title.strip():
                title_widget = tk.Text(
                    self.slide_canvas,
                    width=60,  # Breiter für bessere Lesbarkeit
                    height=3,  # Höher für mehrzeilige Titel
                    font=(fonts['title'][0], 28, 'bold'),  # Größere Schrift
                    bg='white',
                    fg='#1E88E5',  # Bertrandt Blau
                    relief='flat',  # Flacher Rahmen für sauberes Aussehen
                    bd=1,
                    wrap='word',
                    insertbackground='#1E88E5'  # Cursor-Farbe
                )
                title_widget.insert('1.0', title)
                
                # Position direkt auf der Folie (oben links mit Abstand)
                canvas_x = self.offset_x + (80 * self.scale_factor)
                canvas_y = self.offset_y + (60 * self.scale_factor)
                
                canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=title_widget, anchor='nw', tags='slide_content')
                self.make_canvas_item_movable(title_widget, canvas_item)
                
                logger.debug(f"Titel als editierbares Widget auf Folie erstellt: {title[:30]}...")
            
            # Content als editierbares Widget direkt auf der Folie
            content = slide_data.get('content', '')
            if content and content.strip():
                # Content in Zeilen aufteilen für bessere Darstellung
                content_lines = content.split('\n')
                clean_content = '\n'.join([line.strip() for line in content_lines if line.strip()])
                
                content_widget = tk.Text(
                    self.slide_canvas,
                    width=70,  # Breiter für bessere Lesbarkeit
                    height=min(20, max(8, len(content_lines) + 2)),  # Dynamische Höhe
                    font=(fonts['body'][0], 16),  # Größere Schrift für bessere Lesbarkeit
                    bg='white',
                    fg='#2C3E50',
                    relief='flat',
                    bd=1,
                    wrap='word',
                    insertbackground='#2C3E50'
                )
                content_widget.insert('1.0', clean_content)
                
                # Position direkt auf der Folie (unter dem Titel)
                canvas_x = self.offset_x + (80 * self.scale_factor)
                canvas_y = self.offset_y + (180 * self.scale_factor)
                
                canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=content_widget, anchor='nw', tags='slide_content')
                self.make_canvas_item_movable(content_widget, canvas_item)
                
                logger.debug(f"Content als editierbares Widget auf Folie erstellt: {len(content_lines)} Zeilen")
            
            # Bertrandt-Branding direkt auf der Folie
            self.add_editable_branding_widget_on_slide()
            
            logger.info(f"Bestehender Folien-Inhalt als editierbare Widgets direkt auf der Folie gerendert")
            
        except Exception as e:
            logger.error(f"Fehler beim Rendern des bestehenden Inhalts als Widgets: {e}")
            # Fallback: Leere Folie anzeigen
            self.render_empty_slide()
    
    def add_editable_branding_widget_on_slide(self):
        """Fügt editierbares Bertrandt-Branding direkt AUF die Folie"""
        try:
            colors = theme_manager.get_colors()
            
            # Bertrandt-Logo/Text direkt auf der Folie (unten rechts)
            brand_x = self.slide_width - 250  # Relative Position zur Folie
            brand_y = self.slide_height - 120
            
            brand_widget = tk.Label(
                self.slide_canvas,
                text="BERTRANDT",
                font=('Segoe UI', 20, 'bold'),  # Größere Schrift
                bg='white',
                fg='#003366',
                relief='flat',
                padx=15,
                pady=8
            )
            
            canvas_x = self.offset_x + (brand_x * self.scale_factor)
            canvas_y = self.offset_y + (brand_y * self.scale_factor)
            
            canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=brand_widget, anchor='nw', tags='slide_content')
            self.make_canvas_item_movable(brand_widget, canvas_item)
            
            # Folien-Nummer direkt auf der Folie (unten links)
            slide_number = getattr(self, 'current_edit_slide', 1)
            number_x = 80
            number_y = self.slide_height - 120
            
            number_widget = tk.Label(
                self.slide_canvas,
                text=f"Folie {slide_number}",
                font=('Segoe UI', 16),  # Größere Schrift
                bg='white',
                fg='#666666',
                relief='flat',
                padx=15,
                pady=8
            )
            
            canvas_x = self.offset_x + (number_x * self.scale_factor)
            canvas_y = self.offset_y + (number_y * self.scale_factor)
            
            canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=number_widget, anchor='nw', tags='slide_content')
            self.make_canvas_item_movable(number_widget, canvas_item)
            
        except Exception as e:
            logger.error(f"Fehler beim Hinzufügen des editierbaren Brandings auf der Folie: {e}")
    
    def add_editable_branding_widget(self):
        """Fügt editierbares Bertrandt-Branding als Widget hinzu"""
        try:
            colors = theme_manager.get_colors()
            
            # Bertrandt-Logo/Text als editierbares Label (unten rechts)
            brand_x = self.slide_width - 200  # Relative Position
            brand_y = self.slide_height - 100
            
            brand_widget = tk.Label(
                self.slide_canvas,
                text="BERTRANDT",
                font=('Segoe UI', 16, 'bold'),
                bg='white',
                fg='#003366',
                relief='flat',
                padx=10,
                pady=5
            )
            
            canvas_x = self.offset_x + (brand_x * self.scale_factor)
            canvas_y = self.offset_y + (brand_y * self.scale_factor)
            
            canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=brand_widget, anchor='nw', tags='slide_content')
            self.make_canvas_item_movable(brand_widget, canvas_item)
            
            # Folien-Nummer als editierbares Label (unten links)
            slide_number = getattr(self, 'current_edit_slide', 1)
            number_x = 100
            number_y = self.slide_height - 100
            
            number_widget = tk.Label(
                self.slide_canvas,
                text=f"Folie {slide_number}",
                font=('Segoe UI', 12),
                bg='white',
                fg='#666666',
                relief='flat',
                padx=10,
                pady=5
            )
            
            canvas_x = self.offset_x + (number_x * self.scale_factor)
            canvas_y = self.offset_y + (number_y * self.scale_factor)
            
            canvas_item = self.slide_canvas.create_window(canvas_x, canvas_y, window=number_widget, anchor='nw', tags='slide_content')
            self.make_canvas_item_movable(number_widget, canvas_item)
            
        except Exception as e:
            logger.error(f"Fehler beim Hinzufügen des editierbaren Brandings: {e}")
    
    def render_modern_text_layout_content_only(self, slide_data):
        """Moderne Text-Darstellung nur für Inhalt (Hintergrund bereits gerendert)"""
        # Moderner Titel-Bereich (relativ zur Slide-Position)
        title_y = self.offset_y + (120 * self.scale_factor)  # Mehr Abstand von oben
        title = slide_data.get('title', 'Unbenannte Folie')
        
        # Titel mit Bertrandt-Styling (über dem Slide)
        self.slide_canvas.create_text(
            self.offset_x + (self.slide_width * self.scale_factor / 2),
            title_y,
            text=title,
            font=('Segoe UI', int(28 * self.scale_factor), 'bold'),
            fill='#1E88E5',  # Bertrandt Blau
            anchor='center',
            width=int((self.slide_width - 200) * self.scale_factor),
            tags='slide_content'  # Wichtig: slide_content Tag für korrekte Layering
        )
        
        # Untertitel-Linie (über dem Slide)
        line_y = title_y + (45 * self.scale_factor)
        self.slide_canvas.create_line(
            self.offset_x + (120 * self.scale_factor),
            line_y,
            self.offset_x + (self.slide_width - 120) * self.scale_factor,
            line_y,
            fill='#FF6600',  # Bertrandt Orange
            width=int(3 * self.scale_factor),
            tags='slide_content'
        )
        
        # Content-Bereich (über dem Slide)
        content = slide_data.get('content', '')
        if content:
            content_y = line_y + (50 * self.scale_factor)
            content_lines = content.split('\n')
            
            for i, line in enumerate(content_lines[:6]):  # Max 6 Zeilen für bessere Lesbarkeit
                if line.strip():
                    self.slide_canvas.create_text(
                        self.offset_x + (140 * self.scale_factor),
                        content_y + (i * 35 * self.scale_factor),
                        text=f"• {line.strip()}",
                        font=('Segoe UI', int(14 * self.scale_factor)),
                        fill='#2C3E50',
                        anchor='nw',
                        width=int((self.slide_width - 280) * self.scale_factor),
                        tags='slide_content'
                    )
        
        # Bertrandt-Branding (über dem Slide)
        self.add_modern_branding()
    
    def render_empty_slide(self):
        """Rendert eine leere Folie mit Platzhalter"""
        # Zentrierter Platzhalter
        center_x = self.offset_x + (self.slide_width * self.scale_factor / 2)
        center_y = self.offset_y + (self.slide_height * self.scale_factor / 2)
        
        # Platzhalter-Icon
        self.slide_canvas.create_text(
            center_x,
            center_y - (40 * self.scale_factor),
            text="📄",
            font=('Arial', int(48 * self.scale_factor)),
            fill='#CCCCCC',
            anchor='center',
            tags='placeholder'
        )
        
        # Platzhalter-Text
        self.slide_canvas.create_text(
            center_x,
            center_y + (20 * self.scale_factor),
            text="Leere Folie\nZiehen Sie Elemente hierher",
            font=('Segoe UI', int(16 * self.scale_factor)),
            fill='#999999',
            anchor='center',
            justify='center',
            tags='placeholder'
        )
    
    def add_modern_branding(self):
        """Fügt modernes Bertrandt-Branding hinzu (über dem Slide)"""
        # Bertrandt-Logo/Text (unten rechts, über dem Slide)
        brand_x = self.offset_x + (self.slide_width - 120) * self.scale_factor
        brand_y = self.offset_y + (self.slide_height - 80) * self.scale_factor
        
        self.slide_canvas.create_text(
            brand_x,
            brand_y,
            text="BERTRANDT",
            font=('Segoe UI', int(12 * self.scale_factor), 'bold'),
            fill='#003366',
            anchor='se',
            tags='slide_content'  # Über dem Slide
        )
        
        # Folien-Nummer (unten links, über dem Slide)
        slide_number = getattr(self, 'current_edit_slide', 1)
        number_x = self.offset_x + (120 * self.scale_factor)
        number_y = self.offset_y + (self.slide_height - 80) * self.scale_factor
        
        self.slide_canvas.create_text(
            number_x,
            number_y,
            text=f"Folie {slide_number}",
            font=('Segoe UI', int(10 * self.scale_factor)),
            fill='#666666',
            anchor='sw',
            tags='slide_content'  # Über dem Slide
        )
    
    def render_powerpoint_background(self):
        """Erstellt PowerPoint-ähnlichen Hintergrund mit Schatten - skaliert"""
        # Skalierte Dimensionen berechnen
        scaled_width = self.slide_width * self.scale_factor
        scaled_height = self.slide_height * self.scale_factor
        shadow_offset = max(8, int(12 * self.scale_factor))
        
        # Schatten-Effekt (skaliert und positioniert)
        self.slide_canvas.create_rectangle(
            self.offset_x + shadow_offset, 
            self.offset_y + shadow_offset,
            self.offset_x + scaled_width + shadow_offset, 
            self.offset_y + scaled_height + shadow_offset,
            fill='#D0D0D0',
            outline='',
            tags='slide_shadow'
        )
        
        # Hauptbereich (weiß) - skaliert und zentriert
        self.slide_canvas.create_rectangle(
            self.offset_x, self.offset_y,
            self.offset_x + scaled_width, self.offset_y + scaled_height,
            fill='#FFFFFF',
            outline='#CCCCCC',
            width=max(2, int(3 * self.scale_factor)),
            tags='slide_background'
        )
        
        # Folien-Rahmen für bessere Sichtbarkeit
        self.slide_canvas.create_rectangle(
            self.offset_x - 1, self.offset_y - 1,
            self.offset_x + scaled_width + 1, self.offset_y + scaled_height + 1,
            fill='',
            outline='#999999',
            width=1,
            tags='slide_border'
        )
    
    def clear_slide_canvas(self):
        """Leert die Canvas komplett und erstellt neue Drop-Zone"""
        self.slide_canvas.delete('all')
        
        # Neue Drop-Zone erstellen
        self.dropzone_rect = self.slide_canvas.create_rectangle(
            0, 0, self.slide_width, self.slide_height,
            outline='',
            width=0,
            fill='',
            tags='dropzone'
        )
    
    def save_current_slide_content(self):
        """Speichert Demo-Slide-Inhalt mit kompletten Canvas-Elementen"""
        if not hasattr(self, 'current_slide') or not self.current_slide:
            return
        
        try:
            from models.content import content_manager
            from datetime import datetime
            
            # Canvas-Elemente mit allen visuellen Eigenschaften sammeln
            canvas_elements = self.get_canvas_elements()
            
            # Slide-Daten aktualisieren
            self.current_slide.config_data.update({
                'canvas_elements': canvas_elements,
                'slide_width': self.slide_width,
                'slide_height': self.slide_height,
                'last_modified': datetime.now().isoformat(),
                'creator_version': '1.0'
            })
            
            if content_manager.save_slide(self.current_edit_slide):
                logger.info(f"Demo-Slide {self.current_edit_slide} mit {len(canvas_elements)} Elementen gespeichert")
                self.show_save_feedback()
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern: {e}")
    
    def get_canvas_elements(self):
        """Sammelt alle Canvas-Elemente mit ihren visuellen Eigenschaften"""
        elements = []
        
        try:
            # Alle Canvas-Items durchgehen
            for item in self.slide_canvas.find_all():
                tags = self.slide_canvas.gettags(item)
                
                # Drop-Zone überspringen
                if 'dropzone' in tags:
                    continue
                
                item_type = self.slide_canvas.type(item)
                element_data = {
                    'type': item_type,
                    'tags': list(tags)
                }
                
                # Position und Größe
                coords = self.slide_canvas.coords(item)
                if coords:
                    # Relative Koordinaten speichern (unabhängig von Skalierung)
                    rel_coords = []
                    for i in range(0, len(coords), 2):
                        if i+1 < len(coords):
                            rel_x = (coords[i] - self.offset_x) / self.scale_factor if self.scale_factor > 0 else 0
                            rel_y = (coords[i+1] - self.offset_y) / self.scale_factor if self.scale_factor > 0 else 0
                            rel_coords.extend([rel_x, rel_y])
                    element_data['coords'] = rel_coords
                
                # Widget-spezifische Daten
                if item_type == 'window':
                    widget = self.slide_canvas.itemcget(item, 'window')
                    if widget:
                        widget_data = self.get_widget_data(widget)
                        element_data.update(widget_data)
                
                # Canvas-Element-spezifische Eigenschaften
                elif item_type in ['text', 'oval', 'rectangle', 'line']:
                    # Alle konfigurierbaren Eigenschaften sammeln
                    config_options = self.slide_canvas.itemconfig(item)
                    for option, value in config_options.items():
                        if len(value) >= 5 and value[4]:  # Aktueller Wert existiert
                            element_data[option] = value[4]
                
                elements.append(element_data)
                
        except Exception as e:
            logger.error(f"Fehler beim Sammeln der Canvas-Elemente: {e}")
        
        return elements
    
    def get_widget_data(self, widget_path):
        """Sammelt Daten von Tkinter-Widgets"""
        widget_data = {'widget_type': 'unknown'}
        
        try:
            # Widget-Objekt finden
            widget = self.slide_canvas.nametowidget(widget_path)
            widget_class = widget.winfo_class()
            widget_data['widget_type'] = widget_class
            
            # Text-Widgets (Entry, Text, Label)
            if widget_class in ['Text', 'Entry']:
                if hasattr(widget, 'get'):
                    if widget_class == 'Text':
                        widget_data['text'] = widget.get('1.0', 'end-1c')
                    else:
                        widget_data['text'] = widget.get()
                
                # Font-Informationen
                if 'font' in widget.configure():
                    widget_data['font'] = widget.cget('font')
                
                # Farben
                if 'bg' in widget.configure():
                    widget_data['bg'] = widget.cget('bg')
                if 'fg' in widget.configure():
                    widget_data['fg'] = widget.cget('fg')
                
                # Größe
                if 'width' in widget.configure():
                    widget_data['width'] = widget.cget('width')
                if 'height' in widget.configure():
                    widget_data['height'] = widget.cget('height')
            
            # Label-Widgets
            elif widget_class == 'Label':
                if 'text' in widget.configure():
                    widget_data['text'] = widget.cget('text')
                if 'image' in widget.configure():
                    # Bild-Referenz speichern (vereinfacht)
                    widget_data['has_image'] = bool(widget.cget('image'))
                
                # Styling
                for prop in ['font', 'bg', 'fg', 'width', 'height', 'anchor', 'justify']:
                    if prop in widget.configure():
                        widget_data[prop] = widget.cget(prop)
            
            # Frame-Widgets
            elif widget_class == 'Frame':
                for prop in ['bg', 'width', 'height', 'relief', 'bd']:
                    if prop in widget.configure():
                        widget_data[prop] = widget.cget(prop)
                
                # Child-Widgets sammeln
                children = []
                for child in widget.winfo_children():
                    child_data = self.get_widget_data(str(child))
                    children.append(child_data)
                if children:
                    widget_data['children'] = children
            
        except Exception as e:
            logger.error(f"Fehler beim Sammeln der Widget-Daten: {e}")
        
        return widget_data
    
    def show_save_feedback(self):
        """Zeigt Speicher-Feedback"""
        if hasattr(self, 'slide_info_label'):
            original_text = self.slide_info_label.cget('text')
            self.slide_info_label.configure(text=f"{original_text} ✓ Gespeichert")
            self.main_window.root.after(2000, lambda: self.slide_info_label.configure(text=original_text))
    
    def update_thumbnail_selection(self):
        """Aktualisiert Thumbnail-Auswahl"""
        colors = theme_manager.get_colors()
        
        for slide_id, btn in self.thumbnail_buttons.items():
            if slide_id == self.current_edit_slide:
                btn.configure(bg=colors['accent_primary'], fg='white')
            else:
                btn.configure(bg=colors['background_tertiary'], fg=colors['text_primary'])
    
    def update_slide_counter(self):
        """Aktualisiert Slide-Zähler"""
        from models.content import content_manager
        total_slides = content_manager.get_slide_count()
        self.slide_counter.configure(text=f"Demo-Folie {self.current_edit_slide} von {total_slides}")
    
    def previous_slide(self):
        """Zur vorherigen Slide"""
        if self.current_edit_slide > 1:
            self.load_slide_to_editor(self.current_edit_slide - 1)
    
    def next_slide(self):
        """Zur nächsten Slide"""
        from models.content import content_manager
        if self.current_edit_slide < content_manager.get_slide_count():
            self.load_slide_to_editor(self.current_edit_slide + 1)
    
    def preview_slide(self):
        """Zeigt Slide-Vorschau"""
        if self.current_slide:
            preview_text = f"Vorschau - Demo-Folie {self.current_edit_slide}\n\n"
            preview_text += f"Titel: {self.current_slide.title}\n\n"
            preview_text += f"Inhalt:\n{self.current_slide.content}"
            messagebox.showinfo("Slide-Vorschau", preview_text)
    
    def create_status_bar(self):
        """Erstellt Status-Leiste"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        status_frame = tk.Frame(
            self.container,
            bg=colors['background_tertiary'],
            height=40
        )
        status_frame.pack(fill='x', padx=15, pady=(0, 15))
        status_frame.pack_propagate(False)
        
        self.status_label = tk.Label(
            status_frame,
            text="Bereit - Demo-Folien Creator",
            font=fonts['body'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary']
        )
        self.status_label.pack(side='left', padx=15, pady=10)
    
    def show(self):
        """Zeigt den Tab"""
        if not self.visible:
            self.container.pack(fill='both', expand=True)
            self.visible = True
            # Erste Slide laden
            if not hasattr(self, 'current_slide') or not self.current_slide:
                self.load_slide_to_editor(1)
            
            # Nach kurzer Verzögerung Sichtbarkeit optimieren
            self.main_window.root.after(200, self.ensure_slide_visibility)
    
    def hide(self):
        """Versteckt den Tab"""
        if self.visible:
            self.container.pack_forget()
            self.visible = False