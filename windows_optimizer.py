import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import subprocess
import os
import winreg
import shutil
import threading
import ctypes
import sys
from pathlib import Path
import psutil

class WindowsOptimizerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Windows All-in-One Optimizer")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        # Check for admin rights
        self.is_admin = self.check_admin()
        
        # Configure colors
        self.bg_color = "#1e1e2e"
        self.fg_color = "#cdd6f4"
        self.accent_color = "#89b4fa"
        self.button_color = "#313244"
        self.success_color = "#a6e3a1"
        self.warning_color = "#f9e2af"
        self.error_color = "#f38ba8"
        
        self.root.configure(bg=self.bg_color)
        
        self.setup_ui()
        
    def check_admin(self):
        """Check if the app is running with administrator privileges"""
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    
    def setup_ui(self):
        """Setup the user interface"""
        
        # Title frame
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20, padx=20, fill=tk.X)
        
        title_label = tk.Label(
            title_frame,
            text="⚡ Windows All-in-One Optimizer",
            font=("Segoe UI", 24, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack()
        
        # Admin status
        admin_text = "✓ Running as Administrator" if self.is_admin else "⚠ Not running as Administrator"
        admin_color = self.success_color if self.is_admin else self.warning_color
        
        admin_label = tk.Label(
            title_frame,
            text=admin_text,
            font=("Segoe UI", 10),
            bg=self.bg_color,
            fg=admin_color
        )
        admin_label.pack(pady=5)
        
        # System info frame
        info_frame = tk.Frame(self.root, bg=self.button_color, relief=tk.RIDGE, bd=2)
        info_frame.pack(pady=10, padx=20, fill=tk.X)
        
        self.setup_system_info(info_frame)
        
        # Main buttons frame
        buttons_frame = tk.Frame(self.root, bg=self.bg_color)
        buttons_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Create buttons grid
        self.create_action_buttons(buttons_frame)
        
        # Output frame
        output_frame = tk.Frame(self.root, bg=self.bg_color)
        output_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        output_label = tk.Label(
            output_frame,
            text="Activity Log",
            font=("Segoe UI", 12, "bold"),
            bg=self.bg_color,
            fg=self.fg_color
        )
        output_label.pack(anchor=tk.W, pady=5)
        
        self.output_text = scrolledtext.ScrolledText(
            output_frame,
            height=10,
            bg=self.button_color,
            fg=self.fg_color,
            font=("Consolas", 9),
            relief=tk.FLAT,
            insertbackground=self.fg_color
        )
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate',
            length=860
        )
        self.progress.pack(pady=10, padx=20)
        
    def setup_system_info(self, parent):
        """Display system information"""
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        
        info_text = f"CPU: {cpu_percent}% | RAM: {memory.percent}% ({self.bytes_to_gb(memory.used)}/{self.bytes_to_gb(memory.total)} GB) | Disk C: {disk.percent}% ({self.bytes_to_gb(disk.used)}/{self.bytes_to_gb(disk.total)} GB)"
        
        info_label = tk.Label(
            parent,
            text=info_text,
            font=("Segoe UI", 10),
            bg=self.button_color,
            fg=self.fg_color,
            pady=10
        )
        info_label.pack()
    
    def bytes_to_gb(self, bytes_value):
        """Convert bytes to GB"""
        return round(bytes_value / (1024**3), 2)
    
    def create_action_buttons(self, parent):
        """Create all action buttons"""
        buttons = [
            ("🧹 Clean Temp Files", self.clean_temp_files, 0, 0),
            ("🗑️ Clear DNS Cache", self.clear_dns_cache, 0, 1),
            ("📦 Scan Bloatware", self.scan_bloatware, 0, 2),
            ("⚙️ Clean Registry", self.clean_registry, 1, 0),
            ("💾 Disk Cleanup", self.disk_cleanup, 1, 1),
            ("🔧 Optimize Startup", self.optimize_startup, 1, 2),
            ("🌐 Clear Browser Cache", self.clear_browser_cache, 2, 0),
            ("📊 System Report", self.generate_report, 2, 1),
            ("⚡ Run All Optimizations", self.run_all, 2, 2),
        ]
        
        for text, command, row, col in buttons:
            btn = tk.Button(
                parent,
                text=text,
                command=command,
                font=("Segoe UI", 11, "bold"),
                bg=self.button_color,
                fg=self.fg_color,
                activebackground=self.accent_color,
                activeforeground=self.bg_color,
                relief=tk.FLAT,
                cursor="hand2",
                width=25,
                height=3,
                bd=0
            )
            btn.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            
            # Hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.accent_color, fg=self.bg_color))
            btn.bind("<Leave>", lambda e, b=btn: b.config(bg=self.button_color, fg=self.fg_color))
        
        # Configure grid weights
        for i in range(3):
            parent.grid_rowconfigure(i, weight=1)
            parent.grid_columnconfigure(i, weight=1)
    
    def log(self, message, level="INFO"):
        """Log message to output text widget"""
        colors = {
            "INFO": self.fg_color,
            "SUCCESS": self.success_color,
            "WARNING": self.warning_color,
            "ERROR": self.error_color
        }
        
        self.output_text.insert(tk.END, f"[{level}] {message}\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def run_with_progress(self, func):
        """Run a function with progress bar"""
        def wrapper():
            self.progress.start()
            try:
                func()
            except Exception as e:
                self.log(f"Error: {str(e)}", "ERROR")
            finally:
                self.progress.stop()
        
        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
    
    def clean_temp_files(self):
        """Clean temporary files"""
        self.run_with_progress(self._clean_temp_files)
    
    def _clean_temp_files(self):
        self.log("Starting temp file cleanup...", "INFO")
        
        temp_paths = [
            os.environ.get('TEMP'),
            os.environ.get('TMP'),
            'C:\\Windows\\Temp',
            os.path.expanduser('~\\AppData\\Local\\Temp')
        ]
        
        total_freed = 0
        
        for temp_path in temp_paths:
            if temp_path and os.path.exists(temp_path):
                try:
                    for item in os.listdir(temp_path):
                        item_path = os.path.join(temp_path, item)
                        try:
                            if os.path.isfile(item_path):
                                size = os.path.getsize(item_path)
                                os.unlink(item_path)
                                total_freed += size
                            elif os.path.isdir(item_path):
                                size = self.get_directory_size(item_path)
                                shutil.rmtree(item_path)
                                total_freed += size
                        except:
                            pass
                except Exception as e:
                    self.log(f"Error accessing {temp_path}: {str(e)}", "WARNING")
        
        self.log(f"Temp files cleaned! Freed: {self.bytes_to_gb(total_freed)} GB", "SUCCESS")
    
    def get_directory_size(self, path):
        """Calculate directory size"""
        total = 0
        try:
            for entry in os.scandir(path):
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.get_directory_size(entry.path)
        except:
            pass
        return total
    
    def clear_dns_cache(self):
        """Clear DNS cache"""
        self.run_with_progress(self._clear_dns_cache)
    
    def _clear_dns_cache(self):
        self.log("Clearing DNS cache...", "INFO")
        
        if not self.is_admin:
            self.log("Administrator privileges required to clear DNS cache", "ERROR")
            return
        
        try:
            result = subprocess.run(['ipconfig', '/flushdns'], 
                                  capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                self.log("DNS cache cleared successfully!", "SUCCESS")
            else:
                self.log("Failed to clear DNS cache", "ERROR")
        except Exception as e:
            self.log(f"Error clearing DNS cache: {str(e)}", "ERROR")
    
    def scan_bloatware(self):
        """Scan for common bloatware"""
        self.run_with_progress(self._scan_bloatware)
    
    def _scan_bloatware(self):
        self.log("Scanning for bloatware...", "INFO")
        
        # Common bloatware patterns
        bloatware_patterns = [
            'Candy Crush', 'Xbox', 'Spotify', 'Netflix', 'Disney',
            'McAfee', 'Norton', 'CCleaner', 'Bonjour', 'Java Auto Updater'
        ]
        
        found_bloatware = []
        
        # Scan installed programs
        try:
            reg_path = r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, reg_path, 0, winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
            
            for i in range(winreg.QueryInfoKey(key)[0]):
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    subkey = winreg.OpenKey(key, subkey_name)
                    try:
                        display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                        for pattern in bloatware_patterns:
                            if pattern.lower() in display_name.lower():
                                found_bloatware.append(display_name)
                    except:
                        pass
                    winreg.CloseKey(subkey)
                except:
                    pass
            
            winreg.CloseKey(key)
        except Exception as e:
            self.log(f"Error scanning registry: {str(e)}", "WARNING")
        
        if found_bloatware:
            self.log(f"Found {len(found_bloatware)} potential bloatware items:", "WARNING")
            for item in found_bloatware:
                self.log(f"  - {item}", "WARNING")
            self.log("Review these items in Windows Settings > Apps", "INFO")
        else:
            self.log("No obvious bloatware detected!", "SUCCESS")
    
    def clean_registry(self):
        """Clean registry (safe operations only)"""
        self.run_with_progress(self._clean_registry)
    
    def _clean_registry(self):
        self.log("Performing safe registry cleanup...", "INFO")
        
        if not self.is_admin:
            self.log("Administrator privileges required for registry operations", "ERROR")
            return
        
        self.log("Checking for invalid startup entries...", "INFO")
        
        cleaned = 0
        
        # Clean Run key entries
        run_paths = [
            (winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Run"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Run")
        ]
        
        for hkey, path in run_paths:
            try:
                key = winreg.OpenKey(hkey, path, 0, winreg.KEY_READ | winreg.KEY_WRITE)
                i = 0
                while True:
                    try:
                        name, value, _ = winreg.EnumValue(key, i)
                        # Check if file exists
                        if isinstance(value, str) and not os.path.exists(value.split('"')[1] if '"' in value else value.split()[0]):
                            # File doesn't exist - invalid entry
                            self.log(f"Found invalid entry: {name}", "WARNING")
                            cleaned += 1
                        i += 1
                    except OSError:
                        break
                winreg.CloseKey(key)
            except Exception as e:
                self.log(f"Could not access {path}: {str(e)}", "WARNING")
        
        self.log(f"Registry scan complete. Found {cleaned} potential issues", "SUCCESS")
        self.log("Use Windows Registry Editor (regedit) for manual cleanup", "INFO")
    
    def disk_cleanup(self):
        """Run Windows Disk Cleanup"""
        self.run_with_progress(self._disk_cleanup)
    
    def _disk_cleanup(self):
        self.log("Running Windows Disk Cleanup utility...", "INFO")
        
        try:
            subprocess.Popen(['cleanmgr', '/d', 'C:'])
            self.log("Disk Cleanup utility launched!", "SUCCESS")
        except Exception as e:
            self.log(f"Error launching Disk Cleanup: {str(e)}", "ERROR")
    
    def optimize_startup(self):
        """Show startup impact"""
        self.run_with_progress(self._optimize_startup)
    
    def _optimize_startup(self):
        self.log("Analyzing startup programs...", "INFO")
        
        try:
            # Open Task Manager to Startup tab
            subprocess.Popen(['taskmgr', '/0', '/startup'])
            self.log("Task Manager opened to Startup tab", "SUCCESS")
            self.log("Disable unnecessary startup programs to improve boot time", "INFO")
        except Exception as e:
            self.log(f"Error opening Task Manager: {str(e)}", "ERROR")
    
    def clear_browser_cache(self):
        """Clear browser cache locations"""
        self.run_with_progress(self._clear_browser_cache)
    
    def _clear_browser_cache(self):
        self.log("Clearing browser cache...", "INFO")
        
        browser_cache_paths = {
            'Chrome': os.path.expanduser('~\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Cache'),
            'Edge': os.path.expanduser('~\\AppData\\Local\\Microsoft\\Edge\\User Data\\Default\\Cache'),
            'Firefox': os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles')
        }
        
        total_freed = 0
        
        for browser, cache_path in browser_cache_paths.items():
            if os.path.exists(cache_path):
                try:
                    size = self.get_directory_size(cache_path)
                    shutil.rmtree(cache_path, ignore_errors=True)
                    total_freed += size
                    self.log(f"Cleared {browser} cache: {self.bytes_to_gb(size)} GB", "SUCCESS")
                except Exception as e:
                    self.log(f"Could not clear {browser} cache: {str(e)}", "WARNING")
            else:
                self.log(f"{browser} cache not found", "INFO")
        
        self.log(f"Total cache cleared: {self.bytes_to_gb(total_freed)} GB", "SUCCESS")
    
    def generate_report(self):
        """Generate system optimization report"""
        self.run_with_progress(self._generate_report)
    
    def _generate_report(self):
        self.log("Generating system report...", "INFO")
        self.log("=" * 50, "INFO")
        
        # System info
        self.log(f"CPU Usage: {psutil.cpu_percent(interval=1)}%", "INFO")
        
        memory = psutil.virtual_memory()
        self.log(f"RAM Usage: {memory.percent}% ({self.bytes_to_gb(memory.used)}/{self.bytes_to_gb(memory.total)} GB)", "INFO")
        
        disk = psutil.disk_usage('C:\\')
        self.log(f"Disk C Usage: {disk.percent}% ({self.bytes_to_gb(disk.used)}/{self.bytes_to_gb(disk.total)} GB)", "INFO")
        
        # Process count
        self.log(f"Running Processes: {len(psutil.pids())}", "INFO")
        
        self.log("=" * 50, "INFO")
        self.log("Report generated successfully!", "SUCCESS")
    
    def run_all(self):
        """Run all optimization tasks"""
        if not messagebox.askyesno("Confirm", "This will run all optimization tasks. Continue?"):
            return
        
        self.log("Starting full system optimization...", "INFO")
        self.log("=" * 50, "INFO")
        
        self._clean_temp_files()
        self._clear_dns_cache()
        self._scan_bloatware()
        self._clean_registry()
        self._clear_browser_cache()
        self._generate_report()
        
        self.log("=" * 50, "INFO")
        self.log("All optimizations complete!", "SUCCESS")
        messagebox.showinfo("Complete", "All optimizations have been completed!")

def main():
    # Check if running on Windows
    if sys.platform != 'win32':
        print("This application is designed for Windows only.")
        sys.exit(1)
    
    root = tk.Tk()
    app = WindowsOptimizerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()