#!/usr/bin/env python3
"""
Header Component für Dynamic Messe Stand V4
Navigation und Branding
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from core.theme import theme_manager, THEME_VARS, _mix
from core.logger import logger

class HeaderComponent(ttk.Frame):
    """Header-Komponente mit Navigation und Branding"""
    
    def __init__(self, parent, main_window):
        super().__init__(parent, style='Secondary.TFrame')
        self.main_window = main_window
        self.active_tab = "home"
        
        self.setup_header()
    
    def setup_header(self):
        """Erstellt den Header-Bereich - Bertrandt Dark Theme Style"""
        # Verwende theme_manager für konsistente Farben
        colors = theme_manager.get_colors()
        spacing = theme_manager.get_spacing()
        
        # Header-Höhe
        header_height = 70
        self.configure(height=header_height)
        
        # Grid-Konfiguration
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Logo-Bereich (links) - Bertrandt Style
        self.logo_frame = tk.Frame(self, bg=colors['background_secondary'])
        self.logo_frame.grid(row=0, column=0, sticky='nsw', padx=spacing['xl'], pady=spacing['md'])
        
        self.setup_logo()
        
        # Navigation (Mitte) - Bertrandt Style
        self.nav_frame = tk.Frame(self, bg=colors['background_secondary'])
        self.nav_frame.grid(row=0, column=1, sticky='nsew', pady=spacing['md'])
        
        self.setup_navigation()
        
        # Info-Bereich (rechts) - Bertrandt Style
        self.info_frame = tk.Frame(self, bg=colors['background_secondary'])
        self.info_frame.grid(row=0, column=2, sticky='nse', padx=spacing['xl'], pady=spacing['md'])
        
        self.setup_info_area()
    
    def setup_logo(self):
        """Erstellt den Logo-Bereich mit Theme-System"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        # Logo laden
        logo_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'Bertrandt_logo.svg.png')
        
        if os.path.exists(logo_path):
            try:
                # Logo laden und skalieren - Breite wie Status-Panel, Format 2560×265
                logo_width = int(300 * self.main_window.scale_factor)
                # Höhe basierend auf 2560×265 Verhältnis: 300 * (265/2560) = ~31px
                logo_height = int(logo_width * (265/2560))
                
                image = Image.open(logo_path)
                image = image.resize((logo_width, logo_height), Image.Resampling.LANCZOS)
                self.logo_image = ImageTk.PhotoImage(image)
                
                logo_label = tk.Label(
                    self.logo_frame,
                    image=self.logo_image,
                    bg=colors['background_secondary']
                )
                logo_label.pack(side='left', padx=(0, spacing['md']))
                
                # Logo erfolgreich geladen - Flag setzen
                self.logo_loaded = True
                logger.info("Bertrandt Logo erfolgreich geladen")
                
            except Exception as e:
                logger.warning(f"Logo konnte nicht geladen werden: {e}")
                self.logo_loaded = False
        else:
            logger.warning(f"Logo-Datei nicht gefunden: {logo_path}")
            self.logo_loaded = False
        
        # Titel (nur wenn Logo nicht geladen wurde)
        if not getattr(self, 'logo_loaded', False):
            title_label = tk.Label(
                self.logo_frame,
                text="Dynamic Messe Stand V4",
                font=fonts['title'],
                fg=colors['text_primary'],
                bg=colors['background_secondary']
            )
            title_label.pack(side='left')
    
    def create_text_logo(self):
        """Erstellt ein Text-basiertes Logo als Fallback mit Theme-System"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        logo_label = tk.Label(
            self.logo_frame,
            text="B",
            font=('Helvetica Neue', int(32 * self.main_window.scale_factor), 'bold'),
            fg='white',
            bg=colors['bertrandt_blue'],
            width=2,
            height=1
        )
        logo_label.pack(side='left', padx=(0, spacing['md']))
    
    def setup_navigation(self):
        """Erstellt die Navigation - moderne Button-Leiste mit Theme-System"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        radius = theme_manager.get_radius()
        
        # Navigation mit Bertrandt Glass-Container
        colors = theme_manager.get_colors()
        spacing = theme_manager.get_spacing()
        
        nav_container = tk.Frame(
            self.nav_frame, 
            bg=colors['background_tertiary'],  # Bertrandt Glass-Effekt
            relief='flat',
            bd=1,
            highlightbackground=colors['border_medium'],
            highlightthickness=1
        )
        nav_container.pack(expand=True, fill='both', padx=spacing['xl'], pady=spacing['md'])
        
        # Tab-Definitionen mit professionellen Piktogrammen
        self.tabs = [
            {'id': 'home', 'text': 'START', 'icon': '■', 'desc': 'Hauptmenü'},
            {'id': 'demo', 'text': 'DEMO', 'icon': '▶', 'desc': 'Auto-Präsentation'},
            {'id': 'creator', 'text': 'BEARBEITEN', 'icon': '✎', 'desc': 'Folien editieren'},
            {'id': 'presentation', 'text': 'PRÄSENTATION', 'icon': '▦', 'desc': 'Manuelle Steuerung'}
        ]
        
        self.nav_buttons = {}
        
        # Buttons mit Theme-konformem Spacing
        spacing = theme_manager.get_spacing()
        for i, tab in enumerate(self.tabs):
            btn = self.create_nav_button(nav_container, tab)
            btn.pack(side='left', expand=True, fill='both', 
                    padx=spacing['sm'], pady=spacing['sm'])  # Theme-konformes Spacing
            self.nav_buttons[tab['id']] = btn
    
    def create_nav_button(self, parent, tab_info):
        """Erstellt einen Navigation-Button im Bertrandt Dark Theme Style"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        spacing = theme_manager.get_spacing()
        
        # Button-Frame mit Bertrandt Style
        btn_frame = tk.Frame(parent, bg=colors['background_tertiary'])
        
        # Bertrandt Button-Design
        is_active = tab_info['id'] == self.active_tab
        
        if is_active:
            bg_color = colors['accent_primary']  # Bertrandt Blau für aktiven Tab
            fg_color = colors['text_on_accent']
        else:
            bg_color = colors['background_tertiary']  # Panel-Farbe für inaktive Tabs
            fg_color = colors['text_primary']
        
        # Bertrandt Navigation Button
        button = tk.Button(
            btn_frame,
            text=f"{tab_info['icon']}\n{tab_info['text']}",
            font=fonts['nav'],
            bg=bg_color,
            fg=fg_color,
            relief='flat',
            bd=0,
            padx=spacing['xl'],      # Theme-konformes Padding
            pady=spacing['md'],      # Theme-konformes Padding
            cursor='hand2',
            command=lambda: self.main_window.switch_tab(tab_info['id']),
            activebackground=colors['background_hover'],  # Theme-konformer Hover
            activeforeground=colors['text_primary'],
            highlightthickness=0,
            borderwidth=0
        )
        
        # Moderne Hover-Effekte mit sanften Übergängen
        def on_enter(e):
            if tab_info['id'] != self.active_tab:
                button.configure(
                    bg=colors['background_hover'],
                    relief='flat'
                )
        
        def on_leave(e):
            if tab_info['id'] != self.active_tab:
                button.configure(
                    bg=colors['background_secondary'],
                    relief='flat'
                )
        
        # Klick-Effekt
        def on_click(e):
            button.configure(relief='sunken')
            button.after(100, lambda: button.configure(relief='flat'))
        
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        button.bind('<Button-1>', on_click)
        button.pack(fill='both', expand=True)
        
        return btn_frame
    
    def setup_info_area(self):
        """Erstellt den Info-Bereich"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Status-Indikator
        status_frame = tk.Frame(self.info_frame, bg=colors['background_secondary'])
        status_frame.pack(side='right')
        
        # Verbindungsstatus
        self.status_indicator = tk.Label(
            status_frame,
            text="🔴 Offline",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        self.status_indicator.pack(side='top')
        
        # Zeit/Datum (optional)
        import datetime
        time_label = tk.Label(
            status_frame,
            text=datetime.datetime.now().strftime("%H:%M"),
            font=fonts['caption'],
            fg=colors['text_tertiary'],
            bg=colors['background_secondary']
        )
        time_label.pack(side='top')
    
    def update_active_tab(self, tab_id):
        """Aktualisiert die aktive Tab-Anzeige mit sanften Übergängen"""
        if tab_id == self.active_tab:
            return
        
        colors = theme_manager.get_colors()
        
        # Alten Tab deaktivieren mit Animation
        if self.active_tab in self.nav_buttons:
            old_btn = self.nav_buttons[self.active_tab].winfo_children()[0]
            old_btn.configure(
                bg=colors['background_secondary'],
                fg=colors['text_primary'],
                relief='flat'
            )
        
        # Neuen Tab aktivieren mit Highlight
        if tab_id in self.nav_buttons:
            new_btn = self.nav_buttons[tab_id].winfo_children()[0]
            new_btn.configure(
                bg=colors['accent_primary'],
                fg='white',
                relief='flat'
            )
            
            # Kurzer Highlight-Effekt
            def highlight():
                new_btn.configure(bg=colors['accent_secondary'])
                new_btn.after(150, lambda: new_btn.configure(bg=colors['accent_primary']))
            
            new_btn.after(50, highlight)
        
        self.active_tab = tab_id
        logger.debug(f"Header-Navigation aktualisiert: {tab_id}")
    
    def update_status(self, status_text, status_color="🔴"):
        """Aktualisiert den Status-Indikator"""
        self.status_indicator.configure(text=f"{status_color} {status_text}")