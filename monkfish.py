import re
import subprocess
from typing import Tuple, Optional, Dict
from config import MonkFishConfig

class MonkFishParser:
    def __init__(self, config_file="monkfish_config.json"):
        self.config = MonkFishConfig(config_file)
        self.engine = subprocess.Popen(
            self.config.get_engine_path(),
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            bufsize=1
        )
        self._init_engine()
        
    def _init_engine(self):
        self._send_command("uci")
        self._send_command(f"setoption name UCI_UseNNUE value {str(self.config.get_use_nnue()).lower()}")
        self._send_command(f"setoption name Skill Level value {self.config.get_skill_level()}")
        self._send_command(f"setoption name MultiPV value {self.config.get_multipv()}")
        self._send_command("isready")
        self._wait_ready()
        
    def _send_command(self, cmd: str):
        self.engine.stdin.write(f"{cmd}\n")
        self.engine.stdin.flush()
        
    def _wait_ready(self):
        while True:
            line = self.engine.stdout.readline().strip()
            if line == "readyok":
                break
                
    def _parse_info_line(self, line: str) -> Optional[Dict]:
        pattern = r"info depth (\d+).*score cp (-?\d+).*pv ([a-h]\d[a-h]\d(?:[nbrq])?)"
        match = re.search(pattern, line)
        if not match:
            return None
        depth, score, move = match.groups()
        return {
            "depth": int(depth),
            "score": int(score) / 100.0,
            "pv": move
        }
        
    def get_drawing_move(self, position: str, target_depth: int = None) -> Tuple[str, float]:
        if target_depth is None:
            target_depth = self.config.get_default_depth()
            
        if position.startswith("position"):
            position = position.split("moves ")[1] if "moves" in position else ""
            self._send_command(f"position startpos moves {position}")
        else:
            self._send_command(f"position fen {position}")
                
        self._send_command(f"go depth {target_depth}")
        best_info = None
        while True:
            line = self.engine.stdout.readline().strip()
            if "bestmove" in line:
                bestmove = line.split()[1]
                break
                
            info = self._parse_info_line(line)
            if info and abs(info["score"]) <= self.config.get_drawing_threshold():
                best_info = info
                
        return bestmove, best_info["score"] if best_info else 0.0
        
    def quit(self):
        self._send_command("quit")
        self.engine.terminate()