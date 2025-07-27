class UCIOptions:
    def __init__(self, config):
        self.config = config
        self.options = {
            # Standard UCI options
            "Hash": {
                "type": "spin",
                "default": 128,
                "min": 1,
                "max": 2048,
                "value": 128
            },
            "Threads": {
                "type": "spin", 
                "default": 1,
                "min": 1,
                "max": 8,
                "value": 1
            },
            "Ponder": {
                "type": "check",
                "default": False,
                "value": False
            },
            
            # MonkFish specific options
            "MonkFish_Skill": {
                "type": "spin",
                "default": self.config.get_skill_level(),
                "min": 0,
                "max": 20,
                "value": self.config.get_skill_level()
            },
            "Drawing_Threshold": {
                "type": "spin",
                "default": int(self.config.get_drawing_threshold() * 100),
                "min": 0,
                "max": 50,
                "value": int(self.config.get_drawing_threshold() * 100)
            },
            "Search_Depth": {
                "type": "spin",
                "default": self.config.get_default_depth(),
                "min": 1,
                "max": 10,
                "value": self.config.get_default_depth()
            },
            "MultiPV": {
                "type": "spin",
                "default": self.config.get_multipv(),
                "min": 1,
                "max": 100,
                "value": self.config.get_multipv()
            },
            "Use_NNUE": {
                "type": "check",
                "default": self.config.get_use_nnue(),
                "value": self.config.get_use_nnue()
            }
        }
    
    def get_option_strings(self):
        """Return UCI option strings for engine identification"""
        option_strings = []
        for name, opt in self.options.items():
            if opt["type"] == "spin":
                option_strings.append(
                    f"option name {name} type {opt['type']} default {opt['default']} min {opt['min']} max {opt['max']}"
                )
            elif opt["type"] == "check":
                default_val = "true" if opt["default"] else "false"
                option_strings.append(
                    f"option name {name} type {opt['type']} default {default_val}"
                )
        return option_strings
    
    def set_option(self, name, value):
        """Set an option value"""
        if name in self.options:
            opt = self.options[name]
            if opt["type"] == "spin":
                try:
                    val = int(value)
                    if opt["min"] <= val <= opt["max"]:
                        opt["value"] = val
                        return True
                except ValueError:
                    pass
            elif opt["type"] == "check":
                if value.lower() in ["true", "false"]:
                    opt["value"] = value.lower() == "true"
                    return True
        return False
    
    def get_value(self, name):
        """Get current value of an option"""
        if name in self.options:
            return self.options[name]["value"]
        return None
    
    def get_skill_level(self):
        return self.get_value("MonkFish_Skill")
    
    def get_drawing_threshold(self):
        return self.get_value("Drawing_Threshold") / 100.0
    
    def get_search_depth(self):
        return self.get_value("Search_Depth")
    
    def get_multipv(self):
        return self.get_value("MultiPV")
    
    def get_use_nnue(self):
        return self.get_value("Use_NNUE")
    
    def get_hash(self):
        return self.get_value("Hash")
    
    def get_threads(self):
        return self.get_value("Threads")
    
    def get_ponder(self):
        return self.get_value("Ponder")