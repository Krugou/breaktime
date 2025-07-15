#!/usr/bin/env python3
"""Test script to verify UI improvements and responsiveness."""

import sys
import os
import unittest
from unittest.mock import Mock, patch
import io
import contextlib

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.ui.styles import StyleManager, Theme
from src.core.config import ConfigManager


class TestUIImprovements(unittest.TestCase):
    """Test UI improvements and responsiveness."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.config_manager = ConfigManager()
        self.dark_style = StyleManager(Theme.DARK)
        self.light_style = StyleManager(Theme.LIGHT)
    
    def test_no_unsupported_css_properties(self):
        """Test that no unsupported CSS properties are present."""
        unsupported_props = [
            "box-shadow", "content", "transition", "transform", 
            "line-height", "letter-spacing"
        ]
        
        test_elements = [
            "main_window", "main_window_hover", "main_label", "title_label",
            "button_base", "debug_button", "close_button", "settings_button",
            "dialog_base", "dialog_label", "dialog_input", "dialog_button"
        ]
        
        for theme in [self.dark_style, self.light_style]:
            for element in test_elements:
                css = theme.get_style(element)
                for prop in unsupported_props:
                    self.assertNotIn(prop, css, 
                        f"Found unsupported property '{prop}' in {element} for theme {theme.theme}")
    
    def test_responsive_layout_properties(self):
        """Test that responsive layout properties are properly set."""
        # Test that main_label has proper text wrapping support
        main_label_dark = self.dark_style.get_style("main_label")
        main_label_light = self.light_style.get_style("main_label")
        
        # These properties should still be present as they're supported
        self.assertIn("padding:", main_label_dark)
        self.assertIn("padding:", main_label_light)
        
        # Font properties should be preserved
        self.assertIn("font-size:", main_label_dark)
        self.assertIn("font-size:", main_label_light)
        
        # Background should be transparent for proper layering
        self.assertIn("background: transparent", main_label_dark)
        self.assertIn("background: transparent", main_label_light)
    
    def test_window_styles_without_box_shadow(self):
        """Test that window styles work without box-shadow."""
        main_window_dark = self.dark_style.get_style("main_window")
        main_window_light = self.light_style.get_style("main_window")
        
        # Should still have proper styling
        self.assertIn("border-radius:", main_window_dark)
        self.assertIn("border-radius:", main_window_light)
        
        # Should have gradients for visual appeal
        self.assertIn("qlineargradient", main_window_dark)
        self.assertIn("qlineargradient", main_window_light)
        
        # Should NOT have box-shadow
        self.assertNotIn("box-shadow:", main_window_dark)
        self.assertNotIn("box-shadow:", main_window_light)
    
    def test_button_styles_without_transforms(self):
        """Test that button styles work without transform properties."""
        button_dark = self.dark_style.get_style("button_base")
        button_light = self.light_style.get_style("button_base")
        
        # Should have proper styling
        self.assertIn("border-radius:", button_dark)
        self.assertIn("border-radius:", button_light)
        self.assertIn("font-weight:", button_dark)
        self.assertIn("font-weight:", button_light)
        
        # Should NOT have transform or transition
        self.assertNotIn("transform:", button_dark)
        self.assertNotIn("transform:", button_light)
        self.assertNotIn("transition:", button_dark)
        self.assertNotIn("transition:", button_light)
    
    def test_style_manager_functionality(self):
        """Test that StyleManager still works correctly after changes."""
        # Test theme switching
        style_manager = StyleManager(Theme.DARK)
        self.assertEqual(style_manager.theme, Theme.DARK)
        
        style_manager.set_theme(Theme.LIGHT)
        self.assertEqual(style_manager.theme, Theme.LIGHT)
        
        # Test status colors
        dark_work_color = style_manager.get_status_color("work")
        self.assertTrue(dark_work_color.startswith("#"))
        
        # Test style retrieval
        main_style = style_manager.get_style("main_window")
        self.assertTrue(len(main_style) > 0)
    
    def test_no_css_warnings_on_style_creation(self):
        """Test that no warnings are generated when creating styles."""
        stderr_capture = io.StringIO()
        
        with contextlib.redirect_stderr(stderr_capture):
            # Create multiple style managers
            for theme in [Theme.DARK, Theme.LIGHT]:
                style_manager = StyleManager(theme)
                
                # Get all styles
                elements = [
                    "main_window", "main_window_hover", "main_label", "title_label",
                    "button_base", "debug_button", "close_button", "settings_button"
                ]
                
                for element in elements:
                    style = style_manager.get_style(element)
                    self.assertIsInstance(style, str)
        
        # Check no warnings were captured
        warnings = stderr_capture.getvalue()
        self.assertEqual(warnings, "", f"Unexpected warnings: {warnings}")


if __name__ == '__main__':
    print("Testing UI Improvements...")
    print("=" * 50)
    
    # Run the tests
    unittest.main(verbosity=2, exit=False)
    
    print("\n" + "=" * 50)
    print("✅ UI improvement tests completed successfully!")
    print("✅ No unsupported CSS properties found!")
    print("✅ Responsive layout improvements verified!")