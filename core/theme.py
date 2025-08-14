# bertrandt_dark_theme.py
# Bertrandt "Liquid Glass" — Dark Mode (ttk/Tkinter)
# Hinweis: Tkinter unterstützt kein echtes Blur; wir nähern Glasmorphismus über Layer/Abstufungen.

import tkinter as tk
from tkinter import ttk

# =============================
# Zentrales Theme-Definition
# -> Diese Werte kann eine KI dynamisch anpassen (siehe set_theme_vars)
# =============================
THEME_VARS = {
    # Brand Blau - Exakt nach Bertrandt Referenz
    "brand_700": "#0b5ea8",
    "brand_600": "#146ec6", 
    "brand_500": "#1b7fe3",
    "brand_400": "#4e9ef0",

    # Dark-Neutrals - Exakt nach Bertrandt Referenz
    "bg":        "#0e1116",  # App-Hintergrund
    "panel":     "#0f141b",  # Paneel (Cards/Nav)
    "panel_2":   "#131a22",  # leichte Absetzung (Glas-Fake)
    "text":      "#e9edf2",  # Haupttext
    "muted":     "#a5b0bf",  # Gedämpfter Text
    "border":    "#1e2632",  # Rahmen

    # Effekte - Exakt nach Bertrandt Referenz
    "elev_outline": "#223041",   # Erhöhte Elemente Rand
    "elev_fill":    "#111821",   # Erhöhte Elemente Füllung

    # Radii/Abstände - Nach Bertrandt Referenz
    "radius": 16,        # Eckenradius
    "pad": 12,           # Innenabstand

    # Typografie - Nach Bertrandt Referenz
    "font_family": "Segoe UI",
    "size_body": 10,
    "size_h1": 18,
    "size_h2": 14,

    # Fokus-Ring - Nach Bertrandt Referenz
    "ring": "#1b7fe340",  # Ring mit 40 Alpha
}

def set_theme_vars(**overrides):
    """
    Werte im THEME_VARS-Dict live überschreiben.
    Beispiel: set_theme_vars(brand_600="#1a6ee0")
    Danach apply_bertrandt_dark_theme(root, reapply=True) aufrufen.
    """
    THEME_VARS.update(overrides)

def _mix(c1, c2, t=0.5):
    """Einfache Farbinterpolation (hex -> hex)."""
    def hex_to_rgb(h): return tuple(int(h[i:i+2], 16) for i in (1,3,5))
    def rgb_to_hex(r,g,b): return f"#{r:02x}{g:02x}{b:02x}"
    r1,g1,b1 = hex_to_rgb(c1); r2,g2,b2 = hex_to_rgb(c2)
    r = int(r1 + (r2 - r1) * t)
    g = int(g1 + (g2 - g1) * t)
    b = int(b1 + (b2 - b1) * t)
    return rgb_to_hex(r,g,b)

def apply_bertrandt_dark_theme(root: tk.Tk, reapply: bool=False):
    """
    Wendet das Bertrandt-Dark-Theme auf ttk an.
    - Setzt Grundfarben
    - Erstellt Stile: TFrame/TLabel/TButton/TCheckbutton/TEntry/TProgressbar
    - Fügt 'glass' Varianten hinzu (…Glass)
    """
    # Grund-Setup
    root.configure(bg=THEME_VARS["bg"])
    root.option_add("*Font", (THEME_VARS["font_family"], THEME_VARS["size_body"]))
    style = ttk.Style()

    # Auf plattformübergreifendes Theme gehen
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    # Farb-Shortcuts
    BG      = THEME_VARS["bg"]
    PANEL   = THEME_VARS["panel"]
    PANEL2  = THEME_VARS["panel_2"]
    TEXT    = THEME_VARS["text"]
    MUTED   = THEME_VARS["muted"]
    BORDER  = THEME_VARS["border"]
    BRAND   = THEME_VARS["brand_600"]
    BRAND_H = THEME_VARS["brand_400"]  # Hover

    # -------------------------
    # Allgemeine Widget-Defaults
    # -------------------------
    # Frames
    style.configure("TFrame", background=BG, borderwidth=0)
    # "Glass"-Frame (Panel-Look)
    style.configure(
        "Glass.TFrame",
        background=PANEL,
        bordercolor=THEME_VARS["elev_outline"],
        lightcolor=PANEL2,
        darkcolor=PANEL,
        relief="flat",
        borderwidth=1
    )

    # Labels
    style.configure("TLabel", background=BG, foreground=TEXT)
    style.configure("Muted.TLabel", foreground=MUTED, background=BG)
    style.configure("H1.TLabel", background=BG, foreground=TEXT, font=(THEME_VARS["font_family"], THEME_VARS["size_h1"], "bold"))
    style.configure("H2.TLabel", background=BG, foreground=TEXT, font=(THEME_VARS["font_family"], THEME_VARS["size_h2"], "bold"))

    # Buttons
    # Ghost-Button (Rahmen)
    style.configure(
        "Ghost.TButton",
        background=_mix(PANEL, BG, 0.5),
        foreground=TEXT,
        bordercolor=BORDER,
        focusthickness=2,
        focustcolor=THEME_VARS["ring"],
        padding=(12, 8),
        relief="flat"
    )
    style.map(
        "Ghost.TButton",
        background=[("active", _mix(PANEL, BRAND, 0.1))],
        bordercolor=[("active", _mix(BORDER, BRAND, 0.2))]
    )

    # Solid-Primary
    style.configure(
        "Primary.TButton",
        background=BRAND,
        foreground="#ffffff",
        bordercolor=_mix(BRAND, "#000000", 0.3),
        padding=(12, 8),
        relief="flat"
    )
    style.map(
        "Primary.TButton",
        background=[("active", BRAND_H)],
        foreground=[("disabled", _mix("#ffffff", "#888888", 0.6))],
    )

    # Glass-Button (transluzent simuliert)
    style.configure(
        "Glass.TButton",
        background=_mix(PANEL, "#ffffff", 0.06),
        foreground=TEXT,
        bordercolor=_mix(BORDER, "#ffffff", 0.2),
        padding=(12, 8),
        relief="flat"
    )
    style.map(
        "Glass.TButton",
        background=[("active", _mix(PANEL, BRAND, 0.15))]
    )

    # Entry
    style.configure(
        "TEntry",
        fieldbackground=_mix(PANEL, "#000000", 0.0),
        background=_mix(PANEL, "#000000", 0.0),
        foreground=TEXT,
        bordercolor=BORDER,
        lightcolor=_mix(BORDER, "#ffffff", 0.1),
        darkcolor=_mix(BORDER, "#000000", 0.2),
        padding=8,
        relief="flat"
    )

    # Checkbutton / Radiobutton
    style.configure("TCheckbutton", background=BG, foreground=TEXT)
    style.configure("TRadiobutton", background=BG, foreground=TEXT)

    # Progressbar
    style.configure(
        "Glass.Horizontal.TProgressbar",
        background=_mix(BRAND, BRAND_H, 0.5),
        troughcolor=_mix(PANEL, BG, 0.3),
        bordercolor=BORDER,
        lightcolor=BRAND,
        darkcolor=BRAND_H,
        thickness=8
    )

    # Notebook (Tabs)
    style.configure(
        "TNotebook",
        background=BG,
        borderwidth=0
    )
    style.configure(
        "TNotebook.Tab",
        background=_mix(PANEL, BG, 0.4),
        foreground=TEXT,
        bordercolor=BORDER,
        padding=(12, 8)
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", PANEL2), ("active", _mix(PANEL, BRAND, 0.12))],
        foreground=[("selected", TEXT)]
    )

    # Separators
    style.configure("TSeparator", background=BORDER)

    # Hilfsfunktionen für „Cards“ (Glass-Panels) ohne echtes Rounded-Corners
    # -> Wir liefern eine einfache Card-Factory mit Canvas-Hintergrund.
    def make_glass_card(parent, padding=THEME_VARS["pad"]):
        """
        Gibt ein Frame zurück, das optisch einer 'glass' Card ähnelt:
        - Canvas als Hintergrundfläche
        - Innenliegendes Frame (ttk.Frame, Style=Glass.TFrame) für Inhalte
        """
        outer = ttk.Frame(parent, style="TFrame")
        # Hintergrund-Layer
        cv = tk.Canvas(outer, bg=BG, highlightthickness=0, bd=0, height=1)  # Höhe wird via bind angepasst
        cv.grid(row=0, column=0, sticky="nsew")
        outer.grid_rowconfigure(0, weight=1)
        outer.grid_columnconfigure(0, weight=1)

        inner = ttk.Frame(outer, style="Glass.TFrame", padding=padding)
        inner.place(relx=0, rely=0, relwidth=1, relheight=1)

        # softer „Schein“ durch dünne Linie
        def _redraw(_evt=None):
            cv.delete("all")
            w = outer.winfo_width()
            h = outer.winfo_height()
            if w < 2 or h < 2: return
            # simulierte Kontur
            cv.create_rectangle(
                1, 1, w-2, h-2,
                outline=THEME_VARS["elev_outline"],
                width=1
            )
            # leichte Innenfläche („Glas“)
            cv.create_rectangle(
                2, 2, w-3, h-3,
                outline="",
                fill=_mix(PANEL, "#ffffff", 0.04)
            )
        outer.bind("<Configure>", _redraw)
        return outer, inner

    # Füge Fabrik an das Style-Objekt an, damit Apps sie ohne Import-Kollision nutzen können
    style._bertrandt_make_glass_card = make_glass_card

    # -------------------------
    # Demo (optional)
    # -------------------------
    if not reapply and getattr(root, "_bertrandt_demo_injected", False) is False:
        root._bertrandt_demo_injected = True
        _inject_demo_ui(root, style)

def _inject_demo_ui(root, style: ttk.Style):
    root.title("Bertrandt – Liquid Glass (Dark)")
    root.geometry("1050x700")
    root.minsize(900, 600)

    # NAVBAR (Glass)
    nav = ttk.Frame(root, style="Glass.TFrame", padding=(12, 10))
    nav.pack(side="top", fill="x", padx=14, pady=12)

    left = ttk.Frame(nav, style="TFrame")
    left.pack(side="left")
    badge = tk.Canvas(left, width=28, height=28, bg=THEME_VARS["panel"], highlightthickness=0)
    badge.pack(side="left", padx=(0, 10))
    # Badge Verlauf faken
    badge.create_rectangle(2, 2, 26, 26, outline="", fill=_mix(THEME_VARS["brand_600"], THEME_VARS["brand_500"], 0.5))
    ttk.Label(left, text="Bertrandt Interface", style="H2.TLabel").pack(side="left")

    right = ttk.Frame(nav, style="TFrame")
    right.pack(side="right")
    ttk.Button(right, text="Aktion", style="Ghost.TButton", command=lambda: _toast(root, "Aktion ausgeführt")).pack(side="left", padx=6)
    ttk.Button(right, text="Primär", style="Primary.TButton", command=lambda: _toast(root, "Primäraktion")).pack(side="left", padx=6)

    # HERO
    hero_outer, hero = style._bertrandt_make_glass_card(root, padding=16)
    hero_outer.pack(fill="x", padx=14, pady=(0, 12))
    eyebrow = ttk.Label(hero, text="Technischer Überblick", foreground=_mix(THEME_VARS["brand_600"], "#9cc7fb", 0.5))
    eyebrow.pack(anchor="w")
    ttk.Label(hero, text="Liquid-Glass UI im Bertrandt-Stil", style="H1.TLabel").pack(anchor="w", pady=(4, 4))
    ttk.Label(hero, text="Klare Hierarchien, ruhige Flächen, präzise Blau-Akzente. Optimiert für Touch & Desktop.", style="Muted.TLabel", wraplength=900, justify="left").pack(anchor="w")

    # GRID 3 Spalten
    grid = ttk.Frame(root, style="TFrame")
    grid.pack(fill="both", expand=True, padx=14, pady=12)
    grid.columnconfigure((0,1,2), weight=1)
    grid.rowconfigure((0,1), weight=1)

    # Card 1: Status
    c1_outer, c1 = style._bertrandt_make_glass_card(grid, padding=14)
    c1_outer.grid(row=0, column=0, sticky="nsew", padx=6, pady=6)
    ttk.Label(c1, text="Status", style="H2.TLabel").pack(anchor="w")
    ttk.Label(c1, text="Systemauslastung", style="Muted.TLabel").pack(anchor="w")
    pb = ttk.Progressbar(c1, style="Glass.Horizontal.TProgressbar", length=220, mode="determinate")
    pb["value"] = 72
    pb.pack(anchor="w", pady=6)
    btnrow = ttk.Frame(c1, style="TFrame")
    btnrow.pack(anchor="w", pady=(8, 0))
    ttk.Button(btnrow, text="Details", style="Glass.TButton", command=lambda: _toast(root, "Details geöffnet")).pack(side="left", padx=(0, 8))
    ttk.Button(btnrow, text="Starten", style="Primary.TButton", command=lambda: _toast(root, "Aktion gestartet")).pack(side="left")

    # Card 2: Module
    c2_outer, c2 = style._bertrandt_make_glass_card(grid, padding=14)
    c2_outer.grid(row=0, column=1, sticky="nsew", padx=6, pady=6)
    ttk.Label(c2, text="Module", style="H2.TLabel").pack(anchor="w")
    ttk.Label(c2, text="3 aktive • 1 Update", style="Muted.TLabel").pack(anchor="w")
    # „Liste“
    for txt in ("Sensorik – aktiv", "UI-Engine – aktiv", "Netzwerk – aktiv", "Firmware – Update verfügbar"):
        ttk.Label(c2, text="• " + txt).pack(anchor="w", pady=2)

    # Card 3: Verbindungen
    c3_outer, c3 = style._bertrandt_make_glass_card(grid, padding=14)
    c3_outer.grid(row=0, column=2, sticky="nsew", padx=6, pady=6)
    ttk.Label(c3, text="Verbindungen", style="H2.TLabel").pack(anchor="w")
    ttk.Label(c3, text="Sichere Kanäle", style="Muted.TLabel").pack(anchor="w")
    pb2 = ttk.Progressbar(c3, style="Glass.Horizontal.TProgressbar", length=220, mode="determinate")
    pb2["value"] = 88
    pb2.pack(anchor="w", pady=6)
    ttk.Label(c3, text="TLS aktiv, Latenz stabil.", style="TLabel").pack(anchor="w")

    # Card 4: Timeline (breit)
    c4_outer, c4 = style._bertrandt_make_glass_card(grid, padding=14)
    c4_outer.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=6, pady=6)
    ttk.Label(c4, text="Timeline", style="H2.TLabel").pack(anchor="w")
    ttk.Label(c4, text="Letzte Ereignisse", style="Muted.TLabel").pack(anchor="w")
    for txt in ("12:10 – Build erfolgreich", "12:02 – Telemetrie synchronisiert", "11:41 – Firmware geladen"):
        ttk.Label(c4, text="• " + txt).pack(anchor="w", pady=2)

    # Card 5: Quick-Actions
    c5_outer, c5 = style._bertrandt_make_glass_card(grid, padding=14)
    c5_outer.grid(row=1, column=2, sticky="nsew", padx=6, pady=6)
    ttk.Label(c5, text="Quick-Actions", style="H2.TLabel").pack(anchor="w")
    ttk.Label(c5, text="Schnellzugriffe", style="Muted.TLabel").pack(anchor="w")
    row = ttk.Frame(c5, style="TFrame")
    row.pack(anchor="w", pady=6)
    ttk.Button(row, text="Neu verbinden", style="Glass.TButton", command=lambda: _toast(root, "Neu verbunden")).pack(side="left", padx=(0, 8))
    ttk.Button(row, text="Export", style="Glass.TButton", command=lambda: _toast(root, "Export erstellt")).pack(side="left", padx=(0, 8))
    ttk.Button(row, text="Deploy", style="Primary.TButton", command=lambda: _toast(root, "Deploy gestartet")).pack(side="left")

    # Footer
    footer = ttk.Frame(root, style="TFrame")
    footer.pack(side="bottom", fill="x", padx=14, pady=(0, 14))
    ttk.Separator(footer).pack(fill="x", pady=6)
    ttk.Label(footer, text="© Bertrandt • UI-Beispiel „Liquid Glass“", style="Muted.TLabel").pack()

def _toast(root, msg: str, ms=1400):
    # sehr simpler Toast (TopLevel halbtransparent)
    t = tk.Toplevel(root)
    t.overrideredirect(True)
    t.attributes("-topmost", True)
    try:
        t.attributes("-alpha", 0.96)
    except tk.TclError:
        pass
    # Positionieren
    w, h = 260, 44
    rx = root.winfo_rootx()
    ry = root.winfo_rooty()
    rw = root.winfo_width()
    rh = root.winfo_height()
    x = rx + rw//2 - w//2
    y = ry + rh - h - 40
    t.geometry(f"{w}x{h}+{x}+{y}")
    frame = ttk.Frame(t, style="Glass.TFrame", padding=(12, 8))
    frame.pack(fill="both", expand=True)
    ttk.Label(frame, text=msg).pack()
    t.after(ms, t.destroy)

# ThemeManager Klasse für Kompatibilität
class ThemeManager:
    """Verwaltet das Bertrandt Dark Theme"""
    
    def __init__(self):
        self.dark_mode = True   # Nur Dark Mode verfügbar
        self.setup_themes()
    
    def setup_themes(self):
        """Initialisiert das Bertrandt Dark Theme"""
        # Konvertiere THEME_VARS zu unserem Format für Kompatibilität
        self.dark_theme = {
            # Brand Colors
            'brand_700': THEME_VARS["brand_700"],
            'brand_600': THEME_VARS["brand_600"],
            'brand_500': THEME_VARS["brand_500"],
            'brand_400': THEME_VARS["brand_400"],

            # Backgrounds
            'background_primary': THEME_VARS["bg"],
            'background_secondary': THEME_VARS["panel"],
            'background_tertiary': THEME_VARS["panel_2"],
            'background_hover': _mix(THEME_VARS["panel"], THEME_VARS["brand_600"], 0.1),
            'background_accent': THEME_VARS["brand_600"],

            # Text
            'text_primary': THEME_VARS["text"],
            'text_secondary': THEME_VARS["muted"],
            'text_tertiary': _mix(THEME_VARS["muted"], THEME_VARS["bg"], 0.5),
            'text_on_accent': '#ffffff',

            # Accents
            'accent_primary': THEME_VARS["brand_600"],
            'accent_secondary': THEME_VARS["brand_500"],
            'accent_tertiary': THEME_VARS["brand_400"],
            'accent_warning': '#ff9f0a',
            'accent_destructive': '#ff453a',
            'accent_success': '#30d158',

            # Borders
            'border_light': THEME_VARS["border"],
            'border_medium': THEME_VARS["elev_outline"],
            'border_accent': THEME_VARS["brand_600"],

            # Glass Effects (simuliert für Tkinter)
            'glass_bg': THEME_VARS["panel_2"],
            'glass_border': THEME_VARS["elev_outline"],
            'glass_highlight': _mix(THEME_VARS["panel"], "#ffffff", 0.08),
            'glass_shadow_light': THEME_VARS["elev_fill"],
            'glass_shadow_medium': _mix(THEME_VARS["elev_fill"], "#000000", 0.3),
            'glass_shadow_strong': _mix(THEME_VARS["elev_fill"], "#000000", 0.5),

            # Legacy
            'bertrandt_blue': THEME_VARS["brand_600"],
            'bertrandt_orange': '#ff6600',
            'glass_effect': THEME_VARS["panel_2"],
        }
        
        # Light theme = Dark theme (nur Dark Mode)
        self.light_theme = self.dark_theme.copy()
    
    def get_colors(self):
        """Gibt das aktuelle Farbschema zurück (immer Dark Theme)"""
        return self.dark_theme
    
    def get_fonts(self, window_width, window_height):
        """Gibt responsive Schriftarten für 24" 16:9 optimiert zurück (Bertrandt Theme)"""
        # Optimiert für 24" Screen - größere Schriften für bessere Lesbarkeit
        if window_width >= 2560:
            base_multiplier = 1.4   # 4K/QHD - größer
        elif window_width >= 1920:
            base_multiplier = 1.2   # Full HD - Standard (größer für 24")
        else:
            base_multiplier = 1.0   # Fallback
        
        # Bertrandt Theme Fonts (aus THEME_VARS)
        font_family = THEME_VARS["font_family"]
        
        return {
            'display': (font_family, int(THEME_VARS["size_h1"] * base_multiplier * 1.8), 'bold'),     # H1 * 1.8
            'title': (font_family, int(THEME_VARS["size_h1"] * base_multiplier), 'bold'),             # H1
            'subtitle': (font_family, int(THEME_VARS["size_h2"] * base_multiplier), 'bold'),          # H2
            'body': (font_family, int(THEME_VARS["size_body"] * base_multiplier * 1.6), 'normal'),    # Body größer
            'label': (font_family, int(THEME_VARS["size_body"] * base_multiplier * 1.4), 'normal'),   # Labels
            'button': (font_family, int(THEME_VARS["size_body"] * base_multiplier * 1.5), 'bold'),    # Buttons
            'caption': (font_family, int(THEME_VARS["size_body"] * base_multiplier * 1.2), 'normal'), # Caption
            'nav': (font_family, int(THEME_VARS["size_h2"] * base_multiplier * 1.2), 'bold'),         # Navigation
            'large_button': (font_family, int(THEME_VARS["size_h2"] * base_multiplier), 'bold'),      # Große Buttons
            'monospace': ('Courier New', int(THEME_VARS["size_body"] * base_multiplier * 1.4), 'normal'), # Monospace
        }
    
    def get_radius(self):
        """Gibt Border-Radius-Werte zurück (Schöneres, moderneres Design)"""
        return {
            'xs': 8,                # Kleine Elemente (Inputs, kleine Buttons)
            'sm': 12,               # Standard Buttons
            'md': 16,               # Standard Cards
            'lg': 20,               # Große Cards/Panels
            'xl': 24,               # Hero-Bereiche, große Container
            'xxl': 32,              # Extra große Panels
            'round': 999,           # Vollständig rund (Pills, Badges)
        }
    
    def get_spacing(self):
        """Gibt Spacing-Werte zurück (Schöneres, moderneres Design)"""
        pad = THEME_VARS["pad"]
        return {
            'xxs': 4,               # Feine Details
            'xs': 8,                # Kleine Abstände
            'sm': 12,               # Standard klein
            'md': 16,               # Standard (pad)
            'lg': 24,               # Große Abstände
            'xl': 32,               # Sehr große Abstände
            'xxl': 48,              # Extra große Abstände
            'xxxl': 64,             # Mega Abstände für Hero-Bereiche
        }
    
    def get_components(self):
        """Gibt vordefinierte Component-Styles zurück (Bertrandt Theme)"""
        colors = self.get_colors()
        radius = self.get_radius()
        spacing = self.get_spacing()
        
        return {
            # Buttons (Bertrandt Theme)
            'button_primary': {
                'style': 'Primary.TButton',
                'bg_key': 'accent_primary',
                'fg_key': 'text_on_accent',
                'radius': radius['sm'],
                'padx': spacing['md'],
                'pady': spacing['sm'],
            },
            'button_secondary': {
                'style': 'Ghost.TButton',
                'bg_key': 'background_secondary',
                'fg_key': 'text_primary',
                'border_key': 'border_light',
                'radius': radius['sm'],
                'padx': spacing['md'],
                'pady': spacing['sm'],
            },
            'button_glass': {
                'style': 'Glass.TButton',
                'bg_key': 'glass_bg',
                'fg_key': 'text_primary',
                'border_key': 'glass_border',
                'radius': radius['sm'],
                'padx': spacing['md'],
                'pady': spacing['sm'],
                'glass_effect': True,
            },
            
            # Cards/Panels (Glass Cards)
            'card': {
                'style': 'Glass.TFrame',
                'bg_key': 'background_secondary',
                'radius': radius['xl'],
                'pad': spacing['lg'],
                'glass_effect': True,
            },
            'glass_panel': {
                'style': 'Glass.TFrame',
                'bg_key': 'glass_bg',
                'border_key': 'glass_border',
                'radius': radius['xl'],
                'pad': spacing['lg'],
                'glass_effect': True,
            },
            
            # Inputs
            'input': {
                'style': 'TEntry',
                'bg_key': 'background_secondary',
                'fg_key': 'text_primary',
                'border_key': 'border_light',
                'radius': radius['sm'],
                'padx': spacing['md'],
                'pady': spacing['sm'],
            },
            
            # Navigation/Toolbar
            'navbar': {
                'style': 'Glass.TFrame',
                'bg_key': 'glass_bg',
                'border_key': 'glass_border',
                'radius': radius['xl'],
                'height': 60,
                'pad': spacing['sm'],
                'glass_effect': True,
            },
            'toolbar': {
                'style': 'TFrame',
                'bg_key': 'background_tertiary',
                'border_key': 'border_light',
                'height': 56,
                'pad': spacing['md'],
            },
            
            # Progress
            'progress_bar': {
                'style': 'Glass.Horizontal.TProgressbar',
                'bg_key': 'border_light',
                'fill_key': 'accent_primary',
                'height': 8,
            },
        }
    
    def toggle_theme(self):
        """Wechselt zwischen Dark und Light Mode (nur Dark Mode verfügbar)"""
        # Nur Dark Mode verfügbar
        pass
    
    def get_elevation(self):
        """Gibt Elevation/Shadow-Level zurück (Bertrandt Theme)"""
        colors = self.get_colors()
        return {
            # Glass Shadows (simuliert für Tkinter)
            'glass_light': colors['glass_shadow_light'],
            'glass_medium': colors['glass_shadow_medium'],
            'glass_strong': colors['glass_shadow_strong'],
            
            # Legacy Levels
            'level0': 0.00,
            'level1': 0.08,
            'level2': 0.12,
            'level3': 0.20,
            'level4': 0.35,
        }
    
    def get_glass_effects(self):
        """Gibt spezielle Glass-Effekt-Definitionen zurück"""
        colors = self.get_colors()
        return {
            'blur_radius': 18,
            'background': colors['glass_bg'],
            'border': colors['glass_border'],
            'highlight': colors['glass_highlight'],
            'shadow_light': colors['glass_shadow_light'],
            'shadow_medium': colors['glass_shadow_medium'],
            'shadow_strong': colors['glass_shadow_strong'],
        }
    
    def apply_theme_to_root(self, root: tk.Tk):
        """Wendet das komplette Bertrandt Dark Theme auf die Root-Anwendung an"""
        # Direkt das Bertrandt Theme anwenden
        apply_bertrandt_dark_theme(root, reapply=True)
        
        # TTK Style zurückgeben
        return ttk.Style()
    
    def make_glass_card(self, parent, padding=None):
        """Erstellt eine Glass-Card"""
        if padding is None:
            padding = THEME_VARS["pad"]
        
        # Einfaches Glass-Frame
        frame = ttk.Frame(parent, style="Glass.TFrame", padding=padding)
        return frame, frame

# Globale Theme-Instanz
theme_manager = ThemeManager()

# Direkter Start (Demo)
if __name__ == "__main__":
    root = tk.Tk()
    apply_bertrandt_dark_theme(root)
    root.mainloop()
