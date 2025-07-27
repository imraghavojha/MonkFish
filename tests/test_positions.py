import unittest
import subprocess
import time
import threading
import queue
import os

class TestBenchmarkPositions(unittest.TestCase):
    """Test MonkFish against known chess positions to verify consistency"""
    
    # Known positions with expected behavior
    BENCHMARK_POSITIONS = [
        {
            "name": "Starting Position", 
            "fen": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "moves": "",
            "description": "Should play a reasonable opening move"
        },
        {
            "name": "After 1.e4",
            "fen": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1", 
            "moves": "e2e4",
            "description": "Should respond with equalizing move like e5, d5, or c5"
        },
        {
            "name": "King's Pawn Game",
            "fen": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq e6 0 2",
            "moves": "e2e4 e7e5", 
            "description": "Balanced position, should develop pieces"
        },
        {
            "name": "Queen's Gambit",
            "fen": "rnbqkbnr/ppp1pppp/8/3p4/2PP4/8/PP2PPPP/RNBQKBNR b KQkq c3 0 2",
            "moves": "d2d4 d7d5 c2c4",
            "description": "Should handle Queen's Gambit acceptably"
        },
        {
            "name": "Equal Endgame",
            "fen": "8/8/8/3k4/3K4/8/8/8 w - - 0 1",
            "moves": "",
            "description": "King vs King - should play any legal move"
        }
    ]
    
    def setUp(self):
        """Start MonkFish engine"""
        # Change to parent directory to run uci.py
        parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        self.engine = subprocess.Popen(
            ["python3", "uci.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1,
            cwd=parent_dir
        )
        
        self.response_queue = queue.Queue()
        self.reader_thread = threading.Thread(target=self._read_responses)
        self.reader_thread.daemon = True
        self.reader_thread.start()
        
        # Initialize
        self._send_command("uci")
        self._get_responses_until("uciok")
        self._send_command("isready")
        self._get_response()
    
    def tearDown(self):
        if self.engine.poll() is None:
            self._send_command("quit")
            self.engine.wait(timeout=5)
        if self.engine.poll() is None:
            self.engine.terminate()
    
    def _send_command(self, command):
        self.engine.stdin.write(f"{command}\n")
        self.engine.stdin.flush()
    
    def _read_responses(self):
        try:
            while True:
                line = self.engine.stdout.readline()
                if not line:
                    break
                self.response_queue.put(line.strip())
        except:
            pass
    
    def _get_response(self, timeout=5):
        try:
            return self.response_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def _get_responses_until(self, end_marker, timeout=10):
        responses = []
        start_time = time.time()
        while time.time() - start_time < timeout:
            response = self._get_response(1)
            if response:
                responses.append(response)
                if end_marker in response:
                    break
        return responses
    
    def _get_move_for_position(self, position_cmd):
        """Get move for a position command"""
        self._send_command(position_cmd)
        self._send_command("go depth 3")
        response = self._get_response(timeout=15)
        
        if response and response.startswith("bestmove"):
            return response.split()[1]
        return None
    
    def test_benchmark_positions(self):
        """Test MonkFish against benchmark positions"""
        for pos in self.BENCHMARK_POSITIONS:
            with self.subTest(position=pos["name"]):
                # Build position command
                if pos["moves"]:
                    position_cmd = f"position startpos moves {pos['moves']}"
                else:
                    if pos["fen"] == "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1":
                        position_cmd = "position startpos"
                    else:
                        position_cmd = f"position fen {pos['fen']}"
                
                move = self._get_move_for_position(position_cmd)
                
                # Basic validation
                self.assertIsNotNone(move, 
                    f"Should get a move for {pos['name']}: {pos['description']}")
                self.assertRegex(move, r"^[a-h][1-8][a-h][1-8][nbrq]?$",
                    f"Move should be valid format for {pos['name']}: {move}")
                
                print(f"   {pos['name']}: {move}")
    
    
    def test_different_depths(self):
        """Test that MonkFish works at different search depths"""
        position_cmd = "position startpos moves e2e4"
        
        for depth in [1, 2, 3, 4]:
            with self.subTest(depth=depth):
                self._send_command(position_cmd)
                self._send_command(f"go depth {depth}")
                response = self._get_response(timeout=20)
                
                self.assertIsNotNone(response, f"Should get response at depth {depth}")
                self.assertTrue(response.startswith("bestmove"), 
                    f"Should get bestmove at depth {depth}")

if __name__ == '__main__':
    unittest.main()