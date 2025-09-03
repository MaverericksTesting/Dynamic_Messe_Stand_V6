#!/usr/bin/env python3
"""
Content Models für Dynamic Messe Stand V4
Slide und Präsentations-Management
"""

import json
import os
from datetime import datetime
from core.logger import logger
from core.config import config

class Slide:
    """Repräsentiert eine einzelne Slide"""
    
    def __init__(self, slide_id, title="", content="", layout="text", config_data=None):
        self.slide_id = slide_id
        self.title = title
        self.content = content
        self.layout = layout
        self.config_data = config_data or {}
        self.created_at = datetime.now()
        self.modified_at = datetime.now()
        self.signal_id = f"page_{slide_id}"
    
    def to_dict(self):
        """Konvertiert Slide zu Dictionary"""
        return {
            'slide_id': self.slide_id,
            'title': self.title,
            'content': self.content,
            'layout': self.layout,
            'config_data': self.config_data,
            'created_at': self.created_at.isoformat(),
            'modified_at': self.modified_at.isoformat(),
            'signal_id': self.signal_id
        }
    
    @classmethod
    def from_dict(cls, data):
        """Erstellt Slide aus Dictionary"""
        slide = cls(
            slide_id=data['slide_id'],
            title=data.get('title', ''),
            content=data.get('content', ''),
            layout=data.get('layout', 'text'),
            config_data=data.get('config_data', {})
        )
        
        if 'created_at' in data:
            slide.created_at = datetime.fromisoformat(data['created_at'])
        if 'modified_at' in data:
            slide.modified_at = datetime.fromisoformat(data['modified_at'])
        
        return slide
    
    def update(self, **kwargs):
        """Aktualisiert Slide-Eigenschaften"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.modified_at = datetime.now()

class ContentManager:
    """Verwaltet alle Slides und Content"""
    
    def __init__(self):
        self.slides = {}
        self.current_slide = 1
        self.content_dir = config.content_dir
        self.ensure_content_directory()
        self.load_all_slides()
    
    def ensure_content_directory(self):
        """Stellt sicher, dass das Content-Verzeichnis existiert"""
        if not os.path.exists(self.content_dir):
            os.makedirs(self.content_dir)
            logger.info(f"Content-Verzeichnis erstellt: {self.content_dir}")
    
    def load_all_slides(self):
        """Lädt alle Slides aus dem Content-Verzeichnis und erstellt Standard-Slides"""
        try:
            # Suche nach page_* Ordnern
            existing_slides = set()
            for item in os.listdir(self.content_dir):
                item_path = os.path.join(self.content_dir, item)
                if os.path.isdir(item_path) and item.startswith('page_'):
                    try:
                        slide_id = int(item.split('_')[1])
                        self.load_slide(slide_id)
                        existing_slides.add(slide_id)
                    except (ValueError, IndexError):
                        logger.warning(f"Ungültiger Slide-Ordner: {item}")
            
            # Erstelle fehlende Standard-Slides (1-10)
            for slide_id in range(1, 11):
                if slide_id not in existing_slides:
                    self.create_default_slide(slide_id)
            
            logger.info(f"{len(self.slides)} Slides geladen (davon {10 - len(existing_slides)} neu erstellt)")
        except Exception as e:
            logger.error(f"Fehler beim Laden der Slides: {e}")
            # Fallback: Erstelle alle Standard-Slides
            for slide_id in range(1, 11):
                if slide_id not in self.slides:
                    self.create_default_slide(slide_id)
    
    def load_slide(self, slide_id):
        """Lädt eine spezifische Slide"""
        slide_dir = os.path.join(self.content_dir, f"page_{slide_id}")
        config_file = os.path.join(slide_dir, "config.json")
        
        if not os.path.exists(config_file):
            # Erstelle Standard-Slide
            self.create_default_slide(slide_id)
            return
        
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                config_data = json.load(f)
            
            slide = Slide(
                slide_id=slide_id,
                title=config_data.get('title', f'Slide {slide_id}'),
                content=config_data.get('content', ''),
                layout=config_data.get('layout', 'text'),
                config_data=config_data
            )
            
            self.slides[slide_id] = slide
            logger.debug(f"Slide {slide_id} geladen")
            
        except Exception as e:
            logger.error(f"Fehler beim Laden von Slide {slide_id}: {e}")
            self.create_default_slide(slide_id)
    
    def create_default_slide(self, slide_id):
        """Erstellt eine Standard-Slide mit vorgefertigtem Inhalt"""
        slide_dir = os.path.join(self.content_dir, f"page_{slide_id}")
        if not os.path.exists(slide_dir):
            os.makedirs(slide_dir)
        
        # Vordefinierte Slide-Inhalte - Alle im Design von Folie 6
        slide_contents = {
            1: {
                "title": "BumbleB - Das automatisierte Shuttle",
                "content": "Innovative autonome Mobilität:\n\n• Vollständig elektrischer Antrieb\n• Autonome Navigation\n• Umweltfreundliche Technologie\n• Sichere und zuverlässige Fahrt\n• Moderne Benutzeroberfläche\n• Komfortable Innenausstattung\n• Zukunftsweisende Mobilität"
            },
            2: {
                "title": "Technische Spezifikationen",
                "content": "Modernste Technik im Detail:\n\n• Kapazität: 8-12 Passagiere\n• Geschwindigkeit: bis 25 km/h\n• Reichweite: 150 km pro Ladung\n• Ladezeit: 2 Stunden Schnellladung\n• Sensoren: LiDAR, Kameras, Radar\n• Betriebssystem: Linux-basiert\n• Konnektivität: 5G, WiFi, Bluetooth"
            },
            3: {
                "title": "Einsatzgebiete und Vorteile",
                "content": "Vielseitige Anwendungsmöglichkeiten:\n\n• Städtischer öffentlicher Nahverkehr\n• Campus-Transport für Universitäten\n• Flughäfen und Bahnhöfe\n• Touristische Routen\n• Last-Mile-Delivery Service\n• Reduzierte CO2-Emissionen\n• Kosteneffiziente Mobilität"
            },
            4: {
                "title": "Sicherheitssysteme",
                "content": "Höchste Sicherheitsstandards:\n\n• 360° LiDAR-Überwachungssystem\n• Redundante Bremssysteme\n• Notfall-Stopp-Funktion\n• Intelligente Kollisionsvermeidung\n• Wettererkennungssystem\n• Fernüberwachung rund um die Uhr\n• Automatische Systemdiagnose"
            },
            5: {
                "title": "Nachhaltigkeit & Umwelt",
                "content": "Grüne Mobilität der Zukunft:\n\n• 100% elektrischer Antrieb\n• Null lokale Emissionen\n• Energieeffiziente Routenplanung\n• Recycelbare Materialien\n• Solarpanel-Integration möglich\n• CO2-Reduktion um 85%\n• Deutliche Lärmreduzierung"
            },
            6: {
                "title": "Benutzerfreundlichkeit",
                "content": "Einfache Bedienung für alle:\n\n• Intuitive Touch-Bedienung\n• Barrierefreier Zugang\n• Mehrsprachige Benutzeroberfläche\n• Mobile App-Integration\n• Echtzeit-Informationen\n• Komfortable Sitze\n• Klimaanlage"
            },
            7: {
                "title": "Technologie-Innovation",
                "content": "Zukunftstechnologie heute:\n\n• KI-basierte Routenoptimierung\n• Machine Learning Algorithmen\n• Edge Computing Integration\n• 5G-Konnektivität\n• Cloud-basierte Services\n• Predictive Maintenance\n• Over-the-Air Software Updates"
            },
            8: {
                "title": "Wirtschaftlichkeit",
                "content": "Intelligente Investition:\n\n• Niedrige Betriebskosten\n• Minimaler Wartungsaufwand\n• Hohe Verfügbarkeit über 95%\n• Skalierbare Flottengröße\n• ROI innerhalb von 3 Jahren\n• Staatliche Förderungen verfügbar\n• Flexible Leasing-Optionen"
            },
            9: {
                "title": "Zukunftsausblick",
                "content": "Vision der Mobilität:\n\n• Integration in Smart Cities\n• Vernetzung mit anderen Verkehrsmitteln\n• Autonome Fahrzeug-Flotten\n• Personalisierte Transportlösungen\n• Erweiterte KI-Funktionen\n• Globale Expansion geplant\n• Kontinuierliche Innovation"
            },
            10: {
                "title": "Kontakt & Nächste Schritte",
                "content": "Starten Sie mit BumbleB:\n\n• Kostenlose Beratung vereinbaren\n• Pilotprojekt initiieren\n• Individuelle Lösungen entwickeln\n• Finanzierungsoptionen besprechen\n• Demo-Fahrt organisieren\n• Technische Integration planen\n• Langfristige Partnerschaft aufbauen"
            }
        }
        
        # Standard-Inhalt basierend auf Slide-ID
        slide_content = slide_contents.get(slide_id, {
            "title": f"Folie {slide_id}",
            "content": f"Inhalt für Folie {slide_id}\n\n• Punkt 1\n• Punkt 2\n• Punkt 3"
        })
        
        default_config = {
            "title": slide_content["title"],
            "content": slide_content["content"],
            "layout": "text",
            "background_color": "#FFFFFF",
            "text_color": "#000000",
            "slide_width": 1920,
            "slide_height": 1080,
            "canvas_elements": [],
            "creator_version": "1.0"
        }
        
        config_file = os.path.join(slide_dir, "config.json")
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
        
        slide = Slide(
            slide_id=slide_id,
            title=default_config['title'],
            content=default_config['content'],
            layout=default_config['layout'],
            config_data=default_config
        )
        
        self.slides[slide_id] = slide
        logger.info(f"Standard-Slide {slide_id} erstellt: {slide_content['title']}")
    
    def save_slide(self, slide_id):
        """Speichert eine Slide"""
        if slide_id not in self.slides:
            logger.error(f"Slide {slide_id} nicht gefunden")
            return False
        
        slide = self.slides[slide_id]
        slide_dir = os.path.join(self.content_dir, f"page_{slide_id}")
        
        if not os.path.exists(slide_dir):
            os.makedirs(slide_dir)
        
        config_file = os.path.join(slide_dir, "config.json")
        
        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(slide.config_data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Slide {slide_id} gespeichert")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern von Slide {slide_id}: {e}")
            return False
    
    def get_slide(self, slide_id):
        """Gibt eine spezifische Slide zurück"""
        return self.slides.get(slide_id)
    
    def get_all_slides(self):
        """Gibt alle Slides zurück"""
        return dict(sorted(self.slides.items()))
    
    def create_slide(self, slide_id, title="", content="", layout="text"):
        """Erstellt eine neue Slide"""
        if slide_id in self.slides:
            logger.warning(f"Slide {slide_id} existiert bereits")
            return False
        
        config_data = {
            "title": title or f"Slide {slide_id}",
            "content": content,
            "layout": layout,
            "background_color": "#FFFFFF",
            "text_color": "#000000"
        }
        
        slide = Slide(
            slide_id=slide_id,
            title=config_data['title'],
            content=content,
            layout=layout,
            config_data=config_data
        )
        
        self.slides[slide_id] = slide
        self.save_slide(slide_id)
        logger.info(f"Neue Slide {slide_id} erstellt")
        return True
    
    def delete_slide(self, slide_id):
        """Löscht eine Slide"""
        if slide_id not in self.slides:
            return False
        
        # Lösche aus Memory
        del self.slides[slide_id]
        
        # Lösche Verzeichnis
        slide_dir = os.path.join(self.content_dir, f"page_{slide_id}")
        if os.path.exists(slide_dir):
            import shutil
            shutil.rmtree(slide_dir)
        
        logger.info(f"Slide {slide_id} gelöscht")
        return True
    
    def get_slide_count(self):
        """Gibt die Anzahl der Slides zurück"""
        return len(self.slides)
    
    def set_current_slide(self, slide_id):
        """Setzt die aktuelle Slide"""
        if slide_id in self.slides:
            self.current_slide = slide_id
            logger.debug(f"Aktuelle Slide: {slide_id}")
            return True
        return False

# Globale Content-Manager Instanz
content_manager = ContentManager()