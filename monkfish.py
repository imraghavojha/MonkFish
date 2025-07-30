import re
import subprocess
import os
import sys
from typing import Tuple, Optional, Dict
from config import MonkFishConfig

class MonkFishParser:
    def __init__(self, config_file="monkfish_config.json", uci_options=None):
        self.config = MonkFishConfig(config_file)
        self.uci_options = uci_options
        self.engine = None
        
        try:
            self._start_engine()
            self._init_engine()
        except Exception as e:
            self._handle_engine_error(e)
            raise
        
    def _start_engine(self):
        """Start Stockfish engine with better error handling"""
        stockfish_path = self.config.get_engine_path()
        
        # Check if stockfish exists
        if not os.path.exists(stockfish_path):
            raise FileNotFoundError(
                f"Stockfish not found at '{stockfish_path}'. "
                f"Please run 'python3 setup.py' to download Stockfish automatically."
            )
        
        # Check if stockfish is executable
        if not os.access(stockfish_path, os.X_OK):
            raise PermissionError(
                f"Stockfish at '{stockfish_path}' is not executable. "
                f"Try running: chmod +x {stockfish_path}"
            )
        
        try:
            self.engine = subprocess.Popen(
                stockfish_path,
                universal_newlines=True,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                bufsize=1
            )
        except OSError as e:
            raise RuntimeError(
                f"Failed to start Stockfish: {e}. "
                f"Make sure Stockfish is compatible with your system."
            )
        
        # Give engine a moment to start
        import time
        time.sleep(0.1)
        
        # Check if engine started successfully
        if self.engine.poll() is not None:
            stderr_output = self.engine.stderr.read() if self.engine.stderr else ""
            raise RuntimeError(
                f"Stockfish crashed immediately after starting. "
                f"Error output: {stderr_output}"
            )
        
    def _handle_engine_error(self, error):
        """Provide helpful error messages"""
        print(f"info string MonkFish Error: {error}", file=sys.stderr)
        
        if isinstance(error, FileNotFoundError):
            print("info string Solution: Run 'python3 setup.py' to download Stockfish", file=sys.stderr)
        elif isinstance(error, PermissionError):
            print("info string Solution: Make stockfish executable with 'chmod +x stockfish'", file=sys.stderr)
        elif "incompatible" in str(error).lower():
            print("info string Solution: Download the correct Stockfish version for your system", file=sys.stderr)
        
    def _init_engine(self):
        self._send_command("uci")
        
        # Wait for UCI response with timeout
        uci_response = self._wait_for_response("uciok", timeout=5)
        if not uci_response:
            raise RuntimeError("Stockfish did not respond to UCI command within 5 seconds")
        
        self._update_engine_settings()
        self._send_command("isready")
        
        ready_response = self._wait_for_response("readyok", timeout=5)
        if not ready_response:
            raise RuntimeError("Stockfish did not become ready within 5 seconds")
    
    def _wait_for_response(self, expected_response, timeout=5):
        """Wait for a specific response with timeout"""
        import time
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            if self.engine.poll() is not None:
                raise RuntimeError("Stockfish process terminated unexpectedly")
            
            try:
                line = self.engine.stdout.readline().strip()
                if expected_response in line:
                    return True
            except:
                break
        
        return False
    
    def _update_engine_settings(self):
        """Update Stockfish settings based on current UCI options or config"""
        try:
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
        except Exception as e:
            print(f"info string Warning: Could not set all engine options: {e}", file=sys.stderr)
    
    def update_options(self):
        """Update engine settings when UCI options change"""
        try:
            self._update_engine_settings()
        except Exception as e:
            print(f"info string Warning: Could not update engine options: {e}", file=sys.stderr)
        
    def _send_command(self, cmd: str):
        if self.engine and self.engine.stdin:
            try:
                self.engine.stdin.write(f"{cmd}\n")
                self.engine.stdin.flush()
            except (BrokenPipeError, OSError):
                raise RuntimeError("Lost connection to Stockfish engine")
        
    def _wait_ready(self):
        while True:
            try:
                line = self.engine.stdout.readline().strip()
                if line == "readyok":
                    break
                if not line and self.engine.poll() is not None:
                    raise RuntimeError("Stockfish process terminated")
            except:
                raise RuntimeError("Error reading from Stockfish")
                
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
        if not self.engine or self.engine.poll() is not None:
            raise RuntimeError("Stockfish engine is not running")
        
        try:
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
            
            # Wait for response with timeout
            import time
            start_time = time.time()
            timeout = 30  # 30 second timeout
            
            while time.time() - start_time < timeout:
                line = self.engine.stdout.readline().strip()
                
                if "bestmove" in line:
                    bestmove = line.split()[1]
                    if bestmove == "(none)":
                        raise RuntimeError("No legal moves available in this position")
                    return bestmove, best_info["score"] if best_info else 0.0
                    
                info = self._parse_info_line(line)
                if info and abs(info["score"]) <= drawing_threshold:
                    best_info = info
            
            raise RuntimeError(f"Engine did not respond within {timeout} seconds")
            
        except Exception as e:
            print(f"info string Error in get_drawing_move: {e}", file=sys.stderr)
            raise
        
    def quit(self):
        if self.engine:
            try:
                self._send_command("quit")
                self.engine.wait(timeout=3)
            except:
                pass
            finally:
                if self.engine.poll() is None:
                    self.engine.terminate()
                self.engine = None