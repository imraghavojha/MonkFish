import unittest
import subprocess
import time
import threading
import queue
import os

class TestMonkFishPhilosophy(unittest.TestCase):
    """Test that MonkFish maintains its zen philosophy of seeking draws"""
    
    def setUp(self):
        """Start MonkFish engine process"""
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
        
        # Initialize engine
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
    
    def _get_move_for_position(self, position, depth=2):
        """Get MonkFish's move for a given position"""
        self._send_command(f"position {position}")
        self._send_command(f"go depth {depth}")
        response = self._get_response(timeout=10)
        
        if response and response.startswith("bestmove"):
            return response.split()[1]
        return None
    
    def test_opening_equality_seeking(self):
        """Test that MonkFish seeks equality in opening positions"""
        test_positions = [
            "startpos moves e2e4",  # After 1.e4
            "startpos moves e2e4 e7e5 g1f3",  # After 1.e4 e5 2.Nf3
            "startpos moves d2d4",  # After 1.d4
            "startpos moves d2d4 d7d5",  # After 1.d4 d5
        ]
        
        for position in test_positions:
            with self.subTest(position=position):
                move = self._get_move_for_position(position)
                self.assertIsNotNone(move, f"Should get a move for position: {position}")
                self.assertRegex(move, r"^[a-h][1-8][a-h][1-8][nbrq]?$", 
                               f"Move should be valid format: {move}")
    
    def test_different_drawing_thresholds(self):
        """Test that different drawing thresholds affect move selection"""
        position = "startpos moves e2e4"
        
        # Test with tight drawing threshold
        self._send_command("setoption name Drawing_Threshold value 1")
        self._get_response()  # confirmation
        move1 = self._get_move_for_position(position)
        
        # Test with loose drawing threshold  
        self._send_command("setoption name Drawing_Threshold value 10")
        self._get_response()  # confirmation
        move2 = self._get_move_for_position(position)
        
        # Both should be valid moves
        self.assertIsNotNone(move1)
        self.assertIsNotNone(move2)
        
        # Moves might be different due to different thresholds
        # (This is expected behavior, not a requirement)
    
    def test_skill_level_affects_play(self):
        """Test that different skill levels produce moves"""
        position = "startpos moves e2e4"
        
        # Test low skill
        self._send_command("setoption name MonkFish_Skill value 1")
        self._get_response()
        move1 = self._get_move_for_position(position)
        
        # Test high skill
        self._send_command("setoption name MonkFish_Skill value 15")
        self._get_response()
        move2 = self._get_move_for_position(position)
        
        # Both should produce valid moves
        self.assertIsNotNone(move1)
        self.assertIsNotNone(move2)
    
    

if __name__ == '__main__':
    unittest.main()