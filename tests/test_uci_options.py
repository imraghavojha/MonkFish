import unittest
import sys
sys.path.append('..')
from config import MonkFishConfig
from uci_options import UCIOptions

class TestUCIOptions(unittest.TestCase):
    
    def setUp(self):
        self.config = MonkFishConfig()
        self.uci_options = UCIOptions(self.config)
    
    def test_option_strings_format(self):
        """Test that UCI option strings are properly formatted"""
        option_strings = self.uci_options.get_option_strings()
        
        # Should have multiple options
        self.assertGreater(len(option_strings), 5)
        
        # Check format of spin options
        hash_option = None
        for opt in option_strings:
            if "Hash" in opt:
                hash_option = opt
                break
        
        self.assertIsNotNone(hash_option)
        self.assertIn("type spin", hash_option)
        self.assertIn("default 128", hash_option)
        self.assertIn("min 1", hash_option)
        self.assertIn("max 2048", hash_option)
    
    def test_set_valid_options(self):
        """Test setting valid option values"""
        # Test spin option
        result = self.uci_options.set_option("Hash", "256")
        self.assertTrue(result)
        self.assertEqual(self.uci_options.get_value("Hash"), 256)
        
        # Test check option
        result = self.uci_options.set_option("Ponder", "true")
        self.assertTrue(result)
        self.assertTrue(self.uci_options.get_value("Ponder"))
        
        # Test MonkFish specific option
        result = self.uci_options.set_option("MonkFish_Skill", "15")
        self.assertTrue(result)
        self.assertEqual(self.uci_options.get_value("MonkFish_Skill"), 15)
    
    def test_set_invalid_options(self):
        """Test setting invalid option values"""
        # Out of range
        result = self.uci_options.set_option("Hash", "5000")
        self.assertFalse(result)
        
        # Invalid type
        result = self.uci_options.set_option("Hash", "not_a_number")
        self.assertFalse(result)
        
        # Non-existent option
        result = self.uci_options.set_option("NonExistent", "value")
        self.assertFalse(result)
    
    def test_drawing_threshold_conversion(self):
        """Test drawing threshold conversion (percentage to decimal)"""
        self.uci_options.set_option("Drawing_Threshold", "5")
        self.assertEqual(self.uci_options.get_drawing_threshold(), 0.05)
        
        self.uci_options.set_option("Drawing_Threshold", "10")
        self.assertEqual(self.uci_options.get_drawing_threshold(), 0.10)

if __name__ == '__main__':
    unittest.main()