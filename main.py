from datetime import date
import time
from win11toast import toast
import ctypes
import os
import requests

cwd = os.getcwd()
current_day = date.today()

def set_wallpaper(image_path):
    # Standard absolute path resolution
    absolute_path = os.path.abspath(image_path)
    
    # Win32 API SystemParametersInfo flags
    SPI_SETDESKWALLPAPER = 20
    SPIF_UPDATEINIFILE = 0x01
    SPIF_SENDWININICHANGE = 0x02
    
    # Combine flags to update user profile and notify the system instantly
    flags = SPIF_UPDATEINIFILE | SPIF_SENDWININICHANGE
    
    # Call the Windows API (SystemParametersInfoW handles unicode paths)
    result = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 
        0, 
        absolute_path, 
        flags
    )
    
    if result:
        print("Wallpaper changed successfully!")
    else:
        print("Failed to change wallpaper.")

def fetch_nasa_image(api_key="DEMO_KEY", save_dir="nasa_images"):
    # 1. Define the API endpoint
    url = f"https://api.nasa.gov/planetary/apod?api_key=uFGczMvvT3fjAO3mY8Zr2o53yT2ofW5SfebM7uDj"
    
    # Try up to 10 times to fetch, waiting 10 seconds between attempts
    for attempt in range(10):
        try:
            # 2. Request data from NASA
            response = requests.get(url, timeout=15)
            response.raise_for_status() # Raise error for bad HTTP statuses
            data = response.json()
            
            # 3. Extract image metadata and URL
            title = data.get("title")
            date_str = data.get("date")
            image_url = data.get("hdurl") or data.get("url") 
            
            print(f"Found: '{title}' ({date_str})")
            print(f"Downloading from: {image_url}")

            # 4. Create local storage directory
            os.makedirs(save_dir, exist_ok=True)
            
            # Sanitizing the title to create a safe file name
            safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
            file_extension = image_url.split(".")[-1].split("?")[0] # Extract jpg/png safely
            file_name = f"{date_str}_{safe_title}.{file_extension}".replace(" ", "_")
            file_path = os.path.join(save_dir, file_name)

            # 5. Download and save the image file
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            with open(file_path, "wb") as f:
                f.write(img_response.content)
                
            print(f"Success! Image saved to: {file_path}")
            print(f"Explanation: {data.get('explanation')}")
            return file_path

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            if attempt < 9:
                time.sleep(10) # Wait 10 seconds before retrying
            else:
                toast('Error fetching wallpaper', 'Check your internet connection.')
                return None

def main():
    print("Checking for new NASA wallpaper...")
    current_date = str(date.today())
    if os.path.exists('./nasa_images') and any(img.startswith(current_date) for img in os.listdir('./nasa_images')):
        print("Today's wallpaper is already downloaded.")
        return
    new_image = fetch_nasa_image()
    if new_image:
        set_wallpaper(new_image)

if __name__ == "__main__":
    # Check/set wallpaper immediately on startup
    main()
    
    # Run loop to check for date changes once per hour
    while True:
        time.sleep(3600) # Sleep for 1 hour to prevent high CPU usage
        if date.today() != current_day:
            main()
            current_day = date.today() # Update the tracked day
