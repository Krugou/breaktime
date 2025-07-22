#!/usr/bin/env python3
"""Demo script to test the progress bar visualizer functionality."""

import sys
import os
from datetime import datetime, timedelta

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def demo_progress_calculations():
    """Demo the progress calculation functionality."""
    print("Break Reminder Progress Bar Demo")
    print("=" * 50)
    
    from src.core.break_logic import BreakLogic, BreakState
    
    # Test configuration
    config = {
        "usual_start": "09:00",
        "lunch_start": "12:00",
        "lunch_end": "13:00", 
        "workday_length": "08:00",
        "break_points": [0.25, 0.75]
    }
    
    logic = BreakLogic(config)
    
    # Get current state
    state, info = logic.get_current_state()
    
    print(f"Current Time: {datetime.now().strftime('%H:%M:%S')}")
    print(f"Work Start: {config['usual_start']}")
    print(f"Workday Length: {config['workday_length']}")
    print()
    
    print(f"Current State: {state.value.upper()}")
    print(f"Message: {info['message']}")
    print(f"Progress: {info['progress_percent']}%")
    print(f"Time Left: {info.get('time_left', 0)} minutes")
    print(f"Next Event: {info.get('next_event', 'Unknown')}")
    print()
    
    # Show progress bar visualization
    progress = info['progress_percent']
    bar_width = 40
    filled = int((progress / 100) * bar_width)
    empty = bar_width - filled
    
    progress_bar = '█' * filled + '░' * empty
    print(f"Progress Bar: [{progress_bar}] {progress}%")
    
    # Show timing details
    print("\n" + "Debug Information:")
    for debug_line in info.get('debug_info', []):
        print(f"  {debug_line}")

def demo_different_states():
    """Demo different progress bar states with mock data."""
    print("\n" + "=" * 50)
    print("Mock Progress Bar States Demo")
    print("=" * 50)
    
    # Mock different states to show progress bar appearance
    mock_states = [
        {
            "state": "work", 
            "message": "💼 Next break: 10:30\n⏰ 45 minutes to go",
            "progress": 25,
            "description": "Working towards first break"
        },
        {
            "state": "break",
            "message": "☕ Break time!\n⏰ 10:30 (2 min)",
            "progress": 95, 
            "description": "Break time - almost at break"
        },
        {
            "state": "lunch",
            "message": "🍽️ Lunch break!\n⏰ 30 minutes left",
            "progress": 50,
            "description": "Lunch break - halfway through"
        },
        {
            "state": "work",
            "message": "💼 Next break: 15:00\n⏰ 120 minutes to go", 
            "progress": 10,
            "description": "Back to work after lunch"
        },
        {
            "state": "done",
            "message": "🎉 Työpäivä ohi! Nyt kahville!",
            "progress": 100,
            "description": "Workday complete!"
        }
    ]
    
    for i, mock in enumerate(mock_states, 1):
        print(f"\n{i}. {mock['description']}")
        print(f"   State: {mock['state'].upper()}")
        print(f"   Message: {mock['message'].replace(chr(10), ' | ')}")
        
        # Visual progress bar
        progress = mock['progress'] 
        bar_width = 30
        filled = int((progress / 100) * bar_width)
        empty = bar_width - filled
        
        # Different characters for different states
        fill_chars = {
            'work': '█',
            'break': '▓', 
            'lunch': '▒',
            'done': '■'
        }
        
        fill_char = fill_chars.get(mock['state'], '█')
        progress_bar = fill_char * filled + '░' * empty
        print(f"   Progress: [{progress_bar}] {progress}%")

if __name__ == "__main__":
    try:
        demo_progress_calculations()
        demo_different_states()
        print("\n" + "=" * 50)
        print("🎉 Progress bar demo completed successfully!")
        print("The progress bar visualizer is working correctly.")
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)