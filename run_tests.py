#!/usr/bin/env python3
"""
MonkFish Test Runner
Runs all tests and provides a summary report
"""

import unittest
import sys
import time
import os
from io import StringIO

def run_test_suite():
    """Run all MonkFish tests and return results"""
    
    # Test modules to run (in tests/ directory)
    test_modules = [
        'tests.test_config',
        'tests.test_uci_options', 
        'tests.test_uci_protocol',
        'tests.test_philosophy',
        'tests.test_positions'
    ]
    
    print("🐟 MonkFish Test Suite")
    print("=" * 50)
    
    total_tests = 0
    total_failures = 0
    total_errors = 0
    
    for module in test_modules:
        print(f"\n📋 Running {module}...")
        
        # Capture test output
        test_output = StringIO()
        
        # Load and run tests
        try:
            # Add current directory to path for imports
            current_dir = os.path.dirname(os.path.abspath(__file__))
            if current_dir not in sys.path:
                sys.path.insert(0, current_dir)
            
            suite = unittest.TestLoader().loadTestsFromName(module)
            runner = unittest.TextTestRunner(
                stream=test_output,
                verbosity=2,
                buffer=True
            )
            
            start_time = time.time()
            result = runner.run(suite)
            end_time = time.time()
            
            # Update totals
            total_tests += result.testsRun
            total_failures += len(result.failures)
            total_errors += len(result.errors)
            
            # Print summary for this module
            status = "✅ PASS" if result.wasSuccessful() else "❌ FAIL"
            duration = end_time - start_time
            
            print(f"   {status} - {result.testsRun} tests in {duration:.2f}s")
            
            if not result.wasSuccessful():
                print(f"   Failures: {len(result.failures)}, Errors: {len(result.errors)}")
                
                # Show failure details
                for test, traceback in result.failures:
                    print(f"   FAILURE: {test}")
                    print(f"   {traceback.split('AssertionError:')[-1].strip()}")
                
                for test, traceback in result.errors:
                    print(f"   ERROR: {test}")
                    print(f"   {traceback.split('Exception')[-1].strip()}")
        
        except ImportError as e:
            print(f"   ⚠️  SKIP - Could not import {module}: {e}")
        except Exception as e:
            print(f"   ❌ ERROR - Failed to run {module}: {e}")
            total_errors += 1
    
    # Final summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_tests - total_failures - total_errors}")
    print(f"Failed: {total_failures}")
    print(f"Errors: {total_errors}")
    
    if total_failures == 0 and total_errors == 0:
        print("\n🎉 All tests passed! MonkFish is ready for enlightenment.")
        return 0
    else:
        print(f"\n💥 {total_failures + total_errors} test(s) failed. The path to zen requires debugging.")
        return 1

def run_quick_test():
    """Run a quick smoke test to verify basic functionality"""
    print("🚀 Quick Smoke Test")
    print("-" * 30)
    
    try:
        # Add current directory to Python path for imports
        current_dir = os.path.dirname(os.path.abspath(__file__))
        if current_dir not in sys.path:
            sys.path.insert(0, current_dir)
        
        # Test imports
        print("Importing modules...", end=" ")
        from config import MonkFishConfig
        from uci_options import UCIOptions
        from monkfish import MonkFishParser
        print("✅")
        
        # Test config
        print("Testing config...", end=" ")
        config = MonkFishConfig()
        assert config.get_skill_level() is not None
        print("✅")
        
        # Test UCI options
        print("Testing UCI options...", end=" ")
        uci_opts = UCIOptions(config)
        assert len(uci_opts.get_option_strings()) > 0
        print("✅")
        
        print("\n✨ Smoke test passed! Core functionality works.")
        return True
        
    except Exception as e:
        print(f"\n💥 Smoke test failed: {e}")
        return False

if __name__ == "__main__":
    print("Choose test mode:")
    print("1. Quick smoke test (fast)")
    print("2. Full test suite (thorough)")
    print("3. Both")
    
    choice = input("Enter choice (1-3): ").strip()
    
    if choice == "1":
        success = run_quick_test()
        sys.exit(0 if success else 1)
    elif choice == "2":
        sys.exit(run_test_suite())
    elif choice == "3":
        print("\n" + "=" * 60)
        quick_success = run_quick_test()
        print("\n" + "=" * 60)
        if quick_success:
            suite_result = run_test_suite()
            sys.exit(suite_result)
        else:
            print("Skipping full suite due to smoke test failure.")
            sys.exit(1)
    else:
        print("Invalid choice. Running quick test by default.")
        success = run_quick_test()
        sys.exit(0 if success else 1)