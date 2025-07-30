#!/usr/bin/env python3
"""
MonkFish Setup Script
Automatically downloads Stockfish and sets up MonkFish for use
"""

import os
import sys
import platform
import urllib.request
import zipfile
import tarfile
import stat
import shutil

class MonkFishSetup:
    def __init__(self):
        self.system = platform.system().lower()
        self.arch = platform.machine().lower()
        self.stockfish_url = self._get_stockfish_url()
        self.stockfish_filename = self._get_stockfish_filename()
        
    def _get_stockfish_url(self):
        """Get the appropriate Stockfish download URL for this system"""
        base_url = "https://github.com/official-stockfish/Stockfish/releases/download/sf_16/"
        
        if self.system == "darwin":  # macOS
            if "arm" in self.arch or "aarch64" in self.arch:
                return f"{base_url}stockfish-macos-m1-apple-silicon.tar"
            else:
                return f"{base_url}stockfish-macos-x86-64-modern.tar"
        elif self.system == "linux":
            if "aarch64" in self.arch or "arm64" in self.arch:
                return f"{base_url}stockfish-ubuntu-x86-64-modern.tar"  # Fallback
            else:
                return f"{base_url}stockfish-ubuntu-x86-64-modern.tar"
        elif self.system == "windows":
            return f"{base_url}stockfish-windows-x86-64-modern.zip"
        else:
            raise Exception(f"Unsupported system: {self.system}")
    
    def _get_stockfish_filename(self):
        """Get the expected stockfish binary filename"""
        if self.system == "windows":
            return "stockfish.exe"
        else:
            return "stockfish"
    
    def check_python(self):
        """Check Python version"""
        print("🐍 Checking Python version...", end=" ")
        if sys.version_info < (3, 6):
            print("❌")
            print("Error: Python 3.6 or higher required")
            return False
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
        return True
    
    def check_permissions(self):
        """Check if we can write to current directory"""
        print("📁 Checking write permissions...", end=" ")
        try:
            test_file = "test_write_permission.tmp"
            with open(test_file, 'w') as f:
                f.write("test")
            os.remove(test_file)
            print("✅")
            return True
        except:
            print("❌")
            print("Error: Cannot write to current directory")
            return False
    
    def download_stockfish(self):
        """Download and extract Stockfish"""
        if os.path.exists(self.stockfish_filename):
            print(f"📦 Stockfish already exists at {self.stockfish_filename}")
            return True
        
        print(f"📥 Downloading Stockfish for {self.system}...")
        try:
            # Determine file extension
            if self.stockfish_url.endswith('.zip'):
                archive_name = "stockfish.zip"
            else:
                archive_name = "stockfish.tar"
            
            # Download with progress
            def progress_hook(count, block_size, total_size):
                percent = int(count * block_size * 100 / total_size)
                print(f"\r   Progress: {percent}%", end="", flush=True)
            
            urllib.request.urlretrieve(self.stockfish_url, archive_name, progress_hook)
            print("\n   ✅ Download complete")
            
            # Extract
            print("📂 Extracting Stockfish...", end=" ")
            if archive_name.endswith('.zip'):
                with zipfile.ZipFile(archive_name, 'r') as zip_ref:
                    zip_ref.extractall("temp_extract")
            else:
                with tarfile.open(archive_name, 'r') as tar_ref:
                    tar_ref.extractall("temp_extract")
            
            # Find and move the stockfish binary
            self._find_and_move_stockfish()
            
            # Cleanup
            os.remove(archive_name)
            shutil.rmtree("temp_extract", ignore_errors=True)
            
            print("✅")
            return True
            
        except Exception as e:
            print(f"❌ Failed to download Stockfish: {e}")
            return False
    
    def _find_and_move_stockfish(self):
        """Find stockfish binary in extracted files and move to root"""
        for root, dirs, files in os.walk("temp_extract"):
            for file in files:
                if file == self.stockfish_filename or (file == "stockfish" and self.system != "windows"):
                    src = os.path.join(root, file)
                    dst = self.stockfish_filename
                    shutil.move(src, dst)
                    
                    # Make executable on Unix systems
                    if self.system != "windows":
                        st = os.stat(dst)
                        os.chmod(dst, st.st_mode | stat.S_IEXEC)
                    
                    return
        
        raise Exception("Could not find stockfish binary in downloaded archive")
    
    def setup_shell_script(self):
        """Make sure shell script is executable"""
        print("🐚 Setting up shell script...", end=" ")
        try:
            if os.path.exists("MonkFish.sh"):
                if self.system != "windows":
                    st = os.stat("MonkFish.sh")
                    os.chmod("MonkFish.sh", st.st_mode | stat.S_IEXEC)
            print("✅")
            return True
        except Exception as e:
            print(f"❌ {e}")
            return False
    
    def test_engine(self):
        """Test that MonkFish engine works"""
        print("🧪 Testing MonkFish engine...", end=" ")
        try:
            import subprocess
            result = subprocess.run(
                [sys.executable, "uci.py"],
                input="uci\nquit\n",
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if "MonkFish" in result.stdout and "uciok" in result.stdout:
                print("✅")
                return True
            else:
                print("❌")
                print(f"Engine test failed. Output: {result.stdout}")
                return False
                
        except Exception as e:
            print(f"❌ {e}")
            return False
    
    def create_config_if_missing(self):
        """Create default config if it doesn't exist"""
        print("⚙️  Checking configuration...", end=" ")
        if not os.path.exists("monkfish_config.json"):
            # Config will be auto-created by the config module
            pass
        print("✅")
        return True
    
    def run_setup(self):
        """Run the complete setup process"""
        print("🐟 MonkFish Setup")
        print("=" * 40)
        
        steps = [
            self.check_python,
            self.check_permissions,
            self.download_stockfish,
            self.setup_shell_script,
            self.create_config_if_missing,
            self.test_engine
        ]
        
        for step in steps:
            if not step():
                print(f"\n💥 Setup failed at step: {step.__name__}")
                return False
        
        print("\n" + "=" * 40)
        print("🎉 MonkFish setup complete!")
        print("\nNext steps:")
        print("1. Open your chess GUI (like Cute Chess)")
        print("2. Add MonkFish as an engine:")
        print(f"   - Command: {os.path.abspath('MonkFish.sh')}")
        print(f"   - Working Directory: {os.path.abspath('.')}")
        print("   - Protocol: UCI")
        print("\nOr test from command line:")
        print("   python3 uci.py")
        print("\nThe path to chess enlightenment awaits! 🧘‍♂️")
        return True

if __name__ == "__main__":
    try:
        setup = MonkFishSetup()
        success = setup.run_setup()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nSetup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(1)