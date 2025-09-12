#!/usr/bin/env python3
"""
Demo Tab для Dynamic Messe Stand V4
Автоматичне відтворення презентацій з синхронізацією з Creator
"""

import tkinter as tk
from tkinter import ttk
from core.theme import theme_manager
from core.logger import logger
from models.content import content_manager
from ui.components.slide_renderer import SlideRenderer

class DemoTab:
    """Demo Tab для автоматичного відтворення презентацій"""
    
    def __init__(self, parent, main_window):
        self.parent = parent
        self.main_window = main_window
        self.current_slide = 1
        self.total_slides = 10
        self.is_running = False
        self.slide_duration = 5000  # мілісекунди
        self.demo_timer = None
        
        # Підписка на зміни контенту
        content_manager.add_observer(self.on_content_changed)
        
        self.create_demo_content()
    
    def create_demo_content(self):
        """Створює контент Demo Tab"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        # Головний контейнер
        self.container = tk.Frame(self.parent, bg=colors['background_primary'])
        
        # Header з контролами
        self.create_demo_header()
        
        # Головна область презентації
        self.create_presentation_area()
        
        # Навігація та контроли
        self.create_navigation_controls()
        
        # Sidebar зі списком слайдів
        self.create_slides_sidebar()
        
        # Завантажити поточний слайд
        self.load_current_slide()
    
    def create_demo_header(self):
        """Створює header з контролами демо"""
        colors = theme_manager.get_colors()
        fonts = self.main_window.fonts
        
        header_frame = tk.Frame(
            self.container,
            bg=colors['background_secondary'],
            height=70
        )
        header_frame.pack(fill='x', padx=10, pady=(10, 5))
        header_frame.pack_propagate(False)
        
        # Ліва частина - заголовок
        left_frame = tk.Frame(header_frame, bg=colors['background_secondary'])
        left_frame.pack(side='left', fill='y', padx=15)
        
        title_label = tk.Label(
            left_frame,
            text="📽️ BumbleB Story Demo",
            font=fonts['title'],
            fg=colors['text_primary'],
            bg=colors['background_secondary']
        )
        title_label.pack(anchor='w', pady=(10, 0))
        
        subtitle_label = tk.Label(
            left_frame,
            text="Automatische Präsentation",
            font=fonts['caption'],
            fg=colors['text_secondary'],
            bg=colors['background_secondary']
        )
        subtitle_label.pack(anchor='w')
        
        # Права частина - контроли
        right_frame = tk.Frame(header_frame, bg=colors['background_secondary'])
        right_frame.pack(side='right', fill='y', padx=15)
        
        # Demo контроли
        controls_
