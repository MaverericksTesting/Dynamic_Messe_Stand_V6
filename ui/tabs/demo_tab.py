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
        """Erstellt die detaillierte Slide-Inhalts-Anzeige"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        # Clear existing content
        for widget in self.slide_frame.winfo_children():
            widget.destroy()
        
        # Slide-Titel-Bereich mit Theme-Spacing
        title_area = tk.Frame(self.slide_frame, bg=colors['background_secondary'])
        title_area.pack(fill='x', padx=spacing['xl'], pady=(spacing['xl'], spacing['lg']))
        
        self.slide_title_display = tk.Label(
            title_area,
            text="BumbleB - Das automatisierte Shuttle",
            font=fonts['display'],
            fg=colors['accent_primary'],  # Theme-konform: Bertrandt Blue
            bg=colors['background_secondary'],
            justify='left'
        )
        self.slide_title_display.pack(anchor='w')
        
        # Trennlinie mit Theme-Spacing
        separator = tk.Frame(title_area, bg=colors['accent_secondary'], height=4)  # Theme-konform: Bertrandt Orange
        separator.pack(fill='x', pady=(spacing['sm'], 0))
        
        # Slide-Content-Bereich mit Theme-Spacing
        content_area = tk.Frame(self.slide_frame, bg=colors['background_secondary'])
        content_area.pack(fill='both', expand=True, padx=spacing['xl'], pady=(spacing['lg'], spacing['xl']))
        
        # Scrollbarer Text-Bereich
        text_frame = tk.Frame(content_area, bg=colors['background_secondary'])
        text_frame.pack(fill='both', expand=True)
        
        text_scrollbar = tk.Scrollbar(text_frame, bg=colors['background_tertiary'])
        text_scrollbar.pack(side='right', fill='y')
        
        self.slide_content_display = tk.Text(
            text_frame,
            font=fonts['body'],
            bg=colors['background_secondary'],
            fg=colors['text_primary'],
            wrap='word',
            relief='flat',
            bd=0,
            state='disabled',
            yscrollcommand=text_scrollbar.set,
            insertbackground=colors['text_primary']
        )
        self.slide_content_display.pack(side='left', fill='both', expand=True)
        text_scrollbar.config(command=self.slide_content_display.yview)
        
        # Layout-Info (unten)
        layout_info = tk.Frame(self.slide_frame, bg=colors['background_tertiary'])
        layout_info.pack(fill='x', side='bottom')
        
        self.layout_indicator = tk.Label(
            layout_info,
            text="Layout: Text",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_tertiary']
        )
        self.layout_indicator.pack(side='left', padx=spacing['sm'], pady=spacing['xxs'])
        
        # Lade aktuelle Slide (nach vollständiger Initialisierung)
        # self.update_slide_display(1) - wird später aufgerufen
    
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
        """Aktualisiert die Slide-Anzeige mit komplettem Inhalt"""
        slide = content_manager.get_slide(slide_id)
        
        if slide:
            # Titel aktualisieren (falls vorhanden)
            if hasattr(self, 'current_slide_info'):
                self.current_slide_info.configure(text=f"Folie {slide_id}: {slide.title}")
            
            if hasattr(self, 'slide_title_display'):
                self.slide_title_display.configure(text=slide.title)
            
            # Content aktualisieren (falls vorhanden)
            if hasattr(self, 'slide_content_display'):
                self.slide_content_display.configure(state='normal')
                self.slide_content_display.delete('1.0', tk.END)
                self.slide_content_display.insert('1.0', slide.content)
                self.slide_content_display.configure(state='disabled')
            
            # Layout-Info aktualisieren (falls vorhanden)
            if hasattr(self, 'layout_indicator'):
                self.layout_indicator.configure(text=f"Layout: {slide.layout}")
            
            # Slide-Zähler aktualisieren (falls vorhanden)
            if hasattr(self, 'slide_counter'):
                self.slide_counter.configure(text=f"{slide_id}/10")
            
            if hasattr(self, 'current_slide_display'):
                self.current_slide_display.configure(text=f"{slide_id} / 10")
            
            # Thumbnail-Auswahl aktualisieren (falls vorhanden)
            if hasattr(self, 'demo_thumbnail_buttons'):
                self.update_demo_thumbnail_selection(slide_id)
    
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