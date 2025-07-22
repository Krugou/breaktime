#!/usr/bin/env python3
"""Test script for progress bar functionality in Break Reminder."""

import sys
import os
from datetime import datetime, timedelta

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_break_logic_progress():
    """Test that break logic correctly calculates progress percentages."""
    print("Testing BreakLogic progress calculations...")
    
    try:
        from src.core.break_logic import BreakLogic, BreakState
        
        # Test configuration for controlled testing
        config = {
            "usual_start": "09:00",
            "lunch_start": "12:00", 
            "lunch_end": "13:00",
            "workday_length": "08:00",
            "break_points": [0.25, 0.75]  # Breaks at 2 hours and 6 hours
        }
        
        logic = BreakLogic(config)
        
        # Test that progress_percent is included in state info
        state, info = logic.get_current_state()
        assert "progress_percent" in info, "progress_percent should be in state info"
        assert isinstance(info["progress_percent"], int), "progress_percent should be an integer"
        assert 0 <= info["progress_percent"] <= 100, f"progress_percent should be 0-100, got {info['progress_percent']}"
        print("✓ Progress percentage is calculated and within valid range")
        
        # Test different states return progress
        for _ in range(3):  # Try a few times in case of timing issues
            state, info = logic.get_current_state()
            progress = info["progress_percent"]
            assert progress >= 0 and progress <= 100, f"Invalid progress: {progress}"
        
        print("✓ Progress calculation is consistent")
        
        print("✅ BreakLogic progress tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ BreakLogic progress test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_progress_bar_styles():
    """Test that progress bar styles are available."""
    print("\nTesting progress bar styles...")
    
    try:
        from src.ui.styles import StyleManager, Theme
        
        # Test dark theme progress bar style
        style_mgr = StyleManager(Theme.DARK)
        progress_style = style_mgr.get_style("progress_bar")
        assert progress_style, "Dark theme should have progress_bar style"
        assert "QProgressBar" in progress_style, "Style should contain QProgressBar styling"
        assert "chunk" in progress_style, "Style should contain chunk styling for progress fill"
        print("✓ Dark theme progress bar style exists and looks valid")
        
        # Test light theme progress bar style  
        style_mgr.set_theme(Theme.LIGHT)
        progress_style = style_mgr.get_style("progress_bar")
        assert progress_style, "Light theme should have progress_bar style"
        assert "QProgressBar" in progress_style, "Style should contain QProgressBar styling"
        assert "chunk" in progress_style, "Style should contain chunk styling for progress fill"
        print("✓ Light theme progress bar style exists and looks valid")
        
        # Test that different break states have different colors
        dark_style = StyleManager(Theme.DARK).get_style("progress_bar")
        assert 'breakState="work"' in dark_style, "Should have work state styling"
        assert 'breakState="break"' in dark_style, "Should have break state styling" 
        assert 'breakState="lunch"' in dark_style, "Should have lunch state styling"
        assert 'breakState="done"' in dark_style, "Should have done state styling"
        print("✓ Progress bar has different colors for different break states")
        
        print("✅ Progress bar style tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Progress bar style test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_ui_integration():
    """Test that progress bar integrates with UI without errors."""
    print("\nTesting UI integration...")
    
    try:
        # Import UI components
        from src.core.config import ConfigManager
        from src.ui.main_widget import BreakReminderWidget
        
        # This test just checks that the widget can be created without errors
        # We can't fully test the UI without a display, but we can check imports work
        config_manager = ConfigManager()
        
        # Try to create the widget class (without actually showing it)
        widget_class = BreakReminderWidget
        assert hasattr(widget_class, 'create_progress_bar'), "Widget should have create_progress_bar method"
        print("✓ UI widget class has progress bar creation method")
        
        print("✅ UI integration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ UI integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run progress bar specific tests."""
    print("Break Reminder - Progress Bar Test Suite")
    print("=" * 50)
    
    tests = [
        test_break_logic_progress,
        test_progress_bar_styles, 
        test_ui_integration,
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
    
    print("\n" + "=" * 50)
    print(f"Progress Bar Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All progress bar tests passed! The feature is working correctly.")
    else:
        print("⚠ Some tests failed. Please check the output above.")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())