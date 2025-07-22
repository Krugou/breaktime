"""Break reminder logic and time management."""

import random
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict, Any
from enum import Enum


class BreakState(Enum):
    """Enumeration of possible break states."""
    WORK = "work"
    BREAK = "break"
    LUNCH = "lunch"
    DONE = "done"


class BreakLogic:
    """Handles break reminder logic and time calculations."""
    
    FINNISH_FUNNY_MESSAGES = [
        "Työpäivä ohi! Nyt kahville!",
        "Valmista tuli, mene vaikka ulos haukkaamaan happea!",
        "Työt tehty, nyt voi ottaa rennosti!",
        "Nyt on aika sulkea läppäri ja avata elämä!",
        "Työpäivä paketissa – ansaittu tauko!",
        "Voit vihdoin lakata teeskentelemästä kiireistä!",
        "Nyt on lupa olla tekemättä mitään!",
        "Työpäivä ohi, muista venytellä!",
        "Nyt vaikka saunaan!",
        "Hyvää työtä, nyt huilaamaan!"
    ]
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize break logic with configuration.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.start_time = None
        self.lunch_start = None
        self.lunch_end = None
        self.workday_end = None
        self.break_times = []
        self.next_break_idx = 0
        self.close_timer_started = False
        
        self._setup_times()
    
    def _setup_times(self) -> None:
        """Setup work times based on configuration."""
        # Get today's date
        today = datetime.now().date()
        
        # Parse start time
        start_str = self.config.get("usual_start", "08:00")
        self.start_time = datetime.combine(today, datetime.strptime(start_str, '%H:%M').time())
        
        # Parse lunch times
        lunch_start_str = self.config.get("lunch_start", "10:45")
        lunch_end_str = self.config.get("lunch_end", "12:30")
        self.lunch_start = datetime.combine(today, datetime.strptime(lunch_start_str, '%H:%M').time())
        self.lunch_end = datetime.combine(today, datetime.strptime(lunch_end_str, '%H:%M').time())
        
        # Parse workday length
        workday_length_str = self.config.get("workday_length", "08:00")
        if ":" in workday_length_str:
            hours, minutes = map(int, workday_length_str.split(":"))
        else:
            hours, minutes = int(workday_length_str), 0
        
        workday_length = timedelta(hours=hours, minutes=minutes)
        self.workday_end = self.start_time + workday_length
        
        # Calculate break times
        break_points = self.config.get("break_points", [0.25, 0.75])
        total_hours = workday_length.total_seconds() / 3600
        self.break_times = [
            self.start_time + timedelta(hours=total_hours * point) 
            for point in break_points
        ]
    
    def get_current_state(self) -> Tuple[BreakState, Dict[str, Any]]:
        """Get current break state and related information.
        
        Returns:
            Tuple of (state, info_dict) where info_dict contains:
            - message: Display message
            - time_left: Minutes until next event
            - next_event: Description of next event
            - progress_percent: Progress percentage (0-100) until next event
            - debug_info: Debug information if enabled
        """
        now = datetime.now()
        info = {"debug_info": self._get_debug_info(now)}
        
        # Check if workday is over
        if now >= self.workday_end:
            info.update({
                "message": f"🎉 {random.choice(self.FINNISH_FUNNY_MESSAGES)}",
                "time_left": 0,
                "next_event": "Workday complete",
                "progress_percent": 100
            })
            return BreakState.DONE, info
        
        # Check if in lunch break window
        if self.lunch_start <= now <= self.lunch_end:
            time_left = int((self.lunch_end - now).total_seconds() // 60)
            total_lunch_time = int((self.lunch_end - self.lunch_start).total_seconds() // 60)
            elapsed_lunch_time = total_lunch_time - time_left
            progress_percent = int((elapsed_lunch_time / total_lunch_time) * 100) if total_lunch_time > 0 else 0
            
            info.update({
                "message": f"🍽️ Lunch break!\n⏰ {time_left} minutes left",
                "time_left": time_left,
                "next_event": "End of lunch break",
                "progress_percent": progress_percent
            })
            return BreakState.LUNCH, info
        
        # Check regular breaks
        while self.next_break_idx < len(self.break_times) and now > self.break_times[self.next_break_idx]:
            self.next_break_idx += 1
        
        if self.next_break_idx < len(self.break_times):
            next_break = self.break_times[self.next_break_idx]
            time_left = int((next_break - now).total_seconds() // 60)
            
            # Calculate progress based on time segment
            if self.next_break_idx == 0:
                # Progress from start to first break
                segment_start = self.start_time
            else:
                # Progress from previous break to next break
                segment_start = self.break_times[self.next_break_idx - 1]
            
            total_segment_time = int((next_break - segment_start).total_seconds() // 60)
            elapsed_segment_time = int((now - segment_start).total_seconds() // 60)
            progress_percent = int((elapsed_segment_time / total_segment_time) * 100) if total_segment_time > 0 else 0
            progress_percent = max(0, min(100, progress_percent))  # Clamp to 0-100
            
            # Check if we're at break time (within 5 minutes)
            if time_left <= 5 and time_left >= 0:
                info.update({
                    "message": f"☕ Break time!\n⏰ {next_break.strftime('%H:%M')} ({time_left} min)",
                    "time_left": time_left,
                    "next_event": "Break time",
                    "progress_percent": progress_percent
                })
                return BreakState.BREAK, info
            else:
                info.update({
                    "message": f"💼 Next break: {next_break.strftime('%H:%M')}\n⏰ {time_left} minutes to go",
                    "time_left": time_left,
                    "next_event": f"Break at {next_break.strftime('%H:%M')}",
                    "progress_percent": progress_percent
                })
                return BreakState.WORK, info
        else:
            # No more breaks, show time until workday end
            time_left = int((self.workday_end - now).total_seconds() // 60)
            hours_left = time_left // 60
            mins_remaining = time_left % 60
            
            # Calculate progress from last break (or start if no breaks taken) to end
            if len(self.break_times) > 0 and self.next_break_idx > 0:
                # Progress from last break to end of workday
                segment_start = self.break_times[-1]
            else:
                # Progress from start to end of workday (no breaks taken yet)
                segment_start = self.start_time
            
            total_segment_time = int((self.workday_end - segment_start).total_seconds() // 60)
            elapsed_segment_time = int((now - segment_start).total_seconds() // 60)
            progress_percent = int((elapsed_segment_time / total_segment_time) * 100) if total_segment_time > 0 else 0
            progress_percent = max(0, min(100, progress_percent))  # Clamp to 0-100
            
            if hours_left > 0:
                time_str = f"{hours_left}h {mins_remaining}m"
            else:
                time_str = f"{mins_remaining}m"
            
            info.update({
                "message": f"🏁 No more breaks today!\n⏰ {time_str} until home time",
                "time_left": time_left,
                "next_event": "End of workday",
                "progress_percent": progress_percent
            })
            return BreakState.WORK, info
    
    def _get_debug_info(self, now: datetime) -> List[str]:
        """Get debug information for current state.
        
        Args:
            now: Current datetime
            
        Returns:
            List of debug information strings
        """
        debug_lines = [
            f"📅 Now: {now.strftime('%Y-%m-%d %H:%M:%S')}",
            f"🚀 Start: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}",
            f"🏁 Workday end: {self.workday_end.strftime('%Y-%m-%d %H:%M:%S')}",
            f"🍽️ Lunch: {self.lunch_start.strftime('%H:%M')} - {self.lunch_end.strftime('%H:%M')}"
        ]
        
        if self.next_break_idx < len(self.break_times):
            next_break = self.break_times[self.next_break_idx]
            debug_lines.append(f"☕ Next break: {next_break.strftime('%Y-%m-%d %H:%M:%S')}")
        else:
            debug_lines.append("☕ Next break: N/A")
        
        return debug_lines
    
    def update_config(self, config: Dict[str, Any]) -> None:
        """Update configuration and recalculate times.
        
        Args:
            config: New configuration dictionary
        """
        self.config = config
        self._setup_times()
        self.next_break_idx = 0  # Reset break index
    
    def get_time_until_next_event(self) -> Optional[int]:
        """Get minutes until next significant event.
        
        Returns:
            Minutes until next event, or None if no events
        """
        _, info = self.get_current_state()
        return info.get("time_left")
    
    def is_workday_complete(self) -> bool:
        """Check if the workday is complete.
        
        Returns:
            True if workday is over, False otherwise
        """
        return datetime.now() >= self.workday_end