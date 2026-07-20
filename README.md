# NASA APOD Wallpaper Updater 🌌

A lightweight Python script that automatically updates your Windows desktop wallpaper with NASA's Astronomy Picture of the Day (APOD) every day.

## Features
* **Daily Updates:** Automatically fetches NASA's daily Astronomy Picture of the Day.
* **Smart Caching:** Saves images locally in `nasa_images/` and skips downloading if today's image is already present.
* **Network Resilience:** Safe for system startup; automatically waits for a Wi-Fi/Ethernet connection if it isn't ready at login.
* **Windows Integration:** Native Win32 API calls change the wallpaper instantly, accompanied by clean Windows Toast notifications.
* **Zero Resource Footprint:** Runs efficiently in the background using minimal CPU and memory.

## Getting Started

### Prerequisites
You will need Python 3 installed. Install the required libraries:
```bash
pip install requests win11toast
```

### Running the Script
Simply execute the script to check and update your wallpaper:
```bash
python main.py
```

---

## Running Automatically on Windows

You can set this up to run automatically in the background using two methods:

### Method 1: The Startup Folder (Simplest)
1. Build a standalone executable so it runs without showing terminal windows:
   ```bash
   pip install pyinstaller
   pyinstaller --onefile --noconsole --name="NASA_Wallpaper_Updater" main.py
   ```
2. Press `Win + R`, type `shell:startup`, and press Enter.
3. Create a shortcut to the compiled `NASA_Wallpaper_Updater.exe` (found in the `dist` folder) and drop it into the Startup folder.

### Method 2: Windows Task Scheduler
To run it on a set schedule (even if you never reboot your computer):
1. Open **Task Scheduler** and select **Create Basic Task**.
2. Set the trigger to **Daily** or **At log on**.
3. Set the action to **Start a program** and point it to your Python interpreter (or the compiled `.exe`).
4. **Important:** Set the "Start in (optional)" field to the folder containing your script so it can save your wallpaper history in the correct place.
