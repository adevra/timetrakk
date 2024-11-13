![alt text](https://blog.anildevran.com/content/images/size/w800/format/webp/2024/11/ZBrush_SzxcQyMY2R-1.png)

# Time Trakk: Your Personal Work Tracker for DCC Apps

**Time Trakk** is a lightweight Python-based tool designed to track the time you spend in your favorite DCC (Digital Content Creation) software, such as Maya, Blender, ZBrush, Photoshop, and more. It helps freelancers and creatives accurately log work hours, providing insights into project time and ensuring fair compensation.

---

## Features

### 1. Tracks Active Apps
Set up a list of software to monitor (e.g., Maya, Blender, Photoshop), and Time Trakk will automatically track the time spent actively working in them. No need to manually start or stop timers.

### 2. Handles Idle Time
Automatically pauses tracking during idle periods, ensuring your logs are accurate and only reflect actual work time.

### 3. Generates Daily Reports
Get detailed summaries of your workday in HTML format, including:
- Total time spent on each app.
- Session details with start and end times.
The report provides both an overview and in-depth details.

### 4. Runs in the Background
Operates quietly in the background with a system tray icon. Notifications keep you updated on the tracking status without disrupting your workflow.

![alt text](https://blog.anildevran.com/content/images/2024/11/image-3.png)

### 5. User-Friendly GUI
Features an intuitive graphical interface for starting, stopping, and generating detailed usage report in HTML. Designed to be simple and accessible for all users.

---

## Installation and Usage

### **Option 1: Run the Python Script**
If you are familiar with Python and dependency management:
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/time-trakk.git
   cd time-trakk
   ```
2. Create a Conda environment using the provided `environment.yml` file:
   ```bash
   conda env create -f environment.yml
   ```
3. Activate the environment:
   ```bash
   conda activate timetrakk
   ```
4. Run the script:
   ```bash
   python time_trakk.py
   ```

### **Option 2: Download the Portable Executable**
If you prefer a ready-to-use setup:
1. Download the latest `.zip` file from the releases page.
2. Run the executable. No installation required – it comes with a bundled Python interpreter and environment.

---

### **Option 3: Build Your Own Portable Executable**
If you prefer a to build from source
1. Clone the repository
2. Setup your environment as mentioned before, activate the environment and intall pyinstaller package to this environment
3. Build with:
   ```bash
   pyinstaller --noconfirm --onedir --windowed --icon=icon.ico --add-data "config.json;data" --add-data "time_data.json;data" --add-data "icon.ico;data" --collect-all PyQt6 --hidden-import=win32gui --hidden-import=win32process TimeTrakk.py
   ```

---
## How It Works

### 1. Define Your Tracked Apps
Specify the apps you want to track in the `config.json` file:
```json
{
  "apps_to_track": ["Maya", "Photoshop", "Blender"]
}
```
the default config file has all of the industry standard content creation tools already setup.

### 2. Start Tracking
Launch Time Trakk and click the "Start" button. The tool will monitor active applications and log your work time automatically.

### 3. Generate Reports
Click "Generate Report" to create an HTML summary of your activity. The report includes total time spent, session details, and idle exclusions.

---

## Known Limitations

- **Windows-Only**: Currently, Time Trakk is optimized for Windows environments. Support for other platforms is under consideration.
- **Idle Detection**: Idle time detection relies on system-level APIs and may have minor variations depending on usage patterns.

---

## Contributing

Contributions are welcome! If you have ideas for new features, bug fixes, or general improvements, please open an issue or submit a pull request.

---

