import os
import requests

def fetch_nasa_image(api_key="DEMO_KEY", save_dir="nasa_images"):
    # 1. Define the API endpoint
    url = f"https://api.nasa.gov/planetary/apod?api_key=uFGczMvvT3fjAO3mY8Zr2o53yT2ofW5SfebM7uDj"
    
    try:
        # 2. Request data from NASA
        response = requests.get(url)
        response.raise_for_status() # Raise error for bad HTTP statuses
        data = response.json()
        
        # 3. Check if the daily asset is an image (sometimes it is a video)
   

        # 4. Extract image metadata and URL
        title = data.get("title")
        date = data.get("date")
        # Prefer HD image; fall back to standard URL if unavailable
        image_url = data.get("hdurl") or data.get("url") 
        
        print(f"Found: '{title}' ({date})")
        print(f"Downloading from: {image_url}")

        # 5. Create local storage directory
        os.makedirs(save_dir, exist_ok=True)
        
        # Sanitizing the title to create a safe file name
        safe_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).rstrip()
        file_extension = image_url.split(".")[-1].split("?")[0] # Extract jpg/png safely
        file_name = f"{date}_{safe_title}.{file_extension}".replace(" ", "_")
        file_path = os.path.join(save_dir, file_name)

        # 6. Download and save the image file
        img_response = requests.get(image_url)
        img_response.raise_for_status()
        
        with open(file_path, "wb") as f:
            f.write(img_response.content)
            
        print(f"Success! Image saved to: {file_path}")
        print(f"Explanation: {data.get('explanation')}")

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Replace 'DEMO_KEY' with your actual key from api.nasa.gov
    fetch_nasa_image(api_key="DEMO_KEY")
