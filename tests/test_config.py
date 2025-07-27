import unittest
import tempfile
import os
import json
import sys
sys.path.append('..')
from config import MonkFishConfig

class TestMonkFishConfig(unittest.TestCase):
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, "test_config.json")
    
    def tearDown(self):
        if os.path.exists(self.config_file):
            os.remove(self.config_file)
        os.rmdir(self.temp_dir)
    
    def test_default_config_creation(self):
        """Test that default config is created when file doesn't exist"""
        config = MonkFishConfig(self.config_file)
        
        # Check that file was created
        self.assertTrue(os.path.exists(self.config_file))
        
        # Check default values
        self.assertEqual(config.get_skill_level(), 3)
        self.assertEqual(config.get_multipv(), 40)
        self.assertEqual(config.get_default_depth(), 2)
        self.assertEqual(config.get_drawing_threshold(), 0.01)
        self.assertFalse(config.get_use_nnue())
    
    def test_custom_config_loading(self):
        """Test loading custom configuration"""
        custom_config = {
            "engine": {
                "skill_level": 10,
                "multipv": 20
            },
            "search": {
                "default_depth": 5,
                "drawing_threshold": 0.05
            }
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(custom_config, f)
        
        config = MonkFishConfig(self.config_file)
        
        # Check custom values
        self.assertEqual(config.get_skill_level(), 10)
        self.assertEqual(config.get_multipv(), 20)
        self.assertEqual(config.get_default_depth(), 5)
        self.assertEqual(config.get_drawing_threshold(), 0.05)
    
    def test_corrupted_config_fallback(self):
        """Test fallback to defaults when config is corrupted"""
        with open(self.config_file, 'w') as f:
            f.write("invalid json content")
        
        config = MonkFishConfig(self.config_file)
        
        # Should use defaults
        self.assertEqual(config.get_skill_level(), 3)
        self.assertEqual(config.get_multipv(), 40)

if __name__ == '__main__':
    unittest.main()