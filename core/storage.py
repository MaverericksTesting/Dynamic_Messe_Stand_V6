#!/usr/bin/env python3
"""
Speicher-Verwaltung für Dynamic Messe Stand V6
Automatisches und manuelles Speichern von Präsentationsdaten
"""

import os
import json
import yaml
from datetime import datetime
from core.logger import logger

class PresentationStorage:
    """Minimale Speicher-Verwaltung für Präsentationsdaten"""
    
    def __init__(self):
        self.data_dir = "data"
        self.presentation_file = os.path.join(self.data_dir, "presentation.json")
        self.ensure_data_directory()
    
    def ensure_data_directory(self):
        """Erstellt data-Verzeichnis falls nicht vorhanden"""
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Data-Verzeichnis erstellt: {self.data_dir}")
    
    def load_presentation(self):
        """Lädt gespeicherte Präsentationsdaten"""
        try:
            if os.path.exists(self.presentation_file):
                with open(self.presentation_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                logger.debug(f"Präsentation geladen aus {self.presentation_file}")
                return data
            else:
                logger.info("Keine gespeicherte Präsentation gefunden - verwende Standard-Daten")
                return self.get_default_presentation()
        except Exception as e:
            logger.error(f"Fehler beim Laden der Präsentation: {e}")
            return self.get_default_presentation()
    
    def save_presentation(self, presentation_data):
        """Speichert Präsentationsdaten als JSON"""
        try:
            # Metadaten hinzufügen
            save_data = {
                "metadata": {
                    "saved_at": datetime.now().isoformat(),
                    "version": "1.0",
                    "slide_count": len(presentation_data.get("slides", []))
                },
                "presentation": presentation_data
            }
            
            with open(self.presentation_file, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Präsentation gespeichert: {self.presentation_file}")
            return True
            
        except Exception as e:
            logger.error(f"Fehler beim Speichern der Präsentation: {e}")
            return False
    
    def get_default_presentation(self):
        """Gibt Standard-Präsentationsdaten zurück"""
        return {
            "slides": [
                {
                    "id": 1,
                    "title": "Willkommen zum Dynamic Messe Stand",
                    "content": "Bertrandt Automotive Solutions\nInnovative Technologien für die Zukunft",
                    "config_data": {}
                }
            ],
            "settings": {
                "auto_save": True,
                "slide_duration": 5
            }
        }

# Singleton-Instanz für einfache Verwendung
storage_manager = PresentationStorage()

def load_presentation():
    """Lädt aktuelle Präsentation"""
    return storage_manager.load_presentation()

def save_presentation(data):
    """Speichert Präsentationsdaten"""
    return storage_manager.save_presentation(data)
