import ctypes
import os

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

# Example usage (Replace with your actual image path)
set_wallpaper("C:\\Users\\AceNo\\OneDrive\\Desktop\\pROjEcTs\\NASA_Wallpapers\\nasa_images\\2026-07-15_Red_Sprites_in_the_Tatacoa_Desert.jpg")
