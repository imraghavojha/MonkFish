from monkfish import MonkFishParser
from config import MonkFishConfig
from uci_options import UCIOptions
import sys

class UCIHandler:
    def __init__(self):
        try:
            self.config = MonkFishConfig()
            self.uci_options = UCIOptions(self.config)
            self.parser = None
            self.current_position = None
        except Exception as e:
            print(f"info string MonkFish initialization error: {e}")
            sys.exit(1)
    
    def _ensure_parser(self):
        """Lazy initialization of parser to provide better error messages"""
        if self.parser is None:
            try:
                self.parser = MonkFishParser(uci_options=self.uci_options)
            except FileNotFoundError as e:
                print(f"info string {e}")
                print("info string Please run 'python3 setup.py' to download Stockfish")
                return False
            except Exception as e:
                print(f"info string Failed to initialize MonkFish engine: {e}")
                return False
        return True
        
    def handle_position(self, cmd):
        self.current_position = cmd
    
    def handle_setoption(self, cmd):
        """Handle UCI setoption commands"""
        try:
            # Format: setoption name <n> value <value>
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
                            if self.parser:
                                self.parser.update_options()
                            print(f"info string Set {option_name} to {option_value}")
                        else:
                            print(f"info string Invalid option or value: {option_name} = {option_value}")
                except (ValueError, IndexError):
                    print("info string Invalid setoption format")
        except Exception as e:
            print(f"info string Error setting option: {e}")
        
    def handle_go(self, cmd):
        if not self._ensure_parser():
            print("bestmove (none)")
            return
            
        if self.current_position is None:
            print("info string No position set")
            print("bestmove (none)")
            return
        
        try:
            move, score = self.parser.get_drawing_move(self.current_position)
            print(f"bestmove {move}")
        except Exception as e:
            print(f"info string Error generating move: {e}")
            print("bestmove (none)")

    def run(self):
        print("info string MonkFish - The Zen of Chess")
        
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
                    # Try to initialize parser if not done yet
                    if self._ensure_parser():
                        print("readyok")
                    else:
                        print("info string Engine not ready - initialization failed")
                        print("readyok")  # Still respond to keep GUI happy
                elif cmd.startswith("position"):
                    self.handle_position(cmd)
                elif cmd.startswith("setoption"):
                    self.handle_setoption(cmd)
                elif cmd.startswith("go"):
                    self.handle_go(cmd)
                elif cmd == "stop":
                    # Handle stop command gracefully
                    print("bestmove (none)")
                elif cmd.startswith("ponderhit"):
                    # Handle ponderhit (we don't ponder, but respond anyway)
                    pass
                else:
                    # Unknown command - just ignore it
                    pass
                    
            except EOFError:
                # Input stream closed
                break
            except KeyboardInterrupt:
                # Ctrl+C pressed
                break
            except Exception as e:
                print(f"info string Unexpected error: {e}")
        
        # Cleanup
        if self.parser:
            try:
                self.parser.quit()
            except:
                pass

if __name__ == "__main__":
    handler = UCIHandler()
    handler.run()