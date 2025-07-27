import unittest
import subprocess
import time
import threading
import queue
import os
import sys

class TestUCIProtocol(unittest.TestCase):
    
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
        
        # Queue to store engine responses
        self.response_queue = queue.Queue()
        
        # Start thread to read responses
        self.reader_thread = threading.Thread(target=self._read_responses)
        self.reader_thread.daemon = True
        self.reader_thread.start()
    
    def tearDown(self):
        """Clean up engine process"""
        if self.engine.poll() is None:
            self._send_command("quit")
            self.engine.wait(timeout=5)
        
        if self.engine.poll() is None:
            self.engine.terminate()
    
    def _send_command(self, command):
        """Send command to engine"""
        self.engine.stdin.write(f"{command}\n")
        self.engine.stdin.flush()
    
    def _read_responses(self):
        """Read responses from engine in separate thread"""
        try:
            while True:
                line = self.engine.stdout.readline()
                if not line:
                    break
                self.response_queue.put(line.strip())
        except:
            pass
    
    def _get_response(self, timeout=5):
        """Get next response from engine"""
        try:
            return self.response_queue.get(timeout=timeout)
        except queue.Empty:
            return None
    
    def _get_responses_until(self, end_marker, timeout=10):
        """Get all responses until a specific marker"""
        responses = []
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            response = self._get_response(1)
            if response:
                responses.append(response)
                if end_marker in response:
                    break
        
        return responses
    
    def test_uci_handshake(self):
        """Test basic UCI handshake"""
        self._send_command("uci")
        responses = self._get_responses_until("uciok")
        
        # Check required responses
        response_text = " ".join(responses)
        self.assertIn("id name MonkFish", response_text)
        self.assertIn("id author Raghav Ojha", response_text)
        self.assertIn("uciok", response_text)
        
        # Check that options are present
        self.assertIn("option name Hash", response_text)
        self.assertIn("option name MonkFish_Skill", response_text)
    
    def test_isready(self):
        """Test isready command"""
        self._send_command("uci")
        self._get_responses_until("uciok")
        
        self._send_command("isready")
        response = self._get_response()
        self.assertEqual(response, "readyok")
    
    def test_setoption(self):
        """Test setoption command"""
        self._send_command("uci")
        self._get_responses_until("uciok")
        
        self._send_command("setoption name MonkFish_Skill value 10")
        response = self._get_response()
        self.assertIn("Set MonkFish_Skill to 10", response)
    
    def test_position_and_go(self):
        """Test position setup and move generation"""
        self._send_command("uci")
        self._get_responses_until("uciok")
        
        self._send_command("isready")
        self._get_response()  # readyok
        
        self._send_command("position startpos moves e2e4")
        self._send_command("go depth 1")
        
        response = self._get_response(timeout=10)
        self.assertIsNotNone(response)
        self.assertTrue(response.startswith("bestmove"))
        
        # Extract move and validate format
        move = response.split()[1]
        self.assertRegex(move, r"^[a-h][1-8][a-h][1-8][nbrq]?$")

if __name__ == '__main__':
    unittest.main()