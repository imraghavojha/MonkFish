import json
import os

class MonkFishConfig:
    def __init__(self, config_file="monkfish_config.json"):
        self.config_file = config_file
        self.config = self._load_config()
    
    def _load_config(self):
        # Default configuration if file doesn't exist
        default_config = {
            "engine": {
                "stockfish_path": "./stockfish",
                "skill_level": 3,
                "multipv": 40,
                "use_nnue": False
            },
            "search": {
                "default_depth": 2,
                "drawing_threshold": 0.01
            },
            "info": {
                "name": "MonkFish",
                "author": "Raghav Ojha"
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    loaded_config = json.load(f)
                # Merge with defaults (in case new options are added later)
                for section in default_config:
                    if section in loaded_config:
                        default_config[section].update(loaded_config[section])
                    elif section not in default_config:
                        default_config[section] = loaded_config[section]
                return default_config
            except:
                print(f"info string Warning: Could not load {self.config_file}, using defaults")
                return default_config
        else:
            # Create config file with defaults
            self._save_config(default_config)
            return default_config
    
    def _save_config(self, config):
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except:
            pass  
    
    def get(self, section, key):
        return self.config.get(section, {}).get(key)
    
    def get_engine_path(self):
        return self.get("engine", "stockfish_path")
    
    def get_skill_level(self):
        return self.get("engine", "skill_level")
    
    def get_multipv(self):
        return self.get("engine", "multipv")
    
    def get_use_nnue(self):
        return self.get("engine", "use_nnue")
    
    def get_default_depth(self):
        return self.get("search", "default_depth")
    
    def get_drawing_threshold(self):
        return self.get("search", "drawing_threshold")
    
    def get_engine_name(self):
        return self.get("info", "name")
    
    def get_author(self):
        return self.get("info", "author")