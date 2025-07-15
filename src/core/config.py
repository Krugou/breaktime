"""Configuration management for Break Reminder application."""

import json
import os
from typing import Dict, Any


class ConfigManager:
    """Manages application configuration with persistence."""
    
    def __init__(self, config_file: str = None):
        """Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        if config_file is None:
            config_file = os.path.join(os.path.expanduser("~"), ".break_reminder_config.json")
        
        self.config_file = config_file
        self._config = self._load_default_config()
        self.load()
    
    def _load_default_config(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            "usual_start": "08:00",
            "lunch_start": "10:45", 
            "lunch_end": "12:30",
            "workday_length": "08:00",
            "break_points": [0.25, 0.75],  # 1/4 and 3/4 of workday
            "theme": "dark",  # dark, light, auto
            "auto_close_delay": 30,  # minutes
            "window_position": "top-right",  # top-right, top-left, bottom-right, bottom-left
            "notifications_enabled": True,
            "sound_enabled": False,
            "minimize_to_tray": True,
            "start_minimized": False,
            "debug_mode": False
        }
    
    def load(self) -> None:
        """Load configuration from file."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    # Merge with defaults to ensure all keys exist
                    self._config.update(loaded_config)
            except (json.JSONDecodeError, IOError):
                # If file is corrupted or unreadable, use defaults
                pass
    
    def save(self) -> None:
        """Save configuration to file."""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self._config, f, indent=2, ensure_ascii=False)
        except IOError:
            # If save fails, continue without saving
            pass
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value.
        
        Args:
            key: Configuration key
            default: Default value if key doesn't exist
            
        Returns:
            Configuration value or default
        """
        return self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self._config[key] = value
    
    def update(self, config_dict: Dict[str, Any]) -> None:
        """Update multiple configuration values.
        
        Args:
            config_dict: Dictionary of configuration values to update
        """
        self._config.update(config_dict)
    
    def get_all(self) -> Dict[str, Any]:
        """Get all configuration values.
        
        Returns:
            Dictionary of all configuration values
        """
        return self._config.copy()
    
    def reset_to_defaults(self) -> None:
        """Reset configuration to default values."""
        self._config = self._load_default_config()