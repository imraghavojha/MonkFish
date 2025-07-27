import re
import subprocess
from typing import Tuple, Optional, Dict
from config import MonkFishConfig

class MonkFishParser:
    def __init__(self, config_file="monkfish_config.json", uci_options=None):
        self.config = MonkFishConfig(config_file)
        self.uci_options = uci_options
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
        self._update_engine_settings()
        self._send_command("isready")
        self._wait_ready()
    
    def _update_engine_settings(self):
        """Update Stockfish settings based on current UCI options or config"""
        if self.uci_options:
            # Use UCI options if available
            use_nnue = self.uci_options.get_use_nnue()
            skill_level = self.uci_options.get_skill_level()
            multipv = self.uci_options.get_multipv()
            hash_size = self.uci_options.get_hash()
            threads = self.uci_options.get_threads()
        else:
            # Fall back to config
            use_nnue = self.config.get_use_nnue()
            skill_level = self.config.get_skill_level()
            multipv = self.config.get_multipv()
            hash_size = 128
            threads = 1
        
        self._send_command(f"setoption name UCI_UseNNUE value {str(use_nnue).lower()}")
        self._send_command(f"setoption name Skill Level value {skill_level}")
        self._send_command(f"setoption name MultiPV value {multipv}")
        self._send_command(f"setoption name Hash value {hash_size}")
        self._send_command(f"setoption name Threads value {threads}")
    
    def update_options(self):
        """Update engine settings when UCI options change"""
        self._update_engine_settings()
        
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
            if self.uci_options:
                target_depth = self.uci_options.get_search_depth()
            else:
                target_depth = self.config.get_default_depth()
            
        if position.startswith("position"):
            position = position.split("moves ")[1] if "moves" in position else ""
            self._send_command(f"position startpos moves {position}")
        else:
            self._send_command(f"position fen {position}")
                
        self._send_command(f"go depth {target_depth}")
        best_info = None
        
        # Get drawing threshold from UCI options or config
        if self.uci_options:
            drawing_threshold = self.uci_options.get_drawing_threshold()
        else:
            drawing_threshold = self.config.get_drawing_threshold()
            
        while True:
            line = self.engine.stdout.readline().strip()
            if "bestmove" in line:
                bestmove = line.split()[1]
                break
                
            info = self._parse_info_line(line)
            if info and abs(info["score"]) <= drawing_threshold:
                best_info = info
                
        return bestmove, best_info["score"] if best_info else 0.0
        
    def quit(self):
        self._send_command("quit")
        self.engine.terminate()