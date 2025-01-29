from monkfish import MonkFishParser

class UCIHandler:
    def __init__(self):
        self.parser = MonkFishParser("./stockfish")
        
    def handle_position(self, cmd):
        self.current_position = cmd
        
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
                    print("id name MonkFish")
                    print("id author Raghav Ojha")
                    print("uciok")
                elif cmd == "isready":
                    print("readyok")
                elif cmd.startswith("position"):
                    self.handle_position(cmd)
                elif cmd.startswith("go"):
                    self.handle_go(cmd)
            except Exception as e:
                print(f"info string Error: {e}")
        self.parser.quit()

if __name__ == "__main__":
    handler = UCIHandler()
    handler.run()