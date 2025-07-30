#!/usr/bin/env python3
"""
Quick requirements checker for MonkFish
"""

import sys
import os
import platform

def check_requirements():
    """Check all requirements for MonkFish"""
    print("🔍 MonkFish Requirements Check")
    print("=" * 35)
    
    all_good = True
    
    # Python version
    print("🐍 Python version:", end=" ")
    if sys.version_info >= (3, 6):
        print(f"✅ {sys.version_info.major}.{sys.version_info.minor}")
    else:
        print(f"❌ {sys.version_info.major}.{sys.version_info.minor} (need 3.6+)")
        all_good = False
    
    # System info
    print(f"💻 System: {platform.system()} {platform.machine()}")
    
    # Required files
    required_files = [
        "uci.py",
        "monkfish.py", 
        "config.py",
        "uci_options.py",
        "MonkFish.sh"
    ]
    
    print("\n📁 Required files:")
    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (missing)")
            all_good = False
    
    # Stockfish
    print("\n⚡ Stockfish engine:")
    stockfish_names = ["stockfish", "stockfish.exe"]
    stockfish_found = False
    
    for name in stockfish_names:
        if os.path.exists(name):
            if os.access(name, os.X_OK):
                print(f"   ✅ {name} (executable)")
                stockfish_found = True
                break
            else:
                print(f"   ⚠️  {name} (not executable)")
    
    if not stockfish_found:
        print("   ❌ stockfish (not found)")
        print("   💡 Run 'python3 setup.py' to download automatically")
        all_good = False
    
    # Configuration
    print("\n⚙️  Configuration:")
    if os.path.exists("monkfish_config.json"):
        print("   ✅ monkfish_config.json")
    else:
        print("   ⚠️  monkfish_config.json (will be created automatically)")
    
    # Test imports
    print("\n📦 Python modules:")
    required_modules = [
        ("json", "JSON support"),
        ("subprocess", "Process management"), 
        ("re", "Regular expressions"),
        ("os", "Operating system interface")
    ]
    
    for module, description in required_modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} ({description})")
            all_good = False
    
    # Final result
    print("\n" + "=" * 35)
    if all_good:
        print("🎉 All requirements satisfied!")
        print("✨ MonkFish is ready to achieve enlightenment")
        return True
    else:
        print("💥 Some requirements are missing")
        print("🔧 Run 'python3 setup.py' to fix automatically")
        return False

if __name__ == "__main__":
    success = check_requirements()
    sys.exit(0 if success else 1)