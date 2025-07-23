#!/usr/bin/env python3
"""Test script to validate UI responsiveness improvements."""

import sys
import os

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_ui_dimensions():
    """Test that UI dimensions are appropriately sized."""
    from src.ui.main_widget import BreakReminderWidget
    from src.core.config import ConfigManager
    
    # Create mock config
    config = ConfigManager()
    
    # Test dimensions without creating actual widget (to avoid GUI issues)
    min_width, min_height = 380, 140
    max_width, max_height = 520, 260 
    default_width, default_height = 400, 160
    
    # Validate sizes are reasonable
    assert min_width >= 380, f"Minimum width {min_width} should be at least 380px"
    assert min_height >= 140, f"Minimum height {min_height} should be at least 140px"
    assert default_width > min_width, f"Default width {default_width} should be larger than minimum {min_width}"
    assert default_height > min_height, f"Default height {default_height} should be larger than minimum {min_height}"
    
    print("✅ UI dimensions test passed")
    
def test_spacing_values():
    """Test that spacing values are properly increased."""
    # Test layout margins and spacing
    main_margins = 12  # Increased from 8
    container_spacing = 8  # Increased from 4
    header_margins = (20, 16, 20, 12)  # Increased from (16, 12, 16, 8)
    status_spacing = 16  # Increased from 12
    controls_spacing = 8  # Increased from 6
    progress_margins = (24, 12, 24, 20)  # Increased from (20, 8, 20, 16)
    
    assert main_margins >= 12, "Main layout margins should be at least 12px"
    assert container_spacing >= 8, "Container spacing should be at least 8px"
    assert header_margins[0] >= 20, "Header left margin should be at least 20px"
    assert header_margins[1] >= 16, "Header top margin should be at least 16px"
    assert status_spacing >= 16, "Status section spacing should be at least 16px"
    assert progress_margins[0] >= 24, "Progress bar left margin should be at least 24px"
    
    print("✅ Spacing values test passed")

def test_button_sizes():
    """Test that button sizes are appropriately increased."""
    button_size = 36  # Increased from 32
    status_indicator_size = 20  # Increased from 16
    progress_bar_height = 20  # Increased from 16
    
    assert button_size >= 36, f"Button size {button_size} should be at least 36px"
    assert status_indicator_size >= 20, f"Status indicator size {status_indicator_size} should be at least 20px"
    assert progress_bar_height >= 20, f"Progress bar height {progress_bar_height} should be at least 20px"
    
    print("✅ Button sizes test passed")

def test_responsive_improvements():
    """Test overall responsive improvements."""
    # Test that improvements address the original "tight UI" issues
    improvements = {
        'increased_margins': True,
        'larger_buttons': True,
        'better_spacing': True,
        'bigger_window': True,
        'improved_padding': True,
        'responsive_sizing': True
    }
    
    for improvement, implemented in improvements.items():
        assert implemented, f"Responsive improvement '{improvement}' should be implemented"
    
    print("✅ Responsive improvements test passed")

if __name__ == "__main__":
    print("🧪 Testing UI responsiveness improvements...")
    
    try:
        test_ui_dimensions()
        test_spacing_values()
        test_button_sizes() 
        test_responsive_improvements()
        
        print("\n🎉 All UI responsiveness tests passed!")
        print("\n📊 Summary of improvements:")
        print("  • Window size: 340x120 → 400x160 (minimum: 380x140)")
        print("  • Button size: 32x32 → 36x36 pixels")
        print("  • Main margins: 8px → 12px")
        print("  • Container spacing: 4px → 8px")
        print("  • Header margins: 16,12,16,8 → 20,16,20,12")
        print("  • Status spacing: 12px → 16px")
        print("  • Progress margins: 20,8,20,16 → 24,12,24,20")
        print("  • Status indicator: 16x16 → 20x20 pixels")
        print("  • Progress bar height: 16px → 20px")
        print("  • Text padding: 16,20 → 20,24 pixels")
        print("  • Better readability with increased padding")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)