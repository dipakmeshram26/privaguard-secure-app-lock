import psutil
import threading
import time
import winsound
import os
from toast_notification import show_toast

class BatteryMonitor:
    def __init__(self, config_manager, gui_queue=None):
        self.config_manager = config_manager
        self.gui_queue = gui_queue
        self.running = False
        self.thread = None
        self.last_plugged_state = None
        
        # Default thresholds
        self.high_battery_threshold = 90
        self.low_battery_threshold = 20
        
        # Audio alert settings
        self.alarm_active = False

    def _show_toast_safe(self, msg, duration=5000):
        if self.gui_queue:
            self.gui_queue.put(lambda: show_toast(msg, duration))
        else:
            # Fallback if no queue provided
            show_toast(msg, duration)

    def start(self):
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.thread.start()

    def stop(self):
        self.running = False

    def _play_alarm(self):
        """Play a loud siren sound using Windows Beep if no file exists"""
        self.alarm_active = True
        # Play siren-like beep for 10 seconds or until user stops it (future implementation)
        for _ in range(10):
            if not self.alarm_active: break
            winsound.Beep(2500, 500) # Frequency 2500Hz, Duration 500ms
            winsound.Beep(1500, 500) # Frequency 1500Hz, Duration 500ms
        self.alarm_active = False

    def _monitor_loop(self):
        while self.running:
            battery = psutil.sensors_battery()
            if battery is None:
                time.sleep(10)
                continue

            percent = battery.percent
            power_plugged = battery.power_plugged
            
            # 1. ANTI-THEFT LOGIC (Unplugged Alert)
            # Only trigger if Anti-Theft is enabled in config
            anti_theft_enabled = self.config_manager.config_data.get("anti_theft_enabled", True)
            
            if self.last_plugged_state is True and power_plugged is False:
                if anti_theft_enabled:
                    self._show_toast_safe("🚨 SECURITY ALERT: Charger Unplugged!", duration=8000)
                    # Trigger Loud Alarm in a separate thread so it doesn't block monitoring
                    threading.Thread(target=self._play_alarm, daemon=True).start()
            
            # 2. BATTERY HEALTH LOGIC (90% Full Alert)
            if power_plugged and percent >= self.high_battery_threshold:
                # Show notification only once per charge cycle (to avoid spamming)
                if not getattr(self, '_notified_90', False):
                    self._show_toast_safe(f"🔋 Battery at {percent}%: Please unplug to save health.", duration=5000)
                    # Trigger Loud Alarm in a separate thread so it doesn't block monitoring
                    threading.Thread(target=self._play_alarm, daemon=True).start()
                    self._notified_90 = True
            elif percent < 85:
                self._notified_90 = False

            # 3. LOW BATTERY LOGIC (20% Alert)
            if not power_plugged and percent <= self.low_battery_threshold:
                if not getattr(self, '_notified_20', False):
                    self._show_toast_safe(f"⚠️ Low Battery: {percent}%. Please connect charger.", duration=5000)
                    # Trigger Loud Alarm in a separate thread so it doesn't block monitoring
                    threading.Thread(target=self._play_alarm, daemon=True).start()
                    self._notified_20 = True
            elif percent > 25:
                self._notified_20 = False

            self.last_plugged_state = power_plugged
            time.sleep(3) # Check every 3 seconds to save CPU/Battery

    def stop_alarm(self):
        self.alarm_active = False
