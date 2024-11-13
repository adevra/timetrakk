# Introducing Time Trakk: Your Personal Work Tracker for DCC Apps
# https://blog.anildevran.com

import os  # Operating system functions
import time  # Time-related functions
import json  # JSON handling
import psutil  # System and process utilities
import tkinter as tk  # Tkinter for GUI
from tkinter import ttk  # Themed Tkinter widgets
import pygetwindow as gw  # Window management
from threading import Thread  # Threading support
from datetime import datetime, timedelta  # Date and time manipulation
from PIL import Image, ImageTk  # Image processing
import base64  # Base64 encoding/decoding
from io import BytesIO  # Byte stream handling
import sys  # System-specific parameters and functions
from infi.systray import SysTrayIcon  # System tray icon management
import ctypes  # C types for interacting with DLLs
import win32api  # Windows API access
import queue  # Queue data structure
import threading  # Threading support
from PyQt6.QtWidgets import QApplication, QMainWindow  # PyQt6 GUI components
from pyqttoast import Toast, ToastPreset  # Toast notifications for PyQt

if sys.platform == "win32":
    import win32gui
    import win32process

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

CONFIG_FILE = resource_path(os.path.join("data", "config.json"))
DATA_FILE = resource_path(os.path.join("data", "time_data.json"))
HTML_REPORT_FILE = resource_path(os.path.join("data", "activity_report.html"))

MINIMUM_ACTIVITY_DURATION = 10

TRAY_ICON_BASE64 = ('''
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
''')

qt_app = QApplication(sys.argv)

class ToastHandler:
    def __init__(self):
        self.app = QMainWindow()

    def show_notification(self, title, message):
        toast = Toast(self.app)
        toast.setDuration(3000)
        toast.setTitle(title)
        toast.setText(message)
        toast.applyPreset(ToastPreset.INFORMATION_DARK)
        toast.setMinimumWidth(100)
        toast.setMaximumWidth(550)
        toast.setMinimumHeight(50)
        toast.setMaximumHeight(250)
        toast.show()

toast_handler = ToastHandler()

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"apps_to_track": []}

def load_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def get_idle_duration():
    class LASTINPUTINFO(ctypes.Structure):
        _fields_ = [
            ('cbSize', ctypes.c_uint),
            ('dwTime', ctypes.c_int),
        ]

    lastInputInfo = LASTINPUTINFO()
    lastInputInfo.cbSize = ctypes.sizeof(LASTINPUTINFO)
    if not ctypes.windll.user32.GetLastInputInfo(ctypes.byref(lastInputInfo)):
        return 0
    millis = win32api.GetTickCount() - lastInputInfo.dwTime
    return millis / 1000.0

class TimeTracker:
    def __init__(self):
        self.apps_to_track = load_config().get("apps_to_track", [])
        self.data = load_data()
        self.last_app = None
        self.app_start_time = None
        self.is_tracking = False

    def start_tracking(self):
        self.is_tracking = True

        while self.is_tracking:
            try:
                active_process = self.get_active_process_name()
                active_apps = [app for app in self.apps_to_track if app.lower() in (active_process or "").lower()]
                idle_duration = get_idle_duration()

                if active_apps and idle_duration <= IDLE_THRESHOLD:
                    if active_apps[0] != self.last_app:
                        if self.last_app:
                            self.log_time(self.last_app)
                        self.last_app = active_apps[0]
                        self.app_start_time = time.time()
                else:
                    if self.last_app:
                        elapsed_time = time.time() - self.app_start_time
                        if elapsed_time >= MINIMUM_ACTIVITY_DURATION:
                            self.log_time(self.last_app)
                        self.last_app = None
                        self.app_start_time = None
                time.sleep(1)
            except Exception as e:
                print(f"Tracking Error: {e}")
                self.is_tracking = False

    def stop_tracking(self):
        self.is_tracking = False
        if self.last_app and self.app_start_time:
            self.log_time(self.last_app)

    def log_time(self, app_name):
        elapsed_time = int(time.time() - self.app_start_time)
        start_time = (datetime.now() - timedelta(seconds=elapsed_time)).strftime("%H:%M:%S")
        end_time = datetime.now().strftime("%H:%M:%S")
        date_str = datetime.now().strftime("%Y-%m-%d")

        if date_str not in self.data:
            self.data[date_str] = {}
        if app_name not in self.data[date_str]:
            self.data[date_str][app_name] = []

        self.data[date_str][app_name].append({
            "start": start_time,
            "end": end_time,
            "duration": elapsed_time
        })
        save_data(self.data)

    def get_active_process_name(self):
        try:
            if sys.platform == "win32":
                hwnd = win32gui.GetForegroundWindow()
                if hwnd == 0:
                    return None
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                process = psutil.Process(pid)
                return process.name()
            else:
                active_window = gw.getActiveWindow()
                return active_window.title if active_window else None
        except Exception as e:
            print(f"Process Retrieval Error: {e}")
            return None

    def generate_report(self):
        try:
            data = load_data()
            with open(HTML_REPORT_FILE, 'w') as f:
                f.write("<html><head><title>Activity Report</title></head><body><h1>Activity Report</h1>")
                for date, apps in data.items():
                    total_time = sum(session['duration'] for app_sessions in apps.values() for session in app_sessions)
                    hours, remainder = divmod(total_time, 3600)
                    minutes, seconds = divmod(remainder, 60)
                    f.write(f"<h2>{date}, You worked for a total of {hours}h {minutes}m {seconds}s</h2>")
                    for app, sessions in apps.items():
                        total_app_time = sum(session['duration'] for session in sessions)
                        app_hours, app_remainder = divmod(total_app_time, 3600)
                        app_minutes, app_seconds = divmod(app_remainder, 60)
                        f.write(f"<h3>{app}</h3><p>Total time: {app_hours}h {app_minutes}m {app_seconds}s</p><ul>")
                        for session in sessions:
                            f.write(f"<li>{session['start']} - {session['end']} ({session['duration']}s)</li>")
                        f.write("</ul>")
                f.write("</body></html>")
        except Exception as e:
            print(f"Report Generation Error: {e}")

    def generate_summary(self):
        data = load_data()
        summary_lines = []
        date_str = datetime.now().strftime("%Y-%m-%d")
        if date_str in data:
            apps = data[date_str]
            for app, sessions in apps.items():
                total_duration = sum(session['duration'] for session in sessions)
                hours, remainder = divmod(total_duration, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = ""
                if hours > 0:
                    duration_str += f"{hours} hour{'s' if hours != 1 else ''} "
                if minutes > 0:
                    duration_str += f"{minutes} minute{'s' if minutes != 1 else ''} "
                if seconds > 0:
                    duration_str += f"{seconds} second{'s' if seconds != 1 else ''}"
                summary_lines.append(f"{app}: {duration_str.strip()}")
        return "\n".join(summary_lines)

class TimeTrackerGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Time Trakk v1.0.5 Beta")
        self.tracker = TimeTracker()
        self.notification_queue = queue.Queue()
        self.build_ui()
        self.setup_icon()
        self.update_status()
        self.process_notifications()

    def build_ui(self):
        self.root.configure(bg="#2e2e2e")
        self.root.geometry("400x200")

        button_style = {
            "font": ("Segoe UI", 10),
            "bg": "#1e1e1e",
            "fg": "#ffffff",
            "activebackground": "#3e3e3e",
            "relief": "flat",
            "bd": 0,
        }

        def on_enter(e):
            e.widget.config(bg="#3a75c4", fg="#ffffff")

        def on_leave(e):
            e.widget.config(bg="#1e1e1e", fg="#ffffff")

        self.start_button = tk.Button(self.root, text="Start Trakk", **button_style, command=self.start_tracking)
        self.start_button.bind("<Enter>", on_enter)
        self.start_button.bind("<Leave>", on_leave)

        self.stop_button = tk.Button(self.root, text="Stop Trakk", **button_style, command=self.stop_tracking)
        self.stop_button.bind("<Enter>", on_enter)
        self.stop_button.bind("<Leave>", on_leave)

        self.report_button = tk.Button(self.root, text="Generate Report", **button_style, command=self.generate_report)
        self.report_button.bind("<Enter>", on_enter)
        self.report_button.bind("<Leave>", on_leave)

        self.start_button.pack(fill="x", pady=0, padx=1)
        self.stop_button.pack(fill="x", pady=0, padx=1)
        self.report_button.pack(fill="x", pady=0, padx=1)

        self.status_label = tk.Label(
            self.root,
            text="Idle",
            font=("Verdana", 8),
            bg="#2e2e2e",
            fg="#ffffff",
            anchor="w"
        )
        self.status_label.pack(fill="both", expand=True, padx=10, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.root.bind("<Unmap>", self.on_minimize)

    def setup_icon(self):
        if TRAY_ICON_BASE64:
            try:
                image_data = base64.b64decode(TRAY_ICON_BASE64)
                image = Image.open(BytesIO(image_data))
                self.tray_icon_path = resource_path(os.path.join("data", "icon.ico"))
                image.save(self.tray_icon_path, format='ICO')
                icon_path = self.tray_icon_path
                self.root.iconbitmap(icon_path)
            except Exception as e:
                print(f"Icon Setup Error: {e}")
                self.tray_icon_path = None
        else:
            self.tray_icon_path = resource_path(os.path.join('data', 'icon.ico'))

        menu_options = (
            ("Open Time Trakk", None, self.show_window),
        )
        if self.tray_icon_path and os.path.exists(self.tray_icon_path):
            self.systray = SysTrayIcon(
                self.tray_icon_path,
                "Time Trakk",
                menu_options,
                on_quit=self.exit_application
            )
            self.systray.start()
        else:
            print("Tray icon not found or not provided. System tray functionality disabled.")

    def queue_notification(self, title, message):
        self.notification_queue.put((title, message))

    def process_notifications(self):
        if not self.notification_queue.empty():
            title, message = self.notification_queue.get()
            toast_handler.show_notification(title, message)
        self.root.after(100, self.process_notifications)

    def show_window(self, systray=None):
        self.root.after(0, self._show_window)

    def _show_window(self):
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()

    def hide_window(self):
        self.root.withdraw()

    def on_minimize(self, event):
        if self.root.state() == "iconic":
            self.hide_window()

    def start_tracking(self):
        if not self.tracker.is_tracking:
            Thread(target=self.tracker.start_tracking, daemon=True).start()
            self.status_label.config(text="Tracking your work activity across defined Apps")
            self.queue_notification("Time Trakk", "Tracking Started")
        else:
            self.queue_notification("Time Trakk", "Time tracking is already running.")

    def stop_tracking(self):
        if self.tracker.is_tracking:
            self.tracker.stop_tracking()
            self.status_label.config(text="Idle")
            self.queue_notification("Time Trakk", "Tracking Stopped")
        else:
            self.queue_notification("Time Trakk", "Time tracking is not currently running.")

    def generate_report(self):
        self.tracker.generate_report()
        data = load_data()
        date_str = datetime.now().strftime("%Y-%m-%d")
        total_time = 0
        summary_lines = []
        brief_summary = []

        if date_str in data:
            apps = data[date_str]
            for app, sessions in apps.items():
                app_total = sum(session['duration'] for session in sessions)
                total_time += app_total
                hours, remainder = divmod(app_total, 3600)
                minutes, seconds = divmod(remainder, 60)
                duration_str = ""
                if hours > 0:
                    duration_str += f"{hours} hour{'s' if hours != 1 else ''} "
                if minutes > 0:
                    duration_str += f"{minutes} minute{'s' if minutes != 1 else ''} "
                if seconds > 0:
                    duration_str += f"{seconds} second{'s' if seconds != 1 else ''}"
                summary_lines.append(f"{app}: {duration_str.strip()}")
                brief_summary.append(f"{app} {duration_str.strip()}")

        if total_time > 0:
            total_hours, total_remainder = divmod(total_time, 3600)
            total_minutes, total_seconds = divmod(total_remainder, 60)
            total_duration_str = f"{total_hours}h {total_minutes}m {total_seconds}s"
            summary = f"Total: {total_duration_str}\n" + "\n".join(summary_lines)
            brief_summary_str = ", ".join(brief_summary)
            report_path = os.path.abspath(HTML_REPORT_FILE)
            message = f"Today you have worked a total of: {total_duration_str} ({brief_summary_str})\nFor detailed activity report, check:\n{report_path}"
        else:
            message = "No tracked activity found for today."
        
        self.queue_notification("Time Trakk", message)

    def update_status(self):
        if self.tracker.is_tracking:
            self.status_label.config(text="Tracking your work activity now")
        else:
            self.status_label.config(text="Idle")
        self.root.after(1000, self.update_status)

    def exit_application(self, systray=None):
        def shutdown():
            self.tracker.stop_tracking()
            if hasattr(self, 'systray') and self.systray:
                self.systray.shutdown()
            self.root.quit()
            sys.exit()

        self.root.after(0, shutdown)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    gui = TimeTrackerGUI()
    gui.run()
