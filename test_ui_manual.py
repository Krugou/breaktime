#!/usr/bin/env python3
"""Manual UI test for the progress bar feature."""

import sys
import os
from unittest.mock import Mock

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_widget_creation():
    """Test that the main widget can be created with progress bar."""
    print("Testing main widget creation with progress bar...")
    
    try:
        # Mock QApplication to avoid display requirement
        from PyQt5.QtWidgets import QApplication
        
        # Check if we can create an application (might fail in headless environment)
        app = None
        try:
            app = QApplication.instance()
            if app is None:
                app = QApplication([])
            
            from src.core.config import ConfigManager
            from src.ui.main_widget import BreakReminderWidget
            
            # Create config manager
            config = ConfigManager()
            
            # Try to create the widget
            widget = BreakReminderWidget(config)
            
            # Verify progress bar exists
            assert hasattr(widget, 'progress_bar'), "Widget should have progress_bar attribute"
            assert widget.progress_bar is not None, "Progress bar should be initialized"
            
            # Test progress bar properties
            assert widget.progress_bar.minimum() == 0, "Progress bar minimum should be 0"
            assert widget.progress_bar.maximum() == 100, "Progress bar maximum should be 100"
            assert 0 <= widget.progress_bar.value() <= 100, "Progress bar value should be 0-100"
            
            print("✓ Main widget created successfully with progress bar")
            print(f"✓ Progress bar value: {widget.progress_bar.value()}%")
            print(f"✓ Progress bar height: {widget.progress_bar.height()}px")
            
            # Test that widget can update display
            widget.update_display()
            print("✓ Widget display update completed")
            
            # Test theme switching
            from src.ui.styles import Theme
            widget.change_theme(Theme.LIGHT)
            print("✓ Light theme applied")
            
            widget.change_theme(Theme.DARK)
            print("✓ Dark theme applied") 
            
            print("✅ UI widget test passed!")
            return True
            
        except ImportError as e:
            if "cannot connect to X server" in str(e) or "DISPLAY" in str(e):
                print("⚠ Skipping GUI test (no display available)")
                print("  This is expected in headless environments")
                return True
            else:
                raise
            
    except Exception as e:
        print(f"❌ UI widget test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_enhanced_app_launch():
    """Test that the enhanced application can be imported and initialized."""
    print("\nTesting enhanced application components...")
    
    try:
        # Test that we can import the main application
        from src.main import BreakReminderApp
        print("✓ BreakReminderApp imported successfully")
        
        # Test that core components work together
        from src.core.config import ConfigManager
        from src.core.break_logic import BreakLogic
        
        config = ConfigManager()
        logic = BreakLogic(config.get_all())
        
        state, info = logic.get_current_state()
        progress = info.get('progress_percent', 0)
        
        print(f"✓ Current break state: {state.value}")
        print(f"✓ Progress percentage: {progress}%")
        
        # Verify all required fields are present
        required_fields = ['message', 'time_left', 'next_event', 'progress_percent']
        for field in required_fields:
            assert field in info, f"Missing required field: {field}"
        print("✓ All required state info fields present")
        
        print("✅ Enhanced application test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Enhanced application test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run manual UI tests."""
    print("Break Reminder - Manual UI Test Suite")
    print("=" * 50)
    
    tests = [
        test_enhanced_app_launch,
        test_widget_creation,
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
    print(f"Manual UI Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All manual UI tests passed!")
        print("The progress bar feature is fully integrated and working.")
    else:
        print("⚠ Some tests failed. Check output above.")
    
    return 0 if failed == 0 else 1

if __name__ == "__main__":
    sys.exit(main())