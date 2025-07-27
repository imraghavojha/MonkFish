from monkfish import MonkFishParser
from config import MonkFishConfig
from uci_options import UCIOptions

class UCIHandler:
    def __init__(self):
        self.config = MonkFishConfig()
        self.uci_options = UCIOptions(self.config)
        self.parser = MonkFishParser(uci_options=self.uci_options)
        
    def handle_position(self, cmd):
        self.current_position = cmd
    
    def handle_setoption(self, cmd):
        """Handle UCI setoption commands"""
        # Format: setoption name <name> value <value>
        parts = cmd.split()
        if len(parts) >= 4 and parts[1] == "name" and "value" in parts:
            try:
                name_idx = parts.index("name") + 1
                value_idx = parts.index("value") + 1
                if name_idx < len(parts) and value_idx < len(parts):
                    option_name = parts[name_idx]
                    option_value = parts[value_idx]
                    
                    if self.uci_options.set_option(option_name, option_value):
                        # Update engine settings if option changed successfully
                        self.parser.update_options()
                        print(f"info string Set {option_name} to {option_value}")
                    else:
                        print(f"info string Invalid option or value: {option_name} = {option_value}")
            except (ValueError, IndexError):
                print("info string Invalid setoption format")
        
    def handle_go(self, cmd):
        move, score = self.parser.get_drawing_move(self.current_position)
        print(f"bestmove {move}")

    def run(self):
        while True:
            try:
                cmd = input().strip()
                if cmd == "quit": 
                    break
                elif cmd == "uci":
                    print(f"id name {self.config.get_engine_name()}")
                    print(f"id author {self.config.get_author()}")
                    
                    # Send UCI options
                    for option_string in self.uci_options.get_option_strings():
                        print(option_string)
                    
                    print("uciok")
                elif cmd == "isready":
                    print("readyok")
                elif cmd.startswith("position"):
                    self.handle_position(cmd)
                elif cmd.startswith("setoption"):
                    self.handle_setoption(cmd)
                elif cmd.startswith("go"):
                    self.handle_go(cmd)
            except Exception as e:
                print(f"info string Error: {e}")
        self.parser.quit()

if __name__ == "__main__":
    handler = UCIHandler()
    handler.run()