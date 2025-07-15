#!/usr/bin/env python3
"""Test script to verify the enhanced Break Reminder functionality."""

import sys
import os
import tempfile
import json
from datetime import datetime

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_config_manager():
    """Test the configuration manager."""
    print("Testing ConfigManager...")
    
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        config_file = f.name
    
    try:
        from src.core.config import ConfigManager
        
        # Test initialization
        config = ConfigManager(config_file)
        assert config.get("usual_start") == "08:00"
        assert config.get("theme") == "dark"
        print("✓ Default configuration loaded")
        
        # Test setting values
        config.set("usual_start", "09:00")
        config.set("theme", "light")
        config.save()
        
        # Test persistence
        config2 = ConfigManager(config_file)
        assert config2.get("usual_start") == "09:00"
        assert config2.get("theme") == "light"
        print("✓ Configuration persistence works")
        
        # Test update
        config2.update({"usual_start": "07:30", "debug_mode": True})
        assert config2.get("usual_start") == "07:30"
        assert config2.get("debug_mode") == True
        print("✓ Configuration update works")
        
        print("✅ ConfigManager tests passed!")
        
    except Exception as e:
        print(f"❌ ConfigManager test failed: {e}")
        return False
    finally:
        if os.path.exists(config_file):
            os.unlink(config_file)
    
    return True

def test_break_logic():
    """Test the break logic."""
    print("\\nTesting BreakLogic...")
    
    try:
        from src.core.break_logic import BreakLogic, BreakState
        
        # Test with default config
        config = {
            "usual_start": "08:00",
            "lunch_start": "12:00",
            "lunch_end": "13:00",
            "workday_length": "08:00",
            "break_points": [0.25, 0.75]
        }
        
        logic = BreakLogic(config)
        
        # Test state calculation
        state, info = logic.get_current_state()
        assert state in [BreakState.WORK, BreakState.BREAK, BreakState.LUNCH, BreakState.DONE]
        assert "message" in info
        assert "time_left" in info
        print("✓ State calculation works")
        
        # Test configuration update
        new_config = config.copy()
        new_config["usual_start"] = "09:00"
        logic.update_config(new_config)
        print("✓ Configuration update works")
        
        # Test time calculations
        time_left = logic.get_time_until_next_event()
        assert time_left is None or isinstance(time_left, int)
        print("✓ Time calculations work")
        
        print("✅ BreakLogic tests passed!")
        
    except Exception as e:
        print(f"❌ BreakLogic test failed: {e}")
        return False
    
    return True

def test_style_manager():
    """Test the style manager."""
    print("\\nTesting StyleManager...")
    
    try:
        from src.ui.styles import StyleManager, Theme
        
        # Test dark theme
        style_mgr = StyleManager(Theme.DARK)
        assert style_mgr.theme == Theme.DARK
        
        main_style = style_mgr.get_style("main_window")
        assert "background:" in main_style
        assert "border-radius:" in main_style
        print("✓ Dark theme styling works")
        
        # Test light theme
        style_mgr.set_theme(Theme.LIGHT)
        assert style_mgr.theme == Theme.LIGHT
        
        main_style = style_mgr.get_style("main_window")
        assert "background:" in main_style
        print("✓ Light theme styling works")
        
        # Test status colors
        work_color = style_mgr.get_status_color("work")
        assert work_color.startswith("#")
        print("✓ Status colors work")
        
        print("✅ StyleManager tests passed!")
        
    except Exception as e:
        print(f"❌ StyleManager test failed: {e}")
        return False
    
    return True

def test_imports():
    """Test that all modules can be imported."""
    print("\\nTesting module imports...")
    
    try:
        # Test core imports
        from src.core.config import ConfigManager
        from src.core.break_logic import BreakLogic, BreakState
        print("✓ Core modules imported")
        
        # Test UI imports (may fail without Qt)
        try:
            from src.ui.styles import StyleManager, Theme
            print("✓ UI styles module imported")
        except ImportError as e:
            print(f"⚠ UI styles import failed (expected without Qt): {e}")
        
        # Test main module
        from src.main import BreakReminderApp
        print("✓ Main application module imported")
        
        print("✅ Import tests passed!")
        
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests."""
    print("Break Reminder Enhanced - Test Suite")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_config_manager,
        test_break_logic,
        test_style_manager,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            failed += 1
    
    print("\\n" + "=" * 50)
    print(f"Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The enhanced Break Reminder is ready to use.")
    else:
        print("⚠ Some tests failed. Please check the output above.")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())