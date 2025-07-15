#!/usr/bin/env python3
"""Test script to check for CSS warnings in the Break Reminder application."""

import sys
import os
import io
import contextlib

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.styles import StyleManager, Theme


def test_css_warnings():
    """Test that CSS warnings are not generated."""
    # Capture stderr to check for warnings
    stderr_capture = io.StringIO()
    
    with contextlib.redirect_stderr(stderr_capture):
        # Create style manager and test both themes
        dark_style = StyleManager(Theme.DARK)
        light_style = StyleManager(Theme.LIGHT)
        
        # Test getting all styles
        test_elements = [
            "main_window", "main_window_hover", "main_label", "title_label",
            "button_base", "debug_button", "close_button", "settings_button",
            "dialog_base", "dialog_label", "dialog_input", "dialog_button"
        ]
        
        for element in test_elements:
            dark_css = dark_style.get_style(element)
            light_css = light_style.get_style(element)
            
            # Check for known unsupported properties
            unsupported_props = [
                "box-shadow", "content", "transition", "transform", 
                "line-height", "letter-spacing"
            ]
            
            for prop in unsupported_props:
                if prop in dark_css:
                    print(f"ERROR: Found unsupported property '{prop}' in dark theme {element}")
                    return False
                if prop in light_css:
                    print(f"ERROR: Found unsupported property '{prop}' in light theme {element}")
                    return False
    
    # Check if any warnings were captured
    warnings = stderr_capture.getvalue()
    if warnings:
        print(f"Warnings found: {warnings}")
        return False
    
    print("✓ No CSS warnings found!")
    return True


if __name__ == "__main__":
    success = test_css_warnings()
    sys.exit(0 if success else 1)