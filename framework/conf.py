import os
import importlib

class Settings:
    def __init__(self, settings_module):
        self._settings_module = settings_module
        self._load_settings()

    def _load_settings(self):
        settings = importlib.import_module(self._settings_module)
        for setting in dir(settings):
            if setting.isupper():
                setattr(self, setting, getattr(settings, setting))

class LazySettings:
    def __init__(self):
        self._wrapped = None

    def _setup(self):
        # Automatically look for a settings.py file in the project root
        project_root = os.getcwd()
        possible_settings_path = os.path.join(project_root, 'settings.py')
        
        if os.path.exists(possible_settings_path):
            settings_module = 'settings'
        else:
            raise ImportError("settings.py file not found in the project root directory.")
        
        self._wrapped = Settings(settings_module)

    def __getattr__(self, name):
        if self._wrapped is None:
            self._setup()
        return getattr(self._wrapped, name)

# Global lazy settings object
settings = LazySettings()
